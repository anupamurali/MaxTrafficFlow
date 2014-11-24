class City:
	""" City class containing roads, intersections, traffic lights, and bike lanes """

  def __init__(self, nodes, roads):
  	# Vertices of graph (dictionary) maps node to tuple (no_tl, no_tb)
  	# Initialized to (0,0)
    self.nodes = nodes

    # Adjacency list (dictionary) containing nodes mapping to reachable nodes
    # and corresponding edge weights (maximum no of vehicles)
    self.roads = roads

    # Probability you will take edge (u,v) from node u
    # Initialize as uniform distribution 
    self.probabilities = {}
	for u in self.roads:
	  # degree of vertex u
	  n = len(self.roads[u])
	  for v in self.roads[u]
	  	self.probabilities[(u,v)] = float(1/n)

  def update_probabilities(self):
  	""" Given new traffic lights and bike lanes, update probabilities
  	for taking a given edge """
  	pass

