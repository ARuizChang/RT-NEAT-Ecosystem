from backend.entities.herbivore import Herbivore
from backend.entities.carnivore import Carnivore
from backend.neural.network import Network
import random

REPRODUCTION_COOLDOWN = 5.0

def process_reproduction(world, rtneat):
    animals = [
        entity
        for entity in world.entities.values()
        if isinstance(entity, (Herbivore, Carnivore))
    ]

    for animal in animals:
        if animal not in world.entities:
            continue
        if not animal.can_reproduce():
            continue
        if animal.brain is None:
            continue

        #PLACEHOLDER
        reproduce_threshold = 0.3
        if animal.energy > 100.0 * reproduce_threshold:
            if random.random < 0.1:
                _attempt_reproduction(animal, world, rtneat)

def _attempt_reproduction(parent, world, rtneat):
    cost = parent.reproduction_cost()
    if parent.energy < cost:
        return
    
    parent.energy -= cost
    parent.reproduction_cooldown = REPRODUCTION_COOLDOWN

    child_genome = rtneat.spawn_offspring(parent.brain.genome if parent.brain else None)

    offset_x = random.uniform(-20, 20)
    offset_y = random.uniform(-20, 20)
    child_position = (
        max(0, min(world.size[0], parent.position[0] + offset_x)),
        max(0, min(world.size[1], parent.position[1] + offset_y))
    )

    if isinstance(parent, Herbivore):
        child = Herbivore(position=child_position, energy=30.0)
    elif isinstance(parent, Carnivore):
        child = Carnivore(position=child_position, energy=50.0)
    else:
        return

    child.brain = Network(child_genome)
    world.add_entity(child)