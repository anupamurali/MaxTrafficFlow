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

    city = copy.deepcopy(city)
    source = city.source

    # Contains nodes from previous timestep
    prevNodes = [source]

    # Dictionary with incoming flows into nodes
    nodeFlows = {}
    nodeFlows[source] = N

    # If prevNodes is empty, we have no more nodes with exit roads to update
    while len(prevNodes) > 0:
        succNodes = []
        for node in prevNodes:
            exit_roads = city.exit_roads[node]
            for road in exit_roads:
                succ = road.node2
                road.flow += float(nodeFlows[node])*road.probability
                if succ not in nodeFlows:
                    nodeFlows[succ] = float(nodeFlows[node])*road.probability
                else:
                    nodeFlows[succ] += float(nodeFlows[node])*road.probability
                succNodes.append(succ)
        prevNodes = succNodes

    return city

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

    sum_of_inverse_distances = 0
    for node in city.nodes:
        # get roads leaving this node
        exit_roads = city.exit_roads[node]
        # sum over 1/d_i
        sum_of_inverse_dists = sum([1/road.distance for road in exit_roads])
        for exit_road in exit_roads:
            exit_road.probability = (1/exit_road.distance) / sum_of_inverse_dists
    return city

