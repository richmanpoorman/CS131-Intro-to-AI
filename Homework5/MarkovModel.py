
# Bird, Plane
# The previous states
history = []  # The history of confidence of each data set [event][dataPoint][state] (SPEED ONLY)
history2 = [] # The history of confidence of each data set [event][dataPoint][state] (SPEED AND VARIANCE)
pastData = [] # The temporary data to keep track of the Markov Model previous states [dataPoint]

data = []          # Each of the 10 data sets
probabilities = [] # The core data graph (pdf.txt) [NOTE:: RENAME pdf.txt TO probabilities.txt]
mean = []          # The mean of each data set

'''
    Name       : setUpProbAndData
    Parameters : None
    Purpose    : Copies data from the probabilities.txt and data.txt to the correct arrays in the correct format
    Return     : None
    Note       : pdf.txt should be called probabilites.txt
'''
def setUpProbAndData():
    global data, probabilities, mean
    probFile = open("probabilities.txt", "r")
    for x in probFile:
        temp1 = x.split(',')
        temp2 = dict()
        for i in range(len(temp1)):
            if i == "NaN":
                continue
            temp2[i / 2] = float(temp1[i])
        probabilities.append(temp2)
    probFile.close()

    dataFile = open("data.txt", "r")
    for x in dataFile:
        temp1 = x.split(',')
        temp2 = []
        sum = 0
        for i in temp1:
            
            if float(i) == float(i): # Checks if the values are not NaN
                temp2.append(float(i))
                sum += float(i)
            else:
                temp2.append(None)
        mean.append(sum / len(temp2))
        data.append(temp2)
    dataFile.close()

'''
    Name       : getEventGivenState
    Parameters : (int) The current state to get conditional of; (float) The data point 
    Purpose    : Returns the probability that the data point happens given the state 
    Return     : (float) The probability of the event givcn the state
    Note       : Only uses speed; does NOT consider variance; depends on probabilities
'''
def getEventGivenState(state : int, value: float): 
    global probabilities
    key = round(value * 2) / 2
    if key in probabilities[state]:
        return probabilities[state][key]
    return 0

'''
    Name       : getPrevious
    Parameters : (int) The state to check
    Purpose    : Gets the previous state data that was calculated 
    Return     : (float) The probability for being the state in the iteration
    Note       : If there is no data (aka it is the first data point), use 0.5 as probability; depends on pastData
'''
def getPrevious(state : int):
    global pastData 
    if not pastData:
        return 0.5
    return pastData[-1][state]

'''
    Name       : transitionProb 
    Parameters : (int) The state to go to; (int) The state to come from
    Purpose    : Returns the probability of going from the start to the end probability
    Return     : (float) The probability of going to the end state from the start state
    Note       : It is just 0.9 when they match, and 0.1 when they are different
'''
def transitionProb(endState: int, startState: int):
    if endState == startState: 
        return 0.9
    return 0.1 

'''
    Name       : normalize
    Parameters : (float[]) The vector to add before the normalization
    Purpose    : Turns the vector proportional to the probability into the probabilities
    Return     : (None)
    Note       : Adds it to the pastData array; depends on pastData
'''
def normalize(beforeNormalize):
    global pastData
    sum = 0
    for i in beforeNormalize:
        sum += i 
    
    if sum == 0: # If there is no new information...
        if pastData: # Stick with the previous state
            pastData.append(pastData[-1])
        else: # If there was no previous state, then they are equal
            pastData.append([0.5, 0.5])
        return 
    
    for i in range(2):
        beforeNormalize[i] /= sum 
    pastData.append(beforeNormalize)

'''
    Name       : clear
    Parameters : (None)
    Purpose    : Clears out the pastData at the start of the Markov Model
    Return     : (None)
    Note       : Depends on pastData
'''
def clear():
    global pastData
    pastData.clear()

