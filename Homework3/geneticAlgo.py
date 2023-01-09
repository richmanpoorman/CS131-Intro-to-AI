from random import randint

# The packages are stored in the form (weight, value)
packages = [
    (20, 6),
    (30, 5),
    (60, 8),
    (90, 7),
    (50, 6),
    (70, 9),
    (30, 4),
    (30, 5),
    (70, 4),
    (20, 9),
    (20, 2),
    (60, 1)
]

class Individual:
    # CONSTRUCTORS
    '''
    Name       : __init__()
    Parameters : (Individual [optiona]) The one to make a copy of [if none, does default construction]
    Purpose    : The default constructor and copy constructor
    Return     : (none)
    '''
    def __init__(self):
        self.phenotype = []
        # Create the list
        for i in range(0, 12):
            self.phenotype.append(randint(0, 1) == 0)
        # Get weight is calculated in getValue, as the value depends on the
        # weight being under or equal to 250
        self.update()
    
    '''
    Name       : copyConstructor(original)
    Parameters : (Individial) The Individual to make a copy of
    Purpose    : Creates a copy of the Individual
    Return     : (none)
    '''
    def copy(self, original):
        self.phenotype = []
        for i in range(0, 12):
            self.phenotype.append(original.phenotype[i])
        # Copy over the cost and value
        self.update()
    
    # METHODS
    '''
    Name       : update()
    Parameters : (none)
    Purpose    : Set the value with the current values, as well as updatesthe weight [THE FITNESS FUNCTION]
    Return     : The new value
    '''
    def update(self):
        self.value = 0
        self.weight = 0
        for i in range(0, 12):
            if self.phenotype[i]:
                self.weight += packages[i][0]
        
        # If it is overweight, favor the ones with closer weight (it is a negative number)
        if self.weight > 250:
            self.value = 250 - self.weight
            return self.value
        
        # If the weight is proper, go through and find the actual value
        for i in range(0, 12):
            if self.phenotype[i]:
                self.value  += packages[i][1]
        return self.value

    
    '''
    Name       : mutate()
    Parameters : (none)
    Purpose    : Goes through the phenotype, and mutates each of the elements by adding -1, 0 or 1 (minimum 0)
    Return     : (none)
    '''
    def mutate(self):
        idx = randint(0, 11)
        self.phenotype[idx] = not self.phenotype[idx]
        
        # Updates the weight and value
        self.update()
    
    '''
    Name       : crossover(other)
    Parameters : (Individual) The individual to crossover with
    Purpose    : Performs a single point crossover at a random point with the other individual
    Return     : (none)
    '''
    def crossover(self, other):
        crossoverPoint = randint(0, 12)
        # Note that if 12 is pulled, then no crossover is done
        for i in range(crossoverPoint, 12):
            temp = self.phenotype[i]
            self.phenotype[i] = other.phenotype[i]
            other.phenotype[i] = temp
        
        # Updates the weight and value
        self.update()
        other.update()

    ''' SORTING HELPERS '''
    # Note that the operators are flipped as the 
    # Bigger cost should come first, and therefore smaller

        # Less than
    def __lt__(self, obj):
        return self.value > obj.value
        # Greater than
    def __gt__(self, obj):
        return self.value < obj.value
        # Less than or equal
    def __le__(self, obj):
        return self.value >= obj.value
        # Greater than or equal
    def __ge__(self, obj):
        return self.value <= obj.value
        # equal
    def __eq__(self, obj):
        return self.value == obj.value
    
    # Testing to-string function
    def __repr__(self):
        return str((self.weight, self.value))


#################### POPULATION ANALYSIS ####################

# Creates a population of populationSize
population = []
populationSize = 10
for i in range(0, populationSize):
    population.append(Individual())

'''
Name       : solutionTest()
Parameters : (none)
Purpose    : Sorts the array and tests the range of the values
Return     : The value differentiation between the top and the bottom
'''
def solutionTest():
    population.sort()
    # Get the value of the first and last
    if population[0].value <= 0 or population[populationSize - 1].value <= 0:
        return float('inf')
    return population[0].value - population[populationSize - 1].value
'''
Name       : cull()
Parameters : (none)
Purpose    : Culls the bottom 50 percent of the list
Return     : (none)
Note       : Assumes that the solution test was done
'''
def cull():
    # Replaces the values in the bottom half with those in the top half
    temp = (int)(populationSize/2)
    for i in range(0, temp):
        population[i + temp].copy(population[i])

'''
Name       : fringeOperators()
Parameters : (none)
Purpose    : Does the mutations and the crossover of the elements of the list
Return     : None
Note       : Assumes that culling was done
'''
def fringeOperators():
    # 50% chance for a mutation to occur
    for i in range(0, populationSize):
        if randint(0, 1) == 0:
            population[i].mutate()
    
    # 50% chance for any crossover to happen for any member with any member
    for i in range(0, populationSize):
        if randint(0, 1) == 0:
            population[i].crossover(population[populationSize - 1])
        

#################### RUNNING ####################
'''print(population)
print()
print(sorted(population))
print()
print(solutionTest())
print(population)
print()
cull()
print(population)
'''
testCounter = 0
while solutionTest() > 1:
    cull()
    fringeOperators()

print()
print(population)
print(population[0].value)
