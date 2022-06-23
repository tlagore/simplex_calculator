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
        self.constraints = [constraint.deepclone() for constraint in constraints]
        self.objective_function = objective_function.deepclone()
        self.config = config

    def solve(self):
        self.__get_pivot()

    def __get_pivot(self):
        """ """
        if self.config.pivot_method == PivotMethod.LARGEST_COEFFICIENT:
            entering_var = self.__get_largest_coefficient_pivot()

        if entering_var is None and not self.optimal():
            raise Exception("WRONG")
        else:
            leaving_var = self.__get_leaving_variable(entering_var)

        print(f"entering_var: {entering_var}\nleaving_var: {leaving_var}")

    def __get_largest_coefficient_pivot(self):
        max_val = -inf
        entering_var = None

        for var in self.objective_function.itervars():
            if var.coefficient > 0 and var.coefficient > max_val:
                max_val = var.coefficient
                entering_var = var

        return entering_var

    def __get_leaving_variable(self, entering_var: Variable):
        leaving_var = None
        smallest_bound = inf

        for constraint in self.constraints:
            candidate = constraint.get_var(entering_var.varname)
            constant = constraint.get_constant()

            bound = constant.coefficient / candidate.coefficient
            if bound < smallest_bound:
                smallest_bound = bound
                leaving_var = candidate

        return leaving_var

    def __pivot(self, pivot_var):
        """"""

    def optimal(self):
        optimal = True
        
        for var in self.objective_function.itervars():
            optimal = optimal and (var.coefficient <= 0)

        for constraint in self.constraints:
            optimal = optimal and constraint.get_constant() >= 0

        return optimal
    
    def pick_basis_swap(self, var):
        """ """

