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

    def __populate_shortest_dists(self):
        pass
