
class Vertex:
    def __init__(self, _id):
        self.id = _id
    
    def __str__(self):
        return self.id
    
    __repr__ = __str__

class Edge:
    def __init__(self, _v1, _v2, ts, rt):
        self.v1 = _v1
        self.v2 = _v2
        self.tieStrength = ts
        self.relationType = rt
    
    def __str__(self):
        return self.v1 + " - " + self.v2 + " - " + str(self.tieStrength) + " - " + self.relationType + "\n"
    
    __repr__ = __str__


class Graph:
    def __init__(self, inputFile):
        self.vertices = []
        self.edges = []
        self.vertexEdgeMapping = {}
        fileHandler = open(inputFile, 'r')
        
        firstLine = fileHandler.readline()
        firstLineList = firstLine.split()
        self.verticeCount = int(firstLineList[0])
        self.edgeCount = int(firstLineList[1])
        
        for i in xrange(self.verticeCount):
            line = fileHandler.readline()
            vertexId = line.split()[0]
            self.vertices.append(Vertex(vertexId))
            self.vertexEdgeMapping[vertexId] = []
        
        for i in xrange(self.edgeCount):
            line = fileHandler.readline()
            lineList = line.split()
            v1 = lineList[0]
            v2 = lineList[1]
            tieStrength = int(lineList[2])
            relationType = lineList[3]
            self.edges.append(Edge(v1, v2, tieStrength, relationType))
            self.vertexEdgeMapping[v1].append(i)
            self.vertexEdgeMapping[v2].append(i)


# g = Graph("../graph.txt")
# print g.vertices
# print g.edges
# print g.vertexEdgeMapping
            
            
            
        