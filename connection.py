from typing import Optional
from zones import Zone
from parse_error import ParserError


class Connection:
    def __init__(
        self,
        name1: str,
        name2: str,
        max_link_capacity: Optional[int] = 1
    ) -> None:
        self.name1 = name1
        self.name2 = name2
        self.max_link_capacity = max_link_capacity

    def valid_name(self, name: str) -> bool:
        """Bool to check if the connection is valid"""
        return name == self.name1 or name == self.name2

    def return_other(self, name: str) -> str:
        """Returns the other zone of the connection"""
        if name == self.name1:
            return self.name2
        if name == self.name2:
            return self.name1
        raise ParserError(f"Error: Zone {name} is not part of the connection.")

    def __repr__(self) -> str:
        """Return string representation"""
        return (
            f"Connection({self.name1} <-> {self.name2}, "
            f"capacity={self.max_link_capacity})"
        )
