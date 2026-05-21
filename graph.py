from typing import Optional
from zones import Zone
from connection import Connection
from parse_error import ParserError


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

    def get_zone(self, name: str) -> Optional[Zone]:
        """Get the zone name"""
        return self.zones.get(name)

    def add_zone(self, zone: Zone) -> None:
        if zone.name in self.zones:
            raise ParserError(f"Error: already existing zone detected.")
        self.zones[zone.name] = zone

        if zone.is_start:
            if self.start is not None:
                raise ParserError("Error: duplicated start.")
            self.start = zone
        if zone.is_end:
            if self.end is not None:
                raise ParserError("Error: duplicated end.")
            self.end = zone

        self.adjacency[zone.name] = []

    def add_connection(self, connection: Connection):
        if (connection.name1 not in self.zones) or (connection.name2 not in
                                                    self.zones):
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

    def get_neighbors(self, name: str) -> list[str]:
        """Get adjacent zones of the graph"""
        neighbor: list[str] = []
        for i in self.adjacency[name]:
            neighbor.append(i.return_other(name))
        return neighbor

    def get_connection(self, name1: str, name2: str) -> Optional[Connection]:
        """Get the connection between two zones"""
        for i in self.adjacency[name1]:
            if i.valid_name(name2):
                return i
        return None

    def validate(self) -> None:
        """Validates if the graph has a start and end defined"""
        if self.start is None:
            raise ParserError("Error: No start defined.")
        if self.end is None:
            raise ParserError("Error: No end defined.")
    
    def __repr__(self):
        """Return string representation of the Graph."""
        return (
            f"Graph(zones={len(self.zones)}, connections={len(self.connections)}),"
        )
