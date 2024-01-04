# Graph Coloring

## Problem Statement

In this assignment you will design an algorithm to find the smallest coloring of a graph (see http://mathworld.wolfram.com/ChromaticNumber.html). You are provided with a graph and your task is to label the graph's nodes with as few colors as possible such that all pairs of nodes joined by an edge do not have the same color. 

## Assignment

Write an algorithm to minimize the coloring of a graph. The problem is mathematically formulated in the following way. Given a graph $G = \langle N, E \rangle$ with nodes $N \in \{ 0, \ldots, n-1 \}$ and edges $E$, let $c_i \in \mathcal{N}$ be a variable denoting the color of node $i$. Then the graph coloring problem is formalized as the
following optimization problem,

$$\max_{i \in \{ 0, \ldots, n-1 \}} c_i$$

Subject to:

$$c_i \neq c_j \left( \langle i, j \rangle \in E \right)$$

## Data Format Specification

The input consists of $\lvert E \rvert + 1$ lines. The first line contains two numbers $\lvert N \rvert$ and $\lvert E \rvert$. It is followed by $\lvert E \rvert$ lines, each line represents an edge $\lvert u_i, v_j \rvert$ where $u_i, v_j \in \{ 0, \ldots \lvert N \rvert - 1 \}$.

Input Format:

```
|N| |E|
u_0 v_0
u_1 v_1
...
u_{|E|-1} v_{|E|-1}
```

The output has two lines. The first line contains two values $obj$ and $opt$. $obj$ is the numbers of colors used in the coloring (i.e. the objective value). $opt$ should be $1$ if your algorithm proved optimality and $0$ otherwise. The next line is a list of $n$ values in $\mathcal{N}, one for each of the ci variables. This line encodes the solution.

Output Format:

```
obj opt
c_0 c_1 c_2 ... c_{n-1}
```

It is essential that the value order in the solution output matches the value order of the input.

## Examples

Input example:

```
4 3
0 1
1 2
1 3
```

Output example:

```
3 0
0 1 2 2
```

## View the notebooks

[Solution using Tabu search](https://colab.research.google.com/github/jacubero/Optimization/blob/master/coloring/tabu.ipynb)

