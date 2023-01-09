import math, random

# ONE-HOT ENDCODING
# ===================
# Iris-setosa     : 0 
# Iris-versicolor : 1 
# Iris-virginica  : 2 
# ===================

# NODE PARAMS
learning = 0.1

'''
    Name    : Neuron
    Purpose : The class that represents an individual neuron in the ANN
'''
class Neuron: 
    idCounter = 0    # Gives every neuron a unique ID number
    neurons = dict() # Reference to get actual neuron based off of ID number
    
    # Set up
    '''
        Name       : __init__()
        Parameters : (None)
        Purpose    : Creates a new, empty, non-connected neuron for the ANN
        Return     : (None)
        Note       : Adds itself to the neurons dictionary and increments the ID counter
    '''
    def __init__(self):
        # Create the list of weights from the previous layer that connect to the current node
        self.weights = dict()

        # Set the ID of the nodes
        self.id = Neuron.idCounter 
        Neuron.idCounter += 1
        
        # Add to neurons dictionary
        Neuron.neurons[self.id] = self
        
        # Default state of the neurons
        self.actVal = 0
        self.delta = 0
    
    '''
        Name       : addNodeToWeights(id)
        Parameters : (int) the ID of the node to have a weight to the current node
        Purpose    : Create a weighted edge pointing to self from the specified node at the ID
        Return     : (None) 
        Note       : Sets the intial weight to be between -0.1 and 0.1 at random
    '''
    def addNodeToWeights(self, id: int):
        self.weights[id] = random.uniform(-0.1, 0.1)
    
    # To receive an actual value
    '''
        Name       : intialValue(start)
        Parameters : (float) The value to set the activation value 
        Purpose    : Directly sets the activation value instead of pulling from the previous layer
        Return     : (None)
        Note       : Should only be used for input layer and bias node
    '''
    def initialValue(self, start : float):
        self.actVal = start
    
    '''
        Name       : activation()
        Parameters : (None)
        Purpose    : Set the activation of the current node based off of the nodes that contribute to it
        Return     : (float) The activation value that it returns
        Note       : Assumes that the previous node's (aka previous layer) was already properly activated; Uses sigmoid
    '''
    def activation(self):
        # Find contribution
        sum = 0.0
        for key in self.weights:
            sum += self.weights[key] * Neuron.neurons[key].actVal
        
        # Sigmoid value
        value = 1 / (1 + math.e**(-sum)) # Calculate the actual value of the output component
        self.actVal = value
        return value

    # For the back propogation    
    '''
        Name       : clearDeltaWeights()
        Parameters : (None)
        Purpose    : Clears all of the delta weights from the previous iteration out
        Return     : (None)
        Note       : Should be called before calculating loss and back propogation
    '''
    def clearDeltaWeights():
        for key in Neuron.neurons:
            Neuron.neurons[key].delta = 0
    '''
        Name       : expectedValue(value)
        Parameters : (float) Sets the delta [d - o] compared to the answer
        Purpose    : Sets the initial values for calculating loss and back propogation
        Return     : (None)
        Note       : Should be called only for the output layer
    '''
    def expectedValue(self, value : float):
        self.delta = value - self.actVal
    
    '''
        Name       : updateDelta()
        Parameters : (None)
        Purpose    : Updates teh delta of the current node, and propogates its loss to the other nodes
        Return     : (float) The total loss from this node, before multiplying o'(p)
        Note       : Assumes that all of the loss from the next layer are already run (aka the layer above has already run the function) 
    '''
    def updateDelta(self): 
        # print(self.id, self.delta, self.actVal)
        oPrime = self.actVal * (1 - self.actVal)
        loss = self.delta # Before multiplying by the o'(p) factor
        self.delta *= oPrime
        for key in self.weights:
            Neuron.neurons[key].delta += self.weights[key] * self.delta
        return loss
    
    '''
        Name       : updateWeights()
        Parameters : (None)
        Purpose    : Uses the current delta value to change the weights
        Return     : (None)
        Note       : Assumes updateDelta() has already been run
    '''
    def updateWeights(self): 
        global learning 
        for key in self.weights:
            change = learning * Neuron.neurons[key].actVal * self.delta
            self.weights[key] += change
        self.delta = 0
    
    # TESTING
    '''
        Name       : __str__()
        Parameters : (None)
        Purpose    : Prints the string of the data
        Return     : (str) The string representing the Neuron
        Note       : Same as __repr__()
    '''
    def __str__(self):
        return str(self.id) + " Weights: \n" + str(self.weights) + "\n"
    
    '''
        Name       : 
        Parameters : (None)
        Purpose    : Prints the string of the data
        Return     : (str) The string representing the Neuron
        Note       : Same as __str__()
    '''
    def __repr__(self):
        return str(self.id) + " Weights: \n" + str(self.weights) + "\n"
    
        
