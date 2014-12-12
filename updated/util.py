import city
import road
import node
import structure
import city_util

NUMBER_OF_CARS = 150
INFINITY = 999999999
ALL_PATHS_TO_SINK = None

def basic_city():
    nodes = [node.Node( structure.NoStructure,name=str(i) ) for i in xrange(5)]
    cap = 10
    dist = 10
    connections = [(0,1), (1,2), (2,4), (0,3), (3,4), (3,1)]
    roads = [road.Road(cap, dist, nodes[c[0]], nodes[c[1]]) for c in connections]
    newcity = city.City(nodes, roads, nodes[0], nodes[4])
    ALL_PATHS_TO_SINK = city_util.get_all_paths_to_sink(newcity)
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
    ALL_PATHS_TO_SINK = city_util.get_all_paths_to_sink(newcity)
    return newcity

def simple_city_with_cycle():
    nodes = [node.Node( structure.NoStructure,name=str(i) ) for i in xrange(6)]
    cap = 10
    dist = 10
    connections = [(0,1), (1,2), (2,3), (3,4), (3,5)]
    special_dists = {}
    roads = [road.Road(cap, special_dists.get((c[0], c[1]), dist), nodes[c[0]], nodes[c[1]]) for c in connections]
    newcity = city.City(nodes, roads, nodes[0], nodes[-1])
    ALL_PATHS_TO_SINK = city_util.get_all_paths_to_sink(newcity)
    return newcity

def harder_city_with_cycle():
    nodes = [node.Node( structure.NoStructure,name=str(i) ) for i in xrange(8)]
    cap = 10
    dist = 10
    connections = [(0,1),(0,2),(0,3),(1,2),(2,3),(1,6),(2,5),(5,2),(3,4),(4,5),(6,5),(5,7)]
    special_dists = {}
    roads = [road.Road(cap, special_dists.get((c[0], c[1]), dist), nodes[c[0]], nodes[c[1]]) for c in connections]
    newcity = city.City(nodes, roads, nodes[0], nodes[-1])
    print "Computing all paths"
    ALL_PATHS_TO_SINK = city_util.get_all_paths_to_sink(newcity)
    print "Done!"
    return newcity

def another_city():
    nodes = [node.Node(structure.NoStructure,name=str(i)) for i in xrange(11)]
    cap = 40
    dist = 40
    connections = [(0,1),(0,2),(1,2),(2,1),(0,3),(3,6),(2,5),(2,6),(1,4),(4,5),(4,9),(5,8),(5,1),(5,9),(6,2),(6,7),(6,8),(7,10),(8,9),(8,10),(9,10)]
    special_dists = {}
    special_dists = {(3,6): 15, (1,4): 50, (5,8): 30, (1,2): 30}
    roads = [road.Road(cap, special_dists.get((c[0], c[1]), dist), nodes[c[0]], nodes[c[1]]) for c in connections]
    newcity = city.City(nodes, roads, nodes[0], nodes[-1])
    ALL_PATHS_TO_SINK = city_util.get_all_paths_to_sink(newcity)
    return newcity
