class Leaf:
    def __init__(self, elem):
        """
        this class represent a tree leaf
        :param elem: the elem to be stored in the leaf
        """
        self._elem = elem
        self._father = None
        self._sons = []
        self._distance = float('inf')


    def setDistance(self, dist):
        """
        :param dist: float, the visit length
        :return: None
        """
        self._distance = dist

    def getDistance(self):
        """
        :return: float, the visit length
        """
        return self._distance

    def getElem(self):
        """
        :return: the elem stored in the leaf
        """
        return self._elem

    def getFather(self):
        """
        :return: Leaf, the fater
        """
        return self._father

    def setFather(self, father):
        """
        :param father: Leaf
        :return: None
        """
        self._father = father
        self.setDistance(father.getDistance() + 1.0)

    def getSons(self):
        """
        :return: list of Leaf, the sons
        """
        return self._sons

    def addSon(self, son):
        """
        :param son: Leaf
        :return: None
        """
        self._sons.append(son)

class Tree:
    def __init__(self, root):
        """
        this class represent a tree
        :param root: Leaf, the root leaf
        """
        self._root = root
        self._leaves = [root]

    def getRoot(self):
        """
        :return: Leaf, the root
        """
        return self._root

    def insertLeaf(self, sonLeaf, fatherLeaf):
        """
        :param sonLeaf: Leaf, the son Leaf
        :param fatherLeaf: Leaf, the father Leaf which will be linked to its sonLeaf
        :return: None
        """
        self._leaves.append(sonLeaf)
        sonLeaf.setFather(fatherLeaf)
        fatherLeaf.addSon(sonLeaf)

    def cutTree(self, leaf):
        """
        :param leaf: Leaf, the leaf to be cut away
        :return: the tree which root is the leaf
        """
        if leaf.getFather() is None: #leaf is the root!
            return self
        else:
            try:
                leaf.getFather().getSons().remove(leaf)
            except ValueError:
                raise Exception("it is not possible to cut away this leaf!")
            leaf.father = None
            return Tree(leaf)

    def getLeaves(self):
        """
        :return: list of Leaf, list of the tree's leaves
        """
        return self._leaves