# ANN PARAMS
ANN = []
hiddenDepth = 1
hiddenWidth = 6
biasNode = Neuron()

# SETUP

'''
    Name       : setUp()
    Parameters : (None)
    Purpose    : Sets up the ANN using the specified hidden layer Depth and Width
    Return     : (None)
    Note       : Sets the ANN and biasNode global variable
'''
def setUp():
    global hiddenDepth, hiddenWidth, ANN, biasNode
    # Input Nodes
    ANN.append([])
    for i in range(4):
        ANN[0].append(Neuron())

    # Hidden Nodes
    for d in range(1, hiddenDepth + 1):
        ANN.append([])
        for w in range(hiddenWidth):
            ANN[d].append(Neuron())
            for node in ANN[d - 1]:
                ANN[d][w].addNodeToWeights(node.id)
            ANN[d][w].addNodeToWeights(biasNode.id)
    
    # Output Nodes
    ANN.append([])
    for i in range(3):
        ANN[-1].append(Neuron())
        for node in ANN[-2]:
            ANN[-1][i].addNodeToWeights(node.id)
        ANN[-1][i].addNodeToWeights(biasNode.id)


# ANN Running
'''
    Name       : evaluateANN(sepalLength, sepalWidth, petalLength, petalWidth)
    Parameters : (float) sepal length; (float) sepal width; (float) petal length; (float) petal width
    Purpose    : Runs the ANN and gets a value based on the input
    Return     : (int) Gives the expected flower [0 = Iris-Setosa, 1 = Iris-versicolor, 2 = Iris-virginica]
    Note       : Sets the activation values as it goes along, and chooses the one with highest probability
'''
def evaluateANN(sepalLength : float, sepalWidth : float, petalLength : float, petalWidth : float):
    global ANN
    # Set the data as input, and activate the bias node
    ANN[0][0].initialValue(sepalLength)
    ANN[0][1].initialValue(sepalWidth )
    ANN[0][2].initialValue(petalLength)
    ANN[0][3].initialValue(petalWidth )
    biasNode.initialValue(1.0)

    # Run the ANN layer by layer
    for layer in range(1, len(ANN)):
        for node in ANN[layer]:
            node.activation()
    
    # Find the value with the highest probability
    bestValue = 0
    bestIndex = -1
    for i in range(len(ANN[-1])):
        if bestValue < ANN[-1][i].actVal:
            bestIndex = i
            bestValue = ANN[-1][i].actVal

    return bestIndex


'''
    Name       : calculateLoss(actualAnswer)
    Parameters : (int) The actual flower that the observation was for [0 = Iris-Setosa, 1 = Iris-versicolor, 2 = Iris-virginica]
    Purpose    : Calculates the loss of each node, and sets their delta values properly
    Return     : The total sum of loss^2
    Note       : Uses clearDeltaWeights and updateDelta
'''
def calculateLoss(actualAnswer : int):
    global ANN
    # Clear out the previous iteration
    Neuron.clearDeltaWeights()

    # Set the output layer's and the bias node's loss
    for i in range(len(ANN[-1])):
        ANN[-1][i].expectedValue(1.0 if i == actualAnswer else 0.0)
    biasNode.expectedValue(1.0)
    biasNode.updateDelta()
    
    # Go from top to bottom layer by layer, keeping track of the square of the loss
    loss = 0
    for r in range(len(ANN) - 1, -1, -1):
        for node in ANN[r]:
            loss += node.updateDelta()**2
    return loss

'''
    Name       : backPropogate()
    Parameters : (None)
    Purpose    : Uses the delta values in the neurons to update the weights
    Return     : (None)
    Note       : Updates the ANN neurons
'''
def backPropogate():
    global ANN

    for r in range(len(ANN) - 1, -1, -1):
        for node in ANN[r]:
            node.updateWeights()

# RUN

'''
    Name       : setUpData(whichSet, line)
    Parameters : (float[][][]) The list to sort and add data to; (str) The line to parse
    Purpose    : Adds the data to the correct set and sort the data properly
    Return     : (None)
    Note       : Sets the input set to be [flower][dataSetNumer][specificData]
'''
def setUpData(whichSet, line : str):
    ls = line.strip().split(",")
    
    data = []
    for x in ls[0:-1]:
        data.append(float(x))

    if   ls[-1] == "Iris-setosa":
        whichSet[0].append(data)
    elif ls[-1] == "Iris-versicolor":
        whichSet[1].append(data)
    elif ls[-1] == "Iris-virginica":
        whichSet[2].append(data)
    else:
        print("DATA READING ERROR")

'''
    Name       : pullRandom(dataset)
    Parameters : (float[][][]) Data set to pull a random value from
    Purpose    : Gives a piece of data as well as the correct answer
    Return     : ((int, float[])) Gives a tuple of the correct answer and the associated data
    Note       : Used to be used for testing, but that was removed
'''
def pullRandom(dataset):
    which = random.randrange(0, 3)
    actualData = dataset[which][random.randrange(0, len(dataset[which]))]

    return (which, actualData)

