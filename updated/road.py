class Road:
    def __init__(self, probability, capacity, distance):
        self.probability = probability
        self.capacity = capacity
        self.distance = distance
        self.flow = 0 # To be filled by Flow Algorithm