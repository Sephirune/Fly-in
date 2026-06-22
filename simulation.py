from drone import Drone
from graph import Graph
from pathfinding import find_all_paths
from color import Colors
from zones import Zone


class Simulation:
    """Manages the turn-by-turn drone routing simulation."""

    def __init__(self, graph: Graph) -> None:
        """Initialize the Simulation.

        Args:
            graph: The drone network graph.
        """
        self.graph = graph
        self.drones: list[Drone] = []
        self.current_turn: int = 0
        self.mov_history: list[str] = []

    @staticmethod
    def path_cost(graph: Graph, path: list[str]) -> float:
        """Calculate the total movement cost of a path.

        Args:
            graph: The drone network graph.
            path: List of zone names representing the path.

        Returns:
            Total movement cost as a float.
        """
        costs: dict[str, float] = {
            "normal": 1,
            "restricted": 2,
            "priority": 1,
            "blocked": float('inf'),
        }
        total_cost: float = 0
        for zone_name in path[1:]:
            zone = graph.get_zone(zone_name)
            if zone is not None:
                total_cost += costs.get(zone.zone_type, 1)
        return total_cost

    def assign_paths(self) -> None:
        """Assign paths to all drones, prioritizing lower cost routes."""
        all_paths = find_all_paths(
            self.graph,
            self.graph.start,  # type: ignore[arg-type]
            self.graph.end  # type: ignore[arg-type]
        )
        sorted_costs = sorted(
            all_paths,
            key=lambda p: self.path_cost(self.graph, p)
        )
        for i in range(self.graph.nb_drones):
            path = sorted_costs[i % len(sorted_costs)]
            drone = Drone(path_assigned=path, identifier=f"D{i + 1}")
            self.drones.append(drone)

    def validate_movement(
        self,
        drone: Drone,
        zone_occupancy: dict[str, int],
        connection_usage: dict[tuple[str, str], int]
    ) -> bool:
        """Check if a drone can move to its next zone.

        Args:
            drone: The drone to check.
            zone_occupancy: Current drone count per zone.
            connection_usage: Current drone count per connection.

        Returns:
            True if the drone can move, False otherwise.
        """
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
        """Execute one simulation turn.

        Returns:
            List of movement strings for this turn.
        """
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

                connection_key: tuple[str, str] = (
                    min(current_zone_name, next_zone_name),
                    max(current_zone_name, next_zone_name)
                )
                drone.move_drone()

                drone_str = Colors.drone_color(drone.identifier)
                current_zone: Zone | None = self.graph.get_zone(
                    drone.current_zone
                )
                if current_zone is not None:
                    zone_str = Colors.color_output(current_zone)
                    movements.append(f"{drone_str}-{zone_str}")

                zone_occupancy[current_zone_name] -= 1
                zone_occupancy[drone.current_zone] = (
                    zone_occupancy.get(drone.current_zone, 0) + 1
                )
                connection_usage[connection_key] = (
                    connection_usage.get(connection_key, 0) + 1
                )

        self.current_turn += 1
        if movements:
            self.mov_history.append(" ".join(movements))
        return movements

    def loop_turn(self) -> int:
        """Run turns until all drones have arrived.

        Returns:
            Total number of turns with movements.
        """
        max_turns = len(self.drones) * len(self.graph.zones) * 10
        while any(not drone.has_ended for drone in self.drones):
            self.simulate_turn()
            if self.current_turn > max_turns:
                break
        return len(self.mov_history)
