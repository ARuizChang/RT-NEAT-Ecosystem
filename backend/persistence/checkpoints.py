from backend.entities.animal import Animal
from backend.entities.plant import Plant
from backend.entities.herbivore import Herbivore
from backend.entities.carnivore import Carnivore
from backend.neural.genome import Genome
from backend.neural.node_gene import NodeGene
from backend.neural.connection_gene import ConnectionGene
from pathlib import Path
from typing import Any, Dict, List
import json

def entity_to_dict(entity) -> Dict[str, Any]:
    return {
        "id": entity.id,
        "type": entity.__class__.__name__,
        "position": list(entity.position),
        "velocity": list(entity.velocity),
        "direction": entity.direction,
        "energy": entity.energy,
        "age": entity.age,
        "species": entity.species,
        "radius": entity.radius,
    }

def entity_from_dict(data: Dict[str, Any]):
    entity_type = data.get("type", "Plant")

    if entity_type == "Plant":
        entity = Plant(
            position=tuple(data.get("position", (0.0, 0.0))),
            energy=data.get("energy", 20.0),
        )
    elif entity_type == "Herbivore":
        entity = Herbivore(
            position=tuple(data.get("position", (0.0, 0.0))),
            energy=data.get("energy", 100.0),
        )
    elif entity_type == "Carnivore":
        entity = Carnivore(
            position=tuple(data.get("position", (0.0, 0.0))),
            energy=data.get("energy", 100.0),
        )
    else:
        entity = Plant(
            position=tuple(data.get("position", (0.0, 0.0))),
            energy=data.get("energy", 20.0),
        )

    entity.id = data.get("id", entity.id)
    entity.position = tuple(data.get("position", entity.position))
    entity.velocity = tuple(data.get("velocity", entity.velocity))
    entity.direction = data.get("direction", entity.direction)
    entity.energy = data.get("energy", entity.energy)
    entity.age = data.get("age", entity.age)
    entity.species = data.get("species", entity.species)
    entity.radius = data.get("radius", entity.radius)

    return entity

def genome_to_dict(genome: Genome) -> Dict[str, Any]:
    return {
        "nodes": [
            {
                "id": node.id,
                "node_type": node.node_type,
                "activation_function": node.activation_function,
                "bias": node.bias,
            }
            for node in genome.nodes.values()
        ],
        "connections": [
            {
                "innovation_number": connection.innovation_number,
                "in_node": connection.in_node,
                "out_node": connection.out_node,
                "weight": connection.weight,
                "enabled": connection.enabled,
                "recurrent": connection.recurrent,
            }
            for connection in genome.connections.values()
        ],
        "input_ids": genome.input_ids,
        "output_ids": genome.output_ids,
        "bias_id": genome.bias_id,
        "fitness": getattr(genome, "fitness", 0.0),
    }

def genome_from_dict(data: Dict[str, Any], innovation_tracker) -> Genome:
    genome = Genome(innovation_tracker)

    genome.input_ids = data.get("input_ids", [])
    genome.output_ids = data.get("output_ids", [])
    genome.bias_id = data.get("bias_id")
    genome.fitness = data.get("fitness", 0.0)

    for node_data in data.get("nodes", []):
        genome.nodes[node_data["id"]] = NodeGene(
            id=node_data["id"],
            node_type=node_data.get("node_type", "input"),
            activation_function=node_data.get("activation_function", "tanh"),
            bias=node_data.get("bias", 0.0),
        )

    for conn_data in data.get("connections", []):
        genome.connections[conn_data["innovation_number"]] = ConnectionGene(
            innovation_number=conn_data["innovation_number"],
            in_node=conn_data["in_node"],
            out_node=conn_data["out_node"],
            weight=conn_data.get("weight", 0.0),
            enabled=conn_data.get("enabled", True),
            recurrent=conn_data.get("recurrent", False),
        )

    return genome

def save_checkpoint(world, rtneat, path: str) -> None:
    state = {
        "world": {
            "size": list(world.size),
            "time": world.time,
            "entities": [entity_to_dict(entity) for entity in world.entities.values()],
        },
        "population": {
            "genomes": [genome_to_dict(genome) for genome in rtneat.population.genomes],
            "species": [
                {
                    "representative": genome_to_dict(species.representative),
                    "members": [genome_to_dict(member) for member in species.members],
                }
                for species in rtneat.population.species
            ],
        },
    }

    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    with open(path_obj, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def load_checkpoint(world_cls, path: str, rtneat):
    with open(path, "r", encoding="utf-8") as f:
        state = json.load(f)

    world = world_cls(size=tuple(state["world"].get("size", (1000, 1000))))
    world.time = state["world"].get("time", 0.0)

    for raw_entity in state["world"].get("entities", []):
        entity = entity_from_dict(raw_entity)
        world.add_entity(entity)

    # Restore genomes and population
    rtneat.population.genomes = []
    rtneat.population.species = []

    for genome_data in state["population"].get("genomes", []):
        genome = genome_from_dict(genome_data, rtneat.innovation_tracker)
        rtneat.population.add_genome(genome)

    return world