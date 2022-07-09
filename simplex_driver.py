import sys
import time
import simplex.simplex_parser as sp

def main():
    debug = False
    stats = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            debug = True
            stats = True
        if sys.argv[1] == 'stats':
            stats = True

    solver = sp.parse(sys.stdin)

    if debug:
        print("Starting dictionary:")
        print(solver.s_dict)
        solver.enable_debug()

    stats = solver.solve()
    
    if stats:
        stats.print_stats()

if __name__ == "__main__":
    main()