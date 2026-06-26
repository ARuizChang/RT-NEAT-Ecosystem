from backend.neural.genome import Genome
from backend.neural.population import Population
from backend.neural.innovation import InnovationTracker
import random

class RTNEAT:
    def __init__(self, population_size: int, num_inputs: int, num_outputs: int):
        self.innovation_tracker = InnovationTracker()
        self.population = Population()
        self.population_size = population_size
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
    
    def initialize(self):
        for _ in range(self.population_size):
            genome = Genome.create_minimal_genome(self.num_inputs, self.num_outputs, self.innovation_tracker)
            self.population.add_genome(genome)
    
    def on_agent_death(self, genome: Genome):
        self.population.remove_genome(genome)
        parent = self.population.select_parent()
        child = self.spawn_offspring(parent)
        self.population.add_genome(child)
        return child
    
    def spawn_offspring(self, parent: Genome) -> Genome:
        child = Genome(self.innovation_tracker)
        child._copy_from(parent)
        child.mutate_weights()
        if random.random() < 0.05:
            child.add_connection()
        if random.random() < 0.03:
            child.add_node()
        return child
    
    def reproduce(self, parent1: Genome, parent2: Genome) -> Genome:
        child = parent1.crossover(parent2)
        child.mutate_weights()
        if random.random() < 0.05:
            child.add_connection()
        if random.random() < 0.03:
            child.add_node()
        return child