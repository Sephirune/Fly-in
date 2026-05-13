from typing import Optional
from zones import Zone
from connection import Connection
from parser import ParserError

class Graph:
    """Represents the drone flying network as a map of zones and connections"""
    def __init__(self, nb_drones: int) -> None:
        self.nb_drones = nb_drones
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start: Optional[Zone] = None
        self.end: Optional[Zone] = None
        self.connection_keys: set[tuple[str, str]] = set()
        self.adjacency: dict[str, list[Connection]] = {}

    def add_zone(self, zone: Zone) -> None:
        if zone.name in self.zones:
            raise ParserError(f"Error: already existing zone detected.")
        self.zones[zone.name] = zone
        
        if zone.is_start:
            if self.start is not None:
                raise ParserError(f"Error: duplicated start.")
            self.start = zone
        if zone.is_end:
            if self.end is not None:
                raise ParserError(f"Error: duplicated end.")
            self.end = zone
        
        self.adjacency[zone.name] = []


    def add_connection(self, connection: Connection):
        if (connection.name1 not in self.zones) or (connection.name2 not in self.zones):
            raise ParserError("Error: Non existing zone detected.")
        
        valid_keys = tuple(sorted([connection.name1, connection.name2]))
        if valid_keys in self.connection_keys:
            raise ParserError(
                f"Error: connection already exists: "
                f"{connection.name1}, {connection.name2}."
            )
        
        if connection.name1 == connection.name2:
            raise ParserError("Error: Duplicated zone given.")
        
        self.connections.append(connection)
        self.connection_keys.add(valid_keys)
        self.adjacency[connection.name1].append(connection)
        self.adjacency[connection.name2].append(connection)
