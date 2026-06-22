from graph import Graph
from zones import Zone
import heapq
from typing import Optional


def search_multiple_paths(
    graph: Graph,
    current: str,
    end: str,
    visited: set[str],
    path: list[str],
    all_paths: list[list[str]]
) -> None:
    """Search multiple paths via DFS with backtracking.

    Args:
        graph: The drone network graph.
        current: Current zone name being explored.
        end: Target zone name.
        visited: Set of already visited zone names.
        path: Current path being built.
        all_paths: List to collect all found paths.
    """
    if current == end:
        all_paths.append(list(path))
        return
    neighborhood = graph.get_neighbors(current)

    for neighbor in neighborhood:
        neighbor_zone = graph.get_zone(neighbor)
        if (neighbor not in visited
                and neighbor_zone is not None
                and neighbor_zone.zone_type != "blocked"):
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
    """Find all valid paths from start to end using DFS.

    Args:
        graph: The drone network graph.
        start: The starting zone.
        end: The ending zone.

    Returns:
        List of all valid paths as lists of zone names.
    """
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
    """Find the shortest path using Dijkstra's algorithm.

    Args:
        graph: The drone network graph.
        start: The starting zone.
        end: The ending zone.

    Returns:
        List of zone names representing the shortest path, or empty list.
    """
    costs: dict[str, float] = {
        "normal": 1,
        "restricted": 2,
        "priority": 0,
        "blocked": float('inf'),
    }
    zone_cost: dict[str, float] = {start.name: 0}
    previous: dict[str, str] = {}
    queue: list[tuple[float, str]] = []

    heapq.heappush(queue, (0, start.name))
    while queue:
        cost, zone = heapq.heappop(queue)
        if cost > zone_cost.get(zone, float('inf')):
            continue
        if zone == end.name:
            break

        for neighbor in graph.get_neighbors(zone):
            neighbor_zone = graph.get_zone(neighbor)
            if neighbor_zone is None:
                continue
            move_cost = costs.get(neighbor_zone.zone_type, float('inf'))
            if move_cost == float('inf'):
                continue

            total_cost = cost + move_cost
            if total_cost < zone_cost.get(neighbor, float('inf')):
                zone_cost[neighbor] = total_cost
                previous[neighbor] = zone
                heapq.heappush(queue, (total_cost, neighbor))

    current: Optional[str] = end.name
    path: list[str] = []
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()

    if path and path[0] == start.name:
        return path
    return []
