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
