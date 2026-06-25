from ..entities.entity import Entity
from .spatial_grid import SpatialGrid
from typing import List, Dict, Tuple
import time

class World:
    def __init__(self, size: Tuple[int, int] = (1000, 1000), cell_size: float = 50.0):
        self.size = size
        self.entities: Dict[str, Entity] = {}
        self.grid = SpatialGrid(size, cell_size)
        self.time = 0.0
    
    def add_entity(self, entity: Entity):
        self.entities[entity.id] = entity
        self.grid.add_entity(entity)
    
    def remove_entity(self, entity: Entity):
        self.grid.remove_entity(entity)
        self.entities.pop(entity.id, None)
    
    def step(self, delta_time: float):
        for entity in list(self.entities.values()):
            entity.update(delta_time)
            x, y = entity.position
            width, height = self.size
            x = max(0, min(x, width))
            y = max(0, min(y, height))
            entity.position = (x, y)
            self.grid.move_entity(entity)
        self.time += delta_time
    
    def query_nearby_entities(self, position, radius) -> List[Entity]:
        return self.grid.nearby_entities(position, radius, self.entities)
    
    def find_nearest_entity(self, position, radius, species=None) -> Entity:
        candidates = self.query_nearby_entities(position, radius)
        best_entity = None
        best_distance = float('inf')
        for c in candidates:
            if species is None or c.species != species:
                continue
            distance_x = c.position[0] - position[0]
            distance_y = c.position[1] - position[1]
            distance = distance_x ** 2 + distance_y ** 2
            if 0 < distance < best_distance:
                best_distance = distance
                best_entity = c
        return best_entity