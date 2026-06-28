from backend.neural.genome import Genome
from pathlib import Path
from typing import Any, Dict
import json

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


def save_population(rtneat, path: str) -> None:
    payload = {
        "genomes": [genome_to_dict(genome) for genome in rtneat.population.genomes]
    }

    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    with open(path_obj, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)