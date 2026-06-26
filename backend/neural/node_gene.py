from dataclasses import dataclass
import math

@dataclass
class NodeGene:
    id: int
    node_type: str # 'input', 'hidden', 'output' or 'bias'
    activation_function: str = "tanh"
    bias: float = 0.0

    def activate(self, x: float) -> float:
        if self.activation_function == "sigmoid":
            return 1.0 / (1.0 + math.exp(-x))
        if self.activation_function == "relu":
            return max(0.0, x)
        return math.tanh(x)