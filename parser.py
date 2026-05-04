from typing import Tuple
from zone import Zone
from graph import GraphModel
from connection import Connection

class ParserError(Exception):
    """Raised when the parser encounters an error in the input data."""
    pass


def pase_drone(line: str, number: int) -> int:
    """Parse the nb of drones"""
    parsed = line.strip()
    if not parsed.startswith("nb_drones"):
        raise ParserError(f"Invalid line format in line: {number}. Input must be 'nb_drones:', gor '{parsed}'")
    try:
        value = int(parsed.split(":", 1)[1].strip())
    except ValueError:
        raise ParserError(f"Line {number}: nb_drones must be a positive integer")
    if value <= 0:
        raise ParserError(f"Line {number}: nb_drones must be a positive integer")
    return value


def parse_metadata(metadata: str, number: int) -> dict[str,str]:
    """Parse metadata input"""
    meta: dict[str, str] = {}
    data = metadata.strip("[]").strip()
    try:
        for i in data.split():
            if '=' in i:
                j, k = i.split("=", 1)
                meta[j.strip()] = k.strip()
    except Exception:
        raise ParserError(f"Invalid metadata input '{metadata}' in line: {number}")
    return meta


def parse_zone(line: str, number: int) -> Zone:
    """Parse zone line and return Zone object"""
    parsed = line.strip()
    if ":" not in parsed:
        raise ParserError(f"Line {number} missing ':'")
    zone_type, zone_info = parsed.split(":", 1)
    zone_type = zone_type.strip()
    zone_info = zone_info.strip()

    if zone_type not in ("hub", "start_hub", "end_hub"):
        raise ParserError(f"Invalid zone input")
    
    metadata: dict[str, str] = {}
    if "[" in zone_info:
        if not "]" in zone_info:
            raise ParserError(f"Invalid metadata input in line: {number}")
        start = zone_info.index("[") # index returns the first ocurrence of an element
        meta_info = zone_info[start:]
        zone_info = zone_info[:start].strip()
        metadata = parse_metadata(meta_info, number)
    
    parameters = zone_info.split()
    if len(parameters) != 3:
        raise ParserError(f"Invalid parameters. Format must be: name (x) (y)")
    name, xstr, ystr = parameters

    try:
        x = int(xstr)
        y = int(ystr)
    except ValueError:
        raise ParserError(f"(x) and (y) parameters must be integers.")
    
    # parse optional metadata
    color = metadata.get("color", None)
    drones_number = metadata.get("max_drones", "1")
    try:
        max_drones = int(drones_number)
    except ValueError:
        raise ParserError(f"Error. max_drones must be an integer.")
    if max_drones <= 0:
        raise ParserError(f"Error. max_drones must be a positive integer.")
    
    return Zone(
        name=name,
        x=x,
        y=y,
        zone_type=zone_type,
        color=color,
        max_drones=max_drones,
        is_start=(zone_type == "start_hub"),
        is_end=(zone_type == "end_hub")
        )
    