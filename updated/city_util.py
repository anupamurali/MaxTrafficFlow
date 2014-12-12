import copy
import util
import local_search
import objectives

def compute_flows_acyclic(city, N):
    source = city.source
    prevNodes = [r.node2 for r in city.exit_roads[source]]
    nodeFlows = {source:N}
    while prevNodes:
        succ = []
        for node in prevNodes:
            nodeFlows[node] = 0.0
            for r in city.enter_roads[node]:
                r.flow = nodeFlows.get(r.node1,0.0) * r.probability
                nodeFlows[node] += r.flow
            succ.extend([r.node2 for r in city.exit_roads[node]])
        prevNodes = succ
    return city

def get_all_paths_to_sink(city):
    all_paths = {}
    sink = city.sink
    # Compute all paths for each node.
    # During iteration, path "nodes" are defined by a (node, visited) tuple.
    for start in city.nodes:
        startvisited = frozenset([start])
        # Initialize parents of start "node". Indexed by a (node, visited) tuple.
        # Typically contains the parent path "node", namely a (node, visited) tuple.
        node_parents = {(start, startvisited): None}
        # We haven't found any paths to the sink from this node yet
        all_paths[start.name] = []
        # Initialize the queue to contain the start "node" (defined by
        Q = [(start, startvisited)] # (node, visited (incl. node))
        while Q:
            node, visited = Q.pop()
            if node == sink:
                path_nodes = set([sink])
                parent = node_parents[(node, visited)]
                while parent:
                    path_nodes.add(parent[0].name) # Add the node itself, excluding the "visited"
                    parent = node_parents[parent]
                all_paths[start.name].append(path_nodes)
            for r in city.exit_roads[node]:
                if r.node2 not in visited:
                    newvisited = visited.union(frozenset([r.node2]))
                    Q.append( (r.node2, newvisited) )
                    node_parents[(r.node2, newvisited)] = (node, visited)
    return all_paths

