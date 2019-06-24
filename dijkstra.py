from fibonacciheap import *

class Node:
    def __init__(self,id):
        self.id = id
        self.neighbors = []
        self.visited = False
        self.dist = 10**10
        self.parent = None
        
    def __repr__(self):
        return '{}'.format(self.id)
        
class Graph:
    def __init__(self,edges):
        self.edges = edges
        self.nodes = {}
        
    def genNodesById(self):
        for edge in self.edges:
            for nodeId in edge[:2]:
                if nodeId not in self.nodes.keys():
                    self.nodes[nodeId] = Node(nodeId)
    
    def setNeighbors(self):
        for edge in self.edges:
            self.addEdge(edge)
        
    def addEdge(self,edge):
        u,v = [self.nodes[edge[0]],self.nodes[edge[1]]]
        u.neighbors.append((v,edge[2]))
        v.neighbors.append((u,edge[2]))
        
    def unroll(self,node):
        path = []
        while node.parent is not None:
            path.append(node.parent.id)
            node = node.parent
        return path
            
        
    def dijkstra(self,sourceNodeId):
        H = FibonacciHeap()
        H.heapify(list(map(lambda x: 
                           [self.nodes[x].id, self.nodes[x], self.nodes[x].dist],self.nodes.keys())))
        H.decrease_key(sourceNodeId,0)
        HeapNode = H.pull_highest_priority_element()
        current_node = HeapNode.value
        current_node.dist = HeapNode.key
        while H.is_empty() is False:
            for edge in current_node.neighbors:
                neighbor = edge[0]
                dist = current_node.dist + edge[1]
                if neighbor.dist > dist and neighbor.visited is False:
                    H.decrease_key(neighbor.id,dist)
                    neighbor.parent = current_node
            current_node.visited = True
            HeapNode = H.pull_highest_priority_element()
            current_node = HeapNode.value
            current_node.dist = HeapNode.key
            print(current_node, current_node.dist, self.unroll(current_node))