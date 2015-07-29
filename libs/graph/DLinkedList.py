
class Record:
    def __init__(self, elem):
        """
        this class simply represents a list record linked to his next/prev elems
        :param elem: elem stored in the record
        """
        self._elem = elem
        self._next = None
        self._prev = None

    def getElem(self):
        """
        :return elem, the elem stored in the record
        """
        return self._elem

    def addNext(self, elem):
        """
        :return Record, set the next record
        """
        self._next = elem

    def getNext(self):
        """
        :return Record, get the next record
        """
        return self._next

    def addPrev(self, elem):
        """
        :return Record, set the previous record
        """
        self._prev = elem

    def getPrev(self, elem):
        """
        :return Record, get the previous record
        """
        return self._prev


class DoubledLinkedList:
    def __init__(self):
        """
        This class represents a double linked list
        """
        self._count = 0
        self._first = None
        self._last = None
        self._added_last_elems = []

    def getCount(self):
        """
        :return: int, elements' number
        """
        return self._count

    def isEmpty(self):
        """
        :return: bool, true if the list is empty
        """
        return self._first is None

    def getFirst(self):
        """
        :return: elem, the elem stored in the first record
        """
        if self.isEmpty():
            return None
        else:
            return self._first.getElem()

    def getFirstRecord(self):
        """
        :return: Record, the first record of the list
        """
        if self.isEmpty():
            return None
        else:
            return self._first

    def getLast(self):
        """
        :return: elem, the elem stored in the last record
        """
        if self.isEmpty():
            return None
        else:
            return self._last.getElem()

    def getLastRecord(self):
        """
        :return: Record, the last record of the list
        """
        if self.isEmpty():
            return None
        else:
            return self._last

    def addAsFirst(self, elem):
        """
        this function stores the elem in a new record at the top of the list
        :param elem: the elem to be stored
        """
        newRecord = Record(elem)
        self._count += 1
        if self.isEmpty():
            self._first = self._last = newRecord
        else:
            if self._last is None:
                self._last = self.getFirstRecord()
            newRecord.addNext(self.getFirstRecord())
            self._first = newRecord

    def addAsLast(self, elem):
        """
        this function stores the elem in a new record at the bottom of the list
        :param elem: the elem to be stored
        """
        newRecord = Record(elem)
        self._count += 1
        if self.isEmpty():
            self._first = self._last = newRecord
        else:
            newRecord.addPrev(self.getLastRecord())
            self._last.addNext(newRecord)
            self._last = newRecord
        self._added_last_elems.append(elem)

    def popFirst(self):
        """
        this function pops the first record in the list
        :return: Record, the first record of the list
        """
        if self.isEmpty():
            return None
        else:
            pop = self.getFirstRecord()
            self._count -= 1
            self._first = self.getFirstRecord().getNext()
            if self.getFirstRecord() is None:
                self._last = None
            else:
                self.getFirstRecord().addPrev(None)
            return pop


    def popLast(self):
        """
        this function pops the first record in the list
        :return: Record, the first record of the list
        """
        if self.isEmpty():
            return None
        else:
            pop = self.getLastRecord()
            self._last = self.getLastRecord().getPrev()
            if self.getLastRecord() is None:
                self._first = None
            else:
                self.getLastRecord().addNext(None)
            return pop

    def deleteRecord(self, delRecord):
        """
        this function deletes the record specified relinking its prev/next records
        :param delRecord: the record to be deleted
        """
        if self.isEmpty():
            return
        elif delRecord is None:
            return
        else:
            if delRecord.getPrev() is None:
                self._first = delRecord.getNext()
            else:
                linking = delRecord.getNext()
                delRecord.getPrev().addNext(linking)
            if delRecord.getNext() is None:
                self._last = delRecord.getPrev()
            else:
                linking = delRecord.getPrev()
                delRecord.getNext().addPrev(linking)

    def getLastAddedList(self):
        """
        this function returns a plain list of all the last added elems (history of last added elems, it is useful
        for an implementation without any affection by deleting items, such as an adjacency list visit of a static
        graph!)
        :return: list, a list of Nodes
        """
        return self._added_last_elems

    def getList(self):
        """
        this function returns a plain list of all the elems
        :return: list, list of Nodes
        """
        l = []
        if self.isEmpty():
            return l
        else:
            rec = self.getFirstRecord()
            while rec is not None:
                l.append(rec.getElem())
                rec = rec.getNext()
            return l

    def printList(self):
        """
        this function prints the entire list fine formatted
        :return: fine formatted list of elements
        """
        print "List count:", self.getCount()
        rec = self.getFirstRecord()
        while rec is not None:
            print "--->", rec.getElem().get_node()  #in this case we used .get_node() in order to use our personal
            #interface to see every node element
            rec = rec.getNext()


class Queue(DoubledLinkedList):
    """
    this class represent a simple queue
    """

    def enqueue(self, elem):
        self.addAsLast(elem)

    def dequeue(self):
        return self.popFirst().getElem()