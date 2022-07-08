from fractions import Fraction
from simplex.linear_expressions import LinearExpression, Variable
from simplex.simplex_dictionary import SimplexDictionary

def parse(in_file):
    """
    """
    line = in_file.readline().strip()
    obj_fn = parse_obj_function(line)
    print(obj_fn)

    for line in in_file:
        print(line.strip())


def parse_obj_function(line):
    parts = line.split()

    lhs = Variable('z', Fraction(1))

    rhs = []
    for part, idx in enumerate(parts):
        
        # varname = 'x{0}'.format(str(idx+1))

        varname = f'x{idx+1}'


        rhs.append(Variable(varname, Fraction(part)))

    return LinearExpression(lhs, rhs)
