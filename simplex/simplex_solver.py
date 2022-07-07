from math import inf
from simplex.linear_expressions import LinearExpression
from simplex.simplex_dictionary import SimplexDictionary, PivotMethod, SimplexState


class SimplexConfig():
    pivot_method = PivotMethod.LARGEST_COEFFICIENT

class SimplexSolver():
    DEBUG = False

    def __init__(self, objective_function: LinearExpression, constraints: list[LinearExpression], config: SimplexConfig):
        """ """
        self.s_dict = SimplexDictionary(objective_function, constraints)

    def debug_print(self, *args, **kwargs):
        if self.DEBUG:
            print(*args, **kwargs)

    def make_feasible(self):
        """ 
        This does not necessarily succeed
        """

        # STEPS:
        # Save the objective function
        # Overwrite the objective function to be 0 + 0x1 + 0x2 + 0x3... + 0xn
        # Solve the dual
        # Substitute the original objective function back in
        
        orig_fn = self.s_dict.as_dual_init()
        self.solve(auxillery=True)
        
        if self.s_dict.get_state() == SimplexState.OPTIMAL and self.s_dict.get_objective_value() == 0:
            self.debug_print("Dual problem was solvable and optimal value was 0")
            return True

        return False

    def solve(self, auxillery=False):
        if auxillery:
            self.debug_print("SOLVING AUXILLERY PROBLEM!")

        if not self.s_dict.get_state() == SimplexState.FEASIBLE:
            self.make_feasible()

        while self.s_dict.get_state() == SimplexState.FEASIBLE:
            (entering_var, leaving_expr) = self.s_dict.get_pivot(PivotMethod.LARGEST_COEFFICIENT)
            
            if self.s_dict.get_state() == SimplexState.FEASIBLE:
                self.s_dict.pivot(entering_var, leaving_expr)
                self.debug_print(repr(self))
                self.debug_print(f"entering_var: {entering_var}\nleaving_var: {leaving_expr}") 
            
        state = self.s_dict.get_state()
        if state == SimplexState.OPTIMAL:
            self.debug_print("Optimal Dictionary:")
            self.debug_print(repr(self))
            self.debug_print(f"Objective value: {self.s_dict.objective_function.get_constant().coefficient}")
        elif state == SimplexState.INFEASIBLE:
            self.debug_print("INFEASIBLE!")
            self.debug_print(repr(self))
        elif state == SimplexState.UNBOUNDED:
            self.debug_print("UNBOUNDED!")
            self.debug_print(repr(self))

    def __repr__(self):
        return repr(self.s_dict)
