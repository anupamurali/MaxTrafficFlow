import structure
import city
import math

EPSILON = 0.00000001

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

def cost(argcity):
    totalCost = 0
    for n in argcity.nodes:
        totalCost += n.structure['cost']
    return totalCost,

def opt_revenue(argcity):
    totalRevenue = 0
    for n in argcity.nodes:
        totalRevenue += n.structure['revenue']
    return totalRevenue,

def final_objective(argcity):
    maxProfit = argcity.max_profit
    minCongestion = argcity.min_congestion


    totalProfit = 0.0
    totalCongestion = 0.0
    for n in argcity.nodes:
        totalProfit += -n.structure['cost'] + sum([r.flow * n.structure['revenue'] for r in argcity.enter_roads[n]])
    for r in argcity.roads:
        totalCongestion += max(r.flow - r.capacity, 0.0)
    #print totalProfit, maxProfit[0], 'cost = ', maxCost[0], totalCongestion, maxCongestion[0]
    print 'profit = ',abs(totalProfit - maxProfit[0])
    print 'congestion = ',abs(totalCongestion + minCongestion[0])
    details = {}
    details["diff_profit"] = abs(totalProfit - maxProfit[0])
    details["diff_congestion"] = abs(totalProfit - maxProfit[0])
    details["norm_profit"] = abs((totalProfit - maxProfit[0])/(maxProfit[0]+ EPSILON))
    details["norm_congestion"] = abs((totalCongestion + minCongestion[0])/(minCongestion[0] + EPSILON))
    return -(abs((totalProfit - maxProfit[0])/(maxProfit[0]+ EPSILON)) + abs((totalCongestion + minCongestion[0])/(minCongestion[0] + EPSILON))), details


