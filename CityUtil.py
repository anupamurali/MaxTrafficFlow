"""
G is a city graph. Edges are roads in the city, nodes are intersections and
traffic lights. The following are some functions to be used on G. 

G is an adjacency matrix.
"""

"""
BFS for Ford Fulkerson algorithm
"""
def bfs(G,start):
    Q = []
    Q.append([start])
    while len(Q) > 0:
        path = Q.pop(0)
        u = path[-1]
        if u[0] in westIndices:
            return getEdges(path)
        for v in G[u]:
            newPath = list(path)
        if v not in newPath:
        newPath.append(v)
            Q.append(newPath)
    return []


"""
Ford Fulkerson algorithm on city graph. Use to find the maximum traffic flow through G.
"""
def FF(G,start):
    final = 0
    f = {}
    c = {}
    for i in allEdges:
        (u,v) = i
        f[i] = 0
        f[(v,u)] = 0
	if (u[0] != v[0]):
		c[i] = flights[(u[0],v[0])][0]
	else:
		c[i] = float('inf')
        path = bfs(g,start)
    while path and (path != []):
        d = {}
	for i in allEdges:
	    d[i] = c[i] - f[i] 
        pathD = {}
        for i in path:
            pathD[i] = d[i]
        m = min(pathD,key=pathD.get)
        final += pathD[m]
        for i in path:
            (u,v) = i
            f[i] += d[m]
            f[(v,u)] -= d[m]
            
        # Find residual graph
        for i in allEdges:
	    if (c[i] - f[i] <= 0):
		    if i[1] in g[i[0]]:
                g[i[0]].remove(i[1])
        path = bfs(g,start)
    return final