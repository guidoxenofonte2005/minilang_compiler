from abstract_syntax_tree import Node
from globals import NODE_TYPES, REL_OPS, ADD_OPS, MUL_OPS


def leftHandSide(node: Node) -> Node:
    if node.node_type == NODE_TYPES.IDENTIFIER:
        return node
    raise SyntaxError(f"Expressão {node.to_string()} não possui valor à esquerda")


def rightHandSide(node: Node) -> Node:
    if node.node_type == NODE_TYPES.IDENTIFIER:
        return node
    if node.node_type in REL_OPS:
        pass
    else:
        raise SyntaxError(f"Expressão {node.to_string} não possui valor à direita")
