from expression import Variable, Expression
from rational import Rational

import re

expression_re = re.compile('([+-])?(\d)+(\/\d)?([a-zA-Z]+\d+)')


class Simplex():
    def __init__(self):
        """"""
        self.objective_function = None
        self.expressions = None
    

class Parser():
    def __init__(self):
        """"""

    @staticmethod
    def parse(filename):
        simplex = Simplex()

        with open(filename, 'r') as in_file:
            line = in_file.readline()
            # simplex.object_function = Parser.parse_expression(line)

            print(f"first line: {line}")

            line = in_file.readline()

            while line is not None and line != '':
                expr = Parser.parse_expression(line)
                print(expr)
                line = in_file.readline()

        return simplex


    @staticmethod
    def parse_expression(line):
        """ """
        line = line.replace(" ","")
        print(line)
        parts = line.split("<=")
        print(parts)
        fn = parts[0]
        val = int(parts[1])

        ## NOTE: I will need to fix this to read in a rational instead of expecting the fn value to be constant
        ## None is special meaning for the expression meaning it has no variable term
        expr_lst = [Variable(Rational(val, 1), None)]

        match = expression_re.search(fn)
        while match is not None:
            group = match.groups(1)

            # sign is optional for first term, mandatory for subsequent
            sign = group[0]
            # numerator MUST exist

            numerator = int(group[1])

            # denominator optional
            denominator = group[2]
            varname = group[3]

            if sign != 1:
                if sign == '-':
                    numerator = -numerator

            if denominator != 1:
                denominator = denominator.replace("/","")
                numeric_denom = int(denominator)
            else:
                numeric_denom = 1
            
            ## NOTE: we negate the numerator because we are returning the expression
            ## as it will be in the simplex dictionary, i.e. everything on one side
            variable = Variable(Rational(-numerator, numeric_denom), varname)
            expr_lst.append(variable)

            fn = fn.replace(match.groups(0), '')
            match = expression_re.search(fn)

        return Expression(expr_lst)
            
