from backend.entities.plant import Plant
from backend.entities.herbivore import Herbivore
from backend.entities.carnivore import Carnivore
import math

def handle_collisions(world):
    entities_to_remove = []

    for entity_id, entity in list(world.entities.items()):
        if entity_id not in world.entities:
            continue
            
        nearby = world.query_nearby_entities(entity.position, entity.radius + 20.0)

        for neighbor in nearby:
            if neighbor.id == entity.id or neighbor.id not in world.entities:
                continue

            distance = entity.distance_to(neighbor)

            if (isinstance(entity, Herbivore) and isinstance(neighbor, Plant)) or (isinstance(entity, Plant) and isinstance(neighbor, Herbivore)):
                if not isinstance(entity, Herbivore):
                    entity, neighbor = neighbor, entity
                if distance <= entity.radius + neighbor.radius:
                    energy_gained = neighbor.harvest(10.0)
                    entity.energy += energy_gained
                    if neighbor.energy <= 0:
                        entities_to_remove.append(neighbor)
            
            elif (isinstance(entity, Carnivore) and isinstance(neighbor, Herbivore)) or (isinstance(entity, Herbivore) and isinstance(neighbor, Carnivore)):
                if not isinstance(entity, Carnivore):
                    entity, neighbor = neighbor, entity
                if distance <= entity.radius + neighbor.radius:
                    damage = entity.attack_power
                    neighbor.take_damage(damage)
                    if neighbor.is_dead():
                        entity.energy += 30.0
                        entities_to_remove.append(neighbor)
    
    for entity in set(entities_to_remove):
        if entity.id in world.entities:
            world.remove_entity(entity)