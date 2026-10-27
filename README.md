*This project has been created as part of the 42 curriculum by aarogarc.*

# Fly-in

## Description

Fly-in is a drone routing simulation system. The goal is to move a fleet of drones from a start zone to an end zone through a network of connected zones, minimizing the total number of simulation turns.

The system parses a map file describing the zone network, checks reachability with Dijkstra's algorithm, enumerates all valid paths using DFS, distributes the drones across them by cost, and simulates turn-by-turn drone movement while respecting all capacity and movement constraints.

## Instructions

### Requirements

- Python 3.10 or later
- make

### Installation

```bash
make install
```

This creates a virtual environment in `.venv` and installs all dependencies.

### Running

```bash
make run MAP=<map_file>
```

Example:

```bash
make run MAP=example.map
```

### Debug mode

```bash
make debug MAP=<map_file>
```

### Linting

```bash
make lint
make lint-strict  # optional, stricter mypy checks
```

### Cleanup

```bash
make clean
```

## Map File Format

```
nb_drones: <number>
start_hub: <name> <x> <y> [metadata]
end_hub: <name> <x> <y> [metadata]
hub: <name> <x> <y> [metadata]
connection: <zone1>-<zone2> [metadata]
```

Zone metadata options: `zone=<type>`, `color=<value>`, `max_drones=<number>`

Connection metadata options: `max_link_capacity=<number>`

Zone types: `normal` (1 turn), `restricted` (2 turns), `priority` (1 turn, preferred), `blocked` (inaccessible)

## Algorithm

### Pathfinding

**Dijkstra (`dijkstra`)** — computes the minimum-cost path from start to end with a min-heap priority queue (`heapq`), in O((V + E) log V). Costs come from a single table (`ZONE_COSTS` in `zones.py`) shared with the rest of the project. It is used as a fast feasibility check: if it finds no path, the program stops with a clear error before running the more expensive DFS.

**DFS (`find_all_paths`)** — enumerates all valid paths from start to end using depth-first search with backtracking. Blocked zones are excluded. This gives the full set of routes that drones can be spread across.

### Path Assignment

All paths found by the DFS are sorted by total cost (`path_cost`, based on the same `ZONE_COSTS` table). Drones are then distributed cyclically across them using modulo — cheaper paths are filled first and receive more drones, which avoids sending every drone through a single bottleneck.

If the map has no start/end or no path connects them, `assign_paths` raises a `ParserError` instead of crashing.

### Simulation

The simulation runs turn by turn. Each turn:
- Zone occupancy and connection usage are tracked in dictionaries
- Each drone checks if it can move (`validate_movement`) — respecting `max_drones` per zone and `max_link_capacity` per connection
- Drones that move free up their current zone for others in the same turn
- Start and end zones have no occupancy restrictions
- Restricted zones require 2 turns to enter — the drone occupies the connection during transit and the output shows the connection name instead of the zone name

### Complexity

- Dijkstra: O((V + E) log V)
- DFS path enumeration: exponential in the worst case (it lists every simple path)
- Simulation per turn: O(D * Z) where D = drones, Z = zones

### Caching

Paths are computed once at the start via `assign_paths` and stored in each `Drone` object. No recalculation occurs during simulation.

## Performance Benchmarks

Results obtained on all provided maps:

| Map | Drones | Result | Target |
|-----|--------|--------|--------|
| easy_01 — Linear path | 2 | 3 turns | ≤ 6 |
| easy_02 — Simple fork | 4 | 3 turns | ≤ 6 |
| easy_03 — Basic capacity | 4 | 3 turns | ≤ 8 |
| medium_01 — Dead end trap | 5 | 4 turns | ≤ 15 |
| medium_02 — Circular loop | 6 | 8 turns | ≤ 20 |
| medium_03 — Priority puzzle | 5 | 6 turns | ≤ 12 |
| hard_01 — Maze nightmare | 8 | 8 turns | ≤ 45 |
| hard_02 — Capacity hell | 12 | 7 turns | ≤ 60 |
| hard_03 — Ultimate challenge | 15 | 20 turns | ≤ 35 |
| challenger — The Impossible Dream | 25 | 33 turns | ≤ 45 |

## Visual Representation

Zone names in the simulation output are colorized by type using ANSI escape codes:

| Zone type  | Color  |
|------------|--------|
| normal     | White  |
| priority   | Green  |
| restricted | Yellow |
| blocked    | Red    |

Drone identifiers are displayed in cyan.

Colors are rendered in any ANSI-compatible terminal (Linux, macOS, WSL).

## Resources

- [Python heapq documentation](https://docs.python.org/3/library/heapq.html)
- [Dijkstra's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Depth-first search — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [mypy documentation](https://mypy.readthedocs.io/)

### AI Usage

AI was used for:
- Guidance on algorithm structure (Dijkstra, DFS with backtracking)
- Identifying logic bugs in the simulation turn mechanics
- Code review and suggestions for type annotations
- README structure
