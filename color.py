from zones import Zone


class Colors:
    """ANSI color codes for the output."""

    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"

    @staticmethod
    def colorize(text: str, color: str) -> str:
        """Wrap text with a color code and reset."""
        return f"{color}{text}{Colors.RESET}"

    @staticmethod
    def color_output(zone: Zone) -> str:
        """Colorize a zone name based on its type."""
        zone_types: dict[str, str] = {
            "normal": Colors.WHITE,
            "priority": Colors.GREEN,
            "restricted": Colors.YELLOW,
            "blocked": Colors.RED,
        }
        color = zone_types.get(zone.zone_type, Colors.WHITE)
        return Colors.colorize(zone.name, color)

    @staticmethod
    def drone_color(drone_id: str) -> str:
        """Colorize a drone identifier."""
        return Colors.colorize(drone_id, Colors.CYAN)
