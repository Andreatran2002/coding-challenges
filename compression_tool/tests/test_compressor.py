import logging
from bitstring import BitStream, Bits
from app.controllers.compressor import Compressor
from app.models.huffman_node import LeafHuffmanNode, WeightHuffmanNode
from app.services.huffman_tree import HuffmanNodeGenerator

logging.basicConfig(level=logging.INFO)

def test_gen_header():
    compressor = Compressor()
    table_info = {b'a': 2, b'b': 3, b'c': 4}
    file_name = "test_file.txt"
    result = compressor._get_header_data(table_info, file_name)
    expect_header = Bits(f"vct@@{file_name}///b'a'=2,b'b'=3,b'c'=4@@vct".encode("utf-8"))
    assert result.bytes == expect_header.bytes

def test_gen_prefix_table():
    tree = WeightHuffmanNode(
        weight=306,
        left=LeafHuffmanNode(letter=b'e', weight=120),
        right=WeightHuffmanNode(
            weight=186,
            left=WeightHuffmanNode(
                weight=79,
                left=LeafHuffmanNode(letter=b'u', weight=37),
                right=LeafHuffmanNode(letter=b'd', weight=42),
            ),
            right=WeightHuffmanNode(
                weight=107,
                left=LeafHuffmanNode(letter=b'l', weight=42),
                right=WeightHuffmanNode(
                    weight=65,
                    left=LeafHuffmanNode(letter=b'c', weight=32),
                    right=WeightHuffmanNode(
                        weight=33,
                        left=WeightHuffmanNode(
                            weight=9,
                            left=LeafHuffmanNode(letter=b'z', weight=2),
                            right=LeafHuffmanNode(letter=b'k', weight=7),
                        ),
                        right=LeafHuffmanNode(letter=b'm', weight=24),
                    ),
                ),
            ),
        ),
    )
    generator = HuffmanNodeGenerator()
    result = generator.gen_prefix_table(tree)
    expect_prefix_table = {b'e': "0", b'u': "100", b'd': "101", b'l': "110", b'c': "1110", b'z': "111100", b'k': "111101", b'm': "11111"}
    assert result == expect_prefix_table
