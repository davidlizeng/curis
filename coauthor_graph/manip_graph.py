import codecs
import sys
import snap
from collections import deque

def getDistances(graph):
    distances = {}
    nameToNId = {}
    for n in graph.Nodes():
        id = n.GetId()
        nameToNId[graph.GetStrAttrDatN(id, 'name').decode('utf-8')] = id
    infile = codecs.open('csv/dblpusers.csv', 'r', 'utf-8')
    lines = infile.read().splitlines()
    dblpUsers = []
    for line in lines:
        tokens = line.split('||')
        if tokens[2] != '' and tokens[1] in nameToNId:
            id = int(tokens[0])
            distances[id] = {}
            dblpUsers.append({'name': tokens[1], 'id': id})
    for i in range(len(dblpUsers)):
        n1 = dblpUsers[i]['name']
        i1 = dblpUsers[i]['id']
        for j in range(i + 1, len(dblpUsers)):
            n2 = dblpUsers[j]['name']
            i2 = dblpUsers[j]['id']
            # shortest path behavior is weird if no path exists
            dist = snap.GetShortPath(graph, nameToNId[n1], nameToNId[n2])
            distances[i1][i2] = dist
            distances[i2][i1] = dist
    outfile = open('csv/distances.csv', 'w')
    for i1 in distances:
        for i2 in distances[i1]:
            outfile.write(str(i1) + '||' + str(i2) + '||' + str(distances[i1][i2]) + '\n')
    outfile.close()
    infile.close()
    return distances

def shrinkGraph(graph, maxDist):
    nameToNId = {}
    for n in graph.Nodes():
        id = n.GetId()
        nameToNId[graph.GetStrAttrDatN(id, 'name').decode('utf-8')] = id
    infile = codecs.open('csv/dblpusersaff.csv', 'r', 'utf-8')
    lines = infile.read().splitlines()
    validNodes = set()
    for line in lines:
        tokens = line.split('||')
        if tokens[2] != '':
            id = nameToNId[tokens[1]]
            closeNeighborsSet = set()
            pq = deque()
            pq.append((id, 0))
            closeNeighborsSet.add(id)
            while len(pq) > 0:
                (id, dist) = pq.popleft()
                if dist == maxDist:
                    break
                node = graph.GetNI(id)
                for i in range(node.GetOutDeg()):
                    nbrId = node.GetOutNId(i)
                    if nbrId not in closeNeighborsSet:
                        closeNeighborsSet.add(nbrId)
                        pq.append((nbrId, dist + 1))
            validNodes.update(closeNeighborsSet)
            print tokens[0], len(closeNeighborsSet), len(validNodes)
    unused = snap.TIntV()
    for n in graph.Nodes():
        if n.GetId() not in validNodes:
            unused.Add(n.GetId())
    graph.DelNodes(unused)




def bfsForDist(graph, maxDist):
    outfile = open('csv/.distances6.csv', 'w')
    nameToNId = {}
    nIdToUId = {}
    for n in graph.Nodes():
        id = n.GetId()
        nameToNId[graph.GetStrAttrDatN(id, 'name').decode('utf-8')] = id
    infile = codecs.open('csv/dblpusersaff.csv', 'r', 'utf-8')
    lines = infile.read().splitlines()
    infile.close()
    for line in lines:
        tokens = line.split('||')
        if tokens[2] != '':
            id = nameToNId[tokens[1]]
            if id not in nIdToUId:
                nIdToUId[id] = []
            nIdToUId[id].append(tokens[0])
    for id in nIdToUId:
        for uid in nIdToUId[id]:
            closeNeighborsSet = set()
            pq = deque()
            pq.append((id, 0))
            closeNeighborsSet.add(id)
            while len(pq) > 0:
                (curId, dist) = pq.popleft()
                if dist == maxDist:
                    break
                node = graph.GetNI(curId)
                for i in range(node.GetOutDeg()):
                    nbrId = node.GetOutNId(i)
                    if nbrId not in closeNeighborsSet:
                        closeNeighborsSet.add(nbrId)
                        pq.append((nbrId, dist + 1))
                        if nbrId in nIdToUId:
                            for nbrUId in nIdToUId[nbrId]:
                                outfile.write(uid + '||' + nbrUId + '||' + str(dist + 1) + '\n')
            print uid, len(closeNeighborsSet)
    outfile.close()


def loadGraph():
    fin = snap.TFIn('coauthor.graph')
    return snap.TNEANet.Load(fin)

def getConnectivity(graph):
    outfile = open('csv/connectivity.csv', 'w')
    nameToNId = {}
    nIdToUId = {}
    for n in graph.Nodes():
        id = n.GetId()
        nameToNId[graph.GetStrAttrDatN(id, 'name').decode('utf-8')] = id
    infile = codecs.open('csv/dblpusersaff.csv', 'r', 'utf-8')
    lines = infile.read().splitlines()
    infile.close()
    for line in lines:
        tokens = line.split('||')
        if tokens[2] != '':
            id = nameToNId[tokens[1]]
            if id not in nIdToUId:
                nIdToUId[id] = []
            nIdToUId[id].append(tokens[0])
    for id in nIdToUId:
        for uid in nIdToUId[id]:
            closeNeighbors = {}
            pq = deque()
            pq.append((id, 0))
            closeNeighbors = {}
            closeNeighbors[id] = 0
            while len(pq) > 0:
                (curId, dist) = pq.popleft()
                if dist == 2:
                    break
                node = graph.GetNI(curId)
                for i in range(node.GetOutDeg()):
                    nbrId = node.GetOutNId(i)
                    if nbrId not in closeNeighbors:
                        closeNeighbors[nbrId] = dist + 1
                        pq.append((nbrId, dist + 1))
            outfile.write(str(uid) + ',' + str(closeNeighbors.values().count(1)) + ',' +
                str(closeNeighbors.values().count(2)) + '\n')
    outfile.close()

#def getCentralities(network):
network = loadGraph()
nameToNId = {}
uIdToNId = {}
for n in network.Nodes():
    id = n.GetId()
    nameToNId[network.GetStrAttrDatN(id, 'name').decode('utf-8')] = id
infile = codecs.open('csv/dblpusersaff.csv', 'r', 'utf-8')
lines = infile.read().splitlines()
infile.close()
for line in lines:
    tokens = line.split('||')
    if tokens[2] != '':
        nId = nameToNId[tokens[1]]
        uIdToNId[int(tokens[0])] = nId
graph = snap.ConvertGraph(snap.PUNGraph, network)
degCenters = {}
closeCenters = {}
pageRanks = snap.TIntFltH()
eigenCenters = snap.TIntFltH()
# btwnCenters = snap.TIntFltH()
# edgeHash = snap.TIntPrFltH()
print('Running PageRank...')
snap.GetPageRank(graph, pageRanks)
print('Running Eigenvector centrality...')
snap.GetEigenVectorCentr(graph, eigenCenters)
# print('Running Betweeness...')
# snap.GetBetweennessCentr(graph, btwnCenters, edgeHash)
print('Running Degree and Closeness...')
for uId, nId in uIdToNId.iteritems():
    print uId, nId
    degCenters[uId] = snap.GetDegreeCentr(graph, nId)
    closeCenters[uId] = snap.GetClosenessCentr(graph, nId)

outfile = open('csv/centralities.csv', 'w')
for uId, nId in uIdToNId.iteritems():
    outfile.write(str(uId) + ',' + str(pageRanks[nId]) + ',' +\
        str(eigenCenters[nId]) + ',' +\
        str(degCenters[uId]) + ',' + str(closeCenters[uId]) + '\n')
outfile.close()
