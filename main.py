from fly_in_parser import parse_file
from parse_error import ParserError
from simulation import Simulation
import sys


def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 main.py <map_file>")
            sys.exit(1)
        graph = parse_file(sys.argv[1])
        sim = Simulation(graph)
        sim.assign_paths()
        sim.loop_turn()
        for line in sim.mov_history:
            print(line)
        print(f"Total turns: {len(sim.mov_history)}")
    except ParserError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
