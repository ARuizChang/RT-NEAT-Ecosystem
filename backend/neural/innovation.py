from typing import Dict, Tuple

class InnovationTracker:
    def __init__(self):
        self.next_innovation = 1
        self.connection_history: Dict[Tuple[int, int], int] = {}
        self.next_node_id = 1
        self.node_history: Dict[Tuple[int, int], int] = {}

    def get_connection_innovation(self, in_node: int, out_node: int) -> int:
        key = (in_node, out_node)
        if key not in self.connection_history:
            self.connection_history[key] = self.next_innovation
            self.next_innovation += 1
        return self.connection_history[key]
    
    def get_node_id(self) -> int:
        node_id = self.next_node_id
        self.next_node_id += 1
        return node_id