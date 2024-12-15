# Advent of Code 2024

This repository hosts my Python solutions of the Advent of Code 2024 puzzles.
The full puzzle description and the input can be found on [https://adventofcode.com/2024](https://adventofcode.com/2024|).
To run the code, the input files need to be placed in the `input` directory.
The files are either named `dayXX.txt` or `dayXX_example.txt` 
where  `XX` has to be replaced with the day as a tow-digit numbers.
Further, the one with `_example` in the name, contains the input of the small example given in the puzzle description.
If the second question of the day has a different example, create a `dayXX_example2.txt` file.
Run then day by day with `run.py` 
where in the last lines of the script the day (as integer) and whether the example or "real" input should be used.
`test_all.py` runs, as its name says, all puzzles.
Or at least, all which are solved until that moment.

## Day 1

Pairs of numbers are given, where actually each number belongs to a list.
Question is, what is the difference of the two lists, if we look at the (sorted) pairs.
So, build the list and sort them.
Then compare pair-wise and sum the result.
\
Then we compute a similarity score by figuring out, how often each element of the first list appears in the second one.
Python's `collections.Counter()` does the counting quick and easy.
Afterward, we can compare the two counters.

## Day 2

Given is a list of lists of numbers.
First, we looked for all lists which are either strictly increasing or decreasing and 
the difference between two consecutive numbers at most three.
This is pretty straight forward:
Use the first two elements to define if the list is supposed to be increasing or decreasing.
The rest is comparing consecutive numbers.
\
In question two, we looked (additionally) for the lists where all except of one element followed the rule.
Since the lists are short (7 entries), it is possible to try out every possibility:
Leave out each element once and check the list.
This is exactly seven times the number of lists and so still linear O(n) in the numer of lists.

## Day 3

A long string with broken math is given.
In question one, we need to look for all valid multiplications (`mul(x,y)`), where x and y are numbers.
This can be done with a regex search.
\
In question two we also considered `do()` and `don't()` functions which turned on or off the following multiplications.
Again we use regex and simple search for the next occurrence of each kind.
We then see, which comes first and apply it, i.e. either switch on or off our calculater or process the multiplication.

## Day 4

First, walk over the whole grid and look for X.
Once, one is found, we check all eight possible directions (left, right, up, down, four diagonals)
if they contain the letters MAS and therefore make an XMAS with the initial X.
We need to be careful with the boarders of the grid!
\
For the second task, we look for all A, except of the first and last row and column.
Wherever we find an M, we check the two diagonals, if the Form an MAS with the initially found A.
If both diagonals to so, we found an X-MAS and count it.

## Day 5

Given is a list of relations x < y and some lists with values.
\
First we want to find out which of these lists are ordered correctly, 
in the sense that they fulfill all pair-wise constraints.
Todo so, I build a dict where for each element x all the elements y where stored with x < y.
Then, all each list could be checked by comparing each list element to all the previous elements of the list.
If one of the previous elements is supposed to ba a following one, the list is not correctly sorted.
\
Afterward, we wanted to sort the unsorted lists.
The approach taken here works only because almost all necessary relations where given in the relations list.
We can use this and count for each list element, how many list elements need to be to its right (aka later in the list).
Based on this count, we can sort the lists.
If there are "ties", we need to break them by looking up, if the "tied" elements are in the relations list.
Swap them, if needed.

## Day 6

Given is a grid with a starting point and obstacles.
Starting at the start point, moving straight until hitting an obstacle, then turning right, 
we count the number of steps until we leave the grid.
There is no magic, this task has to be performed. 
\
Then we try to add one obstacle, such that we never leave the grid, i.e. at some point the path becomes a loop.
We do this, by (again) following the path.
But now, each time we hit a new, empty grid cell, we first virtually place an obstacle.
Then we turn right and see if this new path leads to a loop.
Once this is figured out, the temporary obstacle is removed and the original path continued.
To detect the loop, we mark on each visited cell all directions we've been walking on with a bit-mask.
Then, when we return to this cell, we quickly can see, if it matches the direction of a previous visit 
(and therefore a loop starts) or not.

## Day 7

Given are the numbers of an equation without the operator, except of the equal sign.
Possible operators are `+` and `*`.
In question two additionally a concatenation operator is possible.
It can be solved straight forward with a recursive (depth first, dfs) method.

## Day 8

Given is a grid of antennas and its frequencies.
Two antennas which have the same frequency send together a signal along the direction their two positions define. \
In question one, all the points (so called anti-nodes) need to be found, 
which have the same distance from one of the two antennas as the distance between them.
To solve it, we first search for all antennas and build lists of them, according to their frequencies.
So, all antennas within a least interact with each other and send signals.
Afterward, all antennas within a list are paired.
For each pair, the distance between them is computed and then added to each of the antennas.
\
In question two, not only the next, but all anti-nodes need to be found.
Again, all antennas within a list (build for question 1) ar paired.
The distance is computed and multiple times added to the antenna positions.
We stop computing anti-nodes, when we leave the grid.

## Day 9

Given where file lengths and spaces after them in a consecutive string.
So, 1234 means first file has size 1, it follows empty space of size 2, then file of size 3, etc.
First goal was to shrink the used memory as much as possible, 
by moving the files from the end of the "memory" in the empty spaces at the beginning.
Files could be moved partially.
One solution is to build the whole memory, including the empty spaces (O(n)).
Then use two pointers, one from left, one from right and move them towards each other.
The left shows the most left empty space, the right one the most right file part.
Then, this file part can be moved to the empty space the left pointer points on.
\
In question two only whole files could be moved,
i.e. we need to look for empty memory, which is big enough to fit the file.
We do this by maintaining to lists.
One with the used memory and one with the empty memory.
Then we start processing the used memory list from right and search through the empty memory list from left.
If we find space, we move the file to it and update the two lists.
The empty memory list is the tricky one: Remove the free space where it was found is one thing.
Freeing up the previously used space another: We add it to the previous free space.
Lastly, we look if we can now concatenate it also with the following free space.
Unfortunately, this solution is quadratic O(n^2), but still fast enough to solve the puzzle in reasonable time.

## Day 10

Given is a map (2-d grid) where each position on the map has a value 0 to 9.
To earn the first start, we need to count all reachable peaks (nine-values) when starting at all zero fields.
First, we walk over the grid and look for all zeros (possible starting points).
Going from there, we use breadth first search (BFS) to find all reachable peaks.
Using a set to save all positions on a height level prevents us from visiting the same position multiple times.
\
Second, we count all possible path.
It is very similar to the peak counter.
The only difference is, that we count the number of ways to reach it.
So, instead of having a set with positions for a level, we use a dict.
The dict key is the position, the value the number of path leading to it.

## Day 11

Given are a few numbers and a process, how they develop in each step.
Some change value, some split such that we have afterward two numbers.
Question is, how many numbers we have after x steps, starting with the few numbers given.
First we're asked for the number of numbers after 25 steps.
It is possible to compute this "brute-force-style".
We can do this for example with a recursive function (DFS-style).
For more steps (75 in question 2) a more efficient approach is needed, since the number numbers grows exponential.
The idea is, to keep for each a map with the number that appear as keys.
The count, how often they apper, is value stored for the key.
Then we compute how each number develops only once and multiply it by its count.
Further, we can cache previously computed development steps.

## Day 12

The first goal is to compute the area and perimeter of the grid cells with the same value.
To find out, which cells are connected, we can use a recursive approach.
It returns a list of the cell coordinates.
The length of the list is already half of the answer: The area.
To get the perimeter we need to figure out how many cell edges are outwards facing.
So, we check for each grid cell, which of the neighbours are not in the list and count them.
\
In the second part, we count the sides.
Grid cell edges are "merged" into one side if they are directly connected and in-line.
We follow a similar approach as for the perimeter.
But when looking for outwards-facing edges, we group them together and look at the end, if they are connected or not.

## Day 13

Given are 2-D locations `P = (Px, Py)` and two possibles moves `A = (Ax, Ay)`, `B = (Bx, By)`.
All numbers are integers.
Question is, is it possible to reach P with a combination of A and B steps.
A (mathematical) reformulation of the problem is, do integer numbers a and b exists,
such that `a * Ax + b * By = Px` and `a * Ax + b * By = Py`.
This is a 2 x 2 equation system which can be solved!
After solving it, we just have to check if a and b are integer numbers.

## Day 14

Given is a rectangular space and a list of robots.
Each robot has a starting position and a velocity, given in fields it moves per second.
If a robot reaches the end of the field, it re-appears at the other end of the field.
So, the field is kind of a sphere, where the robots can go around.
Question is, what are the robot locations after a given time.
Answer: Move the robot for the whole time forward and then compute the location module the grid size.
\
Then we got the info, that at some point the robots from a Christmas tree.
But we don't know when.
How to find out?
It turned out, there is a bounding box around the Christmas tree.
So, we let the robots and check after each step for signs of a bounding box.
We do this by picking the two rows with the most robots in it.
Then, we see which is the most left and most right position, which have robots located in both rows.
This four points define the bounding box.
We look then, how many robots are within the bounding box.
If it is more than 70% of all the robots, we check the grid visually.
Instead of counting the robots in the supposed bounding box, we also could try if the bounding box is a "solid" line. 

## Day 15

A robot moves up, down, left right if it can.
It can move, if the field it wants to move is either free or it has a box which could be moved.
In the first case, the boxes have a size of one field.
So, we check for each field if it is free, is a wall or a box.
In the case of a box, we figure out, if it can be moved by calling the same function again with the box location now.
\
In the second case, boxes have a size of one field high but two fields wide.
To check, if we can move horizontally it is the same as in the previous case.
Vertically is more tricky: We need to make sure that we move whole boxes not just the half which the robot pushes on.
It can be solved with a recursive function, too.


