import city
import road
import node
import structure
import city_util
import json

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

def load_city_from_data(citydata_file):
    with open(citydata_file) as f:
        all_nodes = json.load(f)
    nodes = {}
    roads = []
    max_road_dist = max([dist for _, data in all_nodes.iteritems() for _, dist in data["edges"]])
    for id in all_nodes.keys():
        nodes[id] = node.Node(structure.NoStructure, name=id)
    for id, data in all_nodes.iteritems():
        for dest, dist in data["edges"]:
            # Default road capacity is to hold 25% of all cars at once on the longest road, and fewer on other roads.
            cap = dist/max_road_dist * NUMBER_OF_CARS * 0.25
            roads.append(road.Road(cap, dist, nodes[id], nodes[dest]))
    src = nodes["s"]
    sink = nodes["t"]
    nodes = [n for _, n in nodes.iteritems()]
    nodes.sort(key=lambda n: n.name)
    newcity = city.City(nodes, roads, src, sink)
    return newcity
