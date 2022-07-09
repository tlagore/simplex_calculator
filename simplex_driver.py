import sys

import simplex.simplex_parser as sp

def main():
    debug = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            debug = True

    solver = sp.parse(sys.stdin)

    if debug:
        print("Starting dictionary:")
        print(solver.s_dict)
        solver.enable_debug()

    solver.solve()

if __name__ == "__main__":
    main()