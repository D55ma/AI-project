from operator import itemgetter  # Importing itemgetter function from operator module
import operator  # Importing operator module for additional operations

# Function to find the difference between two lists
def diff(li1, li2):
    """
    Returns the difference between two lists.
    """
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]  # Creates a list containing elements that are in li1 or li2 but not in both
    return li_dif

# Function to get allowed colors for a city
def get_allowed_colors(graph, city, colors):
    """
    Returns allowed colors for a given city based on the graph and available colors.
    """
    not_allowed_colors = [city[1] for city in graph[(city, False)] if city[1] != '']  # Extracts colors not allowed for the given city from the graph
    allowed_colors = diff(colors, not_allowed_colors)  # Finds the difference between all colors and not allowed colors
    return allowed_colors

# Degree heuristic: returns the index of the city or cities with maximum neighbors
def degree_heuristic(graph):
    """
    Returns the index of the city or cities with the maximum number of neighbors.
    """
    # Creates a list of tuples containing index and the number of neighbors for each city
    index_neighbour_len = [(index, len(l[1])) for index, l in enumerate(graph.items()) if l[0][1] is False]
    max_neighbour = max(index_neighbour_len, key=itemgetter(1))[1]  # Finds the maximum number of neighbors
    max_index_neighbour_len = [t[0] for t in index_neighbour_len if t[1] == max_neighbour]  # Finds the index of city/cities with maximum neighbors
    cities = [list(graph)[index][0] for index in max_index_neighbour_len]  # Extracts the city/cities with maximum neighbors
    return cities

# Minimum Remaining Values (MRV): returns the city or cities with the fewest remaining colors
def mrv(graph, colors):
    """
    Returns the city or cities with the minimum remaining values/colors.
    """
    # Extracts cities without assigned color from the graph
    cities_without_color = [(city[0]) for city, colored in graph.items() if city[1] is False]
    allowed_color_each_city = {}
    # Calculates allowed colors for each city
    for city in cities_without_color:
        allowed_color_each_city[city] = get_allowed_colors(graph, city, colors)

    # Finds the minimum number of available colors
    min_available_color_len = min([len(allowed_colors) for city, allowed_colors in allowed_color_each_city.items()])
    # Extracts the city or cities with the minimum remaining colors
    cities = [city for city, colors in allowed_color_each_city.items() if len(colors) == min_available_color_len]
    return cities

# Least Constraining Value (LCV): returns the color or colors that have been used the most
def lcv(graph, colors):
    """
    Returns the color or colors which are used most frequently.
    """
    city_color = []
    color_number = {}

    # Collects all used colors
    for neighbours in graph.values():
        [city_color.append(c) for c in neighbours if c[1] != '']

    all_used_colors = list(dict.fromkeys(city_color))

    if not all_used_colors:  # First iteration
        return colors

    # Counts occurrences of each color
    for cc in all_used_colors:
        if cc[1] not in color_number:
            color_number[cc[1]] = 1
        else:
            color_number[cc[1]] += 1

    # Finds the color or colors used most frequently
    number_of_max = max(color_number.items(), key=operator.itemgetter(1))[1]
    colors = [key for (key, value) in color_number.items() if value == number_of_max]

    return colors

# Function to color the selected city
def coloring(graph, city, color):
    """
    Colors the selected city and updates the graph accordingly.
    """
    neighbours = graph[(city, False)]  # Fetches the neighbors of the selected city
    del graph[(city, False)]  # Deletes the entry for the uncolored city
    graph[(city, True)] = neighbours  # Adds the colored city back to the graph with updated color information

    # Updates the color of the selected city in the neighbors' lists
    for nei_list in graph.values():
        for n in nei_list:
            if n[0] == city:
                l = list(n)
                l[1] = color
                t = tuple(l)
                nei_list.remove(n)
                nei_list.append(t)
