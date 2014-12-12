import city
import road
import node
import city_util
import structure
import util
import local_search
import objectives

newCity = util.load_city_from_data("test.city")
city_util.compute_initial_probabilities(newCity)
util.ALL_PATHS_TO_SINK = city_util.get_all_paths_to_sink(newCity)
city_util.compute_flows(newCity, 150)
for r in newCity.roads:
    print (r.node1.name, r.node2.name), ":", r.flow

hillClimb = local_search.BruteForce()
bestCity, bestObj = hillClimb.run_algorithm(newCity,objectives.profit_and_congestion)
print 'obj  = ',bestObj
for n in bestCity.nodes:
    print n.name, n.structure['name']
for r in bestCity.roads:
    print (r.node1.name, r.node2.name), ":", r.flow
quit()



newCity = util.basic_city()
allPaths = city_util.get_all_paths_to_sink(newCity)

for n in newCity.nodes:
    print n.name
    for path in allPaths[n]:
        print "   ", [nd.name for nd in path]

quit()
city_util.compute_initial_probabilities(newCity)

hillClimb = local_search.HillClimbing()
bestCity, _ = hillClimb.run_algorithm(newCity,objectives.profit_and_congestion)
for n in bestCity.nodes:
    print n.name, n.structure['name']

print "PROBS:"
for r in bestCity.roads:
    print (r.node1.name, r.node2.name), ":", r.probability
print "FLOWS"
for r in bestCity.roads:
    print (r.node1.name, r.node2.name), ":", r.flow
quit()

newCity = util.harder_city()
city_util.compute_initial_probabilities(newCity)
print "PROBS:", [r.probability for r in newCity.roads]

city_util.compute_flows(newCity, 150)
for r in newCity.roads:
    print (r.node1.name, r.node2.name), ":", r.flow