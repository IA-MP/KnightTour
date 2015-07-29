from libs.graph.DLinkedList import Queue, DoubledLinkedList as List
from libs.graph.PriorityQueue import PriorityQueueBinary as PriorityQueue
from libs.graph.Tree import *
#it is better to use a DoubledLinkedList to operate with a great efficiency on
#the lists those will be used in the graph representation

class Node:
    def __init__(self, elem, index, weight = None):
        """
        this class represents a graph node
        :param elem: an object stored into the node
        :param index: int, the index by which the node may be identified
        :param weight: int, the weight of the node and of his object - may not be used
        """
        self._elem = elem
        self._index = index
        self._weight = weight
        self._token = None #used to mark each node during a generic visit
        self._distance = 0 #used to set and retrieve the distance of the node in the visit
        self._knights = 0 #used to keep trace of the knights in the node
        self._knights_arrived = []

    def get_elem(self):
        """
        :return: object stored in the node
        """
        return self._elem

    def get_index(self):
        """
        :return: int, the index of the node
        """
        return self._index

    def get_weight(self):
        """
        :return: int, the weight of the node
        """
        return self._weight

    def get_token(self):
        """
        :return: int, the token of the node
        """
        return self._token

    def set_token(self, token):
        """
        :param token: int, the validation token
        :return: int, the token of the node
        """
        self._token = token

    def get_node(self):
        """
        :return: tuple, (index, elem, weight)
        """
        return self.get_elem(), self.get_weight()

    def set_distance(self, dist):
        """
        this function can be used to set a particular distance in order to provide
        a good interface for BFS and Dijkstra shortest-path algorithms
        :param dist: int, distance
        :return: None
        """
        self._distance += dist
        self._knights += 1

    def get_distance(self):
        """
        :return: int, the distance calculated for the node
        """
        return self._distance

    def get_count(self):
        """
        :return: int, the number of knights
        """
        return self._knights

#I'll use an AdjacenceList Graph because of the unitarian value of all the arcs
class GraphAdjacenceList:
    def __init__(self):
        """
        this class represents a graph using an adjacency list style
        """
        self._nodes = dict() #to store the nodes
        self._adjacency = dict() #to link the nodes to their adjacence list
        self._nextId = 0 #it will be used to store the nodes - id > 0
        self._nodes_elems = dict() #it will be used to store the elems inserted

    def getNodes(self):
        """
        this function is used as an interface to retrieve graph's nodes
        :return: (dictionary, dictionary) the nodes and their adjacency lists
        """
        return self._nodes, self._adjacency


    def insertNode(self, elem, weight = None):
        """
        this function allows the user to insert a node into the graph
        :param elem: the elem to be stored into the node
        :param weight: the weight of the node
        :return: Node, the node already inserted or just inserted
        """
        if elem in self._nodes_elems:
            #if a node has already setted it will be returned
            #assuming the computational cost of this check, as it is implemented in python,
            #as memory access to the list -> O(1)
            return self._nodes_elems[elem]

        newNode = Node(elem, self._nextId, weight)
        self._nodes[newNode.get_index()] = newNode
        self._adjacency[newNode.get_index()] = List()
        self._nextId += 1

        #storing the elem just inserted
        self._nodes_elems[elem] = newNode

        return newNode

    def linkNode(self, tail, head):
        """
        this function links two nodes in a direct connection
        :param tail: Node, the tail node
        :param head: Node, the head node
        :return: None
        """
        adj = self._adjacency[tail.get_index()]
        if head not in adj.getLastAddedList():
            #assuming direct memory access... (see previous method)
            adj.addAsLast(head)



    def printGraph(self):
        """
        this function builds a well formatted visualization of the nodes
        :return: list, a list of nodes visual formatted
        """
        print("Adjacency Lists:")
        for identifier in self._nodes:
            print("node", self._nodes[identifier].get_elem(), self._nodes[identifier].get_weight())
            self._adjacency[identifier].printList()
            print("")

