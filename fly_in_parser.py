from zones import Zone
from graph import Graph
from connection import Connection
from parse_error import ParserError


def pase_drone(line: str, number: int) -> int:
    """Parse the nb of drones"""
    parsed = line.strip()
    if not parsed.startswith("nb_drones"):
        raise ParserError(f"Invalid line format in line: {number}. Input must be 'nb_drones:', gor '{parsed}'")
    try:
        value = int(parsed.split(":", 1)[1].strip())
    except ValueError:
        raise ParserError(f"Line {number}: nb_drones must be a positive integer")
    if value <= 0:
        raise ParserError(f"Line {number}: nb_drones must be a positive integer")
    return value


def parse_metadata(metadata: str, number: int) -> dict[str, str]:
    """Parse metadata input"""
    meta: dict[str, str] = {}
    data = metadata.strip("[]").strip()
    try:
        for i in data.split():
            if '=' in i:
                j, k = i.split("=", 1)
                meta[j.strip()] = k.strip()
    except Exception:
        raise ParserError(f"Invalid metadata input '{metadata}' in line: {number}")
    return meta


def parse_zone(line: str, number: int) -> Zone:
    """Parse zone line and return Zone object"""
    parsed = line.strip()
    if ":" not in parsed:
        raise ParserError(f"Line {number} missing ':'")
    zone_type, zone_info = parsed.split(":", 1)
    zone_type = zone_type.strip()
    zone_info = zone_info.strip()

    if zone_type not in ("hub", "start_hub", "end_hub"):
        raise ParserError("Invalid zone input")

    metadata: dict[str, str] = {}
    if "[" in zone_info:
        if "]" not in zone_info:
            raise ParserError(f"Invalid metadata input in line: {number}")
        start = zone_info.index("[") # index() returns the first ocurrence of an element
        meta_info = zone_info[start:]
        zone_info = zone_info[:start].strip()
        metadata = parse_metadata(meta_info, number)

    parameters = zone_info.split()
    name, xstr, ystr = parameters
    if "-" in name or " " in name:
        raise ParserError("Error: zone names can't contain dashes or spaces.")

    if len(parameters) != 3:
        raise ParserError("Invalid parameters. Format must be: name (x) (y)")

    try:
        x = int(xstr)
        y = int(ystr)
    except ValueError:
        raise ParserError("(x) and (y) parameters must be integers.")

    color = metadata.get("color", None)
    drones_number = metadata.get("max_drones", "1")
    try:
        max_drones = int(drones_number)
    except ValueError:
        raise ParserError("Error. max_drones must be an integer.")
    if max_drones <= 0:
        raise ParserError("Error. max_drones must be a positive integer.")

    zone_type_str = metadata.get("zone", "normal")

    return Zone(
        name=name,
        x=x,
        y=y,
        zone_type=zone_type_str,
        color=color,
        max_drones=max_drones,
        is_start=(zone_type == "start_hub"),
        is_end=(zone_type == "end_hub")
        )


def parse_connection(line: str, number: int, graph: Graph) -> None:
    """Parse a connection line and add it to the graph."""
    parsed = line.strip()
    if ":" not in parsed:
        raise ParserError(f"Line {number}: missing ':' in connection definition")
    connection_type, connection_info = parsed.split(":", 1)
    connection_type = connection_type.strip()
    connection_info = connection_info.strip()

    if connection_type != "connection":
        raise ParserError("Invalid zone input")

    metadata: dict[str, str] = {}
    if "[" in connection_info:
        if "]" not in connection_info:
            raise ParserError(f"Invalid metadata input in line: {number}")
        start = connection_info.index("[")
        meta_info = connection_info[start:]
        connection_info = connection_info[:start].strip()
        metadata = parse_metadata(meta_info, number)

    parameters = connection_info.split("-")
    name1, name2 = parameters[0].strip(), parameters[1].strip()
    if len(parameters) != 2:
        raise ParserError(f"Error. Line: {number} must have exactly two zones.")

    if graph.get_zone(name1) is None:
        raise ParserError(f"Error: line: {number} is an unkown zone.")
    if graph.get_zone(name2) is None:
        raise ParserError(f"Error: line: {number} is an unkown zone.")

    try:
        max_link_capacity = int(metadata.get("max_link_capacity", "1"))
    except ParserError:
        raise ParserError(f"Error: line {number} must be a positive integer.")
    if max_link_capacity <= 0:
        raise ParserError(f"Error: line {number} must be a positive integer.")

    graph.add_connection(Connection(
        name1=name1,
        name2=name2,
        max_link_capacity=max_link_capacity,
    ))


def parse_file(file: str) -> Graph:
    """Parse input file and return a Graph object."""
    try:
        with open(file, "r") as f:
            lines = f.readlines()
    except OSError:
        raise ParserError(f"Error opening file '{file}'.")

    if not lines:
        raise ParserError("Error: File is empty.")

    graph = Graph(pase_drone(lines[0], 1))

    for number, line in enumerate(lines[1:], start=2):
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith(("hub:", "start_hub:", "end_hub:")):
            zone = parse_zone(stripped, number)
            graph.add_zone(zone)

        elif stripped.startswith("connection:"):
            parse_connection(stripped, number, graph)

        else:
            raise ParserError(
                f"Line {number}: unrecognized line '{stripped}'"
            )

    graph.validate()
    return graph
