from fly_in_parser import parse_file
from parse_error import ParserError

try:
    graph = parse_file("example.map")
    print(graph)
    for zone in graph.zones.values():
        print(zone)
    for conn in graph.connections:
        print(conn)
except ParserError as e:
    print(f"Error: {e}")
