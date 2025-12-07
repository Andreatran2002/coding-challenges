from dataclasses import dataclass
import logging
from typing import Dict, List

from app.models.huffman_node import HuffmanNode, LeafHuffmanNode, WeightHuffmanNode
from app.models.letter_frequency import LetterFrequency


class HuffmanNodeGenerator:
    def generate(self, table: Dict[str, int]) -> HuffmanNode:
        list_letters = [
            LetterFrequency(letter=key, value=value) for key, value in table.items()
        ]
        list_letters = sorted(list_letters, key=lambda f: f.value, reverse=True)
        
        node_list = [LeafHuffmanNode(letter=letter.letter, weight=letter.value) for letter in list_letters]

        return self._build_tree(node_list)
    
    def _build_tree(self, node_list: List[HuffmanNode]) -> HuffmanNode:
        while len(node_list) > 1:
            left = node_list.pop()
            right = node_list.pop()
            node = WeightHuffmanNode(left=left,right=right,weight=left.weight+right.weight)
            node_list.append(node)
            node_list = sorted(node_list, key=lambda f: f.weight, reverse=True)
        return node