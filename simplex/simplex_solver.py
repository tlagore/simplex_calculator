import math
from simplex.linear_expressions import LinearExpression
from simplex.simplex_dictionary import SimplexDictionary, PivotMethod, SimplexState

class SimplexConfig():
    pivot_method = PivotMethod.LARGEST_COEFFICIENT

    # 10 degenerative pivots before we consider ourselves cycling
    cycle_threshold = 10

class SimplexSolver():
    DEBUG = False

    def __init__(self, objective_function: LinearExpression, constraints: list[LinearExpression], config: SimplexConfig=None):
        """ """
        self.s_dict = SimplexDictionary(objective_function, constraints)
        self.__cycling = False
        self.degenerate_count = 0

        if config is not None:
            self.config = config
        else:
            self.config = SimplexConfig()

        self.pivot_method = self.config.pivot_method

    def enable_debug(self):
        self.DEBUG = True
        self.s_dict.DEBUG = True

    def debug_print(self, *args, **kwargs):
        if self.DEBUG:
            print('-- ', end='')
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
            # cur_val = self.s_dict.get_objective_value()
            (entering_var, leaving_expr) = self.s_dict.get_pivot(self.pivot_method)
            
            if self.s_dict.get_state() == SimplexState.FEASIBLE:
                self.s_dict.pivot(entering_var, leaving_expr)
                self.debug_print(repr(self))
                self.debug_print(f"entering_var: {entering_var}\nleaving_var: {leaving_expr}") 
                # updated_val = self.s_dict.get_objective_value()

                # self.__check_for_cycling(cur_val, updated_val)
            
        if not auxillery:
            state = self.s_dict.get_state()
            self.print_result(state)

    # might get to delete this
    # def __check_for_cycling(self, prev_val, updated_val):
    #     # if we are not currently cycling, but our objective value did not change, increment degenerate_count
    #     if not self.__cycling and prev_val == updated_val:
    #         self.degenerate_count += 1

    #         # if we have hit our degenerate_count threshold, switch our pivot method to avoid cycling
    #         if self.degenerate_count > self.config.cycle_threshold:
    #             self.__cycling = True
    #             self.pivot_method = PivotMethod.LEXICOGRAPHICAL

    #     # if we were cycling, but we have changed the objective function value, update the pivot rule and reset
    #     # degeneracy counts       
    #     elif self.__cycling and prev_val != updated_val:
    #         self.__cycling = False
    #         self.degenerate_count = 0
    #         self.pivot_method = self.config.pivot_method


    def print_result(self, state):
        if state == SimplexState.OPTIMAL:
            self.debug_print("Optimal Dictionary:")
            self.debug_print(repr(self))
            self.debug_print(f"Objective value: {self.s_dict.objective_function.get_constant().coefficient}")
            objective_value = self.s_dict.objective_function.get_constant().coefficient
            print("optimal")
            print(self.format_float(objective_value))
            basis_sol = self.s_dict.get_basis_values()
            print(self.format_solution(basis_sol))
        elif state == SimplexState.INFEASIBLE:
            print('infeasible')
            self.debug_print("INFEASIBLE!")
            self.debug_print(repr(self))
        elif state == SimplexState.UNBOUNDED:
            print('unbounded')
            self.debug_print("UNBOUNDED!")
            self.debug_print(repr(self))

    def format_solution(self, fn):
        return ' '.join([self.format_float(value) for (_, value) in fn])

    def format_float(self, flt):
        (decimal, _) = math.modf(flt)
        if decimal != 0:
            return f'{float(flt):.7g}'
        else:
            return f'{float(flt):.0f}'

    def __repr__(self):
        return repr(self.s_dict)
