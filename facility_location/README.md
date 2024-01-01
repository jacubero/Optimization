# Facility Location

## Problem Statement

A distribution company uses bulk storage facilities to provide goods to many different customers. The goal of this problem is to determine which facilities will be the
most cost eective for serving the customers. The complexity of the problem comes from the fact
that each facility has dierent costs and storage capabilities.1

## Assignment

Write an algorithm to solve the knapsack problem. The problem is mathematically formulated in the following way. Given $n$ items to choose from, each item $i \in \{ 0, \ldots, n-1 \}$ has a value $v_i$ and a
weight $w_i$. The knapsack has a limited capacity $K$. Let $x_i$ be a variable that is $1$ if you choose to take item $i$ and $0$ if you leave item $i$ behind. Then the knapsack problem is formalized as the following optimization problem,

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
