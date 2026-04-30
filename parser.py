from typing import Tuple
from zone import Zone
from graph import GraphModel
from connection import Connection

class ParserError(Exception):
    """Raised when the parser encounters an error in the input data."""
    pass


def pase_drone(line: int, number: int) -> int:



def parse_metadata(metadata: str, number: int) -> dict[str,str]:
    meta = {}
    data = metadata.strip("[]").strip()
    try:
        for i in data.split():
            if '=' in i:
                j, k = i.split("=", 1)
                meta[j.strip()] = k.strip()
    except Exception:
        raise ParserError(f"Invalid metadata input '{metadata} in line: {number}")
    return meta