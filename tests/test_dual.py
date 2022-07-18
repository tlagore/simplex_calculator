# Author: Tyrone Lagore V00995698

from simplex.simplex_dictionary import SimplexDictionary
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

orig = SimplexDictionary(obj_fn, constraints)

simplex_dictionary = SimplexDictionary(obj_fn, constraints)
print("PRIMAL")
print(simplex_dictionary)

simplex_dictionary.as_dual_nf()
print("DUAL")
print(simplex_dictionary)

print(f'equals original dictionary?: {simplex_dictionary.deepequals(orig)}')

# Should go back to exactly the same
simplex_dictionary.as_dual_nf()
print("PRIMAL")
print(simplex_dictionary)

print(f'equals original dictionary?: {simplex_dictionary.deepequals(orig)}')

simplex_dictionary.as_dual_init()

print(simplex_dictionary)

print(simplex_dictionary.get_state())


print('\n****************************************')
print('Infeasible to Feasible with dual Test')
print('****************************************')

# Infeasible
obj_fn = LinearExpression(Variable('z', Fraction(1)), [Variable(Variable.CONSTANT, Fraction(0)), Variable('x1', Fraction(4)), Variable('x2', Fraction(3))])
constraint1_rhs = [Variable(Variable.CONSTANT, Fraction(-6)), Variable('x1', Fraction(1)), Variable('x2', Fraction(-4))]
constraint2_rhs = [Variable(Variable.CONSTANT, Fraction(4)), Variable('x1', Fraction(-4)), Variable('x2', Fraction(-2))]
constraint3_rhs = [Variable(Variable.CONSTANT, Fraction(5)), Variable('x1', Fraction(-3)), Variable('x2', Fraction(-4))]
constraint4_rhs = [Variable(Variable.CONSTANT, Fraction(5)), Variable('x1', Fraction(-5)), Variable('x2', Fraction(-1))]

constraints = [
    LinearExpression(Variable('x3', Fraction(1)), constraint1_rhs),
    LinearExpression(Variable('x4', Fraction(1)), constraint2_rhs),
    LinearExpression(Variable('x5', Fraction(1)), constraint3_rhs),
    LinearExpression(Variable('x6', Fraction(1)), constraint4_rhs),
]

simplex_dictionary = SimplexDictionary(obj_fn, constraints)
print("Original Dictionary:")
print(simplex_dictionary)
print(simplex_dictionary.get_state())

simplex_dictionary.as_dual_init()

print("Dual Dictionary:")
print(simplex_dictionary)
print(simplex_dictionary.get_state())
