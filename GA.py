"""
Created on Sat Feb  24 20:18:05 2019

@author: Raneem
"""
import numpy
import random
import time
import sys

from solution import solution

def sortPopulation(population, scores):
    
    sortedIndices = scores.argsort()
    population = population[sortedIndices]
    scores = scores[sortedIndices]
    
    return population, scores

def crossoverPopulaton(population, scores, PopSize, crossoverProbability, Keep):
    #initialize a new population
    newPopulation = numpy.empty_like(population)
    newPopulation[0:Keep] = population[0:Keep]
    #Create pairs of parents. The number of pairs equals the number of chromosomes divided by 2
    for i  in range(Keep, PopSize, 2):
        #pair of parents selection        
        parent1, parent2 = pairSelection(population, scores, PopSize)
        crossoverLength = min(len(parent1), len(parent2))
        parentsCrossoverProbability = random.uniform(0.0, 1.0)
        if parentsCrossoverProbability < crossoverProbability:
            offspring1, offspring2 = crossover(crossoverLength, parent1, parent2)
        else:
            offspring1 = parent1.copy()
            offspring2 = parent2.copy()
    
        #Add offsprings to population
        newPopulation[i] = numpy.copy(offspring1)
        newPopulation[i + 1] = numpy.copy(offspring2)
     
    return newPopulation
        
    
def mutatePopulaton(population, PopSize, mutationProbability, Keep, lb, ub):
    for i  in range(Keep, PopSize):
        #Mutation   
        offspringMutationProbability = random.uniform(0.0, 1.0)
        if offspringMutationProbability < mutationProbability:
            mutation(population[i], len(population[i]), lb, ub)
        

def elitism(population, scores, bestIndividual, bestScore):
    """    
    This method performs the elitism operator
    
    Parameters
    ----------    
    population : list
        The list of chromosomes
    scores : list
        The list of fitness values for each chromosome
    bestIndividual : list
        A chromosome of the previous generation having the best fitness value          
    bestScore : float
        The best fitness value of the previous generation        
    
    Returns
    -------
    list
        population : The updated population after applying the elitism
    list
        scores : The updated list of fitness values for each chromosome after applying the elitism
    """
    
    # get the worst chromosome
    worstFitnessId = selectWorstChromosome(scores)
    
    #replace worst cromosome with best one from previous generation if its fitness is less than the other
    if scores[worstFitnessId] > bestScore:
       population[worstFitnessId] = numpy.copy(bestIndividual)
       scores[worstFitnessId] = numpy.copy(bestScore)
       
    
def selectWorstChromosome(scores):
    """    
    It is used to get the worst chromosome in a population based n the fitness value
    
    Parameters
    ---------- 
    scores : list
        The list of fitness values for each chromosome
        
    Returns
    -------
    int
        maxFitnessId: The chromosome id of the worst fitness value
    """
    
    maxFitnessId = numpy.where(scores == numpy.max(scores))
    maxFitnessId = maxFitnessId[0][0]
    return maxFitnessId

def selectBestChromosome(scores):
    """    
    It is used to get the best chromosome in a population based n the fitness value
    
    Parameters
    ---------- 
    scores : list
        The list of fitness values for each chromosome
        
    Returns
    -------
    int
        maxFitnessId: The chromosome id of the best fitness value
    """
    minFitnessId = numpy.where(scores == numpy.min(scores))
    minFitnessId = minFitnessId[0][0]
    return minFitnessId

def pairSelection(population, scores, PopSize):    
    """    
    This is used to select one pair of parents using roulette Wheel Selection mechanism
    
    Parameters
    ---------- 
    population : list
        The list of chromosomes
    scores : list
        The list of fitness values for each chromosome
    PopSize: int
        Number of chrmosome in a population
          
    Returns
    -------
    list
        parent1: The first parent chromosome of the pair
    list
        parent2: The second parent chromosome of the pair
    """
    parent1Id = rouletteWheelSelectionId(scores, PopSize)
    parent2Id = numpy.copy(parent1Id)
    
    parent1 = population[parent1Id].copy()
    while parent1Id == parent2Id:  
        parent2Id = rouletteWheelSelectionId(scores, PopSize)
    
    parent2 = population[parent2Id].copy()
   
    return parent1, parent2
    
def rouletteWheelSelectionId(scores, PopSize): 
    """    
    A roulette Wheel Selection mechanism for selecting a chromosome
    
    Parameters
    ---------- 
    scores : list
        The list of fitness values for each chromosome
    sumScores : float
        The summation of all the fitness values for all chromosomes in a generation
    PopSize: int
        Number of chrmosome in a population
          
    Returns
    -------
    id
        chromosomeId: The id of the chromosome selected
    """
    
    ##reverse score because minimum value should have more chance of selection
    reverse = max(scores) + min(scores)
    reverseScores = reverse - scores.copy()
    sumScores = sum(reverseScores)
    pick    = random.uniform(0, sumScores)
    current = 0
    for chromosomeId in range(PopSize):
        current += reverseScores[chromosomeId]
        if current > pick:
            return chromosomeId

