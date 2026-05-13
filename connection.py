from typing import Optional
from zones import Zone


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

    def valid_name(self, zone: Zone) -> bool:
        """Bool to check if the connection is valid"""
        return zone == self.name1 or zone == self.name2

    def __repr__(self) -> str:
        """Return string representation"""
        return(
            f"Connection({self.name1} <-> {self.name2}, "
            f"capacity={self.max_link_capacity})"
        )