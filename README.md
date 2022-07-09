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
```
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
python simplex_driver.py stats < data/mine/cycle2.txt 
optimal
0.5
2.5 1.5 0 0 0.5 0 0

Simplex Solver Problem Stats
----------------------------------------------------------------------
| Category    | Stat                                    | Value      |
----------------------------------------------------------------------
|             | number of variables:                    |         13 |
| Overview    | number of constraints:                  |          6 |
|             | required auxiliary:                     |        Yes |
----------------------------------------------------------------------
|             | number of pivots:                       |          1 |
| Auxiliary   | number of degenerate pivots:            |          1 |
|             | solution time:                          |      0.01s |
----------------------------------------------------------------------
|             | number of pivots:                       |          6 |
| Main L.P.   | number of degenerate pivots:            |          3 |
|             | solution time:                          |      0.06s |
----------------------------------------------------------------------
```
- `debug`
    - If the `debug` flag is supplied, the program will print all decisions being made and intermediary dictionaries. Flagging debug will also print stats

## Dual Initialization
The L.P. finds an initially feasible dictionary by first checking to see if the normal form L.P. is already feasible. If not, it performs dual initialization by setting the objective function to 0, then solving the dual L.P.

If the Dual L.P. cannot be solved, then the program will output `infeasible`. If the dual L.P. can be solved, the dual of the dual is taken, and the objective function swapped back into the L.P. The program proceeds to solve the primal L.P. with the initially feasible dictionary provided by the dual problem.

## Pivot Method
The program uses the Largest Coefficient rule for all pivoting decisions

## Cycle Avoidance
The program uses the Lexicographical method for breaking ties.  Using the above L.P. as an example, several symbolic "epsilon" values are added to each constraint. Constraint $w_1$ (or $x_{n+1}$) will have $\epsilon_1$, $w_2$, $\epsilon_2$, etc. With the semantics that $0 < \epsilon_1 << \epsilon_2 << ... << \epsilon_m$. Symbolically, these values are on such wildly different scales than one another than there can exist no constant $c$ such that $c\epsilon_{i-1} > c\epsilon_i$.

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

Proof that this method ensures that the program never cycles is left as an exercise to the reader.