import math
import time
import sys 

from simplex.linear_expressions import LinearExpression
from simplex.simplex_dictionary import SimplexDictionary, PivotMethod, SimplexState

class SimplexStats():
    num_variables = 0
    num_constraints = 0

    num_pivots = 0
    num_degenerate_pivots = 0
    solution_time = 0
    pivot_selection_time = 0
    pivot_time = 0

    # if we solve an auxilery problem
    required_auxiliary = False
    aux_stats: 'SimplexStats' = None

    def is_auxiliary(self):
        self.required_auxiliary = True
        self.aux_stats = SimplexStats()
        self.aux_stats.num_pivots = self.num_pivots
        self.aux_stats.num_degenerate_pivots = self.num_degenerate_pivots
        self.aux_stats.solution_time = self.solution_time
        self.aux_stats.pivot_selection_time = self.pivot_selection_time
        self.aux_stats.pivot_time = self.pivot_time

        self.num_pivots = 0
        self.num_degenerate_pivots = 0
        self.solution_time = 0
        self.pivot_selection_time = 0
        self.pivot_time = 0

    def __print_header(self):
        sys.stderr.write("\nSimplex Stats\n")
        sys.stderr.write("{0}\n".format('-'*70))
        sys.stderr.write("| {0:<12}| {1:30}| {2:<20} |\n".format("Category", "Stat", "Value"))
        sys.stderr.write("{0}\n".format('-'*70))

    def __print_stats(self, stats: 'SimplexStats', aux: bool):
        p_type = 'Auxiliary' if aux else 'Main L.P.'
        sys.stderr.write("| {0:<12}| {1:30}| {2:20} |\n".format('', f"number of pivots:", stats.num_pivots))
        sys.stderr.write("| {0:<12}| {1:30}| {2:20} |\n".format('', f"number of degenerate pivots:", stats.num_degenerate_pivots))
        sys.stderr.write("| {0:<12}| {1:30}| {2:19.6f}s |\n".format(p_type, f"avg pivot selection time:", 0 if stats.num_pivots == 0 else stats.pivot_selection_time/stats.num_pivots))
        sys.stderr.write("| {0:<12}| {1:30}| {2:19.6f}s |\n".format('', f"avg pivot time:", 0 if stats.num_pivots == 0 else stats.pivot_time/stats.num_pivots))
        sys.stderr.write("| {0:<12}| {1:30}| {2:19.2f}s |\n".format('', f"solution time:", stats.solution_time))
        sys.stderr.write("{0}\n".format('-'*70))

    def print_stats(self):
        self.__print_header()
        sys.stderr.write("| {0:<12}| {1:30}| {2:>20} |\n".format('', 'number of variables: ', self.num_variables))
        sys.stderr.write("| {0:<12}| {1:30}| {2:>20} |\n".format('Overview', 'number of constraints: ', self.num_constraints))
        sys.stderr.write("| {0:<12}| {1:30}| {2:>20} |\n".format('', "required auxiliary:", "Yes" if self.required_auxiliary else "No"))
        sys.stderr.write("{0}\n".format('-'*70))
        if self.required_auxiliary:
            self.__print_stats(self.aux_stats, True)

        self.__print_stats(self, False)

class SimplexConfig():
    pivot_method = PivotMethod.LARGEST_INCREASE

