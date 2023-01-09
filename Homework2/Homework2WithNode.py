from heapdict import heapdict


# Swap two elements i, j of the array
def swap(arr, i, j):
    temp   = arr[i]
    arr[i] = arr[j]
    arr[j] = temp

# Performs the pancake flip on the array, giving out the (Action to take)
# Takes in the initial spot to flip (inclusive)
def flip(arr, i):
    j = len(arr) - 1
    while i < j:
        swap(arr, i, j)
        i += 1
        j -= 1


# The class which stores the nodes of the frontier 
class Node:
    def __init__(self, tup : tuple, costVal: int, parent = None, flipPos : int = 0):
        self.arr : tuple = tup    # The state
        self.cost : int = costVal # The cost to arrive
        self.flip = flipPos       # The flip to get here
        self.parent = parent      # The parent (default to none)
    
    # Functions for making the nodes recognize the same state (based off of the tuple input)
    def __eq__(self, other):
        return self.arr == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.arr)


# Cost Function
def costFunc(flipIndex): # Just returns 1 right now, but made so that we can edit later
    return 1

# Do the pancake heuristic by checking against whether the next pancake is adjacent (The gap heuristic)
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

# Goes back up the Frontier Tree and gives the path to get to that node from the root
def returnList(curr : Node):
    result = []
    while curr.parent != None: #Only the root has the parent set as null
        result.append(curr.flip)
        curr = curr.parent
    result.reverse() # Since we went from the leaf up, it needs to be reversed
    return result

# Creates the node using the given information for the state, parent node, and flip
# Also requires priority so it can be reused for Uniform Cost
# And needs some memory to keep track of whether it is seen, as well as reference to the priority queue
def insertNode(tup : tuple, parent : Node, flipPos : int, priority : int, frontier : heapdict, seen : dict):
    # Default to 0 cost (when inserting the root), otherwise find the parent's cost
    totalCost = 0
    if parent != None:
        totalCost = parent.cost + costFunc(flipPos)

    # Note that the root starts with 1 cost, which is not a big deal since everything else
    # will have +1 cost
    node = Node(tup, totalCost, parent, flipPos)
    
    # If we have explored it, and it was already better (don't explore)
    if tup in seen and seen[tup] <= priority: 
        return
    
    # If it is new, just add it
    seen[tup] = priority
    frontier[node] = priority
    
############## AStar ###############

# The AStar algorithm that finds the way to stack the pancakes
def AStar(input : list):
    # The heap holding which node to expand to 
    frontier = heapdict()
    # Dictionary to keep track of states we have seen
    seen = {}

    numStatesChecked = 0
    # Inserts the first node
    insertNode(tuple(input), None, -1, 0, frontier, seen)

    # Keep going until no more frontier
    while len(frontier) > 0:
        numStatesChecked += 1 # Just for extra information...
        # The value at the front of the frontier
        
        top = frontier.popitem()[0]
        
        # Check if it is the goal
        if goalCheck(top.arr):
            print("Number of states explored:", numStatesChecked)
            return returnList(top)
        
        # Adds the nodes (if feasible)
        for i in range(0,9):
            # Creates the new state to explore
            temp = list(top.arr)
            flip(temp, i)
            # vvv Where the calculation of feasibility of adding is calculated
            insertNode(tuple(temp), top, i, top.cost + costFunc(i) + heuristic(temp), frontier, seen) 

    # Should only every return when there is no list
    print("Somehow, no solution :(")
    return None

############## Uniform ###############

# The AStar algorithm that finds the way to stack the pancakes
def UniformCostSearch(input : list):
    # The heap holding which node to expand to 
    frontier = heapdict()
    # Dictionary to keep track of states we have seen
    seen = {}

    numStatesChecked = 0
    # Inserts the first node 
    insertNode(tuple(input), None, -1, 0, frontier, seen)

    # Keep going until no more frontier
    while len(frontier) > 0:
        numStatesChecked += 1 # Just for extra information...
        # The value at the front of the frontier
        top = frontier.popitem()[0]
        
        
        # Check if it is the goal
        if goalCheck(top.arr):
            print("Number of states explored:", numStatesChecked)
            return returnList(top)
        
        # Adds the nodes (if feasible)
        for i in range(0,9):
            # Creates the new state to explore
            temp = list(top.arr)
            flip(temp, i)
            # vvv Where the calculation of feasibility of adding is calculated
            insertNode(tuple(temp), top, i, top.cost + costFunc(i), frontier, seen) 

    # Should only every return when there is no list
    print("Somehow, no solution :(")
    return None

############## RUNNABLE ###############

# Get 10 valid inputs
inputList = []
inputSet = set({})
for i in range(0,10):

    inVal = input("Pancake size in range [1, 10] (I assume they are unique): ")
    valid = False
    while not valid:
        try:
            val = int(inVal) # Check if is a number 
            if val < 1 or val > 10: # Check if it is in range [1, 10]
                inVal = input("[Error] Pancake size not in range [1,10]: ")
                continue
            if val in inputSet: # Check if it is a duplicate
                inVal = input("[Error] Value is not unique in range [1, 10]: ")
                continue
            
            valid = True
        except:
            inVal = input("[Error] Value is not a number [1, 10]: ")
        
    # Add it to the list of numbers
    inputSet.add(int(inVal))
    inputList.append(int(inVal))

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
