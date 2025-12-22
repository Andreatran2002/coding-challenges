
from typing import Dict, List
from bitstring import Bits
from app.models.huffman_node import HuffmanNode, LeafHuffmanNode, WeightHuffmanNode


class HuffmanNodeGenerator:
    def gen_node(self, table: Dict[bytes, int]) -> HuffmanNode:
        list_letters = [
            LeafHuffmanNode(letter=key, weight=value) for key, value in table.items()
        ]
        
        return self._build_tree(sorted(list_letters, key=lambda f: f.weight, reverse=True))
    
    def _build_tree(self, node_list: List[HuffmanNode]) -> HuffmanNode:
        while len(node_list) > 1:
            left = node_list.pop()
            right = node_list.pop()
            node = WeightHuffmanNode(left=left,right=right,weight=left.weight+right.weight)
            node_list.append(node)
            node_list = sorted(node_list, key=lambda f: f.weight, reverse=True)
        return node

    def gen_prefix_table(self, tree: HuffmanNode) -> Dict[bytes, str]:
        """Generate prefix table by traversing the Huffman tree."""
        return self._traverse_tree(tree, "", {})
    
    def _traverse_tree(self, node: HuffmanNode, code: str, prefix_table: Dict[bytes, str]) ->  Dict[bytes, str]:
        """Recursively traverse the tree to build prefix codes."""
        if node is None:
            return None
        
        if isinstance(node, LeafHuffmanNode):
            prefix_table[node.letter] = code
        
        if node.left:
            self._traverse_tree(node.left, code + "0", prefix_table)
        if node.right:
            self._traverse_tree(node.right, code + "1", prefix_table)
            
        return prefix_table
            