class SimplexSolver():
    DEBUG = False

    def __init__(self, objective_function: LinearExpression, constraints, config: SimplexConfig=None):
        """ """
        if config is not None:
            self.config = config
        else:
            self.config = SimplexConfig()

        self.s_dict = SimplexDictionary(objective_function, constraints, config)
        self.degenerate_count = 0
        self.stats = SimplexStats()
        self.stats.num_variables = self.s_dict.n
        self.stats.num_constraints = len(constraints)

        self.pivot_method = self.config.pivot_method

    def enable_debug(self):
        self.DEBUG = True
        self.s_dict.DEBUG = True

    def debug_print(self, msg):
        if self.DEBUG:
            sys.stderr.write("{0}\n".format(msg))

    def make_feasible(self):
        """ 
        Attempt to make the dictionary feasibly by solving an auxiliary problem.
        Uses the dual initialization technique
        
        This does not necessarily succeed

        Returns: True if successful, else false
        """

        # self.debug_print(self.s_dict.to_string())
        # self.debug_print("Dictionary is not feasible, attempting auxiliary problem")

        orig_fn = self.s_dict.as_dual_init()
        self.solve(auxiliary=True)
        
        if self.s_dict.get_state() == SimplexState.OPTIMAL:
            # self.debug_print("Dual problem was solvable!")

            # take the dual to get our original problem in terms of the dual-feasible dictionary
            self.s_dict.as_dual_nf()

            orig_vars = list(orig_fn.get_vars())

            for var in orig_vars:
                basis = self.s_dict.get_basis_by_varname(var.varname)
                if basis is not None:
                    orig_fn.substitute(var.varname, basis.get_vars(include_constant=True))

            # self.debug_print("Transformed function:")
            # self.debug_print(orig_fn.to_string())

            self.s_dict.set_objective_function(orig_fn)

            return True

        # self.debug_print("Dual problem was not solvable.")
        return False

    def solve(self, auxiliary = False):
        if not self.s_dict.get_state() == SimplexState.FEASIBLE and not auxiliary:
            if not self.make_feasible():
                self.print_result(SimplexState.INFEASIBLE)
                return

        start_time = time.time()
        while self.s_dict.get_state() == SimplexState.FEASIBLE:
            cur_val = self.s_dict.get_objective_value()
            
            st = time.perf_counter()
            (entering_var, leaving_expr) = self.s_dict.get_pivot(self.pivot_method)
            self.stats.pivot_selection_time += (time.perf_counter() - st)

            if self.s_dict.get_state() == SimplexState.FEASIBLE:
                st = time.perf_counter()
                self.s_dict.pivot(entering_var, leaving_expr)
                self.stats.pivot_time += (time.perf_counter() - st)

                # self.debug_print(self.to_string())
                # self.debug_print(f"entering_var: {entering_var.to_string()}\nleaving_var: {leaving_expr.to_string()}") 
                updated_val = self.s_dict.get_objective_value()
                self.stats.num_pivots += 1
                
                if cur_val == updated_val:
                    self.stats.num_degenerate_pivots += 1

                sys.stderr.write( "{0}{1}\r".format("Dual LP pivots: " if auxiliary else "Main LP pivots: ", self.stats.num_pivots) )

        self.stats.solution_time = time.time() - start_time

        sys.stderr.write("\n")
        
        if not auxiliary:
            state = self.s_dict.get_state()
            self.print_result(state)
        else:
            self.stats.is_auxiliary()

    def print_result(self, state):
        if state == SimplexState.OPTIMAL:
            # self.debug_print("Optimal Dictionary:")
            # self.debug_print(self.to_string())
            # self.debug_print(f"Objective value: {self.s_dict.objective_function.get_constant().coefficient}")
            objective_value = self.s_dict.objective_function.get_constant().coefficient
            print("optimal")
            print(self.format_float(objective_value))
            basis_sol = self.s_dict.get_basis_values()
            print(self.format_solution(basis_sol))
        elif state == SimplexState.INFEASIBLE:
            print('infeasible')
            # self.debug_print("INFEASIBLE!")
            # self.debug_print(self.to_string())
        elif state == SimplexState.UNBOUNDED:
            print('unbounded')
            # self.debug_print("UNBOUNDED!")
            # self.debug_print(self.to_string())

    def format_solution(self, fn):
        return ' '.join([self.format_float(value) for (_, value) in fn])

    def format_float(self, flt):
        (decimal, _) = math.modf(flt)
        if decimal != 0:
            return f'{float(flt):.7g}'
        else:
            return f'{float(flt):.0f}'

    def to_string(self):
        return self.s_dict.to_string()