#The chessboard's graph is unitary-weight-arcs formed so we can use a Breadth First Search to return the list of all the
#minimum-path-trees starting each from a knight

    def validateNodes(self, token):
        """
        this function validate all nodes with a token value in order to accomplish the visit
        :param token: int, the token value to validate the node. 0 if not visited, 21 if explored and 42 (for Douglas) if closed
        :return: None
        """
        nodes = self.getNodes()[0]
        for node in nodes.itervalues():
            node.set_token(token)

    def visitBFS(self, node):
        """
        this is a Breadth First Search starting from a vertex. Please note that all the operations are done on the leaves
        to let the algorithm be more modular (it doesn't seems be affecting the computational time for it remains proportional
        to the dimension of the graph)
        :param node: Node, the starting vertex
        :return: Tree, representing the visit path
        """
        #initializing some useful constants (funny constants too)
        unexplored = 0
        explored = 21
        closed = 42 #So long and thanks for all the fish!
        #validating all the nodes as unexplored and starting from the vertex
        self.validateNodes(unexplored)
        node.set_token(explored)
        #initializing the tree containing the only vertex
        T_root = Leaf(node)
        T_root.setDistance(0.0) #using the float - it is not a counter value
        T = Tree(T_root)
        #initializing the fringe of the visit
        F = Queue()
        F.enqueue(T_root)

        while not F.isEmpty():
            u = F.dequeue()
            n = u.getElem()
            n.set_token(closed)
            for v in self._adjacency[n.get_index()].getLastAddedList():
                if v.get_token() == unexplored:
                    v.set_token(explored)
                    l = Leaf(v)
                    F.enqueue(l)
                    T.insertLeaf(l, u)
        return T

    def visitNodesBFS(self, Nodes):
        """
        this is a simple implementation of a Breadth First Search algorithm to visit the graph
        starting from a selected group of nodes
        :param Nodes: Node list containing the nodes from which start the visit
        :return: list of Trees, the list of all the visits
        """
        T_list = []
        for node in Nodes:
            tree = self.visitBFS(node)
            T_list.append(tree)
        return T_list

#it is interesting to achieve the same result using minimum path algorithm of Dijkstra

    def Dijkstra(self, node):
        """
        this is a Dijstra shortest path algorithm implementation starting from a vertex
        :param node: Node, the starting vertex
        :return: Tree, the shortest paths tree
        """
        INF = float('inf')
        self.validateNodes(INF)
        #we will use the nodes' tokens to store the distance info!
        node.set_token(0.0) #0-distance from itself!
        #initializing the tree
        T_root = Leaf(node)
        T_root.setDistance(node.get_token())
        T = Tree(T_root)
        #initializing a dictionary to keep trace of the leaves
        leaves = dict()
        leaves[node] = T_root
        #initializing the priority queue to mantain the fringe
        PQ = PriorityQueue()
        PQ.insert(T_root, node.get_token())

        while not PQ.isEmpty():
            u = PQ.deleteMin() #retrieving the min node from the leaf
            n = u.getElem()
            for v in self._adjacency[n.get_index()].getLastAddedList():
                if v.get_token() == INF:
                    l = Leaf(v)
                    leaves[v] = l #updating the leaves' dictionary
                    PQ.insert(l, n.get_token() + 1.0) #each edge will be unitary-cost
                    v.set_token(n.get_token() + 1.0)
                    T.insertLeaf(l, u)
                elif n.get_token() + 1.0 < v.get_token():
                    relaxed = n.get_token() + 1.0
                    leaves[v].setDistance(relaxed)
                    #updating the tree... (we are now saving in the priority queue the leaves)
                    leaves[v].setFather(u)
                    leaves[n].addSon(leaves[v])
                    #updating the priority queue
                    PQ.decreaseKey(leaves[v], relaxed)
                    v.set_token(relaxed)
        return T

    def visitDijkstra(self, Nodes):
        """
        this is an implementation of the Dijkstra algorithm to visit the graph
        starting from a selected group of nodes
        :param Nodes: Node list containing the nodes from which start the visit
        :return: list of Trees, the list of all the visits
        """
        T_list = []
        for node in Nodes:
            tree = self.Dijkstra(node)
            T_list.append(tree)
        return T_list

#Pay attention!
# -Bellman condition to decide a shortest path -> for each node it is O(k*n) where k is node's degree
# -save the all available paths in a tree instead of a list of lists -> O(n) (if it is possible...)
# -the chessboard graph is a direct graph with all the arcs costing a single unit
#  (please note that it is necessary to consider each knight own k-value in order to calculate
#   the move number!!)
# -general purpose: in python2.7 the infinite is... INF = float('inf') -> comparisons using floats

    def FloydWarshall(self):
        """
        this is a simple implementation of the Floyd-Warshall algorythm using an O(n^2) space
        but O(n^3) computational complexity. Please note that in our case the chessboard graph
        is unitary-weight-arch created
        :return: list of lists, matrix of the distances between two vertices
        """
        INF = float('inf')
        nodes, adjacency = self.getNodes() #getting the dictionaries

        indexes = nodes.keys() #it is the same to access the two dictionaries
        dim = len(indexes)

        #initializing the matrix
        dist = [[INF for m in range(dim)] for n in range(dim)]
        for i in range(dim):
            ind = indexes[i]
            dist[ind][ind] = 0.0
            adj_nodes = adjacency[ind].getLastAddedList()
            for adj in adj_nodes:
                to_ind = adj.get_index()
                dist[ind][to_ind] = 1.0

        #executing the dinamic programming algorithm
        for k in range(dim):
            for i in range(dim):
                for j in range(dim):
                    if dist[i][k] != INF and dist[k][j] != INF and dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist
