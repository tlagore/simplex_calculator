# Dictionary Based Simplex Linear Program Solver
This is an implementation of the [Simplex Algorithm](https://en.wikipedia.org/wiki/Simplex_algorithm) for solving linear programs. Given a linear program in standard form, the program will determine whether the linear program is feasible, unbounded, or it will provide the optimal value, with the assignment of optimization variables that achieves this optimal value.

## Known Issues
This Simplex L.P. solver runs very slow on larger problems. I have tried to look at ways to optimize the code (threading, different data structures, etc), but have not been able to substantially fix it. On certain L.Ps in the practice set, it will run for hours (I have tested over hours and not seen a "cycle", so I do not believe this is do to any poor anti-cycling logic). This is especially notable if the dictionary is highly degenerate, as there are multiple basis variables that tie to become leaving and many comparisons that need to be done on each pivot.

The following LPs are too large to finish in reasonable time: 
```
77K  netlib_klein2.txt
46K  netlib_sc105.txt
90K  netlib_scagr7.txt
140K netlib_share1b.txt
62K  netlib_stocfor1.txt

```

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

`python3 simplex_driver.py [debug|stats] < input.txt`

`debug`/`stats` is an optional parameter. You may only specify one or the other. They are explained below:

- `stats`
    - If the `stats` flag is supplied, the program will print the statistics of the L.P. after running. 
    - Example:

```
python3 simplex_driver.py stats < data/test_LPs_volume1/input/netlib_adlittle.txt 
optimal
-225495
22.85455 0.5454545 4.626937 0 0 35.10714 4.793015 2.942801 0 0 0 54.28986 0 0 108 0 0 0 11.14599 1.854006 0 0 0 0 211.4223 53.57767 0 25.62903 0 83.71014 3.803724 3.920126 0 0 0 134 31 0 0 0 0 60 111.7273 0 51.90909 34 0 0 0 41.5 0 15.47882 0 15 0 0 3.1 0 0.6909091 0 4.143548 171.3012 0 9.806141 0 0 33.46837 9.53163 10.29308 8.906925 0 0 6.1 0 9.792857 313.1974 51.28813 268.6988 0 13.2 0 1.31448 0.5032609 0 0 0 0 0 0 0 0 13.5 8.737073 0 31.2 0 0

Simplex Solver Problem Stats
----------------------------------------------------------------------
| Category    | Stat                                    | Value      |
----------------------------------------------------------------------
|             | number of variables:                    |         97 |
| Overview    | number of constraints:                  |         71 |
|             | required auxiliary:                     |        Yes |
----------------------------------------------------------------------
|             | number of pivots:                       |        311 |
|             | number of degenerate pivots:            |        311 |
| Auxiliary   | avg pivot selection time:               |  0.274903s |
|             | avg pivot time:                         |  0.692572s |
|             | solution time:                          |    176.99s |
----------------------------------------------------------------------
|             | number of pivots:                       |         94 |
|             | number of degenerate pivots:            |         27 |
| Main L.P.   | avg pivot selection time:               |  0.011632s |
|             | avg pivot time:                         |  0.291614s |
|             | solution time:                          |    241.43s |
----------------------------------------------------------------------

```
- `debug`
    - If the `debug` flag is supplied, the program will print all decisions being made and intermediary dictionaries. Flagging debug will also print stats (warning: large LPs do not have pretty debug output)

## Pivot Method
The program can be configured to use the Largest Coefficient, or the Largest Increase pivot rule by supplying SimplexConfig with pivot_method set to `PivotMethod.LARGEST_COEFFICIENT` or `PivotMethod.LARGEST_INCREASE` respectively. Default is `LARGEST_COEFFICIENT`.

**Note:** `LARGEST_INCREASE` has slow pivot selection on larger L.Ps

To enable `LARGEST_INCREASE` modify this line in `simplex_driver.py`:

```python
[15]    simplex_config = SimplexConfig()
[16]    simplex_config.pivot_method = PivotMethod.LARGEST_COEFFICIENT # this line
```

to

```python
[15]    simplex_config = SimplexConfig()
[16]    simplex_config.pivot_method = PivotMethod.LARGEST_INCREASE # to this
```

## Dual Initialization
The L.P. finds an initially feasible dictionary by first checking to see if the prmimal normal form L.P. is already feasible. If not, it performs dual initialization by setting the objective function to 0, then converting the L.P. to it's normal form dual, then solving the dual L.P.

If the Dual L.P. cannot be solved, then the program will output `infeasible`. If the dual L.P. can be solved, the dual of the dual is taken, and the objective function swapped back into the L.P. The program proceeds to attempt to solve the primal L.P. with the initially feasible dictionary provided by the dual problem.

## Cycle Avoidance
The program uses the Lexicographical (Symbolic Perturbation) method for breaking ties on variables leaving the basis. Several symbolic "epsilon" values are added to each constraint. Constraint $w_1$ (or $x_{n+1}$) will have $\epsilon_1$, $w_2$, $\epsilon_2$, etc. With the semantics that $0 < \epsilon_m << \epsilon_{m-1} << ... << \epsilon_1$. Symbolically, these values are on such wildly different scales than one another than there can exist no constant $c$ such that $c\epsilon_i > \epsilon_{i-1}$. Furthermore, each $\epsilon$ is infinitismally small, as to not change the nature of the L.P. being solved.

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

Under the largest coefficient pivot rule, $x_1$ will be chosen as the entering variable. However, there is a tie between $x_5$ and $x_6$ as to which variable should leave the basis. However, by identifying that $e_2 >> e_1$, we unambiguously break the tie, selecting $x_6$ as the leaving variable.


## Cycle-Avoidance Testing
Aside from the theoretical proof that the lexicographical method does not cycle, as far as practical testing goes:

Since there are some very large LPs that do not finish in a reasonable time with this implementation (as seen in the Known Issues section), to test the cycle-avoidance, many LPs with known cycles under specific pivot rules were tested (i.e. an LP known to cycle on largest coefficient, as seen in lecture slides, as well as others). Furthermore, an optional flag can be set which remembers each basis we have seen so far. It does this by sorting the variables $x_1->x_{n+m}$, then hashes this string i.e. if our basis was $x_1, x_3$ and $x_5$, it would hash the string "x1x3x5". This hash is then stored. Every time we perform a pivot, the new hash is calculated and checked against the history. Since the hash is only 4-8 bytes (depending on platform), even after 1,000,000 iterations this would still only take up max 8MB of memory.

To set this flag, in `simplex_driver.py` set the option:

```python
[15]    simplex_config = SimplexConfig()
[16]    simplex_config.pivot_method = PivotMethod.LARGEST_COEFFICIENT
[17]    simplex_config.test_cycle_avoidance = False # this line
```

to

```python
[15]    simplex_config = SimplexConfig()
[16]    simplex_config.pivot_method = PivotMethod.LARGEST_COEFFICIENT
[17]    simplex_config.test_cycle_avoidance = True # to this
```