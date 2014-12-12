import structure
import city

def profit_and_congestion(argcity, optFor = "Profit"):
    # Returns the objective value of a given city with flows. ALso returns a dictionary of the
    # individual components of it (ex {"profit": 200, "congestion": 1000}
    totalProfit = 0
    totalCongestion = 0
    for n in argcity.nodes:
        totalProfit += -n.structure['cost'] + sum([r.flow * n.structure['revenue'] for r in argcity.enter_roads[n]])
    for r in argcity.roads:
        totalCongestion += max(r.flow - r.capacity, 0.0)
    if optFor == "Profit":
    	return (totalProfit), {"profit": totalProfit, "congestion": totalCongestion}
    elif optFor == "Congestion":
    	return (-totalCongestion), {"profit": totalProfit, "congestion": totalCongestion}


def final_objective(argcity):
	maxProfit = argcity.max_profit
	maxCongestion = argcity.max_congestion

	totalProfit = 0.0
	totalCongestion = 0.0
	for n in argcity.nodes:
		totalProfit += -n.structure['cost'] + sum([r.flow * n.structure['revenue'] for r in argcity.enter_roads[n]])
	for r in argcity.roads:
		totalCongestion += max(r.flow - r.capacity, 0.0)
	return float(totalProfit)/maxProfit[0] + 100000*float(totalCongestion)/maxCongestion[0], 
