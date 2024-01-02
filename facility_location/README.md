# Facility Location

## Problem Statement

A distribution company uses bulk storage facilities to provide goods to many different customers. The goal of this problem is to determine which facilities will be the most cost effective for serving the customers. The complexity of the problem comes from the fact that each facility has different costs and storage capabilities.

## Assignment

Write an algorithm to solve the facility location problem. The problem is mathematically formulated in the following way: there are $N \in \{ 0, \ldots, n-1 \}$ facilities to choose from and $M \in \{ n, \ldots, n+m-1 \}$ customers that need to be served. Each facility, $f \in N$ has a setup cost $s_f$ and a capacity $cap_f$. Each customer, $c \in M$, has a demand $d_c$. Both the facilities and customers are located in a Euclidian space,$\langle x_i, y_i \rangle \ \forall i \in N \cup M$. The cost to deliver goods to a particular customer $c$ from a facility $f$ is the Euclidean distance between two locations, $dist(f, c)$. Lastly, all customers must be served by exactly $1$ facility. Let $a_f$ be a set variable denoting the customers assigned to facility $f$. Then the facility location problem is formalized as the following optimization problem:

$$\min \displaystyle \sum_{f \in N} \left( \left( \lvert a_f \rvert > 0 \right)s_f + \sum_{c \in a_f} dist(f, c) \right) \text{ where } dist(i, j)= \sqrt{(x_i-x_j)^2+(y_i-y_j)^2} $$

Subject to:

$$\displaystyle \sum_{c \in a_f} d_c \leq cap_f \ (f \in N)$$

$$\displaystyle \sum_{f \in N} \left( c \in a_f \right)=1 \ (c \in M)$$

## Data Format Specification

The input consists of $\lvert N \rvert+\lvert M \rvert+1$ lines. The first line contains two numbers, $\lvert N \rvert$ followed by $\lvert M \rvert$. The first line is followed by $\lvert N \rvert$ lines, where each line encodes the facility's setup cost $s_f$, capacity $cap_f$, and the location $x_f$, $y_f$. The remaining $\lvert M \rvert$ lines capture the customer information, where each line encodes the customer's demand, $d_c$, and location $x_c$, $y_c$.

Input Format:

```
|N| |M|
s_0 cap_0 x_0 y_0
s_1 cap_1 x_1 y_1
...
s_{|N|-1} cap_{|N|-1} x_{|N|-1} y_{|N|-1}
d_{|N|} x_{|N|} y_{|N|}
d_{|N|+1} x_{|N|+1} y_{|N|+1}
...
d_{|N|+|M|-1} x_{|N|+|M|-1} y_{|N|+|M|-1}
```

The output has two lines. The first line contains two values: $obj$ and $opt$. $obj$ is the cost of the customer to facility assignment (i.e. the objective value) as a real number. $opt$ should be $1$ if your algorithm proved optimality and $0$ otherwise. The next line is a list of $\lvert M \rvert$ values in $N$ - this is the mapping of customers to facilities.

Output Format:

```
obj opt
c_0 c_1 c_2 ... c_{|M|-1}
```

It is essential that the value order in the solution output matches the value order of the input.

## Examples

Input example:

```
3 4
100 100 1065.0 1065.0
100 100 1062.0 1062.0
100 500 0.0 0.0
50 1397.0 1397.0
50 1398.0 1398.0
75 1399.0 1399.0
75 586.0 586.0
```

Output example:

```
2550.013 0
1 1 0 2
```

This output represents the assignment of customers to facilities, $a_0 = \{ 2 \}$, $a_1 = \{0, 1 \}, $a_2 = \{ 3 \}$. That is, customers 0 and 1 are assigned to facility 1, customer 2 is assigned to facility 0, and customers 3 is assigned to facility 2.

## View the notebooks

[Google Colab Link](https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/facility_location/facility_location.ipynb)
