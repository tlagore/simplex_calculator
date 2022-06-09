from rational import Rational

class Variable():
    def __init__(self, coefficient: Rational, varname: str):
        """
        Represents a variable in an expression. pass varname = None to represent a constant
        """
        self.coefficent = coefficient
        self.varname = varname

class Expression():
    def __init__(self, lhs: Variable, rhs: list['Expression']):
        """
        lhs can be None
        """
        self.lhs = lhs
        self.rhs = rhs
    
    def __simplify(self):
        rhs_lookup = {}

        for variable in self.rhs:
            if variable.varname in rhs_lookup:
                rhs_lookup[variable.varname].append(variable.coefficent)
            else:
                rhs_lookup[variable.varname] = [variable.coefficent]

            
