
from dataclasses import dataclass
from typing import Optional


@dataclass
class HuffmanNode: 
    weight: int
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None
    def __repr__(self) -> str:
        return f"node(weight={self.weight})"
    def __str__(self) -> str:
        return f"node(weight={self.weight})"


@dataclass
class LeafHuffmanNode(HuffmanNode):
    letter: bytes = b""
    is_leaf: bool = True
    def __repr__(self) -> str:
        return f"node(letter={self.letter},weight={self.weight})"
    def __str__(self) -> str:
        return f"node(letter={self.letter},weight={self.weight})"

@dataclass
class WeightHuffmanNode(HuffmanNode):
    is_leaf: bool = False
    def __repr__(self) -> str:
        return f"node(weight={self.weight})"
    def __str__(self) -> str:
        return f"node(weight={self.weight})"