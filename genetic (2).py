import random as rnd
import copy
from itertools import product

class Genetic:
    def __init__(self, graph, num_edges, population_size, num_colors):
        """
        Initialize the Genetic Algorithm with the given parameters.
        """
        self.graph = graph
        self.size = population_size
        self.length = len(graph)
        self.edges = num_edges
        self.num_colors = num_colors
        # Initialize population with random chromosomes
        self.population = [[rnd.randint(1, num_colors) for i in range(self.length)] for i in range(population_size)]

    def fitness(self, chrom):
        """
        Compute the fitness value for a given chromosome.
        """
        f = 0.0
        for node, neighbors in enumerate(self.graph):
            for nei in neighbors:
                # Increment fitness if adjacent nodes have different colors
                if self.population[chrom][node] != self.population[chrom][nei]:
                    f += 1
        # Normalize fitness by dividing by twice the number of edges
        f /= (2 * self.edges)
        return f

    def selection(self, k):
        """
        Perform selection based on tournament selection.
        """
        parents = []
        torns = self.size // k
        for i in range(torns):
            # Perform tournament selection for k members
            candids = [rnd.randint(0, self.size - 1) for j in range(k)]
            chosen = None
            max_fitness = -1.0
            for j in candids:
                fit = self.fitness(j)
                if fit > max_fitness:
                    max_fitness = fit
                    chosen = j
            parents.append(chosen)
        return parents

    def new_generation(self, parents):
        """
        Generate a new generation using crossover.
        """
        children = []
        for i in range(self.size):
            # Randomly select parents for crossover
            x = rnd.randint(0, len(parents) - 1)
            y = 0
            while True:
                y = rnd.randint(0, len(parents) - 1)
                if x != y: break
            # Perform crossover to create a new chromosome
            children.append(self.crossover(self.population[parents[x]], self.population[parents[y]]))
        self.population = children
        
    def crossover(self, x, y):
        """
        Perform crossover between two parent chromosomes.
        """
        child = copy.deepcopy(x)
        # Generate a random binary mask for crossover
        mask = [rnd.uniform(0, 1) for i in range(self.length)]
        for i in range(self.length):
            # Apply crossover mask
            if mask[i] > 0.5:
                child[i] = y[i]
        return child

    def mutation(self, mutation_rate):
        """
        Perform mutation on the population.
        """
        mutated_genes = int(self.size * self.length * mutation_rate)
        if mutated_genes <= 0:
            return
        options = product(range(self.size), range(self.length))
        options = rnd.sample(list(options), mutated_genes)
        for i in range(mutated_genes):
            # Mutate selected genes
            self.population[options[i][0]][options[i][1]] = rnd.randint(1, self.num_colors)
        
    def exec(self, num_iters, k, mutation_rate):
        """
        Execute the genetic algorithm for a given number of iterations.
        """
        high_hist = []
        low_hist = []
        middle_hist = []
        for i in range(num_iters):
            # Record statistics for the current iteration
            high, low, middle = self.stats()
            high_hist.append(high)
            low_hist.append(low)
            middle_hist.append(middle)
            # Perform selection, crossover, and mutation
            parents = self.selection(k)
            self.new_generation(parents)
            self.mutation(mutation_rate)
        return high_hist, low_hist, middle_hist

    def stats(self):
        """
        Compute statistics for the current population.
        """
        high, low, ave = -1, -1, 0.0
        for i, chrom in enumerate(self.population):
            fit = self.fitness(i)
            ave += fit
            if fit > high:
                high = fit
            if fit < low or low == -1:
                low = fit 
        return high, low, (ave/self.size)

def get_graph():
    """
    Get graph input from user.
    """
    ver = int(input('Enter number of vertices: '))
    graph = []
    edges = 0
    for i in range(ver):
        temp_list = []
        face = input()
        face = face.split(' ')
        for j in face:
            temp_list.append(int(j))
            edges += 1
        graph.append(temp_list)
    return graph, ver, edges // 2

def main():
    # Parameters
    generations = 50
    mutation_rate = 0.01
    population_size = 100
    k = 5
    colors = 3

    # Get graph input
    graph, N, M = get_graph()
    
    # Initialize and run Genetic Algorithm
    genet = Genetic(graph, M, population_size, colors)
    high_hist, low_hist, middle_hist = genet.exec(generations, k, mutation_rate)

    # Find best solution
    high = -1
    best = None
    for i, chrom in enumerate(genet.population):
        fit = genet.fitness(i)
        if fit > high:
            high = fit
            best = chrom

    print()
    print('Best coloring:')        
    print(best)
    print("Computational time:", time.time()-startTime,"s")

if __name__ == '__main__':
    main()

