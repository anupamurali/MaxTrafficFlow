import copy
import structure
import city_util
from util import NUMBER_OF_CARS, INFINITY
import random
import math

class LocalSearchAlgorithm:
    def run_algorithm(self, city, objective):
        # Given a city, it returns the most optimal city it could find using the objective provided as well as the objective value.
        raise Exception("Undefined!")
        return city

    def get_successors(self, city, objective, width=INFINITY):
        successors = []
        for i in xrange(len(city.nodes)):
            other_structures = [s for s in structure.ALL_STRUCTURES if s != city.nodes[i].structure]
            for other in other_structures:
                new_city = copy.deepcopy(city)
                new_city.nodes[i].structure = other
                city_util.compute_probabilities(new_city)
                city_util.compute_flows(new_city, NUMBER_OF_CARS)
                successors.append((new_city,objective(new_city)))
        # Sort according to objective score
        successors.sort(key=lambda x: x[1][0], reverse = True)
        # Return best successors
        if width <= len(successors):
            return successors[:width]
        else:
            return successors

class BruteForce:
    def __init__(self):
        self.name = "Brute Force"

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
        self.name = "Hill Climbing"
        self.max_no_improvement = 30 # Max num iterations w/out improvement before the algorithm terminates

    def run_algorithm(self, city, objective):
        same_count = 0
        curr_best_city, curr_best_score = (city, objective(city))
        city_util.compute_probabilities(city)
        city_util.compute_flows(city,NUMBER_OF_CARS)
        while same_count <= self.max_no_improvement:
            # Get all successors
            successors = self.get_successors(curr_best_city, objective, 1)
            best_city, best_score = successors[0]
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

class SimulatedAnnealing(LocalSearchAlgorithm):
    def __init__(self):
        self.name = "Simulated Annealing"
        self.tmax = 50 # Max num iterations before algorithm terminates   

    # Calculates probability of accepting successor city as next to explore
    def accept_prob(self, curr_best_score, successor_score, temperature):
        s = successor_score[0]
        c = curr_best_score[0]
        if c <= s:
            return 1
        else:
            return math.exp((s-c)/temperature)

    def run_algorithm(self, city, objective):
        curr_best_city, curr_best_score = (city, objective(city))
        city_util.compute_probabilities(city)
        city_util.compute_flows(city, NUMBER_OF_CARS)
        t = 0
        while t < self.tmax:
            temperature = (self.tmax - t) / float(self.tmax)
            successor_city, successor_score = random.choice(self.get_successors(curr_best_city, objective))
            if self.accept_prob(curr_best_score, successor_score, temperature) > random.random():
                curr_best_city = successor_city
                curr_best_score = successor_score
            t += 1
        return curr_best_city, curr_best_score


class BeamSearch(LocalSearchAlgorithm):
    def __init__(self):
        self.name = "Beam Search"
        self.memory = 6
        self.max_no_improvement = 3


    def run_algorithm(self, city, objective):
        # Get 'memory' best successors
        city_util.compute_probabilities(city)
        city_util.compute_flows(city, NUMBER_OF_CARS)
        successors = self.get_successors(city, objective, self.memory)
        best_city, best_score = city, objective(city)

        # Keep track of how much best score changes
        same_count = 0

        # If static for too long, exit
        while(same_count <= self.max_no_improvement):
            # Successor is sorted, so curr_city is best city in successors
            curr_city, score = successors.pop(0)
            if score[0] <= best_score[0]:
                same_count += 1
            else:
                same_count = 0 
                best_score = score
                best_city = curr_city
            # Successors of current city
            curr_successors = self.get_successors(curr_city, objective, self.memory)
            for c in curr_successors:
                successors.append(c)
            successors.sort(key=lambda x: x[1][0], reverse = True)
            successors = successors[:self.memory]
            
        return best_city, best_score

    def get_successors(self, city, objective, width):
        successors = []
        for i in xrange(len(city.nodes)):
            other_structures = [s for s in structure.ALL_STRUCTURES if s != city.nodes[i].structure]
            for other in other_structures:
                new_city = copy.deepcopy(city)
                new_city.nodes[i].structure = other
                city_util.compute_probabilities(new_city)
                city_util.compute_flows(new_city, NUMBER_OF_CARS)
                successors.append((new_city,objective(new_city)))
        # Sort according to objective score
        successors.sort(key=lambda x: x[1][0], reverse = True)
        # Return best successors
        if width <= len(successors):
            return successors[:width]
        else:
            return successors


