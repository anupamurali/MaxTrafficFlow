import structure

def profit_and_congestion(argcity):
    # Returns the objective value of a given city with flows. ALso returns a dictionary of the
    # individual components of it (ex {"profit": 200, "congestion": 1000}
    count = 0
    for node in argcity.nodes:
        if node.structure.__class__ == structure.TollBooth:
            count += 1
    return count, {}
