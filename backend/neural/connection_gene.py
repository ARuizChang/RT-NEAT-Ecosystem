from dataclasses import dataclass

@dataclass
class ConnectionGene:
    innovation_number: int
    in_node: int
    out_node: int
    weight: float
    enabled: bool = True
    recurrent: bool = False