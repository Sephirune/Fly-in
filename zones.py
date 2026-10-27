from typing import Optional


class ZoneType:
    """Valid types for zone class."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


ZONE_COSTS: dict[str, float] = {
    ZoneType.NORMAL: 1,
    ZoneType.RESTRICTED: 2,
    ZoneType.PRIORITY: 1,
    ZoneType.BLOCKED: float("inf"),
}


class Zone:
    """Class that represents a zone in the drone pathing network."""

    def __init__(
            self,
            name: str,
            x: int,
            y: int,
            zone_type: str = ZoneType.NORMAL,
            color: Optional[str] = None,
            max_drones: int = 1,
            is_start: bool = False,
            is_end: bool = False,
    ) -> None:
        """Initialize a Zone."""
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
        self.is_start = is_start
        self.is_end = is_end

    def __repr__(self) -> str:
        """Return string representation of Zone."""
        return (
            f"Zone(name={self.name}, type={self.zone_type}, "
            f"pos=({self.x},{self.y}), max_drones={self.max_drones})"
        )
