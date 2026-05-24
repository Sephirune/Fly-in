from typing import Optional


class Drone:
    def __init__(
            self,
            path_assigned: list[str],
            identifier: str
            ):
        self.path_index = 0
        self.path_assigned = path_assigned
        self.has_ended = False
        self.identifier = identifier

    @property
    def current_zone(self) -> str:
        """Return the current zone name"""
        return self.path_assigned[self.path_index]

    @property
    def get_next_zone(self) -> Optional[str]:
        """Gets the name of the next zone"""
        if self.path_index + 1 < len(self.path_assigned):
            return self.path_assigned[self.path_index + 1]
        return None

    def move_drone(self) -> None:
        """Move the drone one step in its path"""
        if not self.has_ended and self.get_next_zone is not None:
            self.path_index += 1

        if self.path_index == len(self.path_assigned) - 1:
            self.has_ended = True
