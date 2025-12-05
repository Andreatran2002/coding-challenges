from dataclasses import dataclass
from typing import List, Optional

from lexical import Lexical, Token


class JsonNode:
    pass

@dataclass
class KeyValueNode(JsonNode):
    key: str
    value: JsonNode
    def __str__(self) -> str:
        return f"{self.key}={str(self.value)}"

class ObjectJsonNode(JsonNode):
    def __init__(self):
        self.items: List[KeyValueNode] = []
    def __str__(self) -> str:
        output = "{"
        for i, item in enumerate(self.items):
            if i > 0:
                output += ","
            output += str(item)
        return output+"}"

class ArrayJsonNode(JsonNode):
    def __init__(self):
        self.items: List[JsonNode] = []
    def __str__(self) -> str:
        output = "["
        for i, item in enumerate(self.items):
            if i > 0:
                output += ","
            output += str(item)
        return output+"]"

class Json:

    def __init__(self, data: str) -> None:
        lexical = Lexical()
        self.index = 0
        self.tokens = lexical.tokenize(data)

    def __str__(self):
        return str(self.parse())

    @property
    def next_token(self) -> Optional[Token]:
        result = self.tokens[self.index] if self.index < len(self.tokens) else None
        return result

    def parse(self) -> JsonNode:

        match (self.next_token.type):
            case ("LBRACE"):
                return self.parse_object()
            case ("LBRACKET"):
                return self.parse_array()
        raise Exception("Invalid")   


    def parse_object(self) -> ObjectJsonNode:
        result = ObjectJsonNode()
        self.__require("LBRACE")
        if self.next_token.type == "RBRACE":
            self.__require("RBRACE")
            return result
        while True:
            result.items.append(self.parse_key_value())
            if self.next_token.type == "RBRACE":
                self.__require("RBRACE")
                return result
            self.__require("COMMA")


    def parse_key_value(self) -> KeyValueNode:
        key = self.parse_string()
        self.__require("COLON")
        match (self.next_token.type):
            case ("STRING"):
                value = self.parse_string()
            case ("NUMBER"):
                value = self.parse_number()
            case ("TRUE"):
                value = self.parse_bool()
            case ("FALSE"):
                value = self.parse_bool()
            case ("NULL"):
                value = self.parse_null()
            case ("LBRACKET"):
                value = self.parse_array()
            case ("LBRACE"):
                value = self.parse_object()
            case _:
                raise Exception(f"Unexpected token type: {self.next_token.type}")
        return KeyValueNode(key=key, value=value)
    
    def parse_string(self) -> str:
        if self.next_token.type != "STRING":
            raise Exception(f"Expect STRING but got {self.next_token.type}")
        result = self.next_token.value.replace("\"","")
        self.index+=1
        return result
    
    def parse_number(self) -> int:
        if self.next_token.type != "NUMBER":
            raise Exception(f"Expect NUMBER but got {self.next_token.type}")
        result = self.next_token.value
        self.index+=1
        return result
   
    def parse_bool(self) -> bool:
        if self.next_token.type != "TRUE" and self.next_token.type != "FALSE" :
            raise Exception(f"Expect BOOL but got {self.next_token.type}")
        result = self.next_token.value
        self.index+=1
        return result

    def parse_null(self):
        if self.next_token.type != "NULL" :
            raise Exception(f"Expect NULL but got {self.next_token.type}")
        result = self.next_token.value
        self.index+=1
        return result

    def parse_array(self) -> ArrayJsonNode:
        self.__require("LBRACKET")
        result = ArrayJsonNode()
        if self.next_token.type == "RBRACKET":
            self.__require("RBRACKET")
            return result
        while True:
            match (self.next_token.type):
                case ("STRING"):
                    result.items.append(self.parse_string())
                case ("NUMBER"):
                    result.items.append(self.parse_number())
                case ("TRUE"):
                    result.items.append(self.parse_bool())
                case ("FALSE"):
                    result.items.append(self.parse_bool())
                case ("NULL"):
                    result.items.append(self.parse_null())
                case ("LBRACKET"):
                    result.items.append(self.parse_array())
                case ("LBRACE"):
                    result.items.append(self.parse_object())
                case _:
                    raise Exception(f"Unexpected token type in array: {self.next_token.type}")
            if self.next_token.type == "RBRACKET":
                self.__require("RBRACKET")
                return result
            self.__require("COMMA")
    
    def __require(self, type: str):
        if self.next_token.type != type: 
            raise Exception(f"Expect {type} but got {self.next_token.type}")
        self.index+=1

