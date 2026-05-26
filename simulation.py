from drone import Drone
from graph import Graph
from pathfinding import find_all_paths, dijkstra
from color import Colors

class Simulation:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.drones: list[Drone] = []
        self.current_turn: int = 0
        self.mov_history: list[str] = []

    @staticmethod
    def path_cost(graph: Graph, path: list[str]) -> float:
        """Calculates total cost of a path"""
        costs = {
            "normal": 1,
            "restricted": 2,
            "priority": 1,
            "blocked": float('inf')
            }
        total_cost: float = 0

        for i in path[1:]:
            zone = graph.get_zone(i)
            if zone is not None:
                total_cost += costs.get(zone.zone_type, 1)

        return total_cost

    def assign_paths(self) -> None:
        all_paths = find_all_paths(self.graph, self.graph.start, self.graph.end)
        sorted_costs = sorted(all_paths, key=lambda p: self.path_cost(self.graph, p))
        for i in range(self.graph.nb_drones):
            path_len = i % len(sorted_costs)
            path = sorted_costs[path_len]
            drone = Drone(path_assigned=path, identifier=f"D{i + 1}")
            self.drones.append(drone)

    def validate_movement(
        self,
        drone: Drone,
        zone_occupancy: dict[str, int],
        connection_usage: dict[tuple[str, str], int]
    ) -> bool:
        """Check if a drone can move to the next zone"""
        next_zone_name = drone.get_next_zone
        if next_zone_name is None:
            return False

        next_zone = self.graph.get_zone(next_zone_name)
        if next_zone is None:
            return False

        if not next_zone.is_end:
            if zone_occupancy.get(next_zone_name, 0) >= next_zone.max_drones:
                return False

        if zone_occupancy.get(next_zone_name, 0) >= next_zone.max_drones:
            return False

        connection = self.graph.get_connection(drone.current_zone, next_zone_name)
        if connection is None:
            return False

        connection_key = tuple(sorted([drone.current_zone, next_zone_name]))
        if connection_usage.get(connection_key, 0) >= connection.max_link_capacity:
            return False

        return True

    def simulate_turn(self) -> list:
        """Simulates a turn"""
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
                current_zone = drone.current_zone
                next_zone = drone.get_next_zone
                connection_key = tuple(sorted([current_zone, next_zone]))
                drone.move_drone()

                drone_str = Colors.drone_color(drone.identifier)
                zone_str = Colors.color_output(self.graph.get_zone(drone.current_zone))
                movements.append(f"{drone_str}-{zone_str}")

                zone_occupancy[current_zone] -= 1
                zone_occupancy[drone.current_zone] = zone_occupancy.get(drone.current_zone, 0) + 1
                connection_usage[connection_key] = connection_usage.get(connection_key, 0) + 1

        self.current_turn += 1
        self.mov_history.append(" ".join(movements))
        return movements

    def loop_turn(self) -> int:
        """Runs turns in a loop until all drones have arrived"""
        while any(not drone.has_ended for drone in self.drones):
            movements = self.simulate_turn()
            if not movements:
                break

        return self.current_turn
