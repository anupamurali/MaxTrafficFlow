import copy
import structure
import city_util
from util import NUMBER_OF_CARS

class LocalSearchAlgorithm:
    def run_algorithm(self, city, objective):
        # Given a city, it returns the most optimal city it could find using the objective provided as well as the objective value.
        raise Exception("Undefined!")
        return city

class HillClimbing(LocalSearchAlgorithm):
    def __init__(self):
        self.max_no_improvement = 30 # Max # of iterations w/out improvement before the algorithm terminates

    def run_algorithm(self, city, objective):
        same_count = 0
        curr_best_city, curr_best_score = (city, objective(city))
        city_util.compute_probabilities(city)
        city_util.compute_flows(city,NUMBER_OF_CARS)
        while same_count <= self.max_no_improvement:
            # Get all successors
            successors = self.get_successors(curr_best_city)
            # Evaluate each one
            evaluations = []
            for successor in successors:
                city_util.compute_probabilities(successor)
                city_util.compute_flows(successor, NUMBER_OF_CARS)
                # Add (successor, objective value) pair to list of evaluated successors
                evaluations.append( (successor, objective(successor) ) )
            # Pick the best one
            evaluations.sort(key=lambda x: x[1], reverse=True)
            best_city, best_score = evaluations[0]
            if best_score[0] > curr_best_score[0]:
                curr_best_city = best_city
                curr_best_score = best_score
                same_count = 0
            else:
                same_count += 1
            print same_count, curr_best_city, curr_best_score
        return curr_best_city, curr_best_score

    def get_successors(self, city):
        # Returns a list of successor cities, each of which differs by 1 change from the original
        successors = []
        # Go over every node
        for i in xrange(len(city.nodes)):
            other_structures = [s for s in structure.ALL_STRUCTURES if s != city.nodes[i].structure]
            # Go over every possible structure we can change it to
            for other in other_structures:
                # Create a new city to change one node in
                new_city = copy.deepcopy(city)
                new_city.nodes[i].structure = other
                # Add this new city to the successors
                successors.append(new_city)
        return successors





