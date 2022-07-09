import sys

import simplex.simplex_parser as sp

def main():
    debug = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            debug = True

    solver = sp.parse(sys.stdin)
    solver.DEBUG = debug
    solver.solve()

if __name__ == "__main__":
    main()