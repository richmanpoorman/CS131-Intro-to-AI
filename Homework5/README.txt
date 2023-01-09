Name: Matthew Wong
Date: 28 November 2022

Program: Naive Baysian Classification
    The program uses a Markov Model to predict whether something is a bird or a plane
    given the speed of the object over a period of time

    It gives what the model thinks based off of speed only as well as based off of speed and variance

Run: 
    run "python3 MarkovModel.py" in the console in the same folder of data.txt and probabilities.txt (rename pdf.txt to probabilities.txt)

Assumptions:
    The data.txt and probabilities.txt files are in the same folder as the MarkovMode.py file. In addition,
    the data.txt files and probabilities.txt files are the correct data collection.
    The data.txt files and probabilities.txt files are in the correct format;
        - In the data.txt, each of the lines represents a different set of data scanned
        - In the data.txt, each of the spots is a float that is a speed or "NaN" in that exact format
        - In the data.txt, there are 10 sets of data to check
        - In the data.txt, the data is in increments in 1 for each data point (aka each point is a measurement at 1s increments)
        - In the data.txt, the datat is a list of discrete data points by the above scale 

        - In the probabilities.txt, the probability of being a bird based on speed is the first lines
        - In the probabilities.txt, the probability of being a plane based on speed is the second line
        - In the probabillites.txt, the data is in 0.5 increments of speed (aka each data point is on a scale of 0.5)
        - In the probabilities.txt, the data is a list of discrete data points by the above scale 

    I assume that the higher variance is a bird and a lower variance is plane; I based it off of the given data
    This means that the model uses variance as a factor to try to make a guess
        This is because birds are much easier to slow down and speed up (ie they are hunting or are floating) whereas
        a plane is in constant motion, and rarley changes speed drastically
    I also assume that variance and speed is indepenedent (which it isn't, but it makes the math easier)
    I assume we start at 0.5 of being either a bird or plane before the first data point
    I also assume that if both have a probability of 0, then no information is added (aka it just keeps what it was)

    The graph shows the development of the probabilities over time, rounded to the nearest tenth, prioritizing the bird.
    The graph also checks every 2 points, so the exact last data point won't be displayed.
    The graph is also rounding by a scale of 0.1 for probabilities.
    
Improvement:
    An improvement to the data is to increase the accuracy is to consider the variance. Looking at the data, the variance
    is a greater indicator then just pure speed tell of the bird or plane, as birds had much larger fluctuations 
    then planes. This is probably because birds are changing what they are doing in the air, speeding up or slowing
    down (such as hunting), but planes have a much harder time changing their speed. Thus, we can account for the 
    variance ALONG side the speed in order to increase the accuracy of the Markov Model with the given data. 
    The variance is calculated by the sum across the data points of the difference from the mean squared.
    For the PDF of the Variance, I used the data to create it by taking windows of the data and finding the variance
    of those bits (relative to the mean of the TOTAL data)