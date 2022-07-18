# Author: Tyrone Lagore V00995698

from simplex.simplex_solver import SimplexSolver, SimplexConfig
from simplex.linear_expressions import LinearExpression, Variable
from fractions import Fraction

obj_fn = LinearExpression(Variable('z', Fraction(1)), [Variable(Variable.CONSTANT, Fraction(0)), Variable('x1', Fraction(4)), Variable('x2', Fraction(3))])
constraint1_rhs = [Variable(Variable.CONSTANT, Fraction(6)), Variable('x1', Fraction(-1)), Variable('x2', Fraction(-4))]
constraint2_rhs = [Variable(Variable.CONSTANT, Fraction(4)), Variable('x1', Fraction(-4)), Variable('x2', Fraction(-2))]
constraint3_rhs = [Variable(Variable.CONSTANT, Fraction(5)), Variable('x1', Fraction(-3)), Variable('x2', Fraction(-4))]
constraint4_rhs = [Variable(Variable.CONSTANT, Fraction(5)), Variable('x1', Fraction(-5)), Variable('x2', Fraction(-1))]

constraints = [
    LinearExpression(Variable('x3', Fraction(1)), constraint1_rhs),
    LinearExpression(Variable('x4', Fraction(1)), constraint2_rhs),
    LinearExpression(Variable('x5', Fraction(1)), constraint3_rhs),
    LinearExpression(Variable('x6', Fraction(1)), constraint4_rhs),
]

simplex_config = SimplexConfig()

simplex = SimplexSolver(obj_fn, constraints, simplex_config)
simplex.DEBUG = True
simplex.solve()

# unbounded
obj_fn = LinearExpression(Variable('z', Fraction(1)), [Variable(Variable.CONSTANT, Fraction(0)), Variable('x1', Fraction(4)), Variable('x2', Fraction(3))])
constraint1_rhs = [Variable(Variable.CONSTANT, Fraction(6)), Variable('x1', Fraction(1)), Variable('x2', Fraction(-4))]
constraint2_rhs = [Variable(Variable.CONSTANT, Fraction(4)), Variable('x1', Fraction(4)), Variable('x2', Fraction(-2))]
constraint3_rhs = [Variable(Variable.CONSTANT, Fraction(5)), Variable('x1', Fraction(3)), Variable('x2', Fraction(-4))]
constraint4_rhs = [Variable(Variable.CONSTANT, Fraction(5)), Variable('x1', Fraction(5)), Variable('x2', Fraction(-1))]

constraints = [
    LinearExpression(Variable('x3', Fraction(1)), constraint1_rhs),
    LinearExpression(Variable('x4', Fraction(1)), constraint2_rhs),
    LinearExpression(Variable('x5', Fraction(1)), constraint3_rhs),
    LinearExpression(Variable('x6', Fraction(1)), constraint4_rhs),
]

simplex = SimplexSolver(obj_fn, constraints, simplex_config)
simplex.DEBUG = True
simplex.solve()

# Infeasible
obj_fn = LinearExpression(Variable('z', Fraction(1)), [Variable(Variable.CONSTANT, Fraction(0)), Variable('x1', Fraction(4)), Variable('x2', Fraction(3))])
constraint1_rhs = [Variable(Variable.CONSTANT, Fraction(-6)), Variable('x1', Fraction(-1)), Variable('x2', Fraction(-4))]
constraint2_rhs = [Variable(Variable.CONSTANT, Fraction(4)), Variable('x1', Fraction(-4)), Variable('x2', Fraction(-2))]
constraint3_rhs = [Variable(Variable.CONSTANT, Fraction(5)), Variable('x1', Fraction(-3)), Variable('x2', Fraction(-4))]
constraint4_rhs = [Variable(Variable.CONSTANT, Fraction(5)), Variable('x1', Fraction(-5)), Variable('x2', Fraction(-1))]

constraints = [
    LinearExpression(Variable('x3', Fraction(1)), constraint1_rhs),
    LinearExpression(Variable('x4', Fraction(1)), constraint2_rhs),
    LinearExpression(Variable('x5', Fraction(1)), constraint3_rhs),
    LinearExpression(Variable('x6', Fraction(1)), constraint4_rhs),
]

simplex_config = SimplexConfig()

simplex = SimplexSolver(obj_fn, constraints, simplex_config)
simplex.DEBUG = True
simplex.solve()