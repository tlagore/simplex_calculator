from fractions import Fraction

class Variable():
    """ """
    def __init__(self, varname: str, coefficient: Fraction):
        """ """
        self.coefficient = coefficient
        self.varname = varname

    def __repr__(self):
        return f"{self.coefficient}{self.varname}"

    # negation -
    def __neg__(self) -> 'Variable':
        """ 
        Override of negation. Allows user to perform -variable to invert sign of variable.
        """
        n = Variable(self.varname, -self.coefficient)

        return n

    # >
    def __gt__(self, other: 'Variable') -> bool:
        return self.coefficient > other.coefficient

    # >=
    def __ge__(self, other: 'Variable') -> bool:
        return self.coefficient >= other.coefficient

    # <
    def __lt__(self, other: 'Variable') -> bool:
        return self.coefficient < other.coefficient

    # <=
    def __le__(self, other: 'Variable') -> bool:
        return self.coefficient <= other.coefficient

    # >
    def __eq__(self, other: 'Variable') -> bool:
        """ 
        Override of ==
        """
        return self.varname == other.varname and self.coefficient == other.coefficient

    # required for ==
    def __hash__(self):
        return object.__hash__(self)

    # - 
    def __sub__(self, other: 'Variable') -> 'Variable':
        """ 
        Subtract another variable from this variable RETURNS A NEW variable representing the subtraction

        Args:
            other [Variable]: The other Variable to add to this one
        Returns
            [Variable]: Variable representing the subtraction
        """
        n = Variable(self.varname, self.coefficient-other.coefficient)
        return n

    # -=
    def __isub__(self, other: 'Variable') -> 'Variable':
        """ 
        Subtract another variable from this variable IN PLACE

        Args:
            other [Variable]: The other Variable to add to this one
        Returns
            [Variable]: self after subtraction
        """
        self.coefficient -= other.coefficient
        return self

    # *=
    def __imul__(self, other: 'Variable') -> 'Variable':
        """ 
        Multiply another variable to this variable IN PLACE

        Args:
            other [Variable]: The other Variable to multiply with this one
        Returns
            [Variable]: self after multiplication
        """
        self.coefficient *= other.coefficient
        return self

    # * left multiply
    def __mul__(self, other: 'Variable') -> 'Variable':
        """ 
        Multiply another variable to this variable RETURNS A NEW Variable representing the product

        Args:
            other [Variable]: The other Variable to multiply with this one
        Returns
            [Variable]: Variable representing the multiplication
        """
        n = Variable(self.varname, self.coefficient*other.coefficient)
        return n

    # * right multiply - not used but needs to be overridden to use mul
    def __rmul__(self, other: 'Variable') -> 'Variable':
        """ 
        Multiply another variable to this variable RETURNS A NEW Variable representing the product

        Args:
            other [Variable]: The other Variable to multiply with this one
        Returns
            [Variable]: Variable representing the multiplication
        """
        n = Variable(self.varname, self.coefficient*other.coefficient)
        return n

    # /=
    def __itruediv__(self, other: 'Variable') -> 'Variable':
        """ 
        Divide this variable by other IN PLACE

        Args:
            other [Variable]: The other Variable to multiply with this one
        Returns
            [Variable]: self after division
        """
        self.coefficient /= other.coefficient
        return self

    # /=
    def __ifloordiv__(self, other: 'Variable') -> 'Variable':
        """ 
        identical implementation to itruediv
        """
        self.coefficient /= other.coefficient
        return self

    # /
    def __truediv__(self, other: 'Variable') -> 'Variable':
        """ 
        Divie this variable by other RETURNS A NEW Variable representing the division

        Args:
            other [Variable]: The other Variable to divide with this one
        Returns
            [Variable]: Variable representing the division
        """
        n = Variable(self.varname, self.coefficient/other.coefficient)
        return n

    # /
    def __floordiv__(self, other: 'Variable') -> 'Variable':
        """ 
        identical implementation to truediv
        """
        n = Variable(self.varname, self.coefficient/other.coefficient)
        return n

    # +
    def __add__(self, other: 'Variable') -> 'Variable':
        """ 
        Add another variable to this variable RETURNS A NEW Variable representing the summation

        Args:
            other [Variable]: The other Variable to add to this one
        Returns
            [Variable]: Variable representing the summation
        """
        n = Variable(self.varname, self.coefficient+other.coefficient)
        return n

    # +=
    def __iadd__(self, other: 'Variable') -> 'Variable':
        """ 
        Add another variable to this variable IN PLACE

        Args:
            other [Variable]: The other Variable to add to this one
        Returns
            [Variable]: self after addition
        """
        self.coefficient += other.coefficient
        return self


class LinearExpression():
    """
        Represents an expression in the form of z = c1x1 + c2x2 + ... cnxn

        Supported operations:
            in_terms_of: rewrite the expression in terms of the supplied variable (must exist in rhs)
            get_var: get the variable by name
            substitute: substitude the given variable with subexpression (list of variables) 
    """
    
    def __init__(self, lhs: Variable, rhs: list[Variable]):
        """ """
        self.__lhs = lhs

        # create a dictionary for quick lookup of variables
        self.__rhs = {val.varname:val for val in rhs}
    
    def in_terms_of(self, varname: str):
        if varname not in self.__rhs:
            raise Exception(f"in_terms_of():: Cannot rewrite expression in terms of '{varname}' because it was not found in the expression.")

        repl_val = self.__rhs.pop(varname)
        self.__lhs.coefficient = -self.__lhs.coefficient
        repl_val.coefficient = -repl_val.coefficient

        self.__rhs[self.__lhs.varname] = self.__lhs
        self.__lhs = repl_val
        self.__normalize()

    def get_var(self, varname: str):
        if varname not in self.__rhs:
            raise Exception(f"get_var():: Expression does not have '{varname}' as a variable")

        return self.__rhs[varname]

    def substitute(self, varname: str, expr: list[Variable]):
        if varname not in self.__rhs:
            raise Exception(f"substitute():: Expression does not have '{varname}' as a variable")

        sub_var = self.__rhs.pop(varname)
        sub_expr = [v*sub_var for v in expr]
        
        for var in sub_expr:
            if var.varname in self.__rhs:
                self.__rhs[var.varname] += var
            else:
                self.__rhs[var.varname] = var

    def __normalize(self):
        """
        normalize expression so lhs coefficient = 1
        """

        if self.__lhs.coefficient == 1:
            return

        for _, var in self.__rhs.items():
            var /= self.__lhs

        # same as dividing by itself
        self.__lhs.coefficient = Fraction(1)

    def itervars(self):
        for var in self.rhs.values():
            yield var

    def __repr__(self):
        rhs_str = ""

        for var in self.__rhs.values():
            rhs_str += ' + ' if var.coefficient > 0  else ' - '
            rhs_str += f'{str(abs(var.coefficient))}{var.varname}'

        return f'{self.__lhs.varname} = {rhs_str}'