import city
import road
import node
import city_util
import structure
import util
import local_search
import objectives

newCity = util.harder_city()
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