from backend.simulation.collision import handle_collisions
from backend.ecology.metabolism import apply_metabolism
from backend.ecology.death import handle_deaths
from backend.ecology.reproduction import process_reproduction
from backend.ecology.feeding import grow_plants, herbivore_feed
from backend.sensors.observation_builder import ObservationBuilder
from backend.neural.network import Network
from backend.entities.animal import Animal
from backend.entities.herbivore import Herbivore
from backend.entities.carnivore import Carnivore
import random
from typing import Optional

def simulate_step(world, delta_time: float, observation_builder: ObservationBuilder, rtneat=None, broadcaster=None):
    animals = [
        entity
        for entity in world.entities.values()
        if isinstance(entity, Animal)
    ]
    for animal in animals:
        observations = observation_builder.build(animal, world)
        animal.perceive_and_act(observations, delta_time)
    
    world.step(delta_time)
    handle_collisions(world)

    for animal in animals:
        if animal.id in world.entities:
            apply_metabolism(animal, delta_time)
    
    handle_deaths(world, rtneat)

    process_reproduction(world, rtneat)

    grow_plants(world, delta_time)

    if broadcaster:
        delta = {
            "time": world.time,
            "plant_count": len([
                entity
                for entity in world.entities.values()
                if entity.species == "plant"
            ]),
            "herbivore_count": len([
                entity
                for entity in world.entities.values()
                if entity.species == "herbivore"
            ]),
            "carnivore_count": len([
                entity
                for entity in world.entities.values()
                if entity.species == "carnivore"
            ]),
        }
        broadcaster(delta)

    return {
        "time": world.time,
        "entity_count": len(world.entities)
    }