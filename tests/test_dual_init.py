from simplex.simplex_dictionary import SimplexDictionary, SimplexConfig
from simplex.linear_expressions import LinearExpression, Variable
from fractions import Fraction

from simplex.simplex_solver import SimplexSolver

print('\n****************************************')
print('Infeasible to Feasible with dual Test')
print('****************************************')

# Infeasible
obj_fn = LinearExpression(Variable('z', Fraction(1)), [Variable(Variable.CONSTANT, Fraction(0)), Variable('x1', Fraction(3)), Variable('x2', Fraction(4))])
constraint1_rhs = [Variable(Variable.CONSTANT, Fraction(-5)), Variable('x1', Fraction(1)), Variable('x2', Fraction(2))]
constraint2_rhs = [Variable(Variable.CONSTANT, Fraction(10)), Variable('x1', Fraction(1)), Variable('x2', Fraction(-2))]
constraint3_rhs = [Variable(Variable.CONSTANT, Fraction(10)), Variable('x1', Fraction(-2)), Variable('x2', Fraction(3))]
constraint4_rhs = [Variable(Variable.CONSTANT, Fraction(13)), Variable('x1', Fraction(-1)), Variable('x2', Fraction(-1))]

constraints = [
    LinearExpression(Variable('x3', Fraction(1)), constraint1_rhs),
    LinearExpression(Variable('x4', Fraction(1)), constraint2_rhs),
    LinearExpression(Variable('x5', Fraction(1)), constraint3_rhs),
    LinearExpression(Variable('x6', Fraction(1)), constraint4_rhs),
]

config = SimplexConfig()

solver = SimplexSolver(obj_fn, constraints, config)
solver.DEBUG = True
solver.solve()

# solver.s_dict.as_dual_nf()

print(solver.s_dict)