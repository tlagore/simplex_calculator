from fractions import Fraction
from simplex.linear_expressions import LinearExpression, Variable
from simplex.simplex_solver import SimplexSolver

def parse(in_file):
    """
    """
    line = in_file.readline().strip()
    (obj_fn, n) = parse_obj_function(line)

    constraints = []
    idx = 0
    for line in in_file:
        constraint = parse_constraint(line, idx+n)
        constraints.append(constraint)
        idx +=1
    
    return SimplexSolver(obj_fn, constraints)
    

def parse_constraint(line, constraint_idx):
    parts = line.split()
    bound = parts.pop()

    lhs = Variable(f'x{constraint_idx}', Fraction(1))
    rhs = parse_rhs(parts, bound)

    return LinearExpression(lhs, rhs)

def parse_obj_function(line):
    parts = line.split()

    lhs = Variable('z', Fraction(1))
    rhs = parse_rhs(parts, 0, True)

    return (LinearExpression(lhs, rhs), len(rhs))

def parse_rhs(parts, constant, obj_fn=False):
    rhs = [Variable(Variable.CONSTANT, Fraction(constant))]
    for idx, part in enumerate(parts):
        varname = f'x{idx+1}'
        coef = Fraction(part) if obj_fn else -Fraction(part)
        rhs.append(Variable(varname, coef))
    return rhs