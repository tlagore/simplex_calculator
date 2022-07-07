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
        self.config = config

    def debug_print(self, *args, **kwargs):
        if self.DEBUG:
            print(*args, **kwargs)

    def make_feasible(self):
        """ 
        Attempt to make the dictionary feasibly by solving an auxillery problem.
        Uses the dual initialization technique
        
        This does not necessarily succeed

        Returns: True if successful, else false
        """

        self.debug_print(self.s_dict)
        self.debug_print("Dictionary is not feasible, attempting auxillery problem")

        orig_fn = self.s_dict.as_dual_init()
        self.solve(auxillery=True)
        
        if self.s_dict.get_state() == SimplexState.OPTIMAL:
            self.debug_print("Dual problem was solvable!")

            # take the dual to get our original problem in terms of the dual-feasible dictionary
            self.s_dict.as_dual_nf()

            orig_vars = list(orig_fn.itervars())

            for var in orig_vars:
                basis = self.s_dict.get_basis_by_varname(var.varname)
                if basis is not None:
                    orig_fn.substitute(var.varname, basis.itervars(include_constant=True))

            self.debug_print("Transformed function:")
            self.debug_print(orig_fn)

            self.s_dict.set_objective_function(orig_fn)

            return True
        else:
            self.s_dict.as_dual_nf()
            self.s_dict.set_objective_function(orig_fn)

        self.debug_print("Dual problem was not solvable.")
        return False

    def solve(self, auxillery = False):
        if not self.s_dict.get_state() == SimplexState.FEASIBLE and not auxillery:
            if not self.make_feasible():
                self.print_result(SimplexState.INFEASIBLE)
                return

        while self.s_dict.get_state() == SimplexState.FEASIBLE:
            (entering_var, leaving_expr) = self.s_dict.get_pivot(self.config.pivot_method)
            
            if self.s_dict.get_state() == SimplexState.FEASIBLE:
                self.s_dict.pivot(entering_var, leaving_expr)
                self.debug_print(repr(self))
                self.debug_print(f"entering_var: {entering_var}\nleaving_var: {leaving_expr}") 
            
        if not auxillery:
            state = self.s_dict.get_state()
            self.print_result(state)

    def print_result(self, state):
        if state == SimplexState.OPTIMAL:
            self.debug_print("Optimal Dictionary:")
            self.debug_print(repr(self))
            self.debug_print(f"Objective value: {self.s_dict.objective_function.get_constant().coefficient}")
            objective_value = self.s_dict.objective_function.get_constant().coefficient
            print("optimal")
            print(f'{float(objective_value):.7f}')
            basis_sol = self.s_dict.get_basis_values()
            print(' '.join([f'{float(value):.7f}' for (_, value) in basis_sol]))

        elif state == SimplexState.INFEASIBLE:
            self.debug_print("INFEASIBLE!")
            self.debug_print(repr(self))
        elif state == SimplexState.UNBOUNDED:
            self.debug_print("UNBOUNDED!")
            self.debug_print(repr(self))

    def __repr__(self):
        return repr(self.s_dict)
