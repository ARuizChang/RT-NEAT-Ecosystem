from backend.neural.genome import Genome
from typing import List

class Species:
    def __init__(self, representative: Genome, compatibility_threshold: float = 3.0):
        self.representative = representative
        self.members: List[Genome] = [representative]
        self.compatibility_threshold = compatibility_threshold
        self.best_fitness = 0.0
        self.staleness = 0
    
    def is_compatible(self, genome: Genome) -> bool:
        return genome.compatibility_distance(self.representative) < self.compatibility_threshold
    
    def add_member(self, genome: Genome):
        self.members.append(genome)
    
    def reset(self):
        self.members = []
    
    def update_stats(self):
        self.members.sort(key=lambda member: member.fitness, reverse=True)
        if self.members and self.members[0].fitness > self.best_fitness:
            self.best_fitness = self.members[0].fitness
            self.staleness = 0
        else:
            self.staleness += 1
    
    def average_fitness(self) -> float:
        if not self.members:
            return 0.0
        return sum(member.fitness for member in self.members) / len(self.members)