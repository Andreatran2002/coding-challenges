from dataclasses import dataclass
import os
from typing import Dict

from app.services.counter import Counter
from app.services.huffman_tree import  HuffmanNodeGenerator


class Compressor:
    def process(self, file: str):
        if not os.path.exists(file):
            raise Exception("File is not exist")
        table = Counter.from_file(file)
        generator = HuffmanNodeGenerator()
        tree = generator.generate(table) 
        print(tree)
    
 
    