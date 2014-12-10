import city
import road
import node
import city_util
import structure
import util
import local_search
import objectives
import time

newCity = util.harder_city_with_cycle()
city_util.compute_initial_probabilities(newCity)
util.ALL_PATHS_TO_SINK = city_util.get_all_paths_to_sink(newCity)
city_util.compute_flows(newCity, 150)
for r in newCity.roads:
    print (r.node1.name, r.node2.name), ":", r.flow

starttime = time.time()
bruteForce = local_search.BruteForce()
for _ in xrange(1):
    bestCity, bestObj = bruteForce.run_algorithm(newCity,objectives.profit_and_congestion)
bruteForceTime = time.time() - starttime

starttime = time.time()
hillClimb = local_search.HillClimbing()
for _ in xrange(1):
    bestCityHill, bestObjHill = hillClimb.run_algorithm(newCity,objectives.profit_and_congestion)
hillClimbTime = time.time() - starttime

starttime = time.time()
simulatedAnnealing = local_search.SimulatedAnnealing()
for _ in xrange(1):
    bestCityAnneal, bestObjAnneal = simulatedAnnealing.run_algorithm(newCity,objectives.profit_and_congestion)
simAnnealTime = time.time() - starttime

print 'BRUTE FORCE: ',bestObj[0]
print '    TIME: ', bruteForceTime

hillClimb = local_search.BruteForce()
bestCity, bestObj = hillClimb.run_algorithm(newCity,objectives.profit_and_congestion)
print 'obj  = ',bestObj

for n in bestCity.nodes:
    print n.name, n.structure['name']
for r in bestCity.roads:
    print (r.node1.name, r.node2.name), ":", r.flow
    
print 'HILL CLIMB: ',bestObjHill[0]
print '    TIME:', hillClimbTime
for n in bestCityHill.nodes:
    print n.name, n.structure['name']
for r in bestCityHill.roads:
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


print 'SIMULATED ANNEALING: ',bestObjAnneal[0]
print '    TIME:', simAnnealTime
for n in bestCityAnneal.nodes:
    print n.name, n.structure['name']
for r in bestCityAnneal.roads:
    print (r.node1.name, r.node2.name), ":", r.flow
    
print "OBJECTIVE DIFFERENCE (brute - hill): ",bestObj[0] - bestObjHill[0]
print "TIME DIFFERENCE (brute - hill): ", bruteForceTime - hillClimbTime
quit()



##newCity = util.basic_city()
##allPaths = city_util.get_all_paths_to_sink(newCity)
##
##for n in newCity.nodes:
##    print n.name
##    for path in allPaths[n]:
##        print "   ", [nd.name for nd in path]
##
##quit()
##city_util.compute_initial_probabilities(newCity)
##
##hillClimb = local_search.HillClimbing()
##bestCity, _ = hillClimb.run_algorithm(newCity,objectives.profit_and_congestion)
##for n in bestCity.nodes:
##    print n.name, n.structure['name']
##
##print "PROBS:"
##for r in bestCity.roads:
##    print (r.node1.name, r.node2.name), ":", r.probability
##print "FLOWS"
##for r in bestCity.roads:
##    print (r.node1.name, r.node2.name), ":", r.flow
##quit()
##
##newCity = util.harder_city()
##city_util.compute_initial_probabilities(newCity)
##print "PROBS:", [r.probability for r in newCity.roads]
##
##city_util.compute_flows(newCity, 150)
##for r in newCity.roads:
##    print (r.node1.name, r.node2.name), ":", r.flow
