from math import inf
from simplex.linear_expressions import LinearExpression, Variable
from enum import Enum

class PivotMethod(Enum):
    LARGEST_COEFFICIENT = 1

class SimplexConfig():
    pivot_method = PivotMethod.LARGEST_COEFFICIENT

class SimplexDictionary():
    def __init__(self, objective_function: LinearExpression, constraints: list[LinearExpression], config: SimplexConfig):
        """ """
        self.basis_exprs = [constraint.deepclone() for constraint in constraints]
        self.objective_function = objective_function.deepclone()
        self.config = config

    def solve(self):
        while not self.optimal():
            (entering_var, leaving_expr) = self.__get_pivot()

            print(f"entering_var: {entering_var}\nleaving_var: {leaving_expr}")
            resultant = leaving_expr.in_terms_of(entering_var.varname)

            self.objective_function.substitute(entering_var.varname, resultant)
            print(self.objective_function)

            for basis_expr in self.basis_exprs:
                if basis_expr == leaving_expr:
                    print(basis_expr)
                    continue
                
                basis_expr.substitute(entering_var.varname, resultant)
                print(basis_expr)

        print("Optimal Dictionary:")
        print(repr(self))

    def __get_pivot(self):
        """ """
        entering_var = None
        leaving_expr = None

        if self.config.pivot_method == PivotMethod.LARGEST_COEFFICIENT:
            entering_var = self.__get_largest_coefficient_pivot()

        if entering_var is None:
            if self.optimal():
                raise Exception("WRONG")
            else:
                print("DONE!")
        else:
            leaving_expr = self.__get_leaving_variable(entering_var)

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

    def __pivot(self, entering, leaving):
        """"""
        

    def optimal(self):
        optimal = True
        
        for var in self.objective_function.itervars():
            optimal = optimal and (var.coefficient <= 0 or var.varname == Variable.CONSTANT)

        for constraint in self.basis_exprs:
            optimal = optimal and constraint.get_constant().coefficient >= 0

        return optimal
    
    def pick_basis_swap(self, var):
        """ """

    def __repr__(self):
        msg = repr(self.objective_function)
        
        for basis_expr in self.basis_exprs:
            msg += f'\n{repr(basis_expr)}'

        return msg
