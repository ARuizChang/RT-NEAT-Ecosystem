from .node_gene import NodeGene
from .connection_gene import ConnectionGene
from .genome import Genome
from typing import List, Dict
import math

class Network:
    def __init__(self, genome: Genome):
        self.genome = genome
        self.node_order = self._topological_sort()
        self.state: Dict[int, float] = {node.id: 0.0 for node in self.genome.nodes}
    
    def _topological_sort(self) -> List[int]:
        in_degree = {node.id: 0 for node in self.genome.nodes}
        children = {node.id: [] for node in self.genome.nodes}
        for connection in self.genome.connections.values():
            if not connection.enabled or connection.recurrent:
                continue
            in_degree[connection.out_node] += 1
            children[connection.in_node].append(connection.out_node)
        
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        order = []
        while queue:
            node_id = queue.pop(0)
            order.append(node_id)
            for out in children[node_id]:
                in_degree[out] -= 1
                if in_degree[out] == 0:
                    queue.append(out)
        for node_id in self.genome.nodes:
            for node_id not in order:
                order.append(node_id)
        
        return order

    def forward(self, inputs: List[float]) -> List[float]:
        assert len(inputs) == len(self.genome.input_ids)
        values = {node_id: 0.0 for node_id in self.genome.nodes}
        for node_id, input_value in zip(self.genome.input_ids, inputs):
            values[node_id] = input_value
        if self.genome.bias_id is not None:
            values[self.genome.bias_id] = 1.0

        for node_id in self.node_order:
            node = self.genome.nodes[node_id]
            if node.type in {'input', 'bias'}:
                continue
            total_input = 0.0
            for connection in self.genome.connections.values():
                if not connection.enabled or connection.out_node != node_id:
                    continue
                total_input += values[connection.in_node] * connection.weight
                if connection.recurrent:
                    total_input += self.state[connection.in_node] * connection.weight
            values[node_id] = self._activation_function(total_input)
        for node_id in values:
            if self.genome.nodes[node_id].type != 'input':
                self.state[node_id] = values[node_id]
            
        return [values[node_id] for node_id in self.genome.output_ids]