import math
import time
from simplex.linear_expressions import LinearExpression
from simplex.simplex_dictionary import SimplexDictionary, PivotMethod, SimplexState

class SimplexStats():
    num_variables = 0
    num_constraints = 0

    num_pivots = 0
    num_degenerate_pivots = 0
    solution_time = 0

    # if we solve an auxilery problem
    required_auxiliary = False
    aux_stats: 'SimplexStats' = None

    def is_auxiliary(self):
        self.required_auxiliary = True
        self.aux_stats = SimplexStats()
        self.aux_stats.num_pivots = self.num_pivots
        self.aux_stats.num_degenerate_pivots = self.num_degenerate_pivots
        self.aux_stats.solution_time = self.solution_time

        self.num_pivots = 0
        self.num_degenerate_pivots = 0
        self.solution_time = 0

    def __print_header(self):
        print("Simplex Solver Problem Stats")
        print("{0:40}{1:>10}".format("Stat", "Value"))
        print('-'*50)

    def __print_stats(self, stats: 'SimplexStats', aux: bool):
        postfix = '-aux' if aux else ''
        print("{0:40}{1:10}".format(f"number of pivots{postfix}:", stats.num_pivots))
        print("{0:40}{1:10}".format(f"number of degenerate pivots{postfix}:", stats.num_degenerate_pivots))
        print("{0:40}{1:10.2f}s".format(f"solution time{postfix}:", stats.solution_time))

    def print_stats(self):
        self.__print_header()
        print("{0:40}{1:>10}".format('number of variables: ', self.num_variables))
        print("{0:40}{1:>10}".format('number of constraints: ', self.num_constraints))
        print("{0:40}{1:>10}".format("required auxiliary:", "Yes" if self.required_auxiliary else "No"))
        if self.required_auxiliary:
            self.__print_stats(self.aux_stats, True)
            print('')
        self.__print_stats(self, False)

class SimplexConfig():
    pivot_method = PivotMethod.LARGEST_COEFFICIENT

    # 10 degenerative pivots before we consider ourselves cycling
    cycle_threshold = 10

class SimplexSolver():
    DEBUG = False

    def __init__(self, objective_function: LinearExpression, constraints, config: SimplexConfig=None):
        """ """
        self.s_dict = SimplexDictionary(objective_function, constraints)
        self.degenerate_count = 0
        self.stats = SimplexStats()
        self.stats.num_variables = self.s_dict.num_variables
        self.stats.num_constraints = len(constraints)

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
        Attempt to make the dictionary feasibly by solving an auxiliary problem.
        Uses the dual initialization technique
        
        This does not necessarily succeed

        Returns: True if successful, else false
        """

        self.debug_print(self.s_dict)
        self.debug_print("Dictionary is not feasible, attempting auxiliary problem")

        orig_fn = self.s_dict.as_dual_init()
        self.solve(auxiliary=True)
        
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

        self.debug_print("Dual problem was not solvable.")
        return False

    def solve(self, auxiliary = False):
        start_time = time.time()

        if not self.s_dict.get_state() == SimplexState.FEASIBLE and not auxiliary:
            if not self.make_feasible():
                self.print_result(SimplexState.INFEASIBLE)
                return

        while self.s_dict.get_state() == SimplexState.FEASIBLE:
            cur_val = self.s_dict.get_objective_value()
            (entering_var, leaving_expr) = self.s_dict.get_pivot(self.pivot_method)
            
            if self.s_dict.get_state() == SimplexState.FEASIBLE:
                self.s_dict.pivot(entering_var, leaving_expr)
                self.debug_print(repr(self))
                self.debug_print(f"entering_var: {entering_var}\nleaving_var: {leaving_expr}") 
                updated_val = self.s_dict.get_objective_value()
                self.stats.num_pivots += 1
                
                if cur_val == updated_val:
                    self.stats.num_degenerate_pivots += 1
            
        self.stats.solution_time = time.time() - start_time
        
        if not auxiliary:
            state = self.s_dict.get_state()
            self.print_result(state)
        else:
            self.stats.is_auxiliary()

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
