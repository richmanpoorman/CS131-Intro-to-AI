
### CLASS ###
'''
    Name       : Square
    Parameters : (int) the value to start out as (optional)
    Purpose    : Stores the variable of the sudoku board
'''
class Square:
    '''
        Name       : __init__
        Parameters : [char] the OPTIONAL character to store at the spot
        Purpose    : Create the square to 
        Return     : None
    '''
    def __init__(self, val = 0):
        self.val = val
        self.possible = set()
        self.tested = []
        for i in range(1,10):
            if i != val:
                self.possible.add(i)
    
    '''
        Name       : isSet
        Parameters : None
        Purpose    : Returns if the value has been set or not
        Return     : (bool) Whether the square has been set to a value
    '''
    def isSet(self):
        return self.val != 0
    
    '''
        Name       : setVal
        Parameters : (char) value to set
        Purpose    : Sets the value of the square
        Return     : None
    '''
    def setVal(self, newVal):
        self.val = newVal
    
    '''
        Name       : unsetVal
        Parameters : None
        Purpose    : Makes the square blank again
        Return     : None
    '''
    def unsetVal(self):
        self.val = 0
    
    '''
        Name       : removePossible
        Parameters : (int) Value that it can not be
        Purpose    : Removes a possibility from what the square is
        Return     : None
    '''
    def removePossible(self, val):
        if val in self.possible:
            self.possible.remove(val)
    
    '''
        Name       : addPossible
        Parameters : (int) Value that it can be
        Purpose    : Adds a possibility from what the square is
        Return     : None
    '''
    def addPossible(self, val):
        self.possible.add(val)

### BOARD FUNCTIONS ###

    ### DECIDE NEXT SQUARE
'''
    Name       : successorFunction
    Parameters : (Square[][]) The board state
    Purpose    : Finds the next square to use
    Return     : Returns the coordinates for the next square, an empty list if no square is found
'''
def successorFunction(board):
    row = -1
    col = -1
    for r in range(9):
        for c in range(9):
            # If it is something set, look for something else
            if not board[r][c].isSet():
                # print(board[r][c].isSet())
                return [r, c]
                '''
                if row == -1 or len(board[r][c].possible) < len(board[row][col].possible):
                    row = r
                if col == -1 or len(board[r][c].possible) < len(board[row][col].possible):
                    col = c    
                '''
            
    
    # If nothing is found
    if row == -1 or col == -1:
        return []
    print(board[5][1].isSet())
    print("Successor Found", row, col)
    return [row, col]


    ### CHECK THE BOARD
'''
    Name       : allDiffRow
    Parameters : (int) The row of the table to search; (Square[][]) The board to check
    Purpose    : Returns if the values in the rows are all different
    Return     : (bool) Whether all of the values in the row are unique
'''
def allDiffRow(row, board):
    valSet = set()
    for i in range(9):
        if board[row][i].val in valSet:
            return False
        if board[row][i].val != 0:
            valSet.add(board[row][i].val)
    return True
'''
    Name       : allDiffCol
    Parameters : (int) The column of the table to search; (Square[][]) The board to check
    Purpose    : Returns if the values in the column are all different
    Return     : (bool) Whether all of the values in the column are unique
'''
def allDiffCol(col, board):
    valSet = set()
    for i in range(9):
        if board[i][col].val in valSet:
            return False
        if board[i][col].val != 0:
            valSet.add(board[i][col].val)
    return True
'''
    Name       : allDiffSquare
    Parameters : (int) The row of the value [Not the coordinates of the square]; 
                 (int) The column of the value [Not the coordinates of the square]; 
                 (Square[][]) The board to check
    Purpose    : Returns if the values in the column are all different
    Return     : (bool) Whether all of the values in the square are unique
'''
def allDiffSquare(row, col, board):
    boardRow = (int)(row / 3)
    boardCol = (int)(col / 3)
    valSet = set()
    for r in range(3):
        for c in range(3):
            if board[boardRow + r][boardCol + c].val in valSet:
                return False 
            if board[boardRow + r][boardCol + c].val != 0:
                valSet.add(board[boardRow + r][boardCol + c].val)
    return True

