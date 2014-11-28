class ObjectiveFunction:
    def evaluate(self, city):
        # Returns the objective value of a given city with flows. ALso returns a dictionary of the
        # individual components of it (ex {"profit": 200, "congestion": 1000}
        raise Exception("Implement the objective function!")

class ProfitAndCongestion(ObjectiveFunction):
    def evaluate(self, city):
        return 0.0, {}