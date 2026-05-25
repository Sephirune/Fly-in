from fly_in_parser import parse_file
from parse_error import ParserError
from pathfinding import dijkstra
from pathfinding import find_all_paths
from simulation import Simulation

try:
    graph = parse_file("generated_graph.map")
    print(graph)
    for zone in graph.zones.values():
        print(zone)
    for con in graph.connections:
        print(con)
    paths = find_all_paths(graph, graph.start, graph.end)
    for p in paths:
        print("Path:", p)

    path = dijkstra(graph, graph.start, graph.end)
    print("Path found:", path)

    sim = Simulation(graph)
    sim.assign_paths()
    turns = sim.loop_turn()
    print(f"turns simulated: {turns}")
    print("movement history:", sim.mov_history)
except ParserError as e:
    print(f"Error: {e}")
