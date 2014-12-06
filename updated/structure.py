class Structure:
    """
    Defines a Structure. Structures can be placed on Nodes.
    """
    def __init__(self):
        pass

class NoStructure(Structure):
    """
    This structure does nothing.
    """
    def __init__(self):
        self.cost = 0 # Cost to place
        self.revenue = 0 # Revenue per passing car
        self.discount = 1.0 # Factor by which probability changes

class ShoppingCenter(Structure):
    """
    Increases the probability that someone visits it
    """
    def __init__(self):
        self.cost = 1000
        self.revenue = 0.10
        self.discount = 1.50


class TollBooth(Structure):
    """
    Decreases the probability that someone visits it
    """
    def __init__(self):
        self.cost = 200
        self.revenue = 0.25
        self.discount = 0.80

# A list of all available structures
ALL_STRUCTURES = [NoStructure, TollBooth]