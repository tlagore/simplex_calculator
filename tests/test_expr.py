from simplex.linear_expressions import LinearExpression, Variable 
from fractions import Fraction


var1 = Variable('x1', Fraction(1,5))
var2 = Variable('w1', Fraction(1))
var3 = Variable('x2', Fraction(33/2))
var4 = Variable(Variable.CONSTANT, Fraction(15))

expr = LinearExpression(var2, [var1, var3, var4])
expr.in_terms_of(var3.varname)

print(expr)

expr.substitute('x1', [Variable('x4', Fraction(3)), Variable('w1', Fraction(3/2))])

print(expr)