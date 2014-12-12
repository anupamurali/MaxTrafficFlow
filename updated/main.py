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

starttime = time.time()
beamSearch = local_search.BeamSearch()
for _ in xrange(1):
    bestCityBeam, bestObjBeam = beamSearch.run_algorithm(newCity,objectives.profit_and_congestion)
beamSearchTime = time.time() - starttime


print 'BRUTE FORCE: ',bestObj[0]
print '    TIME: ', bruteForceTime

bruteForce = local_search.BruteForce()
bestCity, bestObj = bruteForce.run_algorithm(newCity,objectives.profit_and_congestion)
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

print "BEAM SEARCH: ", bestObjBeam[0]
print '    TIME: ', beamSearchTime
for n in bestCityBeam.nodes:
    print n.name, n.structure['name']
for r in bestCityBeam.roads:
    print (r.node1.name, r.node2.name), ":", r.flow

print 'SIMULATED ANNEALING: ',bestObjAnneal[0]
print '    TIME:', simAnnealTime
for n in bestCityAnneal.nodes:
    print n.name, n.structure['name']
for r in bestCityAnneal.roads:
    print (r.node1.name, r.node2.name), ":", r.flow


print "OBJECTIVE DIFFERENCE (brute - hill): ",bestObj[0] - bestObjHill[0]
print "TIME DIFFERENCE (brute - hill): ", bruteForceTime - hillClimbTime

print "OBJECTIVE DIFFERENCE (brute - beam): ",bestObj[0] - bestObjBeam[0]
print "TIME DIFFERENCE (brute - beam): ", bruteForceTime - beamSearchTime

print "OBJECTIVE DIFFERENCE (hill - beam): ",bestObjHill[0] - bestObjBeam[0]
print "TIME DIFFERENCE (hill - beam): ", hillClimbTime - beamSearchTime

print "OBJECTIVE DIFFERENCE (brute - anneal): ",bestObj[0] - bestObjAnneal[0]
print "TIME DIFFERENCE (brute - anneal): ", bruteForceTime - simAnnealTime






    
