import logging
from app.services.huffman_tree import HuffmanNodeGenerator
from app.models.huffman_node import LeafHuffmanNode, WeightHuffmanNode


def test_huffman_tree():
    dicts = {
        "z": 2,
        "k": 7,
        "m": 24,
        "c": 32,
        "l": 42,
        "d": 42,
        "u": 37,
        "e": 120,
    }
    generator = HuffmanNodeGenerator()
    tree = generator.generate(dicts)

    # This Huffman tree is constructed to match the structure and weights from the image.
    expected_tree = WeightHuffmanNode(
        weight=306,
        left=LeafHuffmanNode(letter="e", weight=120, prefix=0),
        right=WeightHuffmanNode(
            weight=186,
            left=WeightHuffmanNode(
                weight=79,
                left=LeafHuffmanNode(letter="u", weight=37, prefix=0),
                right=LeafHuffmanNode(letter="d", weight=42, prefix=1),
                prefix=0
            ),
            right=WeightHuffmanNode(
                weight=107,
                left=LeafHuffmanNode(letter="l", weight=42, prefix=0),
                right=WeightHuffmanNode(
                    weight=65,
                    left=LeafHuffmanNode(letter="c", weight=32, prefix=0),
                    right=WeightHuffmanNode(
                        weight=33,
                        left=WeightHuffmanNode(
                            weight=9,
                            left=LeafHuffmanNode(letter="z", weight=2, prefix=0),
                            right=LeafHuffmanNode(letter="k", weight=7, prefix=1),
                            prefix=0
                        ),
                        right=LeafHuffmanNode(letter="m", weight=24, prefix=1),
                        prefix=1
                    ),
                    prefix=1
                ),
                prefix=1
            ),
            prefix=1
        ),
    )

    # The tree construction is based on left-first, then right, and matches the diagram.
    # Depending on the actual implementation, some prefix or node ordering differences may exist.
    assert tree == expected_tree
    # Optionally, you might want to recurse through the nodes and compare each for full equality instead of just root weight.
