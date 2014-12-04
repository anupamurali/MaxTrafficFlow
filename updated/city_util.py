import copy

def compute_flows(city, N):
    """
    Computes the traffic flow through each road in the city based on the probabilities.

    Params:
        city = A City object
        N    = The number of cars flowing.

    Returns:
        The city object with the new flows.
    """
    return

def balance_probabilities(city):
    """
    Balances the probabilities for all roads in a city to ensure that
    they sum to 1.

    Params:
        city = A City object.

    Returns:
        A city object with the new flows
    """
    city = copy.deepcopy(city)

    for node in city.nodes:
        exit_roads = city.exit_roads[node]
        total_prob = sum(road.probability for road in exit_roads)
        for road in exit_roads:
            road.probability = road.probability / total_prob

    return city

def compute_initial_probabilities(city):
    """
    Computes the initial probabilities for a city based on road distances.

    Suppose roads 0,...,n-1 are sorted in increasing order of distance.
    P(take road i) = dist(road[n - i]) / total_dist

    ANOTHER IDEA: Base road distances on the distance of the shortest path from that node to the sink (more realistic, not hard to do)
    """
    city = copy.deepcopy(city)

##    # Iterate over all city nodes and compute probabilities
##    for node in city.nodes:
##        # Get roads leaving this node
##        exit_roads = city.exit_roads[node]
##        # Sort roads in increasing order for probability computation
##        sorted_exit_roads = sorted([road for road in exit_roads], key=lambda x: x.distance)
##        total_dist = sum([road.distance for road in exit_roads])
##        num_roads = len(exit_roads)
##
##        # Compute probabilities
##        for i in xrange(0,num_roads):
##            sorted_exit_roads[i].probability = sorted_exit_roads[num_roads - i - 1].distance / total_dist
##    return city

    sum_of_inverse_distances = 0
    for node in city.nodes:
        # get roads leaving this node
        exit_roads = city.exit_roads[node]
        sum_of_inverse_dists = 0
        for exit_road in exit_roads:
            sum_of_inverse_dists += 1/exit_road.distance
        for exit_road in exit_roads:
            exit_road.probability = (1/exit_road.distance) / sum_of_inverse_dists
    return city

