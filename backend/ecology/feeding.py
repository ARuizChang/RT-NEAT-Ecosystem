from backend.entities.plant import Plant
from backend.entities.herbivore import Herbivore
import random

PLANT_SPAWN_RATE = 0.5
PLANT_INITIAL_ENERGY = 30.0
PLANT_MAX_ENERGY = 100.0
PLANT_REGEN_RATE = 0.05

def hervibore_feed(herbivore, plant):
    amount = min(10.0, plant.energy)
    herbivore.energy += amount
    plant.energy -= amount
    return amount

def grow_plants(world, delta_time):
    spawn_count = int(PLANT_SPAWN_RATE * delta_time)
    for _ in range(spawn_count):
        x = random.uniform(0, world.size[0])
        y = random.uniform(0, world.size[1])
        plant = Plant(
            position=(x, y),
            energy=PLANT_INITIAL_ENERGY,
            regeneration_rate=PLANT_REGEN_RATE,
            max_energy=PLANT_MAX_ENERGY
        )
        world.add_entity(plant)