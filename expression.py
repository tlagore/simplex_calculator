import functools
import itertools

from rational import Rational

class Variable():
    def __init__(self, coefficient: Rational, varname: str):
        """
        Represents a variable in an expression. pass varname = None to represent a constant
        """
        self.coefficient = coefficient
        self.varname = varname
    
    def __repr__(self):
        if self.coefficient.numerator == 0:
            return ''
        else:
            return f"{self.coefficient}{self.varname}"

class Expression():
    def __init__(self, variables: list['Variable']):
        """
        """

        ## NOTE: We'll want to think about sorting these maybe
        self.variables = variables
    
    def simplify(self):
        simplified = []
        by_var = itertools.groupby(self.variables, lambda x: x.varname)
        for varname, group in by_var:
            coefs = [x.coefficient for x in group]
            var_sum = functools.reduce(lambda x,y: x+y, coefs)
            simplified.append(Variable(var_sum, varname))

        self.variables = simplified


    def __repr__(self):
        return str(self.variables)


        # for variable in self.rhs:
        #     if variable.varname in rhs_lookup:
        #         rhs_lookup[variable.varname].append(variable.coefficent)
        #     else:
        #         rhs_lookup[variable.varname] = [variable.coefficent]

        # for varname, coef_list in rhs_lookup:
        #     val = Rational(0)
        #     for coef in coef_list:
        #         val += coef
        #     simplified.append(Variable(val, varname))

