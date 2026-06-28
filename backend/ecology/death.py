from backend.entities.animal import Animal
from backend.entities.herbivore import Herbivore
from backend.entities.carnivore import Carnivore
from backend.neural.network import Network

MAX_AGE = 180.0

def handle_deaths(world, rtneat):
    animals = [
        entity
        for entity in world.entities.values()
        if isinstance(entity, Animal)
    ]

    for animal in animals:
        if animal.id not in world.entities:
            continue
            
        if animal.energy <= 0 or animal > MAX_AGE:
            world.remove_entity(animal)

            if animal.brain is None:
                child_genome = rtneat.on_agent_death(animal.brain.genome)
            else:
                parent_genome = rtneat.population.select_parent()
                child_genome = rtneat.spawn_offspring(parent_genome)
            
            if isinstance(animal, Herbivore):
                child = Herbivore(position=animal.position, energy=50.0)
            elif isinstance(animal, Carnivore):
                child = Carnivore(position=animal.position, energy=75.0)
            else:
                continue

            child.brain = Network(child_genome)
            world.add_entity(child)
def is_dead(animal: Animal) -> bool:
    return animal.energy <= 0 or animal.age > MAX_AGE