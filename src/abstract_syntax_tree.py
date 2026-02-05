from globals import NODE_TYPES

from typing import override


class Node:
    # TODO: criar classe Node
    def __init__(self, node_type = NODE_TYPES.UNKNOWN):
        self.node_type: NODE_TYPES = node_type

    def ToString(self) -> str:
        return ""