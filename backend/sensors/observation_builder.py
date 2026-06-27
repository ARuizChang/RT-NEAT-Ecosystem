from backend.sensors.vision import Vision
from typing import List
import math

class ObservationBuilder:
    def __init__(self, ray_count: int = 8, max_range = 200.0):
        self.ray_count = ray_count
        self.max_range = max_range
        self.vision = Vision(ray_count=ray_count, max_range=max_range)
    
    def build(self, animal, world) -> List[float]:
        observations = []

        rays = self.vision.sense(animal, world)
        for ray in rays:
            observations.append(ray["distance"])
            observations.append(1.0 if ray["plant"] else 0.0)
            observations.append(1.0 if ray["herbivore"] else 0.0)
            observations.append(1.0 if ray["carnivore"] else 0.0)
        
        observations.append(animal.energy)
        observations.append(math.cos(animal.direction))
        observations.append(math.sin(animal.direction))

        return observations