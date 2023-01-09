
from sys import argv # Reading the given file
from os.path import isfile # Checking if the file is actually a good file

# Stores the values that are availible [STATES]
rows = [] # The numbers availible in a given row 
cols = [] # The numbers availible in a given column
sqrs = [] # The number availible in a given 3x3 square

# There are 9 rows, columns and squares, each which can have the options [1, 9] [ARC CONSISTENCY]
for i in range(9):
    rows.append(set())
    cols.append(set())
    sqrs.append(set())
# Adding [1,9] to the sets for availibility
for i in range(1,10):
    for j in range(9):
        rows[j].add(i)
        cols[j].add(i)
        sqrs[j].add(i)

# The actual board where the numbers are stored
board = [[]]

'''
    Name       : getSquare(row, col) 
    Parameters : (int) The row of the cell; (int) The column of the cell
    Purpose    : Get the square number [in the sqrs array] associated with a given cell
    Return     : (int) The index in the sqrs array
'''
def getSquare(row : int, col : int):
    return int(col / 3) * 3 + int(row / 3)

#### BOARD CELL VALUES ####

'''
    Name       : insert(val, r, c)
    Parameters : (int) The value which is being inserted into the slot;
                 (int) the row of cell being inserted; (int) the column of the cell being inserted
    Purpose    : Put a number into the slot of the board, as well as update future possible slots
    Return     : (bool) Returns true if insertion was successful, False if it was not a number that could be inserted
    Note       : Depends on rows, cols, sqrs, and board global variables
'''
def insert(val : int, r : int, c: int):
    global rows, cols, sqrs, board

    # If the value causes a conflict/doesn't work, then don't use it
    if val not in rows[r] or val not in cols[c] or val not in sqrs[getSquare(r, c)]:
        return False
    
    # Remove the value from the possible in the row, column, and 3x3 the cell is in
    rows[r].remove(val)
    cols[c].remove(val)
    sqrs[getSquare(r, c)].remove(val)
    # Set the cell
    board[r][c] = val
    return True

'''
    Name       : remove(r, c)
    Parameters : (int) The row of the cell to make free; (int) The column of the cell to make free
    Purpose    : Empties the cell of a number [aka undo an attempt if the path was bad]
    Return     : None
    Note       : Depends on rows, cols, sqrs, and board global variables, as well as insert being already called on the cell
'''
def remove(r : int, c : int):
    global rows, cols, sqrs, board
    # Don't remove if it is an empty cell
    if board[r][c] == 0: 
        return
    # Get the value that is already there (as assumed it is not on an empty)
    val = board[r][c]
    # Note that this only works when insert comes before remove (which is enforced in solve)
    # Readds the values which were taken out of the sets
    rows[r].add(val)
    cols[c].add(val)
    sqrs[getSquare(r, c)].add(val)
    # Unset the cell value
    board[r][c] = 0

#### TRYING CELLS ####
'''
    Name       : findNext()
    Parameters : None
    Purpose    : Finds the next spot [SUCCESSOR FUNCTION] by choosing which has the smallest amount of options [Variable Ordering]
    Return     : (int[]) The [r, c] location of the cell
    Note       : Depends on rows, cols, sqrs, and board global variables
'''
def findNext():
    global rows, cols, sqrs, board
    min = 10
    minPos = [-1, -1]
    # Search the board
    for r in range(9):
        for c in range(9):
            # Find a non-empty cell
            if board[r][c] != 0:
                continue

            # Check the size of the intersection (the domain of the cell)
            count = 0
            for i in range(1, 10):
                if i in rows[r] and i in cols[c] and i in sqrs[getSquare(r, c)]:
                    count += 1
            
            # Find the smallest domain
            if count < min:
                min = count
                minPos = [r, c]
    
    # Return empty if nothing found, otherwise return the coordinates of the next cell
    if minPos == [-1, -1]:
        return []
    return minPos

