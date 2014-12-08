class City:
    def __init__(self, nodes, roads, source, sink):
        """
        Initializes the city and all supplemental data structures

        Args:
            nodes: list of integers representing node ID
            roads: list of integers representing road ID
            source: integer representing ID number of start node
            sink: integer representing ID number of end node
            
        """
        self.nodes = nodes
        self.roads = roads
        self.source = source
        self.sink = sink

        # Dictionary telling which roads enter a given node
        self.enter_roads = {}

        # Dictionary telling which roads leave a given node
        self.exit_roads = {}

        # Dictionary of shortest path distances from each node to the sink
        self.shortest_dists = {}

        # Construct entering and exiting node dictionaries
        self.__populate_enter_exit()

        # Populate the shortest_dists dictionary
        self.__populate_shortest_dists()

    def __populate_enter_exit(self):
        for node in self.nodes:
            self.enter_roads[node] = []
            self.exit_roads[node] = []
            for road in self.roads:
                if road.node1 == node:
                    self.exit_roads[node].append(road)
                elif road.node2 == node:
                    self.enter_roads[node].append(road)

    # helper function for __populate_shortest_dists
    def find_shortest_dist_node(self,Q):
        shortest_dist = float("Inf")
        shortest_dist_node = -1 # garbage ID number
        for node in Q:
            if self.shortest_dists[node] < shortest_dist:
                shortest_dist = self.shortest_dists[node]
                shortest_dist_node = node
        return shortest_dist_node

    # ASSUMPTION: ACYCLIC GRAPH
    def __populate_shortest_dists(self):
        return
        self.shortest_dists[self.sink] = 0
        Q = [self.sink]
        while len(Q) != 0:
            print [n.name for n in Q]
            node = self.find_shortest_dist_node(Q)
            Q.remove(node)
            enter_roads = self.enter_roads
            for enter_road in enter_roads[node]:
                if enter_road.node1 not in Q:
                    Q.append(enter_road.node1)
                if enter_road.node1 not in self.shortest_dists:
                    self.shortest_dists[enter_road.node1] = enter_road.distance + self.shortest_dists[node]
                elif self.shortest_dists[enter_road.node1] > enter_road.distance + self.shortest_dists[node]:
                    self.shortest_dists[enter_road.node1] = enter_road.distance + self.shortest_dists[node]
                    
            
            



            
