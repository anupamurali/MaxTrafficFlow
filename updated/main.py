import city
import road
import node
import city_util
import structure
import util
import local_search
import objectives

# newCity = util.basic_city()

# hillClimb = local_search.HillClimbing()
# bestCity, _ = hillClimb.run_algorithm(newCity,objectives.profit_and_congestion)
# print [n.structure for n in bestCity.nodes]

newCity = util.basic_city()
city_util.compute_initial_probabilities(newCity)
print [r.probability for r in newCity.roads]

updatedCity = city_util.compute_flows(newCity, 100)
print [r.flow for r in updatedCity.roads]