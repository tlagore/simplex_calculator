# Dictionary Based Simplex Linear Program Solver
### Author: Tyrone Lagore
This is an implementation of the [Simplex Algorithm](https://en.wikipedia.org/wiki/Simplex_algorithm) for solving linear programs. Given a linear program in standard form, the program will determine whether the linear program is feasible, unbounded, or it will provide the optimal value, with the assignment of optimization variables that achieves this optimal value.

## Input
Input is expected to be in the form of a text file with space-delimited values in normal form. For example, the following L.P:
```
max 3x1 + 3x2 
s.t  
     x1 +  x2       <= 3
           x2 - x3  <= 2
 -1/2x1 -  x2       <= 1
           x1,x2,x3 >= 0

```

Would have a representation like:
```0
   3   3   0   
   1   1   0   3
   0   1  -1   2
-0.5  -1   0   1  
```

The positivity constraints are implied, and not required.

## Running the program
The program expects the input to be fed through stdin. No external libraries are required to run the program. Run the program as follows:

`python3 simplex_driver.py < input.txt`

**NOTE:** The program outputs a number of informational messages and statistics about the solved LP, *but is all printed to `stderr`*. Only the solution is printed to stdout.

## Overview of program architecutre

1. The program uses the dictionary based simplex method
2. Initialization: Dual with specially crafted objective function to find an initially feasible dictionary (or declare infeasibility)
3. Pivot Method: The program uses largest increase by default, but can be optionally configured to use largest coefficient
4. Cycle Avoidance: The *always* uses the above pivot method, and uses the symbolic perturbation method (lexicographical as described in Vanderbei) to break ties to avoid cycles 

# Extra Features
## 1. Pivot Method: Largest Increase with Optional Largest Cofficient (Max +1 Point)
**To view the largest increase code**, please view the function `__get_largest_increase_pivot()` in `simplex_dictionary.py`

The program can be configured to use the Largest Coefficient, or the Largest Increase pivot rule by supplying SimplexConfig with pivot_method set to `PivotMethod.LARGEST_COEFFICIENT` or `PivotMethod.LARGEST_INCREASE` respectively. Default is `LARGEST_INCREASE`.

To enable `LARGEST_COEFFICIENT` modify this line in `simplex_dictionary.py`

```python
[15]    simplex_config = SimplexConfig()
[16]    simplex_config.pivot_method = PivotMethod.LARGEST_INCREASE # this line
```

to

```python
[15]    simplex_config = SimplexConfig()
[16]    simplex_config.pivot_method = PivotMethod.LARGEST_COEFFICIENT # to this
```

## 2. Dual-Primal Initialization
**To view the dual-primal intiialization code**, please view `as_dual_init()`, and `as_dual_nf` in `simplex_dictionary.py`

The L.P. finds an initially feasible dictionary by first checking to see if the prmimal normal form L.P. is already feasible. If not, it performs dual initialization by setting the objective function to [some fully negative objective fn] **(several were attempted, see below)** then converting the L.P. to it's normal form dual, then solving the dual L.P.

Originally it was tried to make the objective function to all 0's, but this caused large degeneracies in the Dual LP that made it take an incredibly long time to solve.

If the Dual L.P. cannot be solved, then the program will output `infeasible`. If the dual L.P. can be solved, the dual of the dual is taken, and the objective function swapped back into the L.P. The program proceeds to attempt to solve the primal L.P. with the initially feasible dictionary provided by the dual problem.

objective function values that were tried and some (brief) testing (solving the `netlib_klein2.txt`):

- **All -1**, took 222 pivots and 1026.55 seconds:
- **Negative Fibbonacci**, took only 170 pivots and 388.93 seconds (shorter time choosing pivots):
- **Negative Prime Sequence**, took 239 pivots and 990.53 seconds 
    - clearly the size of the difference in variables matters and helps largest increase to more easily pick a pivot


In the end, I decided to use a Fibonacci Sequence, 

However there is config for a variation of the Fibonnaci Sequence (starts at 2 to avoid degeneracy):

$\{ 2,3,n_{i-2} + ceil((4/5)\cdot n_{i-1}) \}$

This stopps the sequence from balooning as fast on larger LPs (recommended for netlib_share1b.txt), but did not run as fast as the fibonnaci. It took 163 Pivots and 475.45 seconds.

To enable modified fibonnaci, change:
```python
[15]    simplex_config = SimplexConfig()
...
[17]    simplex_config.initialization_function = InitializationFn.FIBONNACI # this line
```

to

```python
[15]    simplex_config = SimplexConfig()
...
[17]    simplex_config.initialization_function = InitializationFn.MODIFIED_FIBONNACI # to this
```

## 3. Lexicographical Cycle Avoidance (Max +4 points)
**To view the lexicographical anti-cycling code**, please view the functions:
    - `__break__break_ties_lgst` in `simplex_dictionary.py` (breaks ties for largest increase pivot method)
    - `__break_ties_lgst` in `simplex_dictionary.py` (breaks ties for largest coefficient pivot method (if enabled))
        - **NOTE**: `__gt__` has been overridden in `LinearExpression` and will return true if the linear expression has a "larger" epsilon than the other expression (as seen in `compare_eps` below)
    - `set_epsilon` and `compare_eps` in `linear_expression.py`

The program uses the Lexicographical (Symbolic Perturbation) method for breaking ties on variables leaving the basis. Several symbolic "epsilon" values are added to each constraint. Constraint $w_1$ (or $x_{n+1}$) will have $\epsilon_1$, $w_2$ will have $\epsilon_2$, etc. With the semantics that $0 < \epsilon_m << \epsilon_{m-1} << ... << \epsilon_1$. Symbolically, these values are on such wildly different scales than one another than there can exist no constant $c$ such that $c\epsilon_i > \epsilon_{i-1}$. Furthermore, each $\epsilon$ is symbolic, and does not change the nature of the L.P. being solved.

We can then use these $\epsilon$ to uniquely identify the leaving variable on all ties.

An example starting dictionary would look as such:

```
--------------------------------------------------------------------------
z =  + (0) + (3/4)x1 - (20)x2 + (1/2)x3 - (6)x4
--------------------------------------------------------------------------
x5 =  + (0) + (1)e1 + (0)e2 + (0)e3 - (1/4)x1 + (8)x2 + (1)x3 - (9)x4
x6 =  + (0) + (0)e1 + (1)e2 + (0)e3 - (1/2)x1 + (12)x2 + (1/2)x3 - (3)x4
x7 =  + (1) + (0)e1 + (0)e2 + (1)e3 + (0)x1 + (0)x2 - (1)x3 + (0)x4
--------------------------------------------------------------------------
```

Under the largest coefficient pivot rule, $x_1$ will be chosen as the entering variable. However, there is a tie between $x_5$ and $x_6$ as to which variable should leave the basis. However, by identifying that $e_1 >> e_2$, we unambiguously break the tie, selecting $x_5$ as the leaving variable.
