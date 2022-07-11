import sys
import simplex.simplex_parser as sp
from simplex.simplex_dictionary import SimplexConfig, PivotMethod
import cProfile

def main():
    debug = False
    stats = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            debug = True
            stats = True
        if sys.argv[1] == 'stats':
            stats = True

    simplex_config = SimplexConfig()
    simplex_config.pivot_method = PivotMethod.LARGEST_INCREASE
    simplex_config.test_cycle_avoidance = False
    solver = sp.parse(sys.stdin, simplex_config)

    solver.solve()

    if debug:
        print("Starting dictionary:")
        print(solver.s_dict)
        solver.enable_debug()

    if stats:
        solver.stats.print_stats()
#     cProfile.run(
# """
# simplex_config = SimplexConfig()
# simplex_config.pivot_method = PivotMethod.LARGEST_COEFFICIENT
# simplex_config.test_cycle_avoidance = False
# solver = sp.parse(sys.stdin, simplex_config)

# 
# """
#     )
    
    

if __name__ == "__main__":
    main()