from typing import Dict


class Counter:
    @staticmethod
    def from_file(file: str):
        table: Dict[str,int] = {}
        with open(file, 'r') as f: 
            c = f.read(1)
            while c: 
                table[c] = table.get(c,0) + 1
                c = f.read(1)
        return table
            