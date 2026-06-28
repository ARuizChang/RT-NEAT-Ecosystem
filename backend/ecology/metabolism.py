from backend.entities.animal import Animal
import math
METABOLISM_BASE = 0.1
MOVEMENT_COST_MULTIPLIER = 0.05

def apply_metabolism(animal: Animal, delta_time: float):
    base_cost = animal.metabolism_rate * delta_time
    
    speed = math.hypot(animal.velocity[0], animal.velocity[1])
    movement_cost = speed * MOVEMENT_COST_MULTIPLIER * delta_time
    
    total_cost = base_cost + movement_cost
    animal.energy = max(0.0, animal.energy - total_cost)