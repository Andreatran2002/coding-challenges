from dataclasses import dataclass
import os
from typing import Dict

from app.services.counter import Counter
from app.services.huffman_tree import  HuffmanNodeGenerator
@dataclass
class Header:
    table: Dict[str,int]
    file_name: str

class Compressor:
    def process(self, file: str):
        if not os.path.exists(file):
            raise Exception("File is not exist")
        table = Counter.from_file(file)
        generator = HuffmanNodeGenerator()
        tree = generator.generate(table) 
        header = Header(table=table, file_name=file.split("/")[:-1])
        

    def gen_header_data(self, header: Header) -> str:
        data = (f"{x}={y}" for x, y in header.table.items())
        data = ",".join(data)
        return f"vct@@{header.file_name}///{data}@@vct"

    
 
    