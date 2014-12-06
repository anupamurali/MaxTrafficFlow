class Node:
    def __init__(self, structure,name=None):
        # Indicates which structure is on it (ex. NoStructure, Shopping Center, Toll Booth, etc.)
        self.structure = structure
        self.name = name