from decimal import DivisionByZero
import pytest

import operator
from ..rational import Rational

def test_init():
    exception_cases = [
        (1, 0),     # denominator cannot be 0
        (None, 1),  # numerator cannot be none
        (1, -1),    # denominator cannot be negative
        (0.5, 1),   # numerator cannot be float
        (1, 0.5)    # denominator cannot be float
    ]

    number = Rational(1, 1)
    assert number.numerator == 1
    assert number.denominator == 1

    number = Rational(-1, 5)
    assert number.numerator == -1
    assert number.denominator == 5

    for case in exception_cases:
        with pytest.raises(Exception):
            number = Rational(case[0], case[1])

def assert_iop_cases(cases, operation):
    for case, expected in cases.items():
        op = Rational(case[0].numerator, case[0].denominator)
        operand = Rational(case[1].numerator, case[1].denominator)
        operation(op, operand)
        assert op.numerator == expected[0], f"numerator : {op.numerator} did not match expected: {expected[0]}"
        assert op.denominator == expected[1], f"denominator : {op.denominator} did not match expected: {expected[1]}"

def assert_op_cases(cases, operation):
    for case, expected in cases.items():
        op = Rational(case[0].numerator, case[0].denominator)
        operand = Rational(case[1].numerator, case[1].denominator)
        number = operation(op, operand)
        assert number.numerator == expected[0], f"numerator : {number.numerator} did not match expected: {expected[0]}"
        assert number.denominator == expected[1], f"denominator : {number.denominator} did not match expected: {expected[1]}"

def test_simplify():
    """
    To test simplify, we create a bunch of rationals that can be simplified (or not)
    and add 0. The add function simplifies after addition.
    """
    cases = {
        (Rational(2, 4), Rational(0, 1)): (1, 2),
        (Rational(5, 6), Rational(0, 1)): (5, 6),
        (Rational(9, 27), Rational(0, 1)): (1, 3),
        (Rational(18, 3), Rational(0, 1)): (6, 1),
        (Rational(5, 1), Rational(0, 1)): (5, 1)
    }

    assert_op_cases(cases, operator.add)

def test_divide():
    """
    Test adding 2 rationals using the + operator
    """
    cases = {
        (Rational(2, 4), Rational(1, 1)): (1, 2),
        (Rational(5, 6), Rational(1, 4)): (10, 3),
        (Rational(1, 9), Rational(48, 54)): (1, 8),
        (Rational(1, 9), Rational(21, 54)): (2, 7),
        (Rational(18, 3), Rational(1, 8)): (48, 1),
        (Rational(5, 1), Rational(-1, 1)): (-5, 1),
        (Rational(-1, 5), Rational(-1, 1)): (1, 5),
        (Rational(-18, 3), Rational(1, 8)): (-48, 1)
    }
    
    assert_op_cases(cases, operator.truediv)
    assert_op_cases(cases, operator.floordiv)
    assert_op_cases(cases, operator.itruediv)
    assert_op_cases(cases, operator.ifloordiv)

    rat1 = Rational(1,1)
    zero_rational = Rational(0,1)

    with pytest.raises(DivisionByZero):
        rat1 /= zero_rational

    with pytest.raises(DivisionByZero):
        new = rat1 / zero_rational

def test_mul():
    """
    Test adding 2 rationals using the + operator
    """
    cases = {
        (Rational(2, 4), Rational(1, 1)): (1, 2),
        (Rational(5, 6), Rational(1, 4)): (5, 24),
        (Rational(1, 9), Rational(48, 54)): (8, 81),
        (Rational(1, 9), Rational(21, 54)): (7, 162),
        (Rational(18, 3), Rational(1, 8)): (3, 4),
        (Rational(5, 1), Rational(0, 1)): (0, 1),
        (Rational(5, 1), Rational(-1, 1)): (-5, 1),
        (Rational(-1, 5), Rational(-1, 1)): (1, 5),
        (Rational(-18, 3), Rational(1, 8)): (-3, 4)
    }
    
    assert_op_cases(cases, operator.mul)
    assert_op_cases(cases, operator.imul)

def test_add():
    """
    Test adding 2 rationals using the + operator
    """
    cases = {
        (Rational(2, 4), Rational(1, 1)): (3, 2),
        (Rational(5, 6), Rational(18, 3)): (41, 6),
        (Rational(1, 9), Rational(48, 54)): (1, 1),
        (Rational(1, 9), Rational(21, 54)): (1, 2),
        (Rational(18, 3), Rational(1, 8)): (49, 8),
        (Rational(5, 1), Rational(0, 1)): (5, 1),
        (Rational(5, 1), Rational(-1, 1)): (4, 1),
        (Rational(1, 5), Rational(-1, 1)): (-4, 5)
    }
    
    assert_op_cases(cases, operator.add)
    assert_iop_cases(cases, operator.iadd)

def test_subtract():
    """
    Test adding 2 rationals using the - operator
    """
    cases = {
        (Rational(2, 4), Rational(1, 1)): (-1, 2),
        (Rational(5, 6), Rational(18, 3)): (-31, 6),
        (Rational(1, 9), Rational(48, 54)): (-7, 9),
        (Rational(1, 9), Rational(21, 54)): (-5, 18),
        (Rational(18, 3), Rational(-1, 8)): (49, 8),
        (Rational(5, 1), Rational(0, 1)): (5, 1),
        (Rational(5, 1), Rational(1, 1)): (4, 1),
        (Rational(1, 5), Rational(1, 1)): (-4, 5)
    }
    
    assert_op_cases(cases, operator.sub)
    assert_op_cases(cases, operator.isub)

def test_equalities():
    """
    Test adding 2 rationals using the - operator
    """
    op_lookup = {
        operator.le: "<=",
        operator.lt: "<",
        operator.ge: ">=",
        operator.gt: ">",
        operator.eq: "="
    }

    cases = {
        (Rational(1, 1), operator.le, Rational(1, 4)): False,
        (Rational(1, 4), operator.le, Rational(1, 1)): True,
        (Rational(1, 4), operator.le, Rational(1, 4)): True,

        (Rational(1, 1), operator.lt, Rational(1, 4)): False,
        (Rational(1, 4), operator.lt, Rational(1, 4)): False,
        (Rational(1, 4), operator.lt, Rational(3, 8)): True,

        (Rational(2, 4), operator.ge, Rational(1, 1)): False,
        (Rational(1, 4), operator.ge, Rational(1, 8)): True,
        (Rational(2, 4), operator.ge, Rational(1, 2)): True,

        (Rational(99999, 100000), operator.gt, Rational(1, 1)): False,
        (Rational(5, 7), operator.gt, Rational(15, 21)): False,
        (Rational(100001, 100000), operator.gt, Rational(1, 1)): True,
        (Rational(5, 3), operator.gt, Rational(3, 5)): True,

        (Rational(2, 4), operator.eq, Rational(1, 1)): False,
        (Rational(5, 6), operator.eq, Rational(-5, 6)): False,
        (Rational(-1, 2), operator.eq, Rational(1, 2)): False,
        (Rational(1, 2), operator.eq, Rational(1, 2)): True,
        (Rational(32, 2), operator.eq, Rational(16, 1)): True,
        (Rational(-5, 2), operator.eq, Rational(-10, 4)): True,
    }
    
    for (a, op, b), expected in cases.items():
        assert op(a,b) == expected, f"Failed equality assertion. {a} {op_lookup[op]} {b} returned {not expected}, but expected {expected}"