from math import inf
from simplex.linear_expressions import LinearExpression, Variable
from enum import Enum

class PivotMethod(Enum):
    LARGEST_COEFFICIENT = 1

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
    def __init__(self, objective_function: LinearExpression, constraints: list[LinearExpression]):
        """ """
        self.basis_exprs = [constraint.deepclone() for constraint in constraints]
        self.objective_function = objective_function.deepclone()
        self.x_vars = self.objective_function.rhs_vars()
        self.update_state()

    def __is_feasible(self):
        for basis_expr in self.basis_exprs:
            const = basis_expr.get_constant().coefficient
            if const < 0:
                return False

        return True

    def as_nf_dual(self):
        

    def make_feasible(self):
        return False

    def get_pivot(self, pivot_type):
        """ 
        Gets the entering and leaving variables for a specific pivot
        """
        entering_var = None
        leaving_expr = None

        if pivot_type == PivotMethod.LARGEST_COEFFICIENT:
            entering_var = self.__get_largest_coefficient_pivot()

        if entering_var is None:
            if self.optimal():
                self.__state == SimplexState.OPTIMAL
            else:
                self.__state == SimplexState.INFEASIBLE
        else:
            leaving_expr = self.__get_leaving_variable(entering_var)

        if leaving_expr is None:
            self.__state = SimplexState.UNBOUNDED

        return (entering_var, leaving_expr)

    def __get_largest_coefficient_pivot(self) -> Variable:
        max_val = -inf
        entering_var = None

        for var in self.objective_function.itervars():
            if var.varname == Variable.CONSTANT:
                continue

            if var.coefficient > 0 and var.coefficient > max_val:
                max_val = var.coefficient
                entering_var = var

        return entering_var

    def __get_leaving_variable(self, entering_var: Variable) -> LinearExpression:
        leaving_expr = None
        smallest_bound = inf

        for basis_expr in self.basis_exprs:
            candidate = basis_expr.get_var(entering_var.varname)

            # only look at expressions with valid bounds
            if candidate.coefficient > 0:
                continue

            constant = basis_expr.get_constant()

            if candidate.coefficient == 0:
                bound = 0
            else:
                bound = constant.coefficient / -candidate.coefficient

            if bound < smallest_bound:
                smallest_bound = bound
                leaving_expr = basis_expr

        return leaving_expr

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

        self.update_state()
        
    def get_state(self):
        return self.__state

    def update_state(self):
        self.__state = SimplexState.FEASIBLE
            
        if self.__optimal():
            self.__state = SimplexState.OPTIMAL
        elif self.__state != SimplexState.OPTIMAL and not self.__is_feasible():
            self.__state = SimplexState.INFEASIBLE
        else:
            # Need to check if we're unbounded
            # NOTE: This operation is expensive, but we only find all variables one time.
            # If we needed to do this frequently we should make a lookup from variable to 
            # the expressions it appears in
            for var in self.objective_function.itervars():
                if var.varname == Variable.CONSTANT:
                    continue

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
        
        for var in self.objective_function.itervars():
            optimal = optimal and (var.coefficient <= 0 or var.varname == Variable.CONSTANT)

        for constraint in self.basis_exprs:
            optimal = optimal and constraint.get_constant().coefficient >= 0

        return optimal

    def __repr__(self):
        msg = '----------------------------------\n'
        msg += repr(self.objective_function)
        msg += '\n----------------------------------'
        
        for basis_expr in self.basis_exprs:
            msg += f'\n{repr(basis_expr)}'

        msg += '\n----------------------------------'

        return msg
