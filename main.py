import sys  # Importing the sys module for system-specific parameters and functions
from pprint import pprint  # Importing the pprint module for pretty-printing data structures
from build_graph import build_graph  # Importing the build_graph function from the build_graph module
from map_coloring_utils import mrv, degree_heuristic, lcv, get_allowed_colors, coloring  # Importing various utility functions for map coloring
import time  # Importing the time module for time-related functions

if __name__ == "__main__":
    # List of map files to process
    map_files = ['map2.txt', 'map3.txt', 'map4.txt']
    # List of colors available for coloring the maps
    colors = ['RED', 'GREEN', 'BLUE']
    startTime = time.time()  # Record the start time of the program execution
    
    # Iterate over each map file
    for map_file in map_files:
        # Print the header for each map
        if map_file == "map2.txt":
            print("------------------------Australia’s map------------------------")
        elif map_file == "map3.txt":
            print("------------------------Canada’s map------------------------")
        elif map_file == "map4.txt":
            print("------------------------Middle East’s map------------------------")
        else:
            print(f"------------------------{map_file} map ------------------------")

        # Build graph from the map file
        graph = build_graph(map_file)

        # Loop through all cities in the graph
        for _ in range(len(graph)):
            # Apply various heuristics to select the next city to color
            cities_with_max_degree = degree_heuristic(graph)
            cities_with_minimum_remaining_colors = mrv(graph, colors)
            much_used_colors = lcv(graph, colors)

            # Find common cities based on different heuristics
            common_cities = set(cities_with_max_degree).intersection(set(cities_with_minimum_remaining_colors))

            # Select a city to color
            if common_cities:
                selected_city = common_cities.pop()
            else:
                selected_city = cities_with_max_degree[0]  # Select any city from cities_with_max_degree

            # Get allowed colors for the selected city
            colors_of_selected_city = get_allowed_colors(graph, selected_city, colors)

            # Choose a color for the selected city
            common_color = set(much_used_colors).intersection(set(colors_of_selected_city))
            try:
                if common_color:
                    color = common_color.pop()
                else:
                    color = colors_of_selected_city.pop()

                coloring(graph, selected_city, color)  # Color the selected city
            except IndexError:
                sys.exit("Something went wrong. Perhaps there is not enough color for this map")  # Exit if there are not enough colors for the map
            print(selected_city, color)  # Print the city and its color
        
        # Add "Any Color" for cities with no neighbors
        alone_cities = [graph[city].append("Any Color") for city, neighbours in graph.items() if len(neighbours) == 0]
        
        # Print the computational time taken to color the map
        print("Computational time:", time.time() - startTime, "s")
