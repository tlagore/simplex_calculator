from linear_expressions import LinearExpression

class SimplexConfig():
    pivot_method = "largest_coefficient"

class SimplexDictionary():
    def __init__(self, objective_function: LinearExpression, constraints: list[LinearExpression]):
        """ """
        self.constraints = constraints
        self.objective_function = objective_function

    def get_pivot_variable(self):
        """ """
    
    def pick_basis_swap(self, var):
        """ """

