from enum import Enum


class NODE_TYPES(Enum):
    UNKNOWN = 1
    STATEMENT = 2
    EXPRESSION = 3

class Node:
    # TODO: criar classe Node
    def __init__(self, nodeType: int = NODE_TYPES.VOID):
        self.node_type = nodeType

class ProgramNode(Node):
    # TODO: criar classes dependentes
    def __init__(self):
        super().__init__()