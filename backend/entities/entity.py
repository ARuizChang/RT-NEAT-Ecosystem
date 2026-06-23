from dataclasses import dataclass, field
from typing import Tuple, Dict, Any
import uuid
import math

Vector2 = Tuple[float, float]

@dataclass
class Entity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    position: Vector2 = (0.0, 0.0)
    velocity: Vector2 = (0.0, 0.0)
    direction: float = 0.0 #Direction in radians
    energy: float = 0.0
    age: float = 0.0
    species: str = "entity"
    radius: float = 1.0 #Collision radius

    def update(self, delta_time: float):
        position_x, position_y = self.position
        velocity_x, velocity_y = self.velocity
        self.position = (position_x + velocity_x * delta_time, position_y + velocity_y * delta_time)
        self.age += delta_time

    def serialize(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "position": self.position,
            "velocity": self.velocity,
            "direction": self.direction,
            "energy": self.energy,
            "age": self.age,
            "species": self.species,
            "radius": self.radius
        }
    
    def distance_to(self, other: 'Entity') -> float:
        distance_x = self.position[0] - other.position[0]
        distance_y = self.position[1] - other.position[1]
        return math.hypot(distance_x, distance_y)
    
    def take_damage(self, amount: float):
        self.energy -= amount

    def is_dead(self) -> bool:
        return self.energy <= 0