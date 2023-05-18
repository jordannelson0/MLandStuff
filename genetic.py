import random
import statistics
import time
import sys

from pw_AI.finalcode.guessPasswordTests import getFitness


def generateParent(length, geneSet, getFitness):
    genes = []
    while len(genes) < length:
        sampSize = min(length - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampSize))
    genes = ''.join(genes)
    fitness = getFitness(genes)
    return Chromosome(genes, fitness)


def mutate(parent, geneSet, get_fitness):
    index = random.randrange(0, len(parent.Genes))
    chGenes = list(parent.Genes)
    nGene, alternate = random.sample(geneSet, 2)
    chGenes[index] = alternate \
        if nGene == chGenes[index] \
        else nGene
    genes = ''.join(chGenes)
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)


def getBest(getFitness, tgtLen, optFitness, geneSet, display):
    random.seed()
    bParent = generateParent(tgtLen, geneSet, getFitness)
    display(bParent)
    if bParent.Fitness >= optFitness:
        return bParent
    while True:
        child = mutate(bParent, geneSet, getFitness)
        if bParent.Fitness >= child.Fitness:
            continue
        display(child)
        if child.Fitness >= optFitness:
            return child
        bParent = child


class Chromosome:
    Genes = None
    Fitness = None

    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness


class Benchmark:
    @staticmethod
    def run(function):
        timings = []
        stdout = sys.stdout
        for i in range(100):
            sys.stdout = None
            startTime = time.time()
            function()
            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i < 10 or i % 10 == 9:
                print("{0} {1:3.2f} {2:3.2f}".format(
                    1 + i, mean,
                    statistics.stdev(timings, mean)
                    if i > 1 else 0))