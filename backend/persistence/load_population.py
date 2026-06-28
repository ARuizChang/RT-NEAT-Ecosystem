from backend.neural.genome import Genome
from backend.neural.node_gene import NodeGene
from backend.neural.connection_gene import ConnectionGene
from pathlib import Path
from typing import Dict, Any
import json

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


def load_population(rtneat, path: str):
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Population file not found: {path}")

    with open(path_obj, "r", encoding="utf-8") as f:
        payload = json.load(f)

    rtneat.population.genomes = []
    rtneat.population.species = []

    for genome_data in payload.get("genomes", []):
        genome = genome_from_dict(genome_data, rtneat.innovation_tracker)
        rtneat.population.add_genome(genome)

    return rtneat.population