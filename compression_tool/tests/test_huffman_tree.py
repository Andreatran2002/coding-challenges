import logging
from app.services.huffman_tree import HuffmanNodeGenerator
from app.models.huffman_node import LeafHuffmanNode, WeightHuffmanNode


def test_huffman_tree():
    dicts = {
        "z": 2,
        "k": 7,
        "m": 24,
    }
    tree = HuffmanNodeGenerator.generate(dicts)

    assert tree == WeightHuffmanNode(
        weight=33,
        left=WeightHuffmanNode(
            weight=9,
            left=LeafHuffmanNode(letter="z", weight=2, prefix=0),
            right=LeafHuffmanNode(letter="k", weight=7, prefix=1),
            prefix=0
        ),
        right=LeafHuffmanNode(letter="m", weight=24, prefix=1),
    )
