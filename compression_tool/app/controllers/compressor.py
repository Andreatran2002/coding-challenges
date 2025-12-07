from dataclasses import dataclass
import os
from typing import Dict

from app.services.counter import Counter
from app.services.huffman_tree import  HuffmanNodeGenerator
from app.models.huffman_node import HuffmanNode, LeafHuffmanNode
@dataclass
class Header:
    table: Dict[str,int]
    file_name: str

class Compressor:


    def encode(self, file: str):
        if not os.path.exists(file):
            raise Exception("File is not exist")
        table = Counter.from_file(file)
        generator = HuffmanNodeGenerator()
        tree = generator.generate(table) 
        header = Header(table=table, file_name=file.split("/")[:-1])
        output = self.gen_header_data(header)
        with open(file) as f: 
            c = f.read(1)
            encoded_code = self._encode_byte(tree,c)
            output=f"{output}{encoded_code}"
    
    def _encode_byte(self, tree: HuffmanNode, c: str):
        current_node = tree
        code = ""
        while current_node: 
            if isinstance(current_node, LeafHuffmanNode):
                code += current_node.prefix
            
            if current_node.letter == c: 
                return code

    def gen_header_data(self, header: Header) -> str:
        data = (f"{x}={y}" for x, y in header.table.items())
        data = ",".join(data)
        return f"vct@@{header.file_name}///{data}@@vct"

    
 
    