class Road:
    def __init__(self, capacity, distance, node1, node2, probability=None):
        self.probability = probability
        self.capacity = capacity
        self.distance = distance
        self.node1 = node1 # node the road leaves from
        self.node2 = node2 # node the road goes to
        self.flow = 0 # To be filled by Flow Algorithm
