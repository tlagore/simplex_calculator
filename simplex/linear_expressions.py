from fractions import Fraction

class Variable():
    """ """

    CONSTANT = 'C'

    def __init__(self, varname: str, coefficient: Fraction):
        """ """
        self.coefficient = coefficient
        self.varname = varname

    def deepclone(self):
        return Variable(self.varname, Fraction(self.coefficient))

    def __repr__(self):
        msg = ''
        msg += ' + ' if self.coefficient >= 0  else ' - '
        msg += f'({str(abs(self.coefficient))})'
        msg += self.varname if self.varname != Variable.CONSTANT else ''
        return msg

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
        self.set_expression(lhs, rhs)
    
    def rhs_vars(self):
        return list[self.__rhs.keys]

    def num_terms(self):
        """ -1 for constant term """
        return len(self.__rhs) - 1

    def set_expression(self, lhs: Variable, rhs: list[Variable]):
        """
        """
        self.__lhs = lhs

        # create a dictionary for quick lookup of variables
        # deepclone in case caller is reusing variables
        self.__rhs = {val.varname:val.deepclone() for val in rhs}
        if Variable.CONSTANT not in self.__rhs:
            raise Exception(f"Cannot create a linear expression without a constant term. This can be 0, but must exist with the variable name '{Variable.CONSTANT}'")

    def in_terms_of(self, varname: str):
        if varname not in self.__rhs:
            raise Exception(f"in_terms_of():: Cannot rewrite expression in terms of '{varname}' because it was not found in the expression.")

        repl_val = self.__rhs.pop(varname)
        self.__lhs.coefficient = -self.__lhs.coefficient
        repl_val.coefficient = -repl_val.coefficient

        self.__rhs[self.__lhs.varname] = self.__lhs
        self.__lhs = repl_val
        self.__normalize()

        return list(self.__rhs.values())

    def get_constant(self):
        if Variable.CONSTANT not in self.__rhs:
            raise Exception(f'Expression did not have a constant variable')

        return self.__rhs[Variable.CONSTANT]

    def get_var(self, varname: str):
        if varname not in self.__rhs:
            return None

        return self.__rhs[varname]

    def get_lhs(self):
        return self.__lhs.deepclone()

    def varname(self):
        return self.__lhs.varname

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
        for var in self.__rhs.values():
            yield var.deepclone()

    def deepclone(self):
        lhs = self.__lhs.deepclone()
        rhs = [var.deepclone() for var in self.__rhs.values()]

        return LinearExpression(lhs, rhs)

    def deepequals(self, other: 'LinearExpression'):
        """ Check if expression other deepequals self
            This does not care the order of the variables

            deepequals is onlyt used for testing, so it has print statements in it
        """
        if other.__lhs != self.__lhs:
            return False

        for key, var in self.__rhs.items():
            other_var = other.get_var(key)
            if var.coefficient != other_var.coefficient:
                print(f"Variable: '{key}' did not match. {var.coefficient} != {other_var.coefficient}")
                return False

        return True

    def __repr__(self):
        rhs_str = ""

        rhs_vars = list(self.__rhs.values())
        rhs_vars.sort(key=lambda v: v.varname)

        for var in rhs_vars:
            rhs_str += repr(var)

        prefix = '' if self.__lhs.coefficient >= 0  else '-'

        return f'{prefix}{self.__lhs.varname} = {rhs_str}'