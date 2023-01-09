Name    : Matthew Wong
Class   : Intro to AI
Date    : 12 December 2022

Program: Artificial Neural Network
    The goal of the program was to produce an Artificial Neural Network that could destinguish between
    Iris-Setosa, Iris-Versicolor, and Iris-Virginica based on the Sepal Length, Sepal Width, Petal Length, and Petal Width

Running:
    Run the program using the command "python3 ANN.py"
    Note that the "training.txt", "validation.txt", and "test.txt" have to be in the same folder as the "ANN.py"
    The program will run in an infinite loop, until Ctrl + C is used to force end the program

Assumptions:
    The program assumes the training data to be accurate, as well as the inputs to be reasonable numbers. In addition,
    the inputs are assumed to be floats, measured in cm. 
    The Neural Network assumes that the classification is simple enough to be captured in one layer of hidden nodes
        with 12 nodes in the layer. 
    In addition, it assumes that 10000 is enough reading of the data in order to capture the classification. 
    It also assumes that the data corresponds to one of the above plants.
    The data was also assumed to be evenly distributed, as the data was split using the 60-20-20 in order 
        to train, validate, and test, and that this is enough data to train the algorithm.
    The ANN model trains itself evertime it is run, so it will be slightly different every time to program is run.

Specifications:
    Most of the time, the model is around 90-95% accurate on what the plant is; however,
    there are some cases where it can not tell between Iris-Versicolor and Iris-Viriginica.
    In particular, the case [6.2, 2.2, 4.5, 1.5] is particularly difficult in most generations of the ANN. 
    When given the specifications of a plant, the program will print out the plant it thinks it is
    as well as the confidence in that guess. In addition, it will list the confidences for all 3 plants. 
    Finally, it will show the weights of the ANN at the beginning of the program run.
    
    Iris-Setosa     is represented with the index 0 node in the output layer
    Iris-Versicolor is represented with the index 1 node in the output layer
    Iris-Viriginica is represented with the index 2 node in the output layer
    

Data Setup:
    In order to train the model, I split it into 3 sets of data:
    - Training (90 data points, 30 each)
    - Validation (30 data points, 10 each)
    - Testing (30 data points, 10 each)
    The training data is not used in the implementation, but was used during testing 
    and building to make sure that the ANN is working as intended. 

