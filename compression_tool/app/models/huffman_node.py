
from dataclasses import dataclass
from typing import Optional


@dataclass
class HuffmanNode: 
    weight: int
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None
    prefix: int = 0

@dataclass
class LeafHuffmanNode(HuffmanNode):
    letter: str = ""
    is_leaf: bool = True

@dataclass
class WeightHuffmanNode(HuffmanNode):
    is_leaf: bool = False