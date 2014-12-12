import city
import road
import node
import city_util
import structure
import util
import local_search
import objectives
import time


newCity = util.another_city()
city_util.compute_initial_probabilities(newCity)
util.ALL_PATHS_TO_SINK = city_util.get_all_paths_to_sink(newCity)
city_util.compute_flows(newCity, 150)


for r in newCity.roads:
    print (r.node1.name, r.node2.name), ":", r.flow

"""
TESTING FOR BRUTE FORCE
"""
starttime = time.time()
bruteForce = local_search.BruteForce()
city_util.compute_max_profit_congestion(newCity, bruteForce)
for _ in xrange(1):
    bestCity, bestObj = bruteForce.run_algorithm(newCity,objectives.final_objective)
bruteForceTime = time.time() - starttime
for r in newCity.roads:
    print r.node1.name, r.node2.name, r.probability
print " "
for r in bestCity.roads:
    print r.node1.name, r.node2.name, r.probability
print "THERE ARE ",len(newCity.roads), "ROADS"
print "THERE ARE ", len(bestCity.roads), "ROADS"

"""
TESTING FOR HILL CLIMBING
"""
starttime = time.time()
hillClimb = local_search.HillClimbing()
for _ in xrange(1):
    bestCityHill, bestObjHill = hillClimb.run_algorithm(newCity,objectives.final_objective)
hillClimbTime = time.time() - starttime

"""
TESTING FOR SIMULATED ANNEALING
"""
starttime = time.time()
simulatedAnnealing = local_search.SimulatedAnnealing()
city_util.compute_max_profit_congestion(newCity, simulatedAnnealing)
for _ in xrange(1):
    bestCityAnneal, bestObjAnneal = simulatedAnnealing.run_algorithm(newCity,objectives.final_objective)
simAnnealTime = time.time() - starttime

"""
TESTING FOR BEAM SEARCH
"""
starttime = time.time()
beamSearch = local_search.BeamSearch()
city_util.compute_max_profit_congestion(newCity, beamSearch)
for _ in xrange(1):
    bestCityBeam, bestObjBeam = beamSearch.run_algorithm(newCity,objectives.final_objective)
beamSearchTime = time.time() - starttime


print 'BRUTE FORCE: ',bestObj[0]
print '    TIME: ', bruteForceTime

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






    
