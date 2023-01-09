Matthew Wong
Homework 3: Genetic Algorithm

Purpose:
    The purpose is to create a local search algorithm that can try to find a good value for the packing problem

Run: 
    run "python3 main.py" in the folder that you are in to run the program. 

Genetic Algorithm:
    1. Structure of the chromosome
        The chromosome is the amount of each packages, which is an array where each index of the array corresponds to the packages:
        [Weight : Value]
        {
            (20 : 6),
            (30 : 5),
            (60 : 8),
            (90 : 7),
            (50 : 6),
            (70 : 9),
            (30 : 4),
            (30 : 5),
            (70 : 4),
            (20 : 9),
            (20 : 2),
            (60 : 1)
        }
        Since there are 12 possible packages, we can have 12 variables

    2. Selection of an initial population
        I am selecting an intial population of 100 children (so it culls 5 at each step and duplicates), 
            each starting with 

    3. A fitness function is used to simulate the natural selection process
        If the weight is over 250, it returns 250 - weight (aka a negative number with magnitude equal to the distance from the weight);
            otherwise, it returns the total value

    4. The selection process must be established
        Culling 50%: First, sort the children by value. 
            Then, replace the bottom half with duplicates of the top half of the population. 

    5. The genetic operators must be selected
        Single point mutation will occur with 10% chance, flipping the True/False value of a random variable
        Single-point Crossover will happen, with the population that was not culled

    6. A solution test is required if different from the fitness function
        If the worst performing solution is within 1 value point of the best performing one, and neither is zero
        then a solution has been found. It also ends after 300 iterations.

    7. Evolutionary measures can visually indicate the system evolution
        The difference between the worst performing one and the best performing one 