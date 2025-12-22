from dataclasses import dataclass
from typing import Dict


@dataclass
class Header:
    table: Dict[bytes, int]
    file_name: str
