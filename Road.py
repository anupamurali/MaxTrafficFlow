import Node

  class Road:
  """ Class for roads in city. Road is defined by two nodes, a city, traversal probability,
  maximum vehicle flow, and whether there is a bike lane """

    def __init__(self, node1, node2, maxFlow, bl = 0):
  	  self.node1 = node1
  	  self.node2 = node2
   	  self.max_flow = max_flow
  	  self.city = node1.city
  	  self.probability = float(1/Node.degree(node1))