def compute_flows_cyclic(city, N):
    """
    General approach:
        Start from the source. Add all the nodes the source is connected to
        to the list of nodes to visit (prevNodes). Repeat the following steps
        until there are no more nodes to explore:
        For each node we need to visit:
            1) Get all the flows going into this node, differentiated by the paths they took to get there.
            2a) Determine which exit roads can be traversed from this node, adding them to a list.
            2b) For each exit road in the above list, send the appropriate amount of flow down it.
        IMPORTANT: When we use "node" in this function, it refers to the node by name. node_object gives the actual object.
                   We must refer to nodes by name because we want to use ALL_PATHS_TO_SINK, which is keyed by node name.
                   It's keyed this way so that all local search successor cities can still use it even though their
                   node objects are different.
    """
    source_object = city.source
    source = source_object.name
    prevNodes = [r.node2 for r in city.exit_roads[source_object]]
    # Defines all flows leaving a given node. Keyed by node name.
    # Dict of {node: [(destNode, flow, priorPath [incl. this node])] }
    nodeOutFlows = {source: []}

    # Initialize flows leaving source
    for r in city.exit_roads[source_object]:
        nodeOutFlows[source].append((r.node2.name, r.probability * N, frozenset([source])))

    # Keep going until no more nodes are left to explore (all the flow has reached the sink)
    # or we see the same flows again (no more updates)
    flowHasChanged = True
    while prevNodes and flowHasChanged:
        print [n.name for n in prevNodes]
        flowHasChanged = False

        # Set of nodes we have to visit next
        succ = set()
        # Process each node we have left to explore
        for node_object in prevNodes:
            node = node_object.name
            # Define a frozenset so we can union this node into paths later
            node_frozenset = frozenset([node])

            # List of [(srcNode, flow, priorPath [excl. this node])] tuples. Each tuple represents a component
            # of the total flow.
            nodeInFlows = []

            # STEP 1: Get all component flows coming into this node and update the total road flows accordingly
            # Iterate over all roads entering this node
            for enter_road in city.enter_roads[node_object]:
                orig_flow = enter_road.flow
                enter_road.flow = 0
                enter_node = enter_road.node1.name
                # If the entering node has an outgoing flow...
                if enter_node in nodeOutFlows:
                    # Iterate over all flows leaving the entering node
                    for enter_flow_dest, enter_flow, enter_path in nodeOutFlows[enter_node]:
                        # If this flow component is entering this node, add the flow component
                        # to the entering road as well as this node's list of incoming flows.
                        if enter_flow_dest == node:
                            enter_road.flow += enter_flow
                            nodeInFlows.append( (enter_node, enter_flow, enter_path) )
                # If flow changes, must run another iteration
                if orig_flow != enter_road.flow:
                    flowHasChanged = True

            # STEP 2: Propogate incoming component flows to all other nodes
            # Dict of valid exit roads for the flow that came along a given path.
            # {path: [exit_road_1,...,exit_road_k]}
            valid_exit_roads = {}
            # Dict of total probabilities among all exit roads for a given path. Will be useful for re-balancing probabilities
            # when some roads cannot take any flow. Which roads are available depends on the path, and thus the total
            # probability does too.
            # {path: total_prob}
            total_probability = {}

            # STEP 2a: Determine which exit_roads can be traversed

            # Iterate over all flows coming into this node
            for enter_node, enter_flow, enter_path in nodeInFlows:
                valid_exit_roads[enter_path] = []
                total_probability[enter_path] = 0.0
                # Try each road leaving this node to see if it's valid
                for exit_road in city.exit_roads[node_object]:
                    exit_node = exit_road.node2.name
                    # Can't revisit a node already in the path
                    if exit_node not in enter_path:
                        # Can't visit nodes that cannot reach the sink without traversing
                        # nodes already in path
                        for possible_path in util.ALL_PATHS_TO_SINK[exit_node]:
                             if not enter_path.union(node_frozenset).intersection(possible_path):
                                # If all tests pass, update our list of valid exit roads (and total probabilities)
                                # for the flow that arrived via this particular enter_path.
                                total_probability[enter_path] += exit_road.probability
                                valid_exit_roads[enter_path].append(exit_road)
                                break

            # STEP 2b: Update outgoing flows
            nodeOutFlows[node] = []
            # Iterate over all incoming flows
            for inflow_node, inflow_flow, inflow_path in nodeInFlows:
                if node == "2":
                    print node, inflow_path, [r.node2.name for r in valid_exit_roads[inflow_path]]
                # Iterate over all valid exits for this particular incoming flow
                for exit_road in valid_exit_roads[inflow_path]:
                    exit_node_object = exit_road.node2
                    exit_node = exit_node_object.name
                    # Add the node at the other end of this exit to the nodes we must explore
                    succ.add(exit_node_object)
                    # Add this flow to the list of flows leaving this node
                    fullpath = inflow_path.union(node_frozenset)
                    nodeOutFlows[node].append( (exit_node, inflow_flow * exit_road.probability/total_probability[inflow_path], fullpath) )

        # Update the list of nodes we still must explore
        prevNodes = succ



def compute_flows(city, N):
    return compute_flows_cyclic(city,N)

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

def compute_probabilities(city):
    """
    Computes the probabilities for a city based on road distances and structures. Balances automatically.
    """

    sum_of_inverse_distances = 0
    for node in city.nodes:
        # get roads leaving this node
        exit_roads = city.exit_roads[node]
        # sum over 1/d_i
        sum_of_inverse_dists = sum([1.0*road.node2.structure['discount']/(road.distance + city.shortest_dists[road.node2]) for road in exit_roads])
        for exit_road in exit_roads:
            exit_road.probability = (1.0*exit_road.node2.structure['discount']/(road.distance + city.shortest_dists[road.node2])) / sum_of_inverse_dists
    return

def compute_max_profit_congestion(city, searchAlgorithm):
    if searchAlgorithm.name == "Brute Force":
        searchAlgorithm = local_search.BeamSearch()
    def profit(c):
        return objectives.profit_and_congestion(c, "Profit")
    def congestion(c):
        return objectives.profit_and_congestion(c, "Congestion")
    searchAlgorithm = local_search.BeamSearch()
    _, maxProfit = searchAlgorithm.run_algorithm(city, profit)
    _, minCongestion = searchAlgorithm.run_algorithm(city, congestion)

    # Maximimum profit for city over structure placements
    city.max_profit = maxProfit

    # Maximimum profit for city over structure placements        
    city.min_congestion = minCongestion


def export_city_graph(city):
    """
    Exports the graph for the given city.
    """
    pass