import sys
import simplex.simplex_parser as sp
from simplex.simplex_dictionary import SimplexConfig, PivotMethod, InitializationFn

def main():
    debug = False

    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            debug = True

    # Set configurations for simplex program
    # Defaults are LARGEST_INCREASE and FIBONNACI initialization (for substituted dual objective function)
    simplex_config = SimplexConfig()
    simplex_config.pivot_method = PivotMethod.LARGEST_INCREASE
    simplex_config.initialization_function = InitializationFn.FIBONNACI
    solver = sp.parse(sys.stdin, simplex_config)
    sys.stderr.write("Beginning solve...\n")

    if debug:
        sys.stderr.write("Starting dictionary:\n")
        sys.stderr.write("{0}\n".format(solver.s_dict.to_string()))
        solver.enable_debug()

    solver.solve()
    solver.stats.print_stats()

if __name__ == "__main__":
    main()