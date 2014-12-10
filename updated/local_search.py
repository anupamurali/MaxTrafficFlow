import copy
import structure
import city_util
from util import NUMBER_OF_CARS
import random

class LocalSearchAlgorithm:
    def run_algorithm(self, city, objective):
        # Given a city, it returns the most optimal city it could find using the objective provided as well as the objective value.
        raise Exception("Undefined!")
        return city

class BruteForce:
    def get_structure_combinations(self,city):
        """
        For a city of length n, each node containing k possible structures, obtain
        all k^n possible cities with all combinations of structures

        Params:
            city = City object

        Returns:
            cities = List of cities with all possible structure combinations
        """
        n = len(city.nodes)
        allStructures = structure.ALL_STRUCTURES
        prevComb = [[i] for i in allStructures]
        # Build up list of permutations
        for i in xrange(n):
            new = []
            for struct in allStructures:
                for combo in prevComb:
                    newCombo = copy.deepcopy(combo)
                    newCombo.append(struct)
                    new.append(newCombo)
            # Can discard previous layer
            prevComb = new

        # Return list of cities with structures
        cities = []
        for comb in prevComb:
            newCity = copy.deepcopy(city)
            for i in xrange(n):
                newCity.nodes[i].structure = comb[i]
            city_util.compute_probabilities(newCity)
            city_util.compute_flows(newCity,NUMBER_OF_CARS)
            cities.append(newCity)

        return cities

    def run_algorithm(self, city, objective):
        allCombinations = self.get_structure_combinations(city)      
        best_score = -1000000
        best_objective = (best_score,{})
        for c in allCombinations:
            obj = objective(c)
            if obj[0] > best_score:
                best_city = c
                best_objective = obj
                best_score = best_objective[0]
        return best_city, best_objective


class HillClimbing(LocalSearchAlgorithm):
    def __init__(self):
        self.max_no_improvement = 30 # Max num iterations w/out improvement before the algorithm terminates

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
                print "HC OBJECTIVE:", objective(successor)
                # Add (successor, objective value) pair to list of evaluated successors
                evaluations.append( (successor, objective(successor) ) )
            # Pick the best one
            evaluations.sort(key=lambda x: x[1], reverse=True)
            best_city, best_score = evaluations[0]
            # Allow Local Search to transition between different solutions with same objective
            if best_score[0] >= curr_best_score[0]:
                curr_best_city = best_city
                curr_best_score = best_score
            # Only allow it to do this a certain number of times
            if best_score[0] > curr_best_score[0]:
                same_count = 0
            else:
                same_count += 1

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

class SimulatedAnnealing(LocalSearchAlgorithm):
    def __init__(self):
        self.tmax = 200 # Max num iterations before algorithm terminates   

    # calculates probability of accepting successor city as next to explore
    def accept_prob(self, curr_best_score, successor_score, temperature):
        #print curr_best_score
        #print successor_score
        s = successor_score[0]
        c = curr_best_score[0]
        if s >= c:
            return 1
        else:
            return s / c * temperature

    def run_algorithm(self, city, objective):
        curr_best_city, curr_best_score = (city, objective(city))
        city_util.compute_probabilities(city)
        city_util.compute_flows(city, NUMBER_OF_CARS)
        t = 0
        while t < self.tmax:
            temperature = (self.tmax - t) / float(self.tmax)
            successor_city = random.choice(self.get_successors(curr_best_city))
            city_util.compute_probabilities(successor_city)
            city_util.compute_flows(successor_city, NUMBER_OF_CARS)
            successor_score = objective(successor_city)
            print "SA OBJECTIVE:", successor_score
            if self.accept_prob(curr_best_score, successor_score, temperature) > random.random():
                curr_best_city = successor_city
                curr_best_score = successor_score
            t += 1
        return curr_best_city, curr_best_score

    def get_successors(self, city):
        successors = []
        for i in xrange(len(city.nodes)):
            other_structures = [s for s in structure.ALL_STRUCTURES if s != city.nodes[i].structure]
            for other in other_structures:
                new_city = copy.deepcopy(city)
                new_city.nodes[i].stucture = other
                successors.append(new_city)
        return successors