'''
    Name       : goalTest
    Parameters : (Square[][]) The board state
    Purpose    : Checks if the board is a fully valid sudoku board
    Return     : (bool) Whether the board is solved or not
'''
def goalTest(board):
    # Check all of the rows and columns
    for i in range(9):
        if not allDiffRow(i, board) or not allDiffCol(i, board):
            return False

    # Check all of the squares
    for r in range(3):
        for c in range(3):
            if not allDiffSquare(r * 3, c * 3, board):
                return False

    # Check for any unfilled spots
    for r in range(9):
        for c in range(9):
            if board[r][c].val == 0:
                return False
    return True
    

    ### SPOT UPDATE
'''
    Name       : updateRow
    Parameters : (int) The value to remove from sets; (int) The row to update; (Square[][]) The board state
    Purpose    : Removes the possibility from the other squares
    Return     : (bool) Whether something becomes empty from doing that 
'''
def updateRow(val, row, board):
    
    for c in range(9):
        if not board[row][c].isSet():
            board[row][c].removePossible(val)
            if not board[row][c].possible:
                return False
    return True
'''
    Name       : updateCol
    Parameters : (int) The value to remove from sets; (int) The column to update; (Square[][]) The board state
    Purpose    : Removes the possibility from the other squares
    Return     : (bool) Whether something becomes empty from doing that 
'''
def updateCol(val, col, board):
    for r in range(9):
        if not board[r][col].isSet():
            board[r][col].removePossible(val)
            if not board[r][col]:
                return False
    return True
'''
    Name       : updateSquare
    Parameters : (int) The value to remove from sets; (int) The row to update; 
                 (int) The column to update; (Square[][]) The board state
    Purpose    : Removes the possibility from the other squares
    Return     : (bool) Whether something becomes empty from doing that 
'''
def updateSquare(val, row, col, board):
    sqR = (int)(row / 3) * 3
    sqC = (int)(col / 3) * 3
    for r in range(3):
        for c in range(3):
            if not board[sqR + r][sqC + c].isSet():
                board[sqR + r][sqC + c].removePossible(val)
                if not board[sqR + r][sqC + c].possible:
                    return False
    return True

'''
    Name       : update
    Parameters : (int) the row to update; (int) The column to update; (Square[][]) The board state
    Purpose    : Removes the possibility from the other squares
    Return     : (bool) Whether something becomes empty from doing that 
    Note       : Requires that the value be set when running it before hand
'''
def update(row, col, board):
    if not board[row][col].isSet():
        return
    return updateRow(board[row][col].val, row, board) and updateCol(board[row][col].val, col, board) and updateSquare(board[row][col].val, row, col, board)
'''
    Name       : undoRow
    Parameters : (int) The value to add to sets; (int) The row to update; (Square[][]) The board state
    Purpose    : Readds values to the row
    Return     : None
'''
def undoRow(val, row, board):
    for c in range(9):
        if not board[row][c].isSet():
            board[row][c].addPossible(val)
'''
    Name       : undoCol
    Parameters : (int) The value to readd from sets; (int) The column to update; (Square[][]) The board state
    Purpose    : Readds values to the column
    Return     : None
'''
def undoCol(val, col, board):
    for r in range(9):
        if not board[r][col].isSet():
            board[r][col].addPossible(val)
'''
    Name       : updateSquare
    Parameters : (int) The value to readd from sets; (int) The row to update; 
                 (int) The column to update; (Square[][]) The board state
    Purpose    : Readds the values to the board
    Return     : None
'''
def undoSquare(val, row, col, board):
    sqR = (int)(row / 3) * 3
    sqC = (int)(col / 3) * 3
    for r in range(3):
        for c in range(3):
            if not board[sqR + r][sqC + c].isSet():
                board[sqR + r][sqC + c].addPossible(val)

