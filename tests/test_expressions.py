# Author: Tyrone Lagore V00995698

import functools
from simplex.linear_expressions import Variable, LinearExpression
from fractions import Fraction

rhs1 = [Variable(Variable.CONSTANT, Fraction(1)), Variable('x1', Fraction(1)), Variable('x2', Fraction(2))]
rhs2 = [Variable(Variable.CONSTANT, Fraction(1)), Variable('x1', Fraction(3)), Variable('x2', Fraction(4))]

expr1 = LinearExpression(Variable('x3', Fraction(1)), rhs1, (1,4))
expr2 = LinearExpression(Variable('x4', Fraction(1)), rhs2, (2,4))

# expr1 has the larger epsilon
assert expr1.compare_eps(expr2) == 1

val = expr1.in_terms_of('x2')
expr2.substitute('x2', val)

val = expr1.in_terms_of('x1')
expr2.substitute('x1', val)

# expr1 has the larger epsilon
assert expr2.compare_eps(expr1) == -1


# both expressions have eps1, but expr2 has 2*eps2 and expr1 has 1*eps2
rhs1 = [Variable(Variable.CONSTANT, Fraction(1)), Variable('x1', Fraction(1)), Variable('x2', Fraction(2)),
     Variable(f'{Variable.EPSILON}1', Fraction(1)), Variable(f'{Variable.EPSILON}2', Fraction(1))]
rhs2 = [Variable(Variable.CONSTANT, Fraction(1)), Variable('x1', Fraction(3)), Variable('x2', Fraction(4)),
     Variable(f'{Variable.EPSILON}1', Fraction(1)), Variable(f'{Variable.EPSILON}2', Fraction(2))]

expr1 = LinearExpression(Variable('x3', Fraction(1)), rhs1)
expr1.num_epsilon = 2
expr2 = LinearExpression(Variable('x4', Fraction(1)), rhs2)
expr2.num_epsilon = 2

assert expr1.compare_eps(expr2) == -1

expressions = [expr2, expr1]
print(expressions)

# when we sort based on compare_eps, the one with the smallest eps should arrive in front
expressions.sort(key=functools.cmp_to_key(lambda x,y: x.compare_eps(y)))
print(expressions)

first = expressions[0]

assert expr1.deepequals(first)