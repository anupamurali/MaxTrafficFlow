import city
import road
import node
import city_util
import structure
import util
import local_search
import objectives

newCity = util.basic_city()

hillClimb = local_search.HillClimbing()
bestCity, _ = hillClimb.run_algorithm(newCity,objectives.profit_and_congestion)
print [n.structure for n in bestCity.nodes]