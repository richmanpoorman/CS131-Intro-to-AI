from heapdict import heapdict

# Swap two elements i, j of the array
def swap(arr, i, j):
    temp   = arr[i]
    arr[i] = arr[j]
    arr[j] = temp

# The heap holding which node to expand to 
nodeExpansion = heapdict()

# Performs the pancake flip on the array, giving out the (Action to take)
# Takes in the initial spot to flip (inclusive)
def flip(arr, i):
    j = len(arr) - 1
    while i < j:
        swap(arr, i, j)
        i += 1
        j -= 1

# Checks if the state is [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
def goalCheck(arr):
    # Double check the size is 10 (should always stay at 10 elements)
    if len(arr) != 10:
        print("MASSIVE ERROR")
        return False
    
    # Check if all of the elements are 1-indexed
    i = 0
    while i < 10:
        if arr[i] != 10 - i:
            return False
        i += 1
    return True

# Do the pancake heuristic by checking against whether the next pancake is adjacent
def heuristic(arr):
    i = 0
    size = len(arr)
    val = 0
    # Count if the next pancake differs by 1 (no need to check the last element, since there is nothing under)
    while i < size - 1:
        if abs(arr[i] - arr[i + 1]) != 1:
            val += 1
        i += 1
    return val 

# Returns the cost function (which is the amount of elements NOT flipped)
# It is a function for modularity; it makes it easier to change in the future for 
# better cost functions
def costFunction(index):
    return 1

# Stores the current cost of each node by storing it as a (tuple, int) pair
currentCost = {}
# Paths, stored as a (tuple, list) pair
paths = {}
# The Heuristic + Cost of already seen (no need to re explore)
pastValue = {}

# Makes sure things are clear before using any of the elements
def clearBoard():
    nodeExpansion.clear()
    currentCost.clear()
    pastValue.clear()
    paths.clear()
    
# The input (Testing for now)
searchArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Updates the index of the keys given the corresponding pancake ordering (listKey), new cost to get there (newCost), and 
# the new path to get to that node (newPath)
def updateBoard(listKey, newCost, newPath):
    key = tuple(listKey)
    newVal = newCost + heuristic(listKey)
    # If it is not a better path, just don't even look at it
    if key in pastValue and pastValue[key] <= newVal:
        return False

    # Update the frontier, cost function, and path
    pastValue[key]     = newVal  # Store the new, better way of getting there
    nodeExpansion[key] = newVal  # Put it into heap/decrease key
    currentCost[key]   = newCost # Store the current cost to get to the node
    paths[key]         = newPath # Store the better path to the node
    return True

# Tuple representing the final goal state
goal = (10, 9, 8, 7, 6, 5, 4, 3, 2, 1)

###################### AStar #################################


# Given the input array, it outputs the path we need to take
def AStar(arr):
    testCount = 0

    clearBoard()
    updateBoard(arr, 0, [])
    # Keeps going while there is frontier to explore
    while len(nodeExpansion) != 0:
        # Get the min element
        key = nodeExpansion.popitem()[0]
        curr = list(key) # So we can copy/edit to get to the next step

        # Return the path if the best path has been found
        if goalCheck(key):
            print(testCount, "States Explored")
            return paths[goal]

        testCount += 1
        # Add all of the possible steps
        i = 0
        while i < 9:
            
            # Make a copy, then perform the operation to see what is the result of that operation
            temp = curr[:]
            tempPath = paths[key][:]
            flip(temp, i)
            tempPath.append(i)

            # Choose whether or not to add/decrease it
            updateBoard(temp, currentCost[key] + costFunction(i), tempPath)    
            i += 1
    
    # Return a failure if there is a failure
    return "FAILURE :("


################# Uniform Cost Search ######################

# Same as updateBoard above, just without adding the heuristic
def updateBoard2(listKey, newCost, newPath):
    key = tuple(listKey)
    newVal = newCost
    # If it is not a better path, just don't even look at it
    if key in pastValue and pastValue[key] <= newVal:
        return False

    # Update the frontier, cost function, and path
    pastValue[key]     = newVal  # Store the new, better way of getting there
    nodeExpansion[key] = newVal  # Put it into heap/decrease key
    currentCost[key]   = newCost # Store the current cost to get to the node
    paths[key]         = newPath # Store the better path to the node
    return True

def UniformCostSearch(arr):
    testCount = 0

    clearBoard()
    updateBoard(arr, 0, [])
    # Keeps going while there is frontier to explore
    while len(nodeExpansion) != 0:
        # Get the min element
        key = nodeExpansion.popitem()[0]
        curr = list(key) # So we can copy/edit to get to the next step

        # Return the path if the best path has been found
        if goalCheck(key):
            print(testCount, "States Explored")
            return paths[goal]

        testCount += 1
        # Add all of the possible steps
        i = 0
        while i < 9:
            
            # Make a copy, then perform the operation to see what is the result of that operation
            temp = curr[:]
            tempPath = paths[key][:]
            flip(temp, i)
            tempPath.append(i)

            # Choose whether or not to add/decrease it
            
            updateBoard2(temp, currentCost[key] + costFunction(i), tempPath)    
            i += 1
    
    # Return a failure if there is a failure
    return "FAILURE :("

############## RUNNABLE ###############

inputList = []

inputSet = set({})
for i in range(0,10):

    val = int(input("Pancake size in range [1, 10] (I assume they are unique): "))
    valid = False
    while val in inputSet or val < 1 or val > 10:
        if val < 1 or val > 10:
            val = int(input("[Error] Pancake size not in range [1,10]: "))
            continue
        if val in inputSet:
            val = int(input("[Error] Value is not unique in range [1, 10]: "))
            continue
    
    inputSet.add(val)
    inputList.append(val)

# Helper to print out the stack of pancakes from the given array
def printPancake(arr):
    i = len(arr) - 1
    while i >= 0:
        pancake = "["
        for j in range (0, arr[i]):
            pancake += "="
        pancake += "]"
        num = str(arr[i])
        if (num != "10"):
            num += " "
        print(num, pancake) 
        i -= 1

# Gets the initial input array
print("Input: ", inputList)

# Prints the searching process of AStar
print("AStar: ")
AStarList = AStar(inputList)
print("Flip-at-index order", AStarList)
print()

# Displays the steps of AStar
AStarTemp = inputList[:]
for i in AStarList:
    printPancake(AStarTemp)
    print("Flip at: ", i)
    print()
    flip(AStarTemp, i)
printPancake(AStarTemp)


# Prints the searching process of Uniform Cost
print("Uniform Cost Search: (You can quit with Ctrl+C if it takes too long)")
UniformList = UniformCostSearch(inputList)
print("Flip-at-index order", UniformList)

# Displays the steps of Uniform cost
UniformTemp = inputList[:]
for i in UniformList:
    printPancake(UniformTemp)
    print("Flip at: ", i)
    print()
    flip(UniformTemp, i)
printPancake(UniformTemp)
    