'''
    Name       : markovModel
    Parameters : (int) Which set of data points to look at
    Purpose    : Tries to guess the actual state based off of the data based ONLY on speed
    Return     : (int) The state that the Markov Model thinks it is
    Note       : Depends on data, history, pastData; stored data on history
'''
def markovModel(eventNum : int):
    clear()
    global data, history, pastData
    # Look at each of the data points
    for o in data[eventNum]:
        
        if o == None: # Skip empty-data points
            continue

        event = []
        # For each of the states
        for state in range(2):
            value = 0
            # The sum
            for stateSum in range(2):
                value += transitionProb(state, stateSum) * getPrevious(stateSum)
            # Times the emission
            value *= getEventGivenState(state, o)
            event.append(value)
        normalize(event)

    history.append(pastData[:])
    # Store the history of the markov
    # Get most likely from the most recent
    maxVal = 0
    maxIdx = -1
    for state in range(2):
        val = getPrevious(state)
        if maxVal < val:
            maxVal = val 
            maxIdx = state 
    return maxIdx


### MARKOV WITH VARIANCE ###
varianceData = [dict(), dict()]

'''
    Name       : setUpVariance
    Parameters : (None)
    Purpose    : Uses the answer key to make a new Probability Density Function based on variance
    Return     : None
    Note       : Puts the data into varianceData, with window size equal to 5
'''
def setUpVariance():
    global varianceData
    windowSize = 5
    # Add the data for the bird
    numBirds = 0
    for event in [0, 2, 3, 4, 9]:

        meanVal = mean[event]
        # Try all of the windows
        for start in range(len(data[event]) - windowSize):
            if data[event][start] == None: # Don't use the data starting with NaN
                continue
            
            # Use the variance, assuming that it is the same as the previous spot 
            # If the data is NaN 
            varianceMeasure = 0
            prev = data[event][start]
            # Find the variance of the given window
            for i in range(windowSize):
                if data[event][start + i] == None:
                    varianceMeasure += (prev - meanVal) * (prev - meanVal)
                else: 
                    varianceMeasure += (data[event][start + i] - meanVal) * (data[event][start + i] - meanVal)
                    prev = data[event][start + i]
            
            varianceMeasure /= windowSize # Division for variance

            # Actually keep track of the variances
            key = round(varianceMeasure)
            if key in varianceData[0]:
                varianceData[0][key] += 1
            else:
                varianceData[0][key] = 1
            numBirds += 1
    
    # Normalize based on how many data points were added
    for x in varianceData[0].keys():
        varianceData[0][x] = varianceData[0][x] / numBirds
    
    # Add data for the plane 
    numPlane = 0
    for event in [1, 5, 6, 7, 8]:

        meanVal = mean[event]

        # Try all of the windows
        for start in range(len(data[event]) - windowSize):
            if data[event][start] == None: # Skip over ones starting with no information
                continue
            
            # Use variance, assuming that the 
            # NaN is the same as the previous data point
            varianceMeasure = 0
            prev = data[event][start]
            for i in range(windowSize):
                if data[event][start + i] == None:
                    varianceMeasure += (prev - meanVal) * (prev - meanVal)
                else: 
                    varianceMeasure += (data[event][start + i] - meanVal) * (data[event][start + i] - meanVal)
                    prev = data[event][start + i]
            
            varianceMeasure /= windowSize # Division of variance size (across window)

            # Store variance data
            key = round(varianceMeasure)
            if key in varianceData[1]:
                varianceData[1][key] += 1
            else:
                varianceData[1][key] = 1
            numPlane += 1
    
    # Normalize the data
    for x in varianceData[1].keys():
        varianceData[1][x] = varianceData[1][x] / numPlane

