import city
import road
import node
import structure

NUMBER_OF_CARS = 150

def basic_city():
    nodes = [node.Node( structure.NoStructure,name=str(i) ) for i in xrange(5)]
    cap = 10
    dist = 10
    connections = [(0,1), (1,2), (2,4), (0,3), (3,4), (3,1)]
    roads = [road.Road(cap, dist, nodes[c[0]], nodes[c[1]]) for c in connections]
    newcity = city.City(nodes, roads, nodes[0], nodes[4])
    return newcity

def harder_city():
    nodes = [node.Node( structure.NoStructure,name=str(i) ) for i in xrange(8)]
    cap = 10
    dist = 10
    connections = [(0,1),(0,3),(0,5),
                   (1,2),(3,4),(3,2),(5,3), (5,4), (2,4),
                   (4,6),(4,7),(6,7)]
    special_dists = {(3,2): 15, (3,4): 5}
    roads = [road.Road(cap, special_dists.get((c[0], c[1]), dist), nodes[c[0]], nodes[c[1]]) for c in connections]
    newcity = city.City(nodes, roads, nodes[0], nodes[-1])
    return newcity