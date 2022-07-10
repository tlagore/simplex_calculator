import functools
from math import inf
from simplex.linear_expressions import LinearExpression, Variable
from enum import Enum
from fractions import Fraction

class PivotMethod(Enum):
    LARGEST_COEFFICIENT = 1
    LARGEST_INCREASE = 2

class SimplexState(Enum):
    FEASIBLE = 1
    OPTIMAL = 2
    INFEASIBLE = 3
    UNBOUNDED = 4

class SimplexConfig():
    """
    Currently unused, but might be used for to configure different methods of solving down the line
    """
    pivot_method = PivotMethod.LARGEST_COEFFICIENT

class SimplexDictionary():
    DEBUG = False

    def __init__(self, objective_function: LinearExpression, constraints):
        """ """
        self.seen_basis = {}

        self.basis_exprs = [constraint.deepclone() for constraint in constraints]
        self.objective_function = objective_function.deepclone()
        self.x_vars = [x.deepclone() for x in self.objective_function.get_vars()]

        self.iter = 1
        self.__remember_basis()

        self.is_dual = False
        
        # helpful if we need to iterate for Bland's method.
        # -1 because there is a constant in the objective function
        self.n = self.objective_function.num_terms()
        self.m = len(constraints)
        self.update_state(init=True)

    def __remember_basis(self):
        rhs_vars = [expr.get_lhs() for expr in self.basis_exprs]
        rhs_vars.sort(key=functools.cmp_to_key(lambda x,y: x.var_comp(y)))
        rhs_str = [var.varname for var in rhs_vars]
        rhs_hash = hash(''.join(rhs_str))

        if rhs_hash in self.seen_basis:
            raise Exception(f"OH NO! We have seen this basis before on iteration: {self.seen_basis[rhs_hash]}")

        self.seen_basis[hash(''.join(rhs_str))] = self.iter
        self.iter += 1

    def debug_print(self, *args, **kwargs):
        if self.DEBUG:
            print('-- ', end='')
            print(*args, **kwargs)

    def get_basis_values(self):
        """
        """

        basis_sol = []

        self.x_vars.sort(key=functools.cmp_to_key(lambda x,y: x.var_comp(y)))

        for var in self.x_vars:
            varname = var.varname
            basis_expr = self.get_basis_by_varname(varname)
            if basis_expr is None:
                basis_sol += [(varname, Fraction(0))]
            else:
                basis_sol += [(varname, basis_expr.get_constant().coefficient)]

        return basis_sol


    def get_objective_value(self):
        return self.objective_function.get_constant().coefficient

    def __is_feasible(self):
        for basis_expr in self.basis_exprs:
            const = basis_expr.get_constant().coefficient
            if const < 0:
                return False

        return True

    def set_objective_function(self, fn: LinearExpression):
        """
            Set a new objective function. This objective function must be in terms
            of the existing objective function variables
        """
        curvars = {var.varname:var for var in self.objective_function.get_vars()}
        for var in fn.get_vars():
            if var.varname not in curvars:
                raise Exception(f"Cannot set objective function to '{fn}' as it is not in terms of current objective function: '{self.objective_function}'")

        self.objective_function = fn.deepclone()
        self.update_state()

    def as_dual_init(self) -> LinearExpression:
        """
        Transforms the dictionary into a dual dictionary for initialization

        Returns the original objective function
        """
        orig_fn = self.objective_function.deepclone()

        # Zero out the objective function
        obj_rhs = [Variable(Variable.CONSTANT, Fraction(0))] + [ Variable('x' + str(idx), Fraction(0)) for idx in range(1, self.n + 1)]
        obj_lhs = Variable('z', Fraction(1))
        self.objective_function.set_expression(obj_lhs, obj_rhs)
        
        # transpose
        self.as_dual_nf()

        return orig_fn

    def as_dual_nf(self):
        """
        Transforms the dictionary into a dual dictionary in normal form
        """
        self.seen_basis.clear()
        self.iter = 1

        dual_lookup = self.__get_dual_lookup_table()

        (dual_lhs, dual_rhs) = self.__get_dual_obj_fn(dual_lookup)
        dual_basis = self.__get_dual_basis(dual_lookup)

        self.objective_function.set_expression(dual_lhs, dual_rhs)
        self.basis_exprs = dual_basis

        self.is_dual = not self.is_dual

        self.n = self.objective_function.num_terms()
        self.m = len(self.basis_exprs)
        self.update_state()

    def __get_dual_basis(self, dual_lookup):
        dual_basis = []
        
        # for setting epsilon
        basis_var_idx = 1

        num_basis = len(self.objective_function.rhs_vars())

        for var in self.objective_function.get_vars():
            # Each dual expression has negative constant of coefficient of primal objective function
            dual_expr = [Variable(Variable.CONSTANT, Fraction(-var.coefficient))]
            
            # iterate primal basis expressions to extract the variable and create
            # a dual basis expression in the dual dictionary
            for primal_expr in self.basis_exprs:
                next_var = primal_expr.get_var(var.varname)
                dual_varname = dual_lookup[primal_expr.varname()]
                dual_expr += [Variable(dual_varname, Fraction(-next_var.coefficient))]

            dual_slack_name = dual_lookup[var.varname]
            dual_slack_var = Variable(dual_slack_name, Fraction(1))
            dual_basis += [LinearExpression(lhs=dual_slack_var, rhs=dual_expr, epsilon=(basis_var_idx, num_basis))]

            basis_var_idx += 1

        return dual_basis

    def __get_dual_lookup_table(self):
        """ 
        Lookup dictionary for variable names
         x1-n <-> yn+1-yn+m
         xn+1-n+m <-> y1-m
        """
        # if we are already a dual, then we name variables x, otherwise y if we are turning into a dual
        dual_prefix = 'x' if self.is_dual else 'y'
        dual_replace = 'y' if self.is_dual else 'x'

        var_lookup = { f'{dual_replace}{i}':f'{dual_prefix}{self.m+i}' for i in range(1, self.n+1)}
        replace_lookup = {f'{dual_replace}{i}':f'{dual_prefix}{i-self.n}' for i in range(self.n+1, self.n+self.m+1)}
        var_lookup.update(replace_lookup)
        self.debug_print(f'Variable lookup: {var_lookup}')

        return var_lookup


    def __get_dual_obj_fn(self, dual_lookup):
        # set lhs to -z since we are doing -max(-fn)
        # We do it this way instead of just setting it to -1 so that when we 
        # convert back to primal it will be +z
        dual_lhs = Variable('z', -self.objective_function.get_lhs().coefficient)

        dual_rhs = [Variable(Variable.CONSTANT, Fraction(0))]

        idx = 1
        for primal_expr in self.basis_exprs:
            dual_varname = dual_lookup[primal_expr.varname()]
            constant = primal_expr.get_constant()
            dual_rhs += [Variable(dual_varname, Fraction(-constant.coefficient))]
            idx += 1

        return (dual_lhs, dual_rhs)

    def get_pivot(self, pivot_type):
        """ 
        Gets the entering and leaving variables for a specific pivot
        """
        entering_var = None
        leaving_expr = None

        # could add new pivot types here
        if pivot_type == PivotMethod.LARGEST_COEFFICIENT:
            (entering_var, leaving_expr) = self.__get_largest_coefficient_pivot()
        elif pivot_type == PivotMethod.LARGEST_INCREASE:
            (entering_var, leaving_expr) = self.__get_largest_increase_pivot()

        return (entering_var, leaving_expr)

    def __get_largest_increase_pivot(self):
        # First we get all the positive coefficient variables in our objective function
        all_pos = [var for var in self.objective_function.get_vars() if var.coefficient > 0]

        if len(all_pos) == 0:
            if self.__optimal():
                self.__state = SimplexState.OPTIMAL
            else:
                self.__state = SimplexState.INFEASIBLE

            return (None, None)


        candidate_exprs = []
        leaving_expr = None

        # iterate each variable and get a list of all candidate 
        # leaving expressions (largest increase *for just that variable*)
        for var in all_pos:
            inter_exprs = []
            smallest_bound = inf
            multiplier = var.coefficient
            max_increase = -1

            for basis_expr in self.basis_exprs:
                candidate = basis_expr.get_var(var.varname)

                # only look at expressions with valid bounds
                if candidate.coefficient >= 0:
                    continue

                constant = basis_expr.get_constant()

                if candidate.coefficient == 0:
                    bound = 0
                else:
                    bound = constant.coefficient / -candidate.coefficient

                increase = bound*multiplier

                if bound < smallest_bound:
                    smallest_bound = bound
                    inter_exprs = [basis_expr]
                    max_increase = increase
                elif bound == smallest_bound and increase == max_increase:
                    inter_exprs.append(basis_expr)
                elif bound == smallest_bound and increase > max_increase:
                    inter_exprs = [basis_expr]
                    max_increase = increase

            if len(inter_exprs) > 0:
                leaving_expr = self.__break_ties(inter_exprs)
                candidate_exprs.append((var, leaving_expr, max_increase))

        if len(candidate_exprs) == 0:
            # we had positive variables in our non-basic, but nothing to pivot out
            self.__state = SimplexState.UNBOUNDED
            return (None, None)
        else:
            # filter leaving expressions to only the max possible increases
            filtered_exprs = self.__filter_largest_increase(candidate_exprs)
            # break ties based on lexicographical anti-cycling
            leaving_expr = self.__break_ties_lgst(filtered_exprs)
            return (leaving_expr[0], leaving_expr[1])

        
    def __filter_largest_increase(self, candidate_basis):
        largest_increase = -1
        largest = []
        for (entering_var, basis, increase) in candidate_basis:
            if increase > largest_increase:
                largest = [(entering_var, basis)]
                largest_increase = increase
            elif increase == largest_increase:
                largest.append((entering_var, basis))

        return largest

    def __get_largest_coefficient_pivot(self):
        max_val = -inf
        entering_var = None

        for var in self.objective_function.get_vars():
            if var.coefficient > 0 and var.coefficient > max_val:
                max_val = var.coefficient
                entering_var = var
        
        if entering_var is None:
            if self.__optimal():
                self.__state == SimplexState.OPTIMAL
            else:
                self.__state == SimplexState.INFEASIBLE
        else:
            leaving_expr = self.__get_leaving_variable(entering_var)

        return (entering_var, leaving_expr)

    def __get_leaving_variable(self, entering_var: Variable) -> LinearExpression:
        """
        This function just looks for the lowest bound for an entering_variable and returns that basis expression
        """

        leaving_exprs = []

        leaving_expr = None
        smallest_bound = inf

        for basis_expr in self.basis_exprs:
            candidate = basis_expr.get_var(entering_var.varname)

            # only look at expressions with valid bounds
            if candidate.coefficient >= 0:
                continue

            constant = basis_expr.get_constant()

            if candidate.coefficient == 0:
                bound = 0
            else:
                bound = constant.coefficient / -candidate.coefficient

            if bound < smallest_bound:
                smallest_bound = bound
                leaving_exprs = [basis_expr]
            elif bound == smallest_bound:
                leaving_exprs.append(basis_expr)

        if len(leaving_exprs) == 0:
            self.__state = SimplexState.UNBOUNDED
        else:
            leaving_expr = self.__break_ties(leaving_exprs)

        return leaving_expr

    def __break_ties_lgst(self, expressions):
        """
        Break ties using the lexicographical method for largest increase

        Since largest increase requires keeping track of which is the entering variable and which is the exiting expression,
        expressions here is a list of tuples of the form:

        [(varname, candidate_leaving_expression)] 
        """

        if len(expressions) == 0:
            return None

        self.debug_print('Breaking ties:\n{0}'.format("\n".join([str(expression[1]) for expression in expressions])))
        expressions.sort(key=functools.cmp_to_key(lambda x,y: x[1].compare_eps(y[1])))
        self.debug_print(f'Chose: {expressions[0]}')
        return expressions[0]

    def __break_ties(self, expressions):
        """
        Break ties using the lexicographical method

        We sort the expressions by their epsilon values and take the first one
        """
        if len(expressions) == 0:
            return None

        self.debug_print('Breaking ties:\n{0}'.format("\n".join([str(expression) for expression in expressions])))
        expressions.sort(key=functools.cmp_to_key(lambda x,y: x.compare_eps(y)))
        self.debug_print(f'Chose: {expressions[0]}')
        return expressions[0]

    def pivot(self, entering_var, leaving_expr):
        """
        Pivots a specific entering variable for a basis variable.

        The basis variable is the entire basis expression, which is used to
        rewrite the basis expression in terms of the entering variable.
        """
        resultant = leaving_expr.in_terms_of(entering_var.varname)

        self.objective_function.substitute(entering_var.varname, resultant)
        for basis_expr in self.basis_exprs:
            if basis_expr == leaving_expr:
                continue
            
            basis_expr.substitute(entering_var.varname, resultant)

        # check where we are updating state
        self.__remember_basis()
        self.update_state()
        
    def get_state(self):
        return self.__state

    def update_state(self, init=False):
        """
        """

        self.__state = SimplexState.FEASIBLE
            
        if self.__optimal():
            self.__state = SimplexState.OPTIMAL
        elif self.__state != SimplexState.OPTIMAL and not self.__is_feasible():
            self.__state = SimplexState.INFEASIBLE
        elif init:
            # Need to check if we're unbounded
            # NOTE: This operation is expensive, but we only find all variables one time.
            # If we needed to do this frequently we should make a lookup from variable to 
            # the expressions it appears in.
            for var in self.objective_function.get_vars():
                if var.coefficient > 0:
                    all_positive = True

                    for basis_expr in self.basis_exprs:
                        basis_var = basis_expr.get_var(var.varname)
                        if basis_var is not None:
                            if basis_var.coefficient < 0:
                                all_positive = False
                                break
                    
                    if all_positive:
                        self.__state = SimplexState.UNBOUNDED
                        break

    def __optimal(self):
        optimal = True
        
        for var in self.objective_function.get_vars():
            optimal = optimal and (var.coefficient <= 0 or var.varname == Variable.CONSTANT)

        for constraint in self.basis_exprs:
            optimal = optimal and constraint.get_constant().coefficient >= 0

        return optimal

    def get_basis_by_varname(self, varname: str, basis_exprs = None) -> LinearExpression:
        """
        If the variable name exists in the basis, returns the basis expression, otherwise returns None
        """
        if basis_exprs is None:
            basis_exprs = self.basis_exprs

        return next((expr for expr in basis_exprs if expr.varname() == varname), None)
    
    def deepclone(self):
        dict = SimplexDictionary(self.objective_function, self.basis_exprs)
        return dict

    def deepequals(self, other_dict: 'SimplexDictionary'):
        """ 
            check everything is identical
        
            deepequals is onlyt used for testing duality, so it has print statements in it
        """
        if not self.objective_function.deepequals(other_dict.objective_function):
            return False
        
        for basis_expr in self.basis_exprs:
            other_expr = self.get_basis_by_varname(basis_expr.varname(), other_dict.basis_exprs)
            if other_expr is None:
                self.debug_print(f"Could not find expression in other for variable '{basis_expr.varname}'")
                return False

            if not basis_expr.deepequals(other_expr):
                return False

        return True

    def expression_equals(self, first: LinearExpression, second: LinearExpression):
        """
        Check if two LinearExpressions are equal
        """
        if first.num_terms() != second.num_terms():
            return False

        for var in first.get_vars(include_constant=True):
            comp_var = second.get_var(var.varname)

            if comp_var is not None:
                if comp_var.coefficient != var.coefficient:
                    self.debug_print(f"var: {var.varname} coefficients {comp_var.coefficient} != {var.coefficient}")
                    return False
            else:
                self.debug_print(f"var: '{var.varname}' other did not contain var.")
                return False

        return True


    def __repr__(self):
        msg = '\n----------------------------------\n'
        msg += repr(self.objective_function)
        msg += '\n----------------------------------'
        
        for basis_expr in self.basis_exprs:
            msg += f'\n{repr(basis_expr)}'

        msg += '\n----------------------------------'

        return msg
