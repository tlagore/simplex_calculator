from rational import Rational

class Variable():
    def __init__(self, coefficient, varname):
        """
        Represents a variable in an expression. pass varname = None to represent a constant
        """
        self.coefficent = coefficient
        self.varname = varname

class Expression():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    
    def __simplify(self):
        rhs_lookup = {}

        for variable in self.rhs:
            if variable.varname in rhs_lookup:
                rhs_lookup[variable.varname].append(variable.coefficent)
            else:
                rhs_lookup[variable.varname] = [variable.coefficent]