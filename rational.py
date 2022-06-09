from decimal import DivisionByZero
import math
import operator

from typing import Type

class Rational():
    """
    Describes a rational number of the form p/q where both p and q are whole integers.

    Supports all operations, addition, subtraction, division, multiplication, and equality.

    Every pythonic operator is overridden for the above operations, 
    i.e: + += - -= / /= * *= and ==

    Note that == returns true if the 2 rational numbers *represent the same rational number*, 
    which is true for fractions like (2/4 == 1/2). 
    """
    def __init__(self, numerator, denominator=1):
        if denominator <= 0 or denominator is None or not isinstance(denominator, int):
            raise Exception("Denominator must be an integer, " +
                "cannot be less than or equal to 0, and cannot be None. " +
                "Use '1' for whole numbers. Make the numerator negative for negative rationals.")

        if numerator is None or not isinstance(numerator, int):
            raise Exception("Numerator must be an integer")

        self.numerator = numerator
        self.denominator = denominator

    def __subtract(self, other, in_place):
        print(f"{self} - {other} -> ", end='')
        subtractor = Rational(-other.numerator, other.denominator)

        return self.__add(subtractor, in_place)

    def __add(self, other, in_place):
        print(f"{self} + {other} -> ", end='')

        if self.denominator == other.denominator:
            # covers whole numbers (both None) and shared denominators
            if in_place:
                self.numerator += other.numerator
            else:
                return Rational(self.numerator + other.numerator, self.denominator)
        else:
            new_denominator = Rational.__lcm(self.denominator, other.denominator)

            # we don't mutate here
            adder = self.__change_denominator(new_denominator)
            addend = other.__change_denominator(new_denominator)

            summand = Rational(adder.numerator + addend.numerator, new_denominator)

            summand.simplify()

            print(f"{summand}")
            
            if in_place:
                self.numerator = summand.numerator
                self.denominator = summand.denominator
                return self
            else:
                return summand

    def __divide(self, divisor, in_place):
        """
        Divide two rationals by flipping the numerator and denominator and multiplying
        """
        if divisor.numerator == 0:
            raise DivisionByZero(f"Cannot perform division as divisor has numerator of {divisor.numerator}")

        print(f"{self} / {divisor} -> ", end = '')

        # flip the divisor, maintain the sign of the numerator
        new = Rational(int(math.copysign(divisor.denominator, divisor.numerator)), abs(divisor.numerator))
        
        return self.__multiply(new, in_place)
    
    def __multiply(self, other, in_place):
        """
        Multiply two rationals
        """
        print(f"{self} * {other} -> ", end='')
        if in_place:
            new = self
        else:
            new = self.__deepclone()

        new.numerator = new.numerator * other.numerator
        new.denominator = new.denominator * other.denominator
        new.simplify()

        print(f"{new}")
        return new

    def simplify(self, in_place=True):
        """
        Simplifies this rational number and returns it. If in_place is set to true, it will simplify this object
        """
        my_gcd = math.gcd(self.numerator, self.denominator)
        
        new = Rational(self.numerator, self.denominator)
        if my_gcd != 1:
            new.numerator //= my_gcd
            new.denominator //= my_gcd

        if in_place:
            self.numerator = new.numerator
            self.denominator = new.denominator

        return new

    def __change_denominator(self, new_denominator: int):
        """ 
            change denominator to a new denominator, while preserving the 
            rational number. Does not type check as it is an internal function

            Args:
                new_denominator [int]: The new denominator for the fraction
            Returns:
                [Rational]: A new Rational number representing the changed denominator 
            Raises:
                Exception if the denominator cannot be set and remain a rational number in the format p/q where both p and q are integers
        """
        lower = min(self.denominator, new_denominator)
        higher = max(self.denominator, new_denominator)

        if higher % lower != 0:
            raise Exception(f"Cannot raise fraction {self} to denominator {new_denominator} without creating non-integer numerator")

        multiplier = new_denominator // self.denominator

        # same denominator
        if multiplier == 1:
            new_numerator = self.numerator
        else:
            new_numerator = self.numerator * multiplier

        return Rational(new_numerator, new_denominator)
        
    def __unify(a: 'Rational', b: 'Rational'):
        """
        unify takes in rational a and b and returns a tuple of Rationals (a^, b^)
        with both fractions having the same denominator (for comparisons)
        """
        a_hat = a.__deepclone()
        b_hat = b.__deepclone()
        lcm = Rational.__lcm(a_hat.denominator, b_hat.denominator)

        a_hat = a_hat.__change_denominator(lcm)
        b_hat = b_hat.__change_denominator(lcm)

        return (a_hat, b_hat)

    def __lcm(a: int, b: int) -> int:
        """ Finds the lowest common multiple of 2 integers numbers"""
        if a == b:
            return a
        else:
            return (a*b) // math.gcd(a,b)

    def __deepclone(self):
        return Rational(self.numerator, self.denominator)

    def __compare(self, other, comparator: operator):
        """ compare 2 rational numbers with some comparator"""
        (a,b) = Rational.__unify(self, other)
        return comparator(a.numerator,b.numerator)

    ## OVERRIDES:
    def __repr__(self):
        """ string format a/b or a if b = 1"""
        return "({0}{1})".format(self.numerator, '/' + str(self.denominator) if self.denominator != 1 else '')

    # negation -
    def __neg__(self):
        """ 
        Override of negation. Allows user to perform -rational to invert sign of rational.
        """
        n = Rational(-self.numerator, self.denominator)
        return n

    # >
    def __gt__(self, other):
        return self.__compare(other, operator.gt)

    # >=
    def __ge__(self, other):
        return self.__compare(other, operator.ge)

    # <
    def __lt__(self, other):
        return self.__compare(other, operator.lt)

    # <=
    def __le__(self, other):
        return self.__compare(other, operator.le)

    # >
    def __eq__(self, other):
        """ 
        Override of ==. Checks that they both represent the *same rational number*, not that their numerator and denominator are the saem
        """
        a = self.simplify(in_place=False)
        b = other.simplify(in_place=False)

        return a.numerator == b.numerator and a.denominator == b.denominator

    # required for ==
    def __hash__(self):
        return object.__hash__(self)

    # - 
    def __sub__(self, other):
        """ 
        Subtract another rational number from this rational number RETURNS A NEW RATIONAL representing the subtraction

        Args:
            other [Rational]: The other rational to add to this one
        Returns
            [Rational]: Rational representing the subtraction
        """
        return self.__subtract(other, in_place=False)

    # -=
    def __isub__(self, other):
        """ 
        Subtract another rational number from this rational number IN PLACE

        Args:
            other [Rational]: The other rational to add to this one
        Returns
            [Rational]: self after subtraction
        """
        self.__subtract(other, in_place=True)
        return self

    # *=
    def __imul__(self, other):
        """ 
        Multiply another rational number to this rational number IN PLACE

        Args:
            other [Rational]: The other rational to multiply with this one
        Returns
            [Rational]: self after multiplication
        """
        return self.__multiply(other, in_place=True)

    # * left multiply
    def __mul__(self, other):
        """ 
        Multiply another rational number to this rational number RETURNS A NEW RATIONAL representing the product

        Args:
            other [Rational]: The other rational to multiply with this one
        Returns
            [Rational]: Rational representing the multiplication
        """
        return self.__multiply(other, in_place=False)

    # * right multiply - not used but needs to be overridden to use mul
    def __rmul__(self, other):
        """ 
        Multiply another rational number to this rational number RETURNS A NEW RATIONAL representing the product

        Args:
            other [Rational]: The other rational to multiply with this one
        Returns
            [Rational]: Rational representing the multiplication
        """
        return self.__multiply(other, in_place=False)

    # /=
    def __itruediv__(self, other):
        """ 
        Divide this rational number by other IN PLACE

        Args:
            other [Rational]: The other rational to multiply with this one
        Returns
            [Rational]: self after division
        """
        return self.__divide(other, in_place=True)

    # /=
    def __ifloordiv__(self, other):
        """ 
        identical implementation to itruediv
        """
        return self.__divide(other, in_place=True)

    # /
    def __truediv__(self, other):
        """ 
        Divie this rational number by other RETURNS A NEW RATIONAL representing the division

        Args:
            other [Rational]: The other rational to divide with this one
        Returns
            [Rational]: Rational representing the division
        """
        return self.__divide(other, in_place=False)

    # /
    def __floordiv__(self, other):
        """ 
        identical implementation to truediv
        """
        return self.__divide(other, in_place=False)

    # +
    def __add__(self, other):
        """ 
        Add another rational number to this rational number RETURNS A NEW RATIONAL representing the summation

        Args:
            other [Rational]: The other rational to add to this one
        Returns
            [Rational]: Rational representing the summation
        """
        return self.__add(other, in_place=False)

    # +=
    def __iadd__(self, other):
        """ 
        Add another rational number to this rational number IN PLACE

        Args:
            other [Rational]: The other rational to add to this one
        Returns
            [Rational]: self after addition
        """
        return self.__add(other, in_place=True)