'''
    Name       : isFloat(value)
    Parameters : (str) the value to be checked if it is a float
    Purpose    : Double checks if the string is a float, for parsing purposes
    Return     : (bool) whether the value is a string
    Note       : Got from online at https://www.programiz.com/python-programming/examples/check-string-number 
'''
def isFloat(value : str):
    try:
        float(value)
        return True
    except:
        return False

'''
    Name       : recieveAndPrint()
    Parameters : (None)
    Purpose    : Gets the data and puts it runs the ANN, and prints the output
    Return     : (None)
    Note       : Put inside an infinte loop in the future
'''
def recieveAndPrint():
    global ANN
    # Get good input
    a = "a"
    b = "b"
    c = "c"
    d = "d"
    while not isFloat(a):
        a = input("Sepal Length: ")
    while not isFloat(b):
        b = input("Sepal Width : ")
    while not isFloat(c):
        c = input("Petal Length: ")
    while not isFloat(d):
        d = input("Petal Width : ")
    
    # Prints the data
    print("============================================")
    value = evaluateANN(float(a), float(b), float(c), float(d))

    if   value == 0:
        print("It is Iris-setosa with confidence: %", round(ANN[-1][0].actVal * 100, 4))
    elif value == 1:
        print("It is Iris-versicolor with confidence: %", round(ANN[-1][1].actVal * 100, 4))
    elif value == 2:
        print("It is Iris-virginica  with confidence: %", round(ANN[-1][2].actVal * 100, 4))
    print()
    print("Probabilities")
    print("Iris-setosa     :", ANN[-1][0].actVal)
    print("Iris-versicolor :", ANN[-1][1].actVal)
    print("Iris-virginica  :", ANN[-1][2].actVal)
    print("============================================")




trainingFile   = open("training.txt"  , "r")
validationFile = open("validation.txt", "r")
testFile       = open("test.txt"      , "r")

# EACH SET IS THE TYPE IT IS, AND EACH LIST INSIDE IS THE DATA
# Sepal Length = 0, Sepal Width = 1, Petal Length = 2, Petal Width = 3
trainingData   = [[], [], []]
validationData = [[], [], []]
testData       = [[], [], []]

# Process each file
for x in trainingFile:
    setUpData(trainingData, x)
for x in validationFile:
    setUpData(validationData, x)
for x in testFile:
    setUpData(testData, x)

trainingFile.close()
validationFile.close()
testFile.close()

# Training data variables
threshold = 0.001
maxLoops  = 10000

# Sets the ANN up
setUp()

# run for the maximum amount of time
print("Training...")
for i in range(maxLoops):
    # Train using a random pull
    pull = pullRandom(trainingData)
    answer = pull[0]
    data = pull[1]
    # Run th ANN
    evaluateANN(data[0], data[1], data[2], data[3])
    calculateLoss(answer)
    backPropogate()
    
    # Validation (every 10 cycles)
    if i % 10 == 9: # Looks for total accuracy across all of the different classes
        totalSum = 0
        for i in range(3): # For each class...
            for test in range(10): # Try 10 random samles...
                tempData = validationData[i][random.randrange(0, len(validationData[i]))]
                gotten = evaluateANN(tempData[0], tempData[1], tempData[2], tempData[3])
                totalSum += calculateLoss(i)

        # If the loss from that is negligible, then break the loop
        # Take the average of sum of loss values
        if totalSum / 30 < threshold:
            break
print("Done!")

# Print out the found neural network
print("Network:\n============================================")
for r in range(len(ANN)):
    print("LAYER",r)
    for c in ANN[r]:
        print(c, end=" ")
    print("----")
print("============================================")

# Testing (UNCOMMENT TO DO SOME TESTING/USE TESTING FILE)
'''
print("Testing...")
test  = 0
total = 0
for i in range(3):
    for x in testData[i]:
        testGot = evaluateANN(x[0], x[1], x[2], x[3])
        if testGot != i: # If not correct, print out the data
            print(x, i)
            print("Iris-setosa     :", ANN[-1][0].actVal)
            print("Iris-versicolor :", ANN[-1][1].actVal)
            print("Iris-virginica  :", ANN[-1][2].actVal)
            test += 1
        total += 1
print("\nAmount of errors:",test,"/", total)

    # TESTING A RANDOM PULL
for i in range(3):
    answer = i
    data = testData[i][random.randrange(0, len(testData[i]))]
    gotten = evaluateANN(data[0], data[1], data[2], data[3])
    print(gotten, answer)
    print("Iris-setosa     :", ANN[-1][0].actVal)
    print("Iris-versicolor :", ANN[-1][1].actVal)
    print("Iris-virginica  :", ANN[-1][2].actVal)
'''

# Run program to accept data input
while True:
    print("Give Flower Data: ")
    recieveAndPrint()