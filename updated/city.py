import objectives
import local_search

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

        self.max_profit = 0
        self.min_congestion = 0

        # Construct entering and exiting node dictionaries
        self.__populate_enter_exit()

        # Populate the shortest_dists dictionary
        self.__populate_shortest_dists()


    def __populate_enter_exit(self):
        for n in self.nodes:
            self.enter_roads[n] = []
            self.exit_roads[n] = []
            for r in self.roads:
                if r.node1 == n:
                    self.exit_roads[n].append(r)
                elif r.node2 == n:
                    self.enter_roads[n].append(r)

    # Helper function for __populate_shortest_dists
    def find_shortest_dist_node(self,Q):
        shortest_dist = float("Inf")
        shortest_dist_node = -1 # garbage ID number
        for n in Q:
            if self.shortest_dists[n] < shortest_dist:
                shortest_dist = self.shortest_dists[n]
                shortest_dist_node = n
        return shortest_dist_node

    # ASSUMPTION: ACYCLIC GRAPH
    def __populate_shortest_dists(self):
        done = []
        self.shortest_dists[self.sink] = 0.0
        Q = [self.sink]
        while len(Q) > 0:
            n = self.find_shortest_dist_node(Q)
            Q.remove(n)
            done.append(n)
            enter_roads = self.enter_roads
            for enter_road in enter_roads[n]:
                if enter_road.node1 not in Q and enter_road.node1 not in done:
                    Q.append(enter_road.node1)
                if enter_road.node1 not in self.shortest_dists:
                    self.shortest_dists[enter_road.node1] = enter_road.distance + self.shortest_dists[n]
                elif self.shortest_dists[enter_road.node1] > enter_road.distance + self.shortest_dists[n]:
                    self.shortest_dists[enter_road.node1] = enter_road.distance + self.shortest_dists[n]
                    
            
    



            
