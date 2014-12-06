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
    # Flow is (totalFlow, flowThatHasntLeftYet)
    nodeFlows = {}
    nodeFlows[source] = (N, N)

    # If prevNodes is empty, we have no more nodes with exit roads to update

    # CURRENT ALGORITHM IS WRONG. Next time, try to recompute based on flow of
    # entering roads each time
    while len(prevNodes) > 0:
        print 'prevNodes = ', [nodeFlows[n] for n in prevNodes]
        print 'prevNames = ', [n.name for n in prevNodes]
        print 'road flows = ', [r.flow for r in city.roads]
        succNodes = []
        for node in prevNodes:
            exit_roads = city.exit_roads[node]
            flowGone = 0
            for r in exit_roads:
                succ = r.node2
                if node in nodeFlows:
                    r.flow += float(nodeFlows[node][1])*r.probability
                    if succ not in nodeFlows:
                        nodeFlows[succ] = (float(nodeFlows[node][1])*r.probability,float(nodeFlows[node][1])*r.probability)
                    else:
                        addFlow = float(nodeFlows[node][1])*r.probability
                        nodeFlows[succ] = (nodeFlows[succ][0] + addFlow, nodeFlows[succ][1] + addFlow)
                        flowGone += float(nodeFlows[node][1])*r.probability      
                succNodes.append(succ)
            nodeFlows[node] = (nodeFlows[node][0], nodeFlows[node][1] - flowGone)
        # Set new layer for next timestep
        prevNodes = succNodes

    print nodeFlows    

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

    sum_of_inverse_distances = 0
    for node in city.nodes:
        # get roads leaving this node
        exit_roads = city.exit_roads[node]
        # sum over 1/d_i
        sum_of_inverse_dists = sum([1.0/road.distance for road in exit_roads])
        for exit_road in exit_roads:
            exit_road.probability = (1.0/exit_road.distance) / sum_of_inverse_dists
    return

