import city
import road
import node
import structure

NUMBER_OF_CARS = 5000

def basic_city():
    nodes = [node.Node( structure.NoStructure(),name=str(i) ) for i in xrange(5)]
    cap = 10
    dist = 10
    connections = [(0,1), (1,2), (2,4), (0,3), (3,4), (3,1)]
    roads = [road.Road(cap, dist, nodes[c[0]], nodes[c[1]]) for c in connections]
    newcity = city.City(nodes, roads, nodes[0], nodes[4])
    return newcity