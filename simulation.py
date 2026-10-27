from drone import Drone
from graph import Graph
from pathfinding import find_all_paths, dijkstra
from color import Colors
from parse_error import ParserError
from zones import ZONE_COSTS


class Simulation:
    """Manages the turn-by-turn drone routing simulation."""

    def __init__(self, graph: Graph) -> None:
        """Initialize the Simulation."""
        self.graph = graph
        self.drones: list[Drone] = []
        self.current_turn: int = 0
        self.mov_history: list[str] = []

    @staticmethod
    def path_cost(graph: Graph, path: list[str]) -> float:
        """Calculate the total movement cost of a path."""
        total_cost: float = 0
        for zone_name in path[1:]:
            zone = graph.get_zone(zone_name)
            if zone is not None:
                total_cost += ZONE_COSTS.get(zone.zone_type, 1)
        return total_cost

    def assign_paths(self) -> None:
        """Assign paths to all drones, prioritizing lower cost routes.

        Raises:
            ParserError: If the graph has no start/end or no valid path
                connects them.
        """
        start = self.graph.start
        end = self.graph.end
        if start is None or end is None:
            raise ParserError("graph has no start or end zone.")

        if not dijkstra(self.graph, start, end):
            raise ParserError("no valid path from start to end.")

        all_paths = find_all_paths(self.graph, start, end)
        sorted_paths = sorted(
            all_paths,
            key=lambda p: self.path_cost(self.graph, p)
        )
        for i in range(self.graph.nb_drones):
            path = sorted_paths[i % len(sorted_paths)]
            drone = Drone(path_assigned=path, identifier=f"D{i + 1}")
            self.drones.append(drone)

    def validate_movement(
        self,
        drone: Drone,
        zone_occupancy: dict[str, int],
        connection_usage: dict[tuple[str, str], int]
    ) -> bool:
        """Check if a drone can move to its next zone."""
        next_zone_name = drone.get_next_zone
        if next_zone_name is None:
            return False

        next_zone = self.graph.get_zone(next_zone_name)
        if next_zone is None:
            return False

        if not next_zone.is_end:
            if zone_occupancy.get(next_zone_name, 0) >= next_zone.max_drones:
                return False

        connection = self.graph.get_connection(
            drone.current_zone, next_zone_name
        )
        if connection is None:
            return False

        max_cap: int = connection.max_link_capacity if (
            connection.max_link_capacity is not None
        ) else 1
        connection_key: tuple[str, str] = (
            min(drone.current_zone, next_zone_name),
            max(drone.current_zone, next_zone_name)
        )
        if connection_usage.get(connection_key, 0) >= max_cap:
            return False

        return True

    def simulate_turn(self) -> list[str]:
        """Execute one simulation turn."""
        movements: list[str] = []
        zone_occupancy: dict[str, int] = {
            zone_name: sum(
                1 for d in self.drones
                if d.current_zone == zone_name
                and not d.has_ended
                and not self.graph.zones[zone_name].is_start
            )
            for zone_name in self.graph.zones
        }
        connection_usage: dict[tuple[str, str], int] = {}

        for drone in self.drones:
            if drone.has_ended:
                continue
            if self.validate_movement(drone, zone_occupancy, connection_usage):
                current_zone_name = drone.current_zone
                next_zone_name = drone.get_next_zone
                if next_zone_name is None:
                    continue

                next_zone = self.graph.get_zone(next_zone_name)
                next_is_restricted = (
                    next_zone is not None and next_zone.zone_type ==
                    "restricted"
                )
                drone.move_drone(next_is_restricted=next_is_restricted)

                drone_str = Colors.drone_color(drone.identifier)
                if drone.in_transit:
                    conn_name = (
                        f"{min(current_zone_name, next_zone_name)}"
                        f"_{max(current_zone_name, next_zone_name)}"
                    )
                    movements.append(f"{drone_str}-{conn_name}")
                else:
                    current_zone = self.graph.get_zone(drone.current_zone)
                    if current_zone is not None:
                        zone_str = Colors.color_output(current_zone)
                        movements.append(f"{drone_str}-{zone_str}")

        self.current_turn += 1
        if movements:
            self.mov_history.append(" ".join(movements))
        return movements

    def loop_turn(self) -> int:
        """Run turns until all drones have arrived."""
        max_turns = len(self.drones) * len(self.graph.zones) * 10
        while any(not drone.has_ended for drone in self.drones):
            self.simulate_turn()
            if self.current_turn > max_turns:
                break
        return len(self.mov_history)
