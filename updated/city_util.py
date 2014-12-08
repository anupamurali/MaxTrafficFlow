import copy
import util

def compute_flows(city, N):
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
        all_paths[start] = []
        # Initialize the queue to contain the start "node" (defined by
        Q = [(start, startvisited)] # (node, visited (incl. node))
        while Q:
            node, visited = Q.pop()
            if node == sink:
                path_nodes = set([sink])
                parent = node_parents[(node, visited)]
                while parent:
                    path_nodes.add(parent[0]) # Add the node itself, excluding the "visited"
                    parent = node_parents[parent]
                all_paths[start].append(path_nodes)
            for r in city.exit_roads[node]:
                if r.node2 not in visited:
                    newvisited = visited.union(frozenset([r.node2]))
                    Q.append( (r.node2, newvisited) )
                    node_parents[(r.node2, newvisited)] = (node, visited)
    return all_paths

def compute_flows_cycles(city, N):
    source = city.source
    prevNodes = [r.node2 for r in city.exit_roads[source]]
    nodeInFlows = {source: []} # Dict of { node: [(srcNode, flow, priorPath [excl. this node)] }
    nodeOutFlows = {source: []} # Dict of {node: [(destNode, flow, priorPath [incl. this node])] }

    for r in city.exit_roads[source]:
        nodeOutFlows[source].append((r.node2, r.probability * N, frozenset([source])))

    conseqItersWithNoFlowChange = 0
    while prevNodes and conseqItersWithNoFlowChange <= 1:
        succ = set()
        print [n.name for n in prevNodes]

        flowChanged = False

        for node in prevNodes:
            #print [n.name for n in prevNodes]
            print "Processing node ", node.name
            node_frozenset = frozenset([node])
            nodeInFlows[node] = []

            print "    Step 1"
            # STEP 1: Get all component flows coming into this node and update the total road flows accordingly
            for enter_road in city.enter_roads[node]:
                origFlow = enter_road.flow
                enter_road.flow = 0
                enter_node = enter_road.node1
                if enter_node in nodeOutFlows:
                    for enter_flow_dest, enter_flow, enter_path in nodeOutFlows[enter_node]:
                        if enter_flow_dest == node:
                            enter_road.flow += enter_flow
                            nodeInFlows[node].append( (enter_node, enter_flow, enter_path) )
                if enter_road.flow != origFlow:
                    flowChanged = True
            # STEP 2: Propogate incoming component flows to all other nodes
            valid_exit_roads = {}
            total_probability = {}

            print "    Step 2a"
            # STEP 2a: Determine which exit_roads can be traversed
            for enter_node, enter_flow, enter_path in nodeInFlows[node]:
                valid_exit_roads[enter_path] = []
                total_probability[enter_path] = 0.0
                for exit_road in city.exit_roads[node]:
                    exit_node = exit_road.node2
                    # Can't revisit a node already in the path
                    if exit_node not in enter_path:
                        # Can't visit nodes that cannot reach the sink without traversing
                        # nodes already in path
                        for possible_path in util.ALL_PATHS_TO_SINK[exit_node]:
                             if not enter_path.union(node_frozenset).intersection(possible_path):
                                total_probability[enter_path] += exit_road.probability
                                if node.name=="7":
                                    print "Adding road from ",exit_road.node1.name,"to",exit_road.node2.name,"for enter path",[n.name for n in enter_path]
                                valid_exit_roads[enter_path].append(exit_road)
                                break

            print "    Step 2b"
            # print "    Valid Exits: ", [(r.node1.name, r.node2.name) for r in valid_exit_roads]
            # STEP 2b: Update outgoing flows
            nodeOutFlows[node] = []
            # print "EXIT_ROADS: ",valid_exit_roads
            for inflow_node, inflow_flow, inflow_path in nodeInFlows[node]:
                for exit_road in valid_exit_roads[inflow_path]:
                    exit_node = exit_road.node2
                    succ.add(exit_node)
                    exit_node_frozenset = frozenset([exit_node])
                    fullpath = inflow_path.union(node_frozenset)
                    if node.name == "7":
                        print [f.name for f in fullpath]
                    nodeOutFlows[node].append( (exit_node, inflow_flow * exit_road.probability/total_probability[inflow_path], fullpath) )
            print "    Step 2b done"

            for n, v in nodeOutFlows.iteritems():
                for vv in v:
                    pass#print n.name,"->",vv[0].name,":",vv[1]
            print "     "

        prevNodes = succ
        if not flowChanged:
            conseqItersWithNoFlowChange += 1
        else:
            conseqItersWithNoFlowChange = 0

    for src, flow, prior in nodeInFlows[city.nodes[-1]]:
        print src.name, flow, [n.name for n in prior]

    for dest, flow, prior in nodeOutFlows[city.nodes[5]]:
        print dest.name, flow, [n.name for n in prior]








def compute_flows_old(city, N):
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

def compute_probabilities(city):
    """
    Computes the probabilities for a city based on road distances and structures. Balances automatically.
    """

    sum_of_inverse_distances = 0
    for node in city.nodes:
        # get roads leaving this node
        exit_roads = city.exit_roads[node]
        # sum over 1/d_i
        sum_of_inverse_dists = sum([1.0*road.node2.structure['discount']/road.distance for road in exit_roads])
        for exit_road in exit_roads:
            exit_road.probability = (1.0*exit_road.node2.structure['discount']/exit_road.distance) / sum_of_inverse_dists
    return