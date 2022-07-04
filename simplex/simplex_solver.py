from math import inf
from simplex.linear_expressions import LinearExpression
from simplex.simplex_dictionary import SimplexDictionary, PivotMethod, SimplexState


class SimplexConfig():
    pivot_method = PivotMethod.LARGEST_COEFFICIENT

class SimplexSolver():
    def __init__(self, objective_function: LinearExpression, constraints: list[LinearExpression], config: SimplexConfig):
        """ """
        self.s_dict = SimplexDictionary(objective_function, constraints)

    def make_feasible(self):
        """ 
        This does not necessarily succeed
        """
        return False

    def solve(self):
        if not self.s_dict.get_state() == SimplexState.FEASIBLE:
            self.make_feasible()

        while self.s_dict.get_state() == SimplexState.FEASIBLE:
            (entering_var, leaving_expr) = self.s_dict.get_pivot(PivotMethod.LARGEST_COEFFICIENT)
            
            if self.s_dict.get_state() == SimplexState.FEASIBLE:
                self.s_dict.pivot(entering_var, leaving_expr)
                print(repr(self))
                print(f"entering_var: {entering_var}\nleaving_var: {leaving_expr}") 
            
        state = self.s_dict.get_state()
        if state == SimplexState.OPTIMAL:
            print("Optimal Dictionary:")
            print(repr(self))
            print(f"Objective value: {self.s_dict.objective_function.get_constant().coefficient}")
        elif state == SimplexState.INFEASIBLE:
            print("INFEASIBLE!")
            print(repr(self))
        elif state == SimplexState.UNBOUNDED:
            print("UNBOUNDED!")
            print(repr(self))

    def __repr__(self):
        return repr(self.s_dict)