'''
    Name       : getEventGivenVariance
    Parameters : (int) The state to check based off of; (float) The accumulated variance up to this point; (float) The data point
    Purpose    : Returns the probability that the data point happens given the state, using Variance as well
    Return     : (float) The probability of the event givcn the state
    Note       : Uses speed AND variance to calculate; assumes variance and data point are independent to multiply probabilities; 0.9 bird if high variance, 0.9 plane if low variance
'''
def getEventGivenVariance(state : int, variance: float, value : float): 
    global varianceData
    key = round(variance)
    var = 0
    if key in varianceData[state]:
        var = varianceData[state][key]
    return var * getEventGivenState(state, value)

'''
    Name       : markovVariance
    Parameters : (int) The set of data point to look at
    Purpose    : Tries to guess the actual state based off of the data based on speed AND varaince
    Return     : (int) The state that the Markov Model thinks it is
    Note       : Depends on data, history2, pastData; stored data on history2
'''
def markovVariance(eventNum : int):
    clear()
    global data, history2, pastData, mean

    varianceSum = 0  # Stores the variance 
    dataIdx = 0
    for o in data[eventNum]:
        
        if o == None: # Skip over empty data points
            continue
        event = []
        # For each of the states
        varianceSum += (o - mean[eventNum]) * (o - mean[eventNum])
        for state in range(2):
            value = 0
            # The sum
            for stateSum in range(2):
                value += transitionProb(state, stateSum) * getPrevious(stateSum)
            # Times the emission
            value *= getEventGivenVariance(state, varianceSum / (dataIdx + 1), o) # Change to include variance again
            event.append(value)
        normalize(event)

        dataIdx += 1

    history2.append(pastData[:])
    # Store the history of the markov
    # Get most likely from the most recent
    maxVal = 0
    maxIdx = -1
    for state in range(2):
        val = getPrevious(state)
        if maxVal < val:
            maxVal = val 
            maxIdx = state 
    return maxIdx

'''
    Name       : displayConfidenceHistory
    Parameters : (float[][]) The history of the specific event during the developoment of the markov model of what it thinks it is
    Purpose    : Prints the graph of the development of the markov model over time
    Return     : (None)
    Note       : Prints the graph, assuming it is the history of the markov model
'''
def displayConfidenceHistory(currentHistory):
    # Shared variables
    jump   = 2
    yScale = 0.1
    
    numRows = int(1 / yScale) + 1 
    size    = round(len(currentHistory) / jump)

    printStrs = []
    for i in range(numRows):
        printStrs.append([])
        for j in range(size):
            printStrs[i].append('-')
    
    for i in range(size):
        birdIdx  = round(currentHistory[i * jump][0] / yScale)
        planeIdx = round(currentHistory[i * jump][1] / yScale)
        
        printStrs[planeIdx][i] = 'O'
        printStrs[birdIdx][i]  = 'X'
        

    for i in range(numRows):
        print(round(1 - i * yScale, 2), "[" + "".join(printStrs[len(printStrs) - i - 1]) + "]")

### RUNNABLE ###
setUpProbAndData()

# Prints the data in readable for speed ONLY
print("---------------------------------------------------")
print("Speed Only")
print("---------------------------------------------------")
for i in range(10):
    answer = markovModel(i)
    # Which data set (header)
    print("Data Set", i + 1, (" " if i < 9 else "") + ":", "Bird " if answer == 0 else "Plane", ":: Confidence: %s%%" % (round(history[i][-1][answer] * 100, 2)))
    
    # Key
    print("SCALE:: Bird: X, Plane: O")
    
    # Graph over time
    displayConfidenceHistory(history[i])
    print()
print()

# Prints the data in readable for speed AND variance
print("---------------------------------------------------")
print("Including Variance")
print("---------------------------------------------------")

setUpVariance()
for i in range(10):
    answer = markovVariance(i)
    # Which data set (header)
    print("Data Set", i + 1, (" " if i < 9 else "") + ":", "Bird " if answer == 0 else "Plane", ":: Confidence: %s%%" % (round(history2[i][-1][answer] * 100, 2)))
    
    # Key
    print("SCALE:: Bird: X, Plane: O")
    
    # Graph over time
    displayConfidenceHistory(history2[i])
    print()