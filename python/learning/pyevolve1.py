'''
Created on Apr 9, 2011

@author: egg
'''
#TODO: get matplotlib/numpy/etc installed

#from pyevolve.G1DList import G1DList
from pyevolve import G1DList, GSimpleGA

def eval_func(chromosome):
    score = 0
    
    for val in chromosome:
        if not val: score += 1
    return score

genome = G1DList.G1DList(20)
genome.evaluator.set(eval_func)

ga = GSimpleGA.GSimpleGA(genome)
ga.evolve(freq_stats=10)
print ga.bestIndividual()