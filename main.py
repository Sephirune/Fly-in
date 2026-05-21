from fly_in_parser import parse_file
from parse_error import ParserError
from pathfinding import dijkstra
from pathfinding import find_all_paths

try:
    graph = parse_file("example.map")
    print(graph)
    for zone in graph.zones.values():
        print(zone)
    for conn in graph.connections:
        print(conn)
    paths = find_all_paths(graph, graph.start, graph.end)
    for p in paths:
        print("Path:", p)

    path = dijkstra(graph, graph.start, graph.end)
    print("Path found:", path)
except ParserError as e:
    print(f"Error: {e}")
