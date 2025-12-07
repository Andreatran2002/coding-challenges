
from dataclasses import dataclass
from typing import Optional


@dataclass
class HuffmanNode: 
    weight: int
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None
    prefix: int = 0
    def __rep__(self) -> str:
        return f"node({self.letter},{self.weight})"
    def __str__(self) -> str:
        return f"node({self.letter},{self.weight})"


@dataclass
class LeafHuffmanNode(HuffmanNode):
    letter: str = ""
    is_leaf: bool = True
    def __rep__(self) -> str:
        return f"node({self.letter},{self.weight})"
    def __str__(self) -> str:
        return f"node({self.letter},{self.weight})"

@dataclass
class WeightHuffmanNode(HuffmanNode):
    is_leaf: bool = False
    def __rep__(self) -> str:
        return f"node({self.weight})"
    def __str__(self) -> str:
        return f"node({self.weight})"