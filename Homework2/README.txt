Matthew Wong
12 October 2022
Homework 2: Pancake Problem
==========================

Purpose:
    The puprose of this program is to write an A* algorithm that can find a sequence of flips to get to the end goal 
    of getting the pancakes, labeled [1, 2, ... , 10] in order. The operation that we have to do that is being able  
    to insert a spatula, and flip over the pancakes above it. 

Running:
    Run the program "python3 Homework2.py" for the non-node program which does not use nodes, 
    Run the program "python3 Homework2WithNode.py" for the node program which does use nodes,
    
    In both cases, it asks for the numbers 1-10 in a random ordering

Help:
    I talked to Tanay Nistala when working on the project

Assumptions:
    The input data is a reordering of the numbers [1, 2, ..., 10]
    I also have the "heapdict" library installed to do make the heap implementation work with decrease-key
    The final goal is to get to the array [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], as the first element is the one closest to the bottom
    The initial array (the starting state) will be inputted by the user 
    The program will only be run one at a time (is not running 2 AStar searches simultaneously)

A* Algorithm:
    Heuristic Function: The number of pancakes are non-adjacent to the one below
    Cost Function     : The amount of flips needed to get to that step

Questions:
    1. Define the search problem;
        The search is to find a sequence of flips to get to the ordering of [1, 2, ... , 10] using flips. 

        Initial State      : The initial ordering of the pancakes
        Possible Action    : Flip (starting from a given index, reverse that portion to the end) 
                             on the indicies 0...8 (9 just flips with itself)
        Successor Function : All possible flips that do not get us to a previous State
        Goal Test          : Whether the ordering is [1, 2, ..., 10]
        Path Cost          : The amount of flips in total
    
    2. Define a possible cost Function
        Cost Function: The amount of flips needed to get to that step

    3. Define a posisble heuristic Function
        Heuristic Function: The number of pancakes are non-adjacent to the one below

    4. Implement an A* algorithm in Python.
        Homework2.py

    5. Could the Uniform-Cost-Search algorithm be used?
        Although a Uniform-Cost-Search could be used (and implemented in Homework2.py), 
        practically, it is not very good. 
        This is because the cost function is just returning 1, so Uniform-Cost-Search is
        very similar to BFS, without overlap. Since the frontier expands exponentially,
        as there are 9 possible options every time, it is not very practical.