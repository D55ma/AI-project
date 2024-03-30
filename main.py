import sys
from pprint import pprint
from build_graph import build_graph
from map_coloring_utils import mrv, degree_heuristic, lcv, get_allowed_colors, coloring
import time
if __name__ == "__main__":
    
    map_files = ['map2.txt', 'map3.txt', 'map4.txt']
    colors = ['RED', 'GREEN','BLUE']
    startTime=time.time()
    
    for map_file in map_files:
        if map_file == "map2.txt":
            print("------------------------Australia’s map------------------------")
        elif map_file == "map3.txt":
            print("------------------------Canada’s map------------------------")
        elif map_file == "map4.txt":
            print("------------------------Middle East’s map------------------------")
        else:
            print(f"------------------------{map_file} map ------------------------")
        # Build graph from file
        graph = build_graph(map_file)

        for _ in range(len(graph)):
            cities_with_max_degree = degree_heuristic(graph)
            cities_with_minimum_remaining_colors = mrv(graph, colors)
            much_used_colors = lcv(graph, colors)

            common_cities = set(cities_with_max_degree).intersection(set(cities_with_minimum_remaining_colors))

            if common_cities:
                selected_city = common_cities.pop()
            else:
                selected_city = cities_with_max_degree[0]  # Select any city from cities_with_max_degree
                
                
            # Get allowed color for selected city
            colors_of_selected_city = get_allowed_colors(graph, selected_city, colors)

            # Final chosen color
            common_color = set(much_used_colors).intersection(set(colors_of_selected_city))

            try:
                if common_color:
                    color = common_color.pop()
                else:
                    color = colors_of_selected_city.pop()

                coloring(graph, selected_city, color)
            except IndexError:
                sys.exit("Something went wrong. Perhaps there is not enough color for this map")
            print(selected_city, color)

        alone_cities = [graph[city].append("Any Color") for city, neighbours in graph.items() if len(neighbours) == 0]
        
        # print(graph)
        print("Computational time:", time.time()-startTime,"s")
