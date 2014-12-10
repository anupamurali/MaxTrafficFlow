import structure

def profit_and_congestion(argcity):
    # Returns the objective value of a given city with flows. ALso returns a dictionary of the
    # individual components of it (ex {"profit": 200, "congestion": 1000}
    totalProfit = 0
    totalCongestion = 0
    for node in argcity.nodes:
        totalProfit += -node.structure['cost'] + sum([r.flow * node.structure['revenue'] for r in argcity.enter_roads[node]])
    for r in argcity.roads:
        totalCongestion += max(r.flow - r.capacity, 0.0)
    return (totalProfit), {"profit": totalProfit, "congestion": totalCongestion}
