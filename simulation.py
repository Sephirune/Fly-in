from drone import Drone
from graph import Graph
from pathfinding import find_all_paths, dijkstra


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

    def validate_movement(self, drone: Drone) -> bool:
        """Check if a drone can move to the next zone"""
        if drone.get_next_zone is not None:
            zone_name = drone.get_next_zone
            next_zone = self.graph.get_zone(zone_name)

            drones_in_zone = 0
            for i in self.drones:
                if i.current_zone == next_zone:
                    drones_in_zone += 1
                if drones_in_zone >= next_zone.max_drones:
                    return False

            connection = self.graph.get_connection(drone.current_zone, zone_name)
            if connection is not None:
                drones_flying = 0
                for j in self.drones:
                    if j.current_zone == drone.current_zone and j.get_next_zone == next_zone:
                        drones_flying += 1
                    if drones_flying >= connection.max_link_capacity:
                        return False

            return True

    def simulate_turn(self) -> str:
        """Simulates a turn"""
        movements = {}