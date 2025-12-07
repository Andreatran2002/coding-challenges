from dataclasses import dataclass
from typing import Dict, List

from app.models.huffman_node import HuffmanNode, LeafHuffmanNode, WeightHuffmanNode
from app.models.letter_frequency import LetterFrequency


class HuffmanNodeGenerator:
    def generate(table: Dict[str, int]) -> HuffmanNode:
        list_letters = [
            LetterFrequency(letter=key, value=value) for key, value in table.items()
        ]
        list_letters = sorted(list_letters, key=lambda f: f.value)
        if len(list_letters) < 2:
            return LeafHuffmanNode(
                letter=list_letters[0].letter, weight=list_letters[0].value
            )

        root_left_node = LeafHuffmanNode(
            letter=list_letters[0].letter, weight=list_letters[0].value
        )
        root_right_node = LeafHuffmanNode(
            letter=list_letters[1].letter, weight=list_letters[1].value
        )
        root_node = WeightHuffmanNode(
            left=root_left_node,
            right=root_right_node,
            weight=root_left_node.weight + root_right_node.weight,
        )

        position = 2

        while position < len(list_letters):
            right_node = LeafHuffmanNode(
                letter=list_letters[position].letter,
                weight=list_letters[position].value,
            )
            root_node = WeightHuffmanNode(
                left=root_node,
                right=right_node,
                weight=root_node.weight + right_node.weight,
            )
            position += 1

        return root_node
