from typing import Dict


class Counter:
    @staticmethod
    def from_file(file: str):
        table: Dict[bytes,int] = {}
        with open(file, 'rb') as f: 
            c = f.read(1)
            while c: 
                table[c] = table.get(c,0) + 1
                c = f.read(1)
        return table
            