Name: Matthew Wong
Date: 14 November 2022

Program: Sudoku Solving 
    The program takes a given input file with a unsolved sudoku board, and tries to solve it.
    The program needs the os.path library and sys library in order to read the files. 

Run: 
    To run the program, type "python3 sudokuSolve2.py [filename]"
    where the [filename] is the name of the text file with the sudoku board
    (See board.txt for a format of the board)
    ex "python3 sudokuSolve2.py board.txt"
    Note that you need to put the path, but can just put the file name if they are in the same folder.

Assumptions:
    On the board, blank spaces are denoted with a "X" (NOT LOWER CASE), and numbers are the digits [1-9].
    In addition, it is assumed that the initial set up does not lead to impossible situations and that it is incomplete
    (ie the starting board has a conflict from the get go or the board is already complete).
    Finally, it assumes that the board is in the format given in board.txt, which is listed below;
        + - - - + - - - + - - - +
        | X X X | X X X | X X X |
        | X X X | X X X | X X X | 
        | X X X | X X X | X X X | 
        + - - - + - - - + - - - + 
        | X X X | X X X | X X X |
        | X X X | X X X | X X X | 
        | X X X | X X X | X X X | 
        + - - - + - - - + - - - + 
        | X X X | X X X | X X X |
        | X X X | X X X | X X X | 
        | X X X | X X X | X X X | 
        + - - - + - - - + - - - + 

Design:
        The program uses Depth-First-Search to try to find a solution. Two optimizations that I used 
    were Arc Consistency and Variable Picking. I thought that Value picking did not really help,
    as a value that is availible to be picked will affect the same amount of squares as other
    values in the domain. I also did not do advanced backjumping, as the effect of backjumping 
    does not really help, as almost all of the options will cause some sort of conflict,
    and there is very little times where backjumping would come into play. I thought that
    the overhead cost of checking for backjumping would cancel out the benefits of backjumping.
        In order to do arc consistency, I kept a set for each of the rows, cols, and squares
    which kept track of what values were still left. This is arc consistency, as it kept track
    if there were still values for the other squares to possibly take, even if it doesn't end up working out.
    I also used this set to keep track of the possible domains of the cells, as the domain was the intersection
    of the three sets at the given cell. Since there were only 9 possible values, I found it quite quick 
    to just manually check if 1-9 were in all of the sets. 
        In order to do variable choosing, I did the value with the least amount of options possible. This is because
    the amount of cells impacted by a given cell was mostly the same, so it was better to check by the size of the
    domain. In addition, this allowed be to quickly go down paths that had no options, as when I made a choice that
    caused all of the elements to disappear, that cell would be chosen next immediately, as 0 is the smallest 
    possible size of the intersect. This allowed me to quickly find when I hit a dead end in one extra call onto the
    stack, making it similar to filtering out by set. 
        These two operations made my program very quickly, and the results that I got seemed to be correct when 
    I tested (given my assumptions). 