# Facility Location

## Problem Statement

A distribution company uses bulk storage facilities to provide goods to many different customers. The goal of this problem is to determine which facilities will be the most cost effective for serving the customers. The complexity of the problem comes from the fact that each facility has different costs and storage capabilities.

## Assignment

Write an algorithm to solve the facility location problem. The problem is mathematically formu-
lated in the following way: there are N = 0 : : : n􀀀1 facilities to choose from and M = n : : : n+m􀀀1
customers that need to be served. Each facility, f 2 N has a setup cost sf and a capacity capf .
Each customer, c 2 M, has a demand dc. Both the facilities and customers are located in a Euclid-
ian space, hxi; yii i 2 N [M. The cost to deliver goods to a particular customer c from a facility
f is the Euclidean distance between two locations, dist(f ; c).2 Lastly, all customers must be served
by exactly 1 facility. Let af be a set variable denoting the customers assigned to facility f. Then
the facility location problem is formalized as the following optimization problem:

$$\max \displaystyle \sum_{i=0}^{n-1} v_ix_i$$

Subject to:

$$\displaystyle \sum_{i=0}^{n-1} w_ix_i \leq K \text{ where } x_i \in \{0,1\} \ \forall i \in \{ 0, \ldots, n-1 \}$$

## Data Format Specification

A knapsack input contains $n+1$ lines. The first line contains two integers, the first is the number of items in the problem, $n$. The second number is the capacity of the knapsack, $K$. The remaining lines present the data for each of the items. Each line, $i \in \{ 0, \ldots, n-1 \}$ contains two integers, the item's value $v_i$ followed by its weight $w_i$.

Input Format:

```
n K
v_0 w_0
v_1 w_1
...
v_{n-1} w_{n-1}
```

The output contains a knapsack solution and is made of two lines. The first line contains two values $obj$ and $opt$. $obj$ is the total value of the items selected to go into the knapsack (i.e. the objective value). $opt$ should be $1$ if your algorithm proved optimality and $0$ otherwise. The next line is a list of n 0/1-values, one for each of the $x_i$ variables. This line encodes the solution.

Output Format:

```
obj opt
x_0 x_1 x_2 ... x_{n-1}
```

It is essential that the value order in the solution output matches the value order of the input.

## Examples

Input example:

```
4 11
8 4
10 5
15 8
4 3
```

Output example:

```
19 0
0 0 1 1
```

## View the notebooks

[Google Colab Link](https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/facility_location/facility_location.ipynb)
