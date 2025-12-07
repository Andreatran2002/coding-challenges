from app.controllers.compressor import Compressor, Header
from app.models.huffman_node import HuffmanNode, LeafHuffmanNode, WeightHuffmanNode


def test_gen_header():
    compressor = Compressor()
    header = Header(table={"a": 2, "b": 3, "c": 4}, file_name="test_file.txt")
    result = compressor.gen_header_data(header)
    expect_header = "vct@@test_file.txt///a=2,b=3,c=4@@vct"
    assert result == expect_header

def test_gen_prefix_table():
    compressor = Compressor()
    tree = WeightHuffmanNode(
        weight=306,
        left=LeafHuffmanNode(letter="e", weight=120),
        right=WeightHuffmanNode(
            weight=186,
            left=WeightHuffmanNode(
                weight=79,
                left=LeafHuffmanNode(letter="u", weight=37),
                right=LeafHuffmanNode(letter="d", weight=42),
            ),
            right=WeightHuffmanNode(
                weight=107,
                left=LeafHuffmanNode(letter="l", weight=42),
                right=WeightHuffmanNode(
                    weight=65,
                    left=LeafHuffmanNode(letter="c", weight=32),
                    right=WeightHuffmanNode(
                        weight=33,
                        left=WeightHuffmanNode(
                            weight=9,
                            left=LeafHuffmanNode(letter="z", weight=2),
                            right=LeafHuffmanNode(letter="k", weight=7),
                        ),
                        right=LeafHuffmanNode(letter="m", weight=24),
                    ),
                ),
            ),
        ),
    )
    result = compressor.gen_prefix_table(tree)
    expect_prefix_table = {"e": "0", "u": "100", "d": "101", "l": "110", "c": "1110", "z": "111100", "k": "111101", "m": "11111"}
    assert result == expect_prefix_table
