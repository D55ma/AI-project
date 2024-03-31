def build_graph(map):
    # Initialize an empty dictionary to represent the graph
    # Key: (X, Bool). X represents city AND Bool represents whether the city is colored or not
    # Value: List of tuples containing neighbors of the city. Each tuple contains (X, ''), where X is the neighbor city and '' represents no color assigned yet
    graph = {}

    # Open the map file in read mode
    with open(map, 'r') as cities_file:
        # Read all lines from the file
        cities = cities_file.readlines()
        # Remove leading and trailing whitespaces, and remove empty lines
        cities = [city.strip('\n').replace(" ", "") for city in cities if len(city.strip('\n').replace(" ", "")) != 0]

    # Iterate over each line in the map file
    for city_neighbours in cities:
        # Split the line into city name and its neighbors
        city, neighbours = city_neighbours.split(":")
        # Remove unnecessary characters and split neighbors into a list
        neighbours = neighbours.replace("[", "").replace("]", "").replace("\n", "").split(",")

        # Convert format of neighbors from [X, Y] to [('X', ''), ('Y', '')]
        neighbours = [(neighbour, '') for neighbour in neighbours if neighbour != '']
        # Add the city and its neighbors to the graph with no color assigned yet (False)
        graph[(city, False)] = neighbours

    # Return the graph
    return graph
