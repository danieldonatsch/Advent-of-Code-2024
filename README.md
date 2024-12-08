# Advent of Code 2024

## Day 1

## Day 2

## Day 3

## Day 4

First, walk over the whole grid and look for X.
Once, one is found, we check all eight possible directions (left, right, up, down, four diagonals)
if they contain the letters MAS and therefore make an XMAS with the initial X.
We need to be careful with the boarders of the grid!

For the second task, we look for all A, except of the first and last row and column.
Wherever we find an M, we check the two diagonals, if the Form an MAS with the initially found A.
If both diagonals to so, we found an X-MAS and count it.

## Day 5

Given is a list of relations x < y and some lists with values.

First we want to find out which of these lists are ordered correctly, 
in the sense that they fulfill all pair-wise constraints.
Todo so, I build a dict where for each element x all the elements y where stored with x < y.
Then, all each list could be checked by comparing each list element to all the previous elements of the list.
If one of the previous elements is supposed to ba a following one, the list is not correctly sorted.

Afterward, we wanted to sort the unsorted lists.
The approach taken here works only because almost all necessary relations where given in the relations list.
We can use this and count for each list element, how many list elements need to be to its right (aka later in the list).
Based on this count, we can sort the lists.
If there are "ties", we need to break them by looking up, if the "tied" elements are in the relations list.
Swap them, if needed.

## Day 6


## Day 7

Given where the numbers of an equation without the operator, except of the equal sign.
As operators in question one can + and * be used.
In question two additionally a concatenation operator. 
It can be solved straight forward with a recursive (depth first, dfs) method.

## Day 8

Given is a grid of antennas and its frequencies.
Two antennas which have the same frequency send together a signal along the direction their two positions define.

In question one, all the points (so called anti-nodes) need to be found, 
which have the same distance from one of the two antennas as the distance between them.
To solve it, we first search for all antennas and build lists of them, according to their frequencies.
So, all antennas within a least interact with each other and send signals.
Afterward, all antennas within a list are paired.
For each pair, the distance between them is computed and then added to each of the antennas.

In question two, not only the next, but all anti-nodes need to be found.
Again, all antennas within a list (build for question 1) ar paired.
The distance is computed and multiple times added to the antenna positions.
We stop computing anti-nodes, when we leave the grid.
