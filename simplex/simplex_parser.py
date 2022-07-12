import sys
from fractions import Fraction

from simplex.linear_expressions import LinearExpression, Variable
from simplex.simplex_solver import SimplexSolver

def parse(in_file, simplex_config):
    """
    """
    sys.stderr.write("Parsing LP...\n")
    line = in_file.readline().strip()
    (obj_fn, n) = parse_obj_function(line)

    constraints = []
    basis_count = 0
    for line in in_file:
        constraint = parse_constraint(line, basis_count+n)
        constraints.append(constraint)
        basis_count += 1

    for i, constraint in enumerate(constraints):
        constraint.set_epsilon(i+1, basis_count)

    return SimplexSolver(obj_fn, constraints, simplex_config)

def parse_constraint(line, constraint_idx):
    """
    basis_idx is a 0 indexed index for the basis (for setting epsilon)
    constraint_idx is the index of this basis variable
    """
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
    # let Fraction do the heavy lifting of the convertion from string to fraction, then convert to Fraction
    rhs = [Variable(Variable.CONSTANT, Fraction(constant))]
    for idx, part in enumerate(parts):
        varname = f'x{idx+1}'

        coef = Fraction(part) if obj_fn else -Fraction(part)
        rhs.append(Variable(varname, coef))

    return rhs
