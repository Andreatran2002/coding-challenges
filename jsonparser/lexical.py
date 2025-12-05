from dataclasses import dataclass
from enum import Enum
import re
from typing import Dict, List


@dataclass
class Token:
    type: str
    value: str | int | float | bool | None = None
    def __repr__(self):
        return f"{self.value}"

class Lexical():
    dicts : Dict[str,str]= {
        "LBRACE" : r"{",
        "RBRACE" : r"}",
        "LBRACKET" : r"\[",
        "RBRACKET" : r"\]",
        "COLON" : r"\:",
        "COMMA" : ",",
        "STRING" : r"\"[^\"]*\"",
        "NUMBER" : r"\-?\d+(\.\d+)?",
        "TRUE" : r"true",
        "FALSE" : r"false",
        "NULL" : r"null",
        "WHITESPACE" : r"\s+",
    }
    def tokenize(self, data: str) -> List[Token]:
        tokens = []
        position = 0
        while position < len(data):
            match = None
            for key, regex in self.dicts.items():
                match = re.match(regex, data[position:])
                if match:
                    if key != "WHITESPACE":
                        tokens.append(Token(type=key, value=match.group(0)))
                    position = position + match.end()
                    break
            if not match:
              raise Exception(f"Invalid token at position {position}")
            
        return tokens
                