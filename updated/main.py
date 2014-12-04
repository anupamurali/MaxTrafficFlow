import city
import road
import node
import city_util
import structure
import util
import local_search

newCity = util.basic_city()

hillClimb = local_search.HillClimbing()
hillClimb.run_algorithm(newCity,objectives.Profit)