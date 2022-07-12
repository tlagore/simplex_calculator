# Dictionary Based Simplex Linear Program Solver
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

`python3 simplex_driver.py [debug] < input.txt`

- `debug` is an optional flag. If supplied, the program will print all decisions being made and intermediary dictionaries to `stderr`.  **(warning: large LPs do not have pretty debug output)**

**NOTE:** The program outputs a number of informational messages and statistics about the solved LP, *but is all printed to `stderr`*. Only the solution is printed to stdout.

## Overview of program architecutre

1. The program uses the dictionary based simplex method
2. Initialization: Dual with specially crafted objective function to find an initially feasible dictionary (or declare infeasibility)
3. Pivot Method: The program uses largest increase by default, but can be optionally configured to use largest coefficient
4. Cycle Avoidance: The *always* uses the above pivot method, and uses the symbolic perturbation method (lexicographical as described in Vanderbei) to break ties to avoid cycles 

# Extra Features
## 1. Pivot Method: Largest Increase with Optional Largest Cofficient (Max +1 Point)
The program can be configured to use the Largest Coefficient, or the Largest Increase pivot rule by supplying SimplexConfig with pivot_method set to `PivotMethod.LARGEST_COEFFICIENT` or `PivotMethod.LARGEST_INCREASE` respectively. Default is `LARGEST_INCREASE`.

To enable `LARGEST_COEFFICIENT` modify this line in `simplex_driver.py`:

```python
[15]    simplex_config = SimplexConfig()
[16]    simplex_config.pivot_method = PivotMethod.LARGEST_INCREASE # this line
```

to

```python
[15]    simplex_config = SimplexConfig()
[16]    simplex_config.pivot_method = PivotMethod.LARGEST_COEFFICIENT # to this
```

## 2. Dual Initialization (Max +2 Points)
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

# Appendix
## Long Running Files
All supplied files have been tested against the program and do finish. The longest such file is netlib_share1b.txt, which takes ~13 minutes using the `FIBONNACI` dual intialization  and `LARGEST_INCREASE` pivot rules.

```
optimal
76589.32
333.9 0 77.86822 0 0 3.794088 72.8 0 10.53246 0 0 0 799.4498 0 108.5993 351 0 54.33938 136.3972 10491.44 54369.9 15190.23 1277857 241.5632 0 1158.818 215 8159.058 604 2408.847 162.6116 124 44 428 163 891.1206 82.8 0 0 24.77519 54.46011 0 148.4 0 0 141.3706 0 673.6659 0 59.25929 589.1693 0 2115.6 177710.4 12421.08 3633.588 130.7018 0 123.5357 104 934.7553 0 2020.024 79.35278 121 0 110.4643 890.626 202.0024 575 209.2659 113 0 279 248 9953.891 2848.077 47187.21 0 0 0 0 0 198.7407 108 11197.64 2873.431 62302.87 562.0498 8171.439 6595.421 0 417.8238 49.60279 0 69.11528 0 0 0 422 0 2569.511 4.627695 224.5924 23.01764 0 0 2.388709 10.27614 0 0 0 47.1315 101.9824 0 0 0 6316.159 0 0 0 0 0 0 0 0 0 0 0 4175.28 0 0 0 0 0 0 7122.173 0 0 77.80248 917.0735 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1413.972 0 0 3.564697 4.954708 2.07467 19.66551 5.571858 0 0 0 0 0 87.20019 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2028.4 0 93.86653 41.57828 0 0 1002.185 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 953.405 0 0 64.43365 0 0 0

----------------------------------------------------------------------
| Category    | Stat                          | Value                |
----------------------------------------------------------------------
|             | number of variables:          |                  225 |
| Overview    | number of constraints:        |                  206 |
|             | required auxiliary:           |                  Yes |
----------------------------------------------------------------------
|             | number of pivots:             |                  256 |
|             | number of degenerate pivots:  |                    0 |
| Auxiliary   | avg pivot selection time:     |            0.247069s |
|             | avg pivot time:               |            1.084367s |
|             | solution time:                |              548.05s |
----------------------------------------------------------------------
|             | number of pivots:             |                   91 |
|             | number of degenerate pivots:  |                   35 |
| Main L.P.   | avg pivot selection time:     |            0.471295s |
|             | avg pivot time:               |            1.482558s |
|             | solution time:                |              253.73s |
----------------------------------------------------------------------
```


## Optional test script
`test.sh` can be used to automatically test the files that were supplied in the project description.

**It expects the data to fall under `data/test_LPs_volume1` and `data/test_LPs_volume2`**

It can be run as follows (in the same directory as simplex_driver.py):

`sh test.sh [output_directory]`

Example:

`sh test.sh results/`

It will run every single LP, save the output, and `diff` the file with the expected output