class ZoneType:
    """Valid types for zone class"""
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone:
    """Class that represents a zone in the drone pathing network"""
    def __init__(
            self,
            name: str,
            x: int,
            y: int,
            zone_type: ZoneType = ZoneType.NORMAL,
            color: Optional[str] = None,
            max_drones: int = 1,
            is_start: bool = False,
            is_end: bool = False,
    ) -> None:
        """Init the zone parameters"""
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
        self.is_start = is_start
        self.is_end = is_end
