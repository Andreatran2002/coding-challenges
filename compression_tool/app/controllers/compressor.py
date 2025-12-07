from dataclasses import dataclass
import logging
import os
from typing import Dict

from app.services.counter import Counter
from app.services.huffman_tree import HuffmanNodeGenerator
from app.models.huffman_node import HuffmanNode, LeafHuffmanNode, WeightHuffmanNode


@dataclass
class Header:
    table: Dict[str, int]
    file_name: str


class Compressor:
    def __init__(self) -> None:
        self.generator = HuffmanNodeGenerator()
        self.prefix_table = {}

    def encode(self, file: str):
        if not os.path.exists(file):
            raise Exception("File is not exist")
        table = Counter.from_file(file)
        file_name = os.path.basename(file)
        header_data = self.gen_header_data(
            Header(table=table, file_name=file_name)
        )
        self.tree = self.generator.generate(table)
        self.prefix_table = self.gen_prefix_table(self.tree)
        print(self.prefix_table)
        # with open(file) as f:
        #     c = f.read(1)
        #     output = f"{output}{self.prefix_table[c]}"

    def gen_prefix_table(
        self,
        tree: HuffmanNode,
    ) -> Dict[str, str]:
        """Generate prefix table by traversing the Huffman tree."""
        prefix_table = {}
        self._traverse_tree(tree, "", prefix_table)
        return prefix_table
    
    def _traverse_tree(self, node: HuffmanNode, code: str, prefix_table: Dict[str, str]) -> None:
        """Recursively traverse the tree to build prefix codes."""
        if node is None:
            return
        
        if isinstance(node, LeafHuffmanNode):
            prefix_table[node.letter] = code
            return
        
        if node.left:
            self._traverse_tree(node.left, code + "0", prefix_table)
        if node.right:
            self._traverse_tree(node.right, code + "1", prefix_table)
            
    def _get_code_by_letter(self, key: str) -> str:
        """Get the Huffman code for a given letter."""
        return self.prefix_table.get(key, "")


    def gen_header_data(self, header: Header) -> str:
        data = [f"{x}={y}" for x, y in header.table.items()]
        data = ",".join(data)
        return f"vct@@{header.file_name}///{data}@@vct"
