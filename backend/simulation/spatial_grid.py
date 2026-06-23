from collections import defaultdict
from typing import List, Tuple, Dict, Set
import math

class SpatialGrid:
    def __init__(self, world_size: Tuple[float, float], cell_size: float = 50.0):
        self.world_width, self.world_height = world_size
        self.cell_size = cell_size
        self.columns = max(1, math.ceil(self.world_width / self.cell_size))
        self.rows = max(1, math.ceil(self.world_height / self.cell_size))
        self.cells: Dict[Tuple[int, int], Set[str]] = defaultdict(set)
        self.entity_index: Dict[str, Tuple[int, int]] = {}

    def _cell_coords(self, position):
        x, y = position
        column = int(x / self.cell_size)
        row = int(y / self.cell_size)
        column = max(0, min(column, self.columns - 1))
        row = max(0, min(row, self.rows - 1))
        return (column, row)
    
    def add_entity(self, entity):
        cell_coords = self._cell_coords(entity.position)
        self.cells[cell_coords].add(entity.id)
        self.entity_index[entity.id] = cell_coords

    def remove_entity(self, entity):
        cell_coords = self.entity_index.pop(entity.id, None)
        if cell_coords:
            self.cells[cell_coords].discard(entity.id)
    
    def move_entity(self, entity):
        old_cell_coords = self.entity_index.get(entity.id)
        new_cell_coords = self._cell_coords(entity.position)
        if old_cell_coords is None:
            raise ValueError(f"Entity {entity.id} not found in spatial grid.")
        if old_cell_coords != new_cell_coords:
            self.cells[old_cell_coords].discard(entity.id)
            self.cells[new_cell_coords].add(entity.id)
            self.entity_index[entity.id] = new_cell_coords
    
    def query_radius(self, position, radius) -> List[Tuple[int, int]]:
        column, row = self._cell_coords(position)
        cell_radius = int(math.ceil(radius / self.cell_size))
        results = []
        for dx in range(-cell_radius, cell_radius + 1):
            for dy in range(-cell_radius, cell_radius + 1):
                neighbor_column = column + dx
                neighbor_row = row + dy
                if 0 <= neighbor_column < self.columns and 0 <= neighbor_row < self.rows:
                    results.append((neighbor_column, neighbor_row))
        return results
    
    def nearby_entities(self, position, radius, entity_map) -> List:
        coords = self.query_radius(position, radius)
        found_entities = []
        for cell in coords:
            for entity_id in self.cells.get(cell, ()):
                entity = entity_map.get(entity_id)
                if entity:
                    distance_x = entity.position[0] - position[0]
                    distance_y = entity.position[1] - position[1]
                    if distance_x ** 2 + distance_y ** 2 <= radius ** 2: #used squared distance to avoid sqrt for performance
                        found_entities.append(entity)
        return found_entities
                