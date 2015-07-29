class BinaryHeapNode:
    def __init__(self, elem, key, index):
        """
        this class represents a generic binary heap node
        :param elem: the elem to store
        :param key: int, the key to be used as priority function
        :param index: int, the index related to the binary node
        """
        self._elem = elem
        self._key = key
        self._index = index

    def getElem(self):
        """
        :return: the elem stored in the node
        """
        return self._elem

    def getKey(self):
        """
        :return: int, the key
        """
        return self._key

    def setKey(self, value):
        """
        :param value: int, the node's new key
        :return: None
        """
        self._key = value

    def getIndex(self):
        """
        :return: int, the nodes' index
        """
        return self._index

    def setIndex(self, ind):
        """
        :param ind: int, the node's new index
        :return: None
        """
        self._index = ind


class PriorityQueueBinary:
    def __init__(self):
        """
        this class is a representation of a Binary Heap used in order to achieve the
        Priority Queue structure operations
        """
        self._heap = []
        self._heap_elemstonode = dict()
        self._length = 0

    def getLength(self):
        """
        :return: int, the heap length
        """
        return self._length

    def isEmpty(self):
        """
        :return: bool, True if the priority queue is empty
        """
        if self.getLength() == 0:
            return True
        else:
            return False

    def getHeap(self):
        """
        we can use a very useful binary tree relation in order to access the heap members:
        heap [ 2 * node_position + node_child_position ] = information to child in that position
        moreover we can access the father by -> heap [ node_position / 2 ]
        Attention: for it is binary the child_position can only be 1 or 2!!
        it is S(n) = O(n) structure type
        :return: list, the heap
        """
        return self._heap



    def minSon(self, bNode):
        """
        this function returns the lowest son of the node
        :param bNode: BinaryHeapNode
        :return: BinaryHeapNode
        """
        ind = bNode.getIndex()
        if 2 * ind + 1 > self.getLength() - 1:
            return None #heap leaf reached
        if 2 * ind + 2 > self.getLength() - 1:
            return self.getHeap()[2 * ind + 1] #only one son

        first_son = self.getHeap()[2 * ind + 1]
        second_son = self.getHeap()[2 * ind + 2]
        if first_son.getKey() < first_son.getKey():
            return first_son
        else:
            return second_son


    def swapNodes(self, first_node, second_node):
        """
        this function performs a swap between the two nodes
        :param first_node: BinaryHeapNode
        :param second_node: BinaryHeapNode
        :return: None
        """
        self.getHeap()[first_node.getIndex()] = second_node
        self.getHeap()[second_node.getIndex()] = first_node
        tmp = first_node.getIndex()
        first_node.setIndex(second_node.getIndex())
        second_node.setIndex(tmp)

    def moveUp(self, lower_node):
        """
        this function performs a moveUp operation in the heap
        :param lower_node: BinaryHeapNode
        :return: None
        """
        #in case of there is no way to move further up
        if lower_node.getIndex() <= 0:
            return
        #moving up
        upper_father = self.getHeap()[(lower_node.getIndex() - 1) / 2]
        while lower_node.getIndex() > 0 and lower_node.getKey() < upper_father.getKey():
            self.swapNodes(lower_node, upper_father)
            upper_father = self.getHeap()[(lower_node.getIndex() - 1) / 2]

    def moveDown(self, upper_node):
        """
        this function performs a moveDown operation in the heap
        :param upper_node: BinaryHeapNode
        :return: None
        """
        lower_son = self.minSon(upper_node)
        while lower_son is not None and lower_son.getKey() < upper_node.getKey():
            self.swapNodes(upper_node, lower_son)
            lower_son = self.minSon(upper_node)

    def insert(self, elem, key):
        """
        :param elem: the elem to be stored in the binary heap node
        :param key: the priority key
        :return: None
        """
        newNode = BinaryHeapNode(elem, key, self.getLength())
        #in order to keep trace of the delete...
        if self.getLength() < len(self.getHeap()):
            self.getHeap()[self.getLength()] = newNode
        else:
            self.getHeap().append(newNode)
        self._heap_elemstonode[elem] = newNode
        self._length += 1
        self.moveUp(newNode)

    def decreaseKey(self, bNode, new_key):
        """
        we are assuming only priority decreasing in this implementation: we only need to call a moveUp
        :param bNode: Leaf which is in the heap
        :param new_key: int, the new node's key
        :return: None
        """
        binary = self._heap_elemstonode[bNode]
        binary.setKey(new_key)
        self.moveUp(binary)

    def deleteMin(self):
        """
        this function is the bulge of the priority queue structuer: it returns the minimum in the queue
        :return: BinaryHeapNode
        """
        if self.getLength() == 0:
            return None
        first_node = self.getHeap()[0]
        del self.getHeap()[0]
        self._length -= 1
        minimum = first_node.getElem()
        return minimum