def crossover(chromosomeLength, parent1, parent2):
    """    
    The crossover operator
    
    Parameters
    ---------- 
    chromosomeLength: int
        The maximum index of the crossover
    parent1 : list
        The first parent chromosome of the pair
    parent2 : list
        The second parent chromosome of the pair
          
    Returns
    -------
    list
        offspring1: The first updated parent chromosome of the pair
    list
        offspring2: The second updated parent chromosome of the pair
    """
    
    # The point at which crossover takes place between two parents. 
    crossover_point = random.randint(0, chromosomeLength - 1)

    # The new offspring will have its first half of its genes taken from the first parent and second half of its genes taken from the second parent.
    offspring1 = numpy.concatenate([parent1[0:crossover_point],parent2[crossover_point:]])
    # The new offspring will have its first half of its genes taken from the second parent and second half of its genes taken from the first parent.
    offspring2 = numpy.concatenate([parent2[0:crossover_point],parent1[crossover_point:]])
      
    return offspring1, offspring2


def mutation(offspring, chromosomeLength, lb, ub):
    """    
    The mutation operator
    
    Parameters
    ---------- 
    offspring : list
        A generated chromosome after the crossover
    chromosomeLength: int
        The maximum index of the crossover
    lb: int
        lower bound limit
    ub: int
        Upper bound limit
         
    Returns
    -------
    list
        offspring: The updated offspring chromosome
    """
    mutationIndex = random.randint(0, chromosomeLength - 1)
    mutationValue = random.uniform(lb, ub)
    offspring[mutationIndex] = mutationValue


def clearDups(Population, lb, ub):
    newPopulation = numpy.unique(Population, axis=0)
    oldLen = len(Population)
    newLen = len(newPopulation)
    if newLen < oldLen:
        nDuplicates = oldLen - newLen
        newPopulation = numpy.append(newPopulation, numpy.random.uniform(0,1,(nDuplicates,len(Population[0]))) *(ub-lb)+lb, axis=0)
        
    return newPopulation

def calculateCost(objf, ga, PopSize, lb, ub):  
    scores = numpy.full(PopSize, numpy.inf)
    
    #Loop through chromosomes in population
    for i in range(0,PopSize):
        # Return back the search agents that go beyond the boundaries of the search space
        ga[i,:]=numpy.clip(ga[i,:], lb, ub)

        # Calculate objective function for each search agent
        scores[i] = objf(ga[i,:]) 
        
    return scores
        

def GA(objf,lb,ub,dim,PopSize,iters):
        
    """    
    This is the main method which implements GA
    
    Parameters
    ----------    
    objf : function
        The objective function selected
    lb: int
        lower bound limit
    ub: int
        Upper bound limit
    PopSize: int
        Number of chrmosomes in a population
    iters: int
        Number of iterations / generations of GA
    
    Returns
    -------
    N/A
    """
    
    cp = 1 #crossover Probability
    mp = 0.01 #Mutation Probability
    keep = 2; # elitism parameter: how many of the best individuals to keep from one generation to the next
    
    s=solution()
        
    bestIndividual=numpy.zeros(dim)    
    scores=numpy.random.uniform(0.0, 1.0, PopSize) 
    bestScore=float("inf")
    
    ga=numpy.random.uniform(0,1,(PopSize,dim)) *(ub-lb)+lb
    convergence_curve=numpy.zeros(iters)
    
    print("GA is optimizing  \""+objf.__name__+"\"")  
    
    timerStart=time.time() 
    s.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    
    for l in range(iters):

        #crossover
        ga = crossoverPopulaton(ga, scores, PopSize, cp, keep)
           
        #mutation
        mutatePopulaton(ga, PopSize, mp, keep, lb, ub)
           
        ga = clearDups(ga, lb, ub)
        
        scores = calculateCost(objf, ga, PopSize, lb, ub)
            
        bestScore = min(scores)
        
        #Sort from best to worst
        ga, scores = sortPopulation(ga, scores)
         
        convergence_curve[l]=bestScore     
        
        if (l%1==0):
            print(['At iteration '+ str(l+1)+ ' the best fitness is '+ str(bestScore)]);
        
    timerEnd=time.time()  
    s.bestIndividual = bestIndividual
    s.endTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime=timerEnd-timerStart
    s.convergence=convergence_curve
    s.optimizer="GA"
    s.objfname=objf.__name__

    return s
