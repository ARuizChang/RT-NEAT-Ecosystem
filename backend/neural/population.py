from backend.neural.genome import Genome
from backend.neural.species import Species
from typing import List
import random

class Population:
    def __init__(self, compatibility_threshold: float = 3.0):
        self.genomes: List[Genome] = []
        self.species: List[Species] = []
        self.compatibility_threshold = compatibility_threshold
    
    def add_genome(self, genome: Genome):
        self.genomes.append(genome)
        self._assign_to_species(genome)

    def remove_genome(self, genome: Genome):
        self.genomes.remove(genome)
        for species in self.species:
            if genome in species.members:
                species.members.remove(genome)
    
    def _assign_to_species(self, genome: Genome):
        for species in self.species:
            if species.is_compatible(genome):
                species.add_member(genome)
                return
        self.species.append(Species(representative=genome, compatibility_threshold=self.compatibility_threshold))
    
    def speciate(self):
        for species in self.species:
            species.reset()
        for genome in self.genomes:
            self._assign_to_species(genome)
        self.species = [species for species in self.species if species.members]
    
    def select_parent(self) -> Genome:
        weighted = []
        for species in self.species:
            species.update_stats()
            for genome in species.members:
                weighted.append((genome, genome.fitness))
        total_fitness = sum(fitness for _, fitness in weighted)
        if total_fitness == 0:
            return random.choice(self.genomes)
        r = random.random() * total_fitness
        cumulative = 0.0
        for genome, weight in weighted:
            cumulative += weight
            if cumulative >= r:
                return genome
        return self.genomes[-1]