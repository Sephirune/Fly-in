from typing import Optional
from zones import Zone


class Connection:
    def __init__(
        self,
        name1: str,
        name2: str,
        max_link_capacity: Optional[int] = 1
    ) -> None:
        self.zone1 = name1
        self.zone2 = name2
        self.max_link_capacity = max_link_capacity

        def valid_name(self, zone: Zone) -> bool:
            """Bool to check if the connection is valid"""
            return zone == self.zone1 or zone == self.zone2

        def return_other_zone(self, zone1: )