'''
    Name       : undo
    Parameters : (int) the row to undo; (int) The column to undo; (Square[][]) The board state
    Purpose    : Undoes an update
    Return     : None
    Note       : Requires that the value be set when running it before hand
'''
def undo(row, col, board):
    if not board[row][col].isSet():
        return
    undoRow(board[row][col].val, row, board)
    undoCol(board[row][col].val, col, board)
    undoSquare(board[row][col].val, row, col, board)
    board[row][col].unsetVal()

    ### BOARD SET UP
'''
    Name       : intialState
    Parameters : None
    Purpose    : Create a board to represent the states from the input data (which is at board.txt)
    Return     : The initial board
'''
def initialState():
    temp = [[]]
    row = 0
    col = 0
    
    # Read from board.txt
    file = open("board.txt", "r")

    # Read line by line, left to right
    for x in file:
        for c in x:
            # Skip over non-valid input
            if c != 'X' and (c < '0' or c > '9'):
                continue 
            
            # Put in the values into the correct slot on the board
            if c == 'X':
                temp[row].append(Square())
            else:
                temp[row].append(Square((int)(c)))
            
            # Go to the next slot
            col += 1
            if col >= 9:
                col = 0
                row += 1
                temp.append([])
    # Update the values of all of the inputs
    for r in range(9):
        for c in range(9):
            if temp[r][c].isSet():
                update(r, c, temp)
    file.close()
    return temp
            
'''
    Name       : printBoard
    Parameters : (Square[][]) The sudoku board to display in the console
    Purpose    : Prints out the sudoku board in a readable format
    Return     : None (prints out the board to the console)
'''
def printBoard(board):
    for r in range(9):
        # Add the top portions of the blocks
        if r % 3 == 0:
            print("+-------+-------+-------+")
        
        for c in range(9):
            if c % 3 == 0:
                # Add the Divider between blocks
                print("|", end=' ')
            
            if board[r][c].val == 0:
                print("X", end=' ')
            else:
                print(board[r][c].val, end=' ')
        
        # Right  edge
        print("|")
    # Bottom line
    print("+-------+-------+-------+")

    ### Solve
counter = 0
def solveRecurse(r, c, board):
    '''
    global counter
    if counter % 100 == 0:
        printBoard(board)
        print("Board", r, c)
    counter += 1'''
    for i in board[r][c].possible:
        board[r][c].setVal(i)
        # If no empty solutions were created when updating:
        if update(r, c, board):
            # Find the next spot to test out
            nextVal = successorFunction(board)
            ## print("Found:", nextVal)
            # If no next spot is found
            if not nextVal:
                # If it is a solution, then just end here
                if goalTest(board):
                    return True
                # Otherwise, take a step back and go backwards
                undo(r, c, board)
                return False
            # Since there is a next spot, try filling that up too
            if solveRecurse(nextVal[0], nextVal[1], board):
                return True
            
        # This path is a dud; undo the work from this and go back
        undo(r, c, board)
        
    # No solution from here was found
    return False

'''
    Name       : solve
    Parameters : (Square[][]) The intial state
    Purpose    : Sets the board to a valid state
    Return     : None
'''
def solve(board): # TODO 
    next = successorFunction(board)
    print(next)
    if not next:
        return
    if not solveRecurse(next[0],next[1], board):
        print("No solution")


### RUNNABLE ###
    # Defines the intial state of the board
state = initialState()
print("Initial State")
printBoard(state)
print()

    # Prints out the solved board
print("Solve")
solve(state)
printBoard(state)

## TEST
'''

for r in range(3):
    for c in range(3):
        print(r, c, state[r][c].possible)
print()
print(state[0][1].possible)
print(state[1][0].possible)
print(state[8][4].possible)
print(state[2][1].possible)
print(state[0][3].possible)
print(state[0][6].possible)
'''
'''
    Name       : 
    Parameters : 
    Purpose    : 
    Return     : 
'''