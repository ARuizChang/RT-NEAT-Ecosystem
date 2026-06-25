from .node_gene import NodeGene
from .connection_gene import ConnectionGene
from .innovation import InnovationTracker
from typing import List, Dict, Optional
import random

class Genome:
    def __init__(self, innovation: InnovationTracker):
        self.innovation = innovation
        self.nodes: Dict[int, NodeGene] = {}
        self.connections: Dict[int, ConnectionGene] = {}
        self.input_ids: List[int] = []
        self.output_ids: List[int] = []
        self.bias_id: Optional[int] = None
    
    @classmethod
    def create_minimal_genome(cls, num_inputs: int, num_outputs: int, innovation: InnovationTracker):
        genome = cls(innovation)
        for i in range(num_inputs):
            node_id = innovation.get_node_id()
            genome.nodes[node_id] = NodeGene(id=node_id, node_type='input')
            genome.input_ids.append(node_id)
        
        bias_id = innovation.get_node_id()
        genome.nodes[bias_id] = NodeGene(id=bias_id, node_type='bias')
        genome.bias_id = bias_id

        for o in range(num_outputs):
            node_id = innovation.get_node_id()
            genome.nodes[node_id] = NodeGene(id=node_id, node_type='output')
            genome.output_ids.append(node_id)

        for in_id in genome.input_ids + [genome.bias_id]:
            for out_id in genome.output_ids:
                innovation_number = innovation.get_connection_innovation(in_id, out_id)
                genome.connections[innovation_number] = ConnectionGene(
                    innovation_number=innovation_number,
                    in_node=in_id,
                    out_node=out_id,
                    weight=random.uniform(-1.0, 1.0)
                    enabled=True
                )
        
        return genome
    
    def mutate_weights(self, perturb_chance = 0.9, step_size = 0.1):
        for c in self.connections.values():
            if random.random() < perturb_chance:
                c.weight += random.uniform(-step_size, step_size)
            else:
                c.weight = random.uniform(-1.0, 1.0)
    
    def add_connection(self, max_attempts = 50):
        node_ids = list(self.nodes.keys())
        for _ in range(max_attempts):
            a = random.choice(node_ids)
            b = random.choice(node_ids)
            if self.nodes[a].node_type == 'output' and self.nodes[b].node_type == 'input':
                continue
            if a == b:
                continue
            
            existing_connection = any(
                c.in_node == a and c.out_node == b
                for c in self.connections.values()
            )
            if existing_connection:
                continue
            
            innovation_number = self.innovation.get_connection_innovation(a, b)
            self.connections[innovation_number] = ConnectionGene(
                innovation_number=innovation_number,
                in_node=a,
                out_node=b,
                weight=random.uniform(-1.0, 1.0),
                enabled=True
            )
            return True
        return False

    def add_node(self):
        enabled_connections = [c for c in self.connections.values() if c.enabled]
        if not enabled_connections:
            return False
        
        connection_to_split = random.choice(enabled_connections)
        connection_to_split.enabled = False

        new_node_id = self.innovation.get_node_id()
        self.nodes[new_node_id] = NodeGene(id=new_node_id, node_type='hidden')

        innovation_number1 = self.innovation.get_connection_innovation(connection_to_split.in_node, new_node_id)
        innovation_number2 = self.innovation.get_connection_innovation(new_node_id, connection_to_split.out_node)

        self.connections[innovation_number1] = ConnectionGene(
            innovation_number=innovation_number1,
            in_node=connection_to_split.in_node,
            out_node=new_node_id,
            weight=1.0,
            enabled=True
        )
        self.connections[innovation_number2] = ConnectionGene(
            innovation_number=innovation_number2,
            in_node=new_node_id,
            out_node=connection_to_split.out_node,
            weight=connection_to_split.weight,
            enabled=True
        )
        return True
    
    def crossover(self, other: 'Genome') -> 'Genome':
        if len(self.connections) < len(other.connections):
            parent1, parent2 = other, self
        else:
            parent1, parent2 = self, other
        
        child = Genome(self.innovation)
        child.nodes = {node_id: NodeGene(**vars(node)) for node_id, node in parent1.nodes.items()}
        child.input_ids = list(parent1.input_ids)
        child.output_ids = list(parent1.output_ids)
        child.bias_id = parent1.bias_id

        for innovation_number, conn1 in parent1.connections.items():
            conn2 = parent2.connections.get(innovation_number)
            if conn2 and random.random() < 0.5 and conn2.enabled:
                chosen_conn = conn2
            else:
                chosen_conn = conn1
            
            child.connections[innovation_number] = ConnectionGene(
                innovation_number=chosen_conn.innovation_number,
                in_node=chosen_conn.in_node,
                out_node=chosen_conn.out_node,
                weight=chosen_conn.weight,
                enabled=chosen_conn.enabled
                recurrent=chosen_conn.recurrent
            )
        
        return child

def compatibility_distance(self, other: 'Genome', c1=1.0, c2=1.0, c3=0.4) -> float:
    this_conn = self.connections
    other_conn = other.connections
    max_innovation = max(this_conn.keys() if this_conn else 0, other_conn.keys() if other_conn else 0)

    disjoint = 0
    weights = []
    for innovation_number in range(1, max_innovation + 1):
        conn1 = this_conn.get(innovation_number)
        conn2 = other_conn.get(innovation_number)
        if conn1 and conn2:
            weights.append(abs(conn1.weight - conn2.weight))
        elif conn1 or conn2:
            disjoint += 1
    
    average_weight_diff = sum(weights) / len(weights) if weights else 0.0
    N = max(len(this_conn), len(other_conn))
    if N < 20:
        N = 1
        
    return (c1 * disjoint / N) + (c2 * average_weight_diff)