from graph import Graph
from zones import Zone, ZoneType
import heapq  # Python library that imports queue priority. This will be used in dijkstra because this algorythm calculates the path with the lesser cost
from typing import Optional


def search_multiple_paths(
    graph: Graph,
    current: str,
    end: str,
    visited: set[str],
    path: list[str],
    all_paths: list[list[str]]
) -> None:
    """Search multiple paths via DFS thanks to K-shortest paths"""
    if current == end:
        all_paths.append(list(path))
        return
    neighborhood = graph.get_neighbors(current)

    for neighbor in neighborhood:
        neighbor_zone = graph.get_zone(neighbor)
        if neighbor not in visited and neighbor_zone is not None and neighbor_zone.zone_type != ZoneType.BLOCKED:
            path.append(neighbor)
            visited.add(neighbor)
            search_multiple_paths(
                    graph,
                    neighbor,
                    end,
                    visited,
                    path,
                    all_paths
                )
            path.pop()
            visited.remove(neighbor)


def find_all_paths(graph: Graph, start: Zone, end: Zone) -> list[list[str]]:
    """Wrapper method to find all the posible paths between start and end"""
    all_paths: list[list[str]] = []
    search_multiple_paths(
        graph,
        start.name,
        end.name,
        {start.name},
        [start.name],
        all_paths
    )
    return all_paths


def dijkstra(graph: Graph, start: Zone, end: Zone) -> list[str]:
    costs = {
        "normal": 1,
        "restricted": 2,
        "priority": 0,
        "blocked": float('inf')  # the algorythm'll never choose this one because this represents infinite
    }
    zone_cost: dict[str, float] = {start.name: 0}
    previous: dict[str, str] = {}
    queue: list[tuple[float, str]] = []

    heapq.heappush(queue, (0, start.name))
    while queue:
        cost, zone = heapq.heappop(queue)  # pops the smallest item from the heap to extract the one with the lesser priority
        if cost > zone_cost.get(zone, float('inf')):
            continue
        if zone == end.name:
            break

        for neighbor in graph.get_neighbors(zone):
            neighbor_zone = graph.get_zone(neighbor)
            new_costs = costs.get(neighbor_zone.zone_type, float('inf'))
            if new_costs == float('inf'):  # blocked zones
                continue

            total_cost = cost + new_costs
            if total_cost < zone_cost.get(neighbor, float('inf')):
                zone_cost[neighbor] = total_cost
                previous[neighbor] = zone
                heapq.heappush(queue, (total_cost, neighbor))  # We push here the item into the queue to add priority and cost

    zone_type: Optional[str] = end.name
    path = []
    while zone_type is not None:
        path.append(zone_type)
        zone_type = previous.get(zone_type)
    path.reverse()

    if path and path[0] == start.name:
        return path
    return []