'''
    Name       : checkBoard()
    Parameters : None
    Purpose    : Checks if the board doesn't have any zeros [GOAL TEST]
    Return     : (bool) Returns whether the board is a solved state
    Note       : Depends on board global variables; the board is assumed not to have any same number conflicts
                 Which is ensured by insertion deleting from the set (which represents the possible items of each
                 row/col/3x3 that any item is in, and can only choose from the intersection)
'''
def checkBoard():
    global board
    # Only check for empty, as non-repeated are implicitly assumed via the sets
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return False
    return True
'''
    Name       : solve(r, c)
    Parameters : (int) The row of the cell to solve for; (int) The column of the cell to solve for
    Purpose    : Tries to solve for the current cell by testing out options (which is the possible values in [1,9]),
                 and tries to recursively solve the board and backtrack [POSSIBLE ACTIONS]
    Return     : (bool) True if the board is solved, False if there is not a solution
    Note       : Depends on rows, cols, sqrs, and board global variables
'''
def solve(r : int, c : int):
    global rows, cols, sqrs, board
    # Try the numbers [1,9]
    for i in range(1,10):
        if insert(i, r, c): # Automatically filters out things that don't work via return False
            nextPos = findNext()
            # Return true if a solution is found
            if nextPos and solve(nextPos[0], nextPos[1]):
                return True
            # If there are no more spots, so check the board
            if not nextPos and checkBoard():
                return True
            remove(r, c) # Removes ONLY IF we have already inserted (via the insert function)
    # Note that it immediately jumps to the false if an empty set is found, so ends when it is empty
    return False

#### RUNNER FUNCTIONS ####
'''
    Name       : initialState()
    Parameters : None
    Purpose    : Sets up the board to the given input upon running (or "board.txt" by default)
    Return     : (bool) True if the board was properly set up, False if the board is not proper
    Note       : Sets the board global variable
'''
def initialState():
    global board
    
    boardFile = "board.txt"
    if len(argv) == 2:
        boardFile = argv[1]
    # Read from board.txt
    if not isfile(boardFile):
        return False
    file = open(boardFile, "r")

    
    # Read line by line, left to right
    row = 0
    col = 0
    for x in file:
        for c in x:
            # Skip over non-valid input
            if c != 'X' and (c < '0' or c > '9'):
                continue 
            
            # Put in the values into the correct slot on the board
            if c == 'X':
                board[row].append(0)
            else:
                board[row].append((int)(c))

            
            # Go to the next slot
            col += 1
            if col >= 9:
                col = 0
                row += 1
                if row < 9: # Don't append the 
                    board.append([])
                if row > 9: # Too many lines
                    file.close()
                    return False
    file.close()

    # If not a good board size, then just return that no board was found
    if len(board) < 9 or len(board[8]) < 9:
        return False
    # Update the values of all of the inputs
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                insert(board[r][c], r, c)
    return True
    
'''
    Name       : printBoard()
    Parameters : None
    Purpose    : Prints the board global variable in a readable manner 
    Return     : None
    Note       : Depends on the board global variable
'''
def printBoard():
    global board
    for r in range(9):
        # Add the top portions of the blocks
        if r % 3 == 0:
            print("+-------+-------+-------+")
        
        for c in range(9):
            if c % 3 == 0:
                # Add the Divider between blocks
                print("|", end=' ')
            
            if board[r][c] == 0:
                print("X", end=' ')
            else:
                print(board[r][c], end=' ')
        
        # Right  edge
        print("|")
    # Bottom line
    print("+-------+-------+-------+")


'''
    Name       : run()
    Parameters : None
    Purpose    : Runs the actual sudoku solving using the helper functions by printing the initial board and solution board
    Return     : None
'''
def run():
    # Only run if valid board is given
    if not initialState():
        print("Invalid Input")
        return
    
    # Print the intial state
    print("Initial")
    printBoard()
    print()

    # Print the solved state
    firstStart = findNext()
    print("Solve")
    solve(firstStart[0], firstStart[1])

    # Print if the board worked out
    if checkBoard():
        printBoard()
    else:
        print("No Solution")

#### RUNNABLE ####
run()