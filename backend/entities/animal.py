from backend.entities.entity import Entity
import math
from typing import Optional

class Animal(Entity):
    def __init__(self, position=(0.0, 0.0), energy=100.0, metabolism_rate=0.1, max_speed=100.0, turn_rate=2.0):
        super().__init__(position=position, energy=energy)
        self.species = "animal"
        self.metabolism_rate = metabolism_rate
        self.max_speed = max_speed
        self.turn_rate = turn_rate
        self.brain = None
        self.reproduction_cooldown = 0.0

    def perceive_and_act(self, observations: list, delta_time: float):
        if self.brain is None:
            return
        outputs = self.brain.forward(observations)
        #outputs: [turn_left, turn_right, forward, attack, reproduce]
        turn = (outputs[0] - outputs[1]) * self.turn_rate * delta_time
        self.direction += turn
        forward_power = outputs[2]
        velocity_x = math.cos(self.direction) * forward_power * self.max_speed
        velocity_y = math.sin(self.direction) * forward_power * self.max_speed
        self.velocity = (velocity_x, velocity_y)
        #attack and reproduce are handled by world/ecology

    def update(self, delta_time: float):
        self.energy -= self.metabolism_rate * delta_time
        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown = max(0.0, self.reproduction_cooldown - delta_time)
        super().update(delta_time)

    def can_reproduce(self) -> bool:
        return self.energy > 0.0 and self.reproduction_cooldown == 0.0 and self.age > 1.0

    def reproduction_cost(self) -> float:
        return max(10.0, self.energy * 0.2)