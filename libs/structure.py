"""
This class builds the structure of k-knights and chessboard
"""

from libs.graph.Graph import GraphAdjacenceList

class Knight:
    def __init__(self, x, y, k):
        """
        This class builds up the knight whit its attributes and methods.
        @param x: int, the row position in chessboard
        @param y: int, the column position in chessboard
        @param k: int, the value of k-knight
        """
        self._row = x
        self._col = y
        self._value = k
        self._k_moves = 0
        self._moves = []
        self._tour_buffer = [] #temporary used to bufferize the tour
        self._distance_from_target = -1
        self._turn_from_target = -1

    def move(self, pos):
        """
        This method allows to move the knight. It also clears the list of moves of previous position.
        @param pos: tuple, the new position (row, col)
        """
        self._row = pos[0]
        self._col = pos[1]
        self._k_moves = 0
        self._moves = 0

    def set_value(self, k):
        """
        This method sets k-value of the knight.
        @param k: int, the new k-value
        """
        self._value = k

    def get_moves(self, r, c, debug=False):
        """
        This method allows to get all the possible moves that a k-knight can be done in a r x c chessboard. It checks if
        the moves was already calculated in this case it return that, otherwise it calculates.
        @param r: int, the number of rows in chessboard
        @param c: int, the number of columns in chessboard
        @param debug: boolean, a boolean that control debug
        @return: list, the list of possible moves
        """
        if self._k_moves == 0:
            moves = []
            for i in range(-2, 3):
                if i != 0:
                    for j in range(-2, 3):
                        if j != 0 and abs(j) != abs(i):
                            row = self._row + i
                            col = self._col + j
                            if 0 <= row <= r - 1 and 0 <= col <= c - 1:
                                moves.append((row, col))
            if debug:
                print(str(self.get_position()) + " can moves: " + str(moves))

            self._k_moves = 1
            self._moves = moves
            return moves
        else:
            if debug:
                print(str(self.get_position()) + " can moves: " + str(self._moves))

            return self._moves

    def get_other_moves(self, r, c, debug=False):
        """
        This method returns other moves that a k-knight can do. It appends this moves to other yet calculeted ones but it
        returns only the new moves.
        @param r: int, the number of rows in chessboard
        @param c: int, the number of columns in chessboard
        @param debug: boolean, a boolean that control debug
        @return: list, the list of possible new moves
        """
        moves = []
        assert self._moves != 0, "Non sono ancora state calcolate le mosse base"
        assert self._k_moves < self._value, "Non possono essere calcolate altre mosse"
        for n in range(0, len(self._moves)):
            for i in range(-2, 3):
                if i != 0:
                    for j in range(-2, 3):
                        if j != 0 and abs(j) != abs(i):
                            row = self._moves[n][0] + i
                            col = self._moves[n][1] + j
                            if 0 <= row <= r - 1 and 0 <= col <= c - 1:
                                if not (row, col) in self._moves:
                                    moves.append((row, col))
                                    self._moves.append((row, col))
        if debug:
            print(str(self.get_position()) + " can other moves: " + str(moves))
        self._k_moves += 1
        return moves

    def get_knight(self):
        """
        This method returns the knight.
        @return: tuple, the tuple with all attributes of knight
        """
        return self._row, self._col, self._value

    def get_position(self):
        """
        This method returns the position of the knight.
        @return: tuple, the tuple with row position and column position
        """
        return self._row, self._col

    def get_row(self):
        """
        This method return the row position of the knight.
        @return: int, the row position
        """
        return self._row

    def get_col(self):
        """
        This method return the column position of the knight.
        @return: int, the column position
        """
        return self._col

    def get_value(self):
        """
        This method return the value of the knight.
        @return: int, the value
        """
        return self._value

    def set_distance(self, distance):
        self._distance_from_target = distance

        self._turn_from_target = 0
        if distance != 0:
            while True:
                distance = distance - self._value
                self._turn_from_target += 1

                if distance <= 0:
                    break

    def get_distance(self):
        """
        This method return the distance from the target.
        @return: int, the distance
        """
        assert self._distance_from_target != -1, "Non e' ancora stata settata la distanza dal target"

        return self._distance_from_target

    def get_turn(self):
        """
        This method return the turns that knight have to do in order to arrive in target position.
        @return: int, the turns
        """
        assert self._distance_from_target != -1, "Non e' ancora stata settata la distanza dal target"

        return self._turn_from_target

    def is_found(self):
        if self._distance_from_target != -1:
            return True
        else:
            return False

    def getMoves(self):
        """
        this function can be used as an interface to manipulate the next-move list
        :return: list, the knight's next moves
        """
        return self._moves


    def refreshBuffer(self):
        """
        this function is invoked to refresh the moves' buffer
        :return: None
        """
        self._tour_buffer = []

    def calculateWeight(self, dist):
        """
        this function calculate the effective weight of a move using the distance between
        the initial position of the knight and its specific k-value
        :param dist: int, distance of the move
        :return: int, the weight for that distance
        """
        weight = 0
        knight = self.get_value()
        while dist > 0.0:
            weight += 1
            dist -= knight
        return weight

    def singleMove(self, position, rows, cols):
        """
        this function calculate all the available moves of the knight from a specific position
        this function is specifically optimized to check and avoid cycles in the knight moves
        (it is achieved using a list as a buffer of the knight moves previously calculated)
        :param position: tuple, the position by which calculate the moves
        :param rows: int, rows of the chessboard
        :param cols: int, cols of the chessboard
        :return: list, if moves have been added, the list of the moves calculated, else an empty one
        """
        x = position[0]
        y = position[1]
        move_list = []
        for i in range(-2, 3):
            if i == 0:
              continue

            newX = x + i
            if (newX < 0) or (newX > rows - 1):
              continue

            if abs(i) % 2 == 0:
              val = abs(i) - 1
              newY = y + val
              newY_bis = y - val
            else:
              val = abs(i) + 1
              newY = y + val
              newY_bis = y - val

            #we will bufferize the moves previously calculated using a support list
            if not (newY < 0 or newY > cols - 1):
              pos = (newX, newY)
              if not pos == self.get_position():
                  if not pos in self._tour_buffer:
                    self._tour_buffer.append(pos)
                    move_list.append(pos)
            if not (newY_bis < 0 or newY_bis > cols - 1):
              pos_bis = (newX, newY_bis)
              if not pos_bis == self.get_position():
                  if not pos_bis in self._tour_buffer:
                    self._tour_buffer.append(pos_bis)
                    move_list.append(pos_bis)

        return move_list


    def completeTour(self, rows, cols):
        """
        this function can be used to calculate a definitive tour for the knight
        :param rows: int, the rows of the chessboard
        :param cols: int, the columns of the chessboard
        :return: None
        """
        count = 1 #a deep-level counter
        value = 1 #a counter to keep trace of the value of the knight during the "visit"
        #using a support list we will extend the fringe of the previous calculated moves in order
        #to accomplish an entire knight's tour, keeping trace of the level of the tour from the knight
        moves = [self.get_position()]
        start = 0
        stop = len(moves)
        #if no other move is possible the while ends
        while start != stop:
            for move in moves[start:stop]:
                new_moves = self.singleMove(move, rows, cols)
                for new in new_moves:
                    self._moves.append((move, new, count))
                moves += new_moves

            start = stop
            stop = len(moves)

            value += 1
            if value > self.get_value():
                value = 1
                count += 1


class Match:
    def __init__(self, r, c):
        """
        This class builds up a r x c chessboard and it keeps a list of knight over it. It also keeps a max, that is the
        maximum k-value among all the k-values of the knights.
        @param r: int, the number of rows of the chessboard
        @param c: int, the number of columns of the chessboard
        """
        self._rows = r
        self._cols = c
        self._max = 0
        self._num_pieces = 0
        self._knights = []
        self._knights_nodes = []
        self._total_k = 0
        self._graph = GraphAdjacenceList()
        self._knights_found = -1
        self._turns = 0
        self._is_finished = False

    def add_knight(self, knight):
        """
        This method allows to add knight to chessboard.
        @param knight:  Knight, the knight to add
        """
        if self._max < knight.get_value() != 1:
            self._max = knight.get_value()
        if knight not in self._knights:
            self._knights.append(knight)
            self._total_k += knight.get_value()
        self._num_pieces = len(self._knights)

    def get_knights(self):
        """
        This method returns the list of the knights in the match.
        @return: list, list of knights in the match
        """
        return self._knights

    def get_rows(self):
        """
        This method returns the number of rows of the chessboard.
        @return: int, the number of the rows of the chessboard
        """
        return self._rows

    def get_cols(self):
        """
        This method returns the number of columns of the chessboard.
        @return: int, the number of the columns of the chessboard
        """
        return self._cols

    def get_max(self):
        """
        This method returns maximum k-value among all the k-values of the knights in the chessboard.
        @return: int, the max value of the match
        """
        return self._max

    def view_knights(self):
        """
        This methods prints all the knights of the match.
        """
        for knight in self._knights:
            print(knight.get_knight())

    def view_specs(self):
        """
        This methods prints the specifications of the match.
        """
        print(self._rows, self._cols, self._knights)

    def is_finished(self):
        """
        This methods return true or false in case of tha match is finished or not.
        @return: bool, true if match is finished
        """
        return self._is_finished

    def knight_found(self, knight, distance):
        """
        This method allow to
        @param knight:
        @param distance:
        """
        assert len(self._knights) != self._knights_found + 1, "Sono gia' stati trovati tutti i cavalli"

        self._knights_found += 1

        self._knights[self._knights.index(knight)].set_distance(distance)
        turns = knight.get_turn()
        self._turns += turns

    def finish(self, force=False):
        """
        This methods close the match ONLY if is time to close and calculates the numbers of turns in order to complete itself.
        """
        self._knights_found += 1
        if len(self._knights) == self._knights_found:
            self._is_finished = True
        else:
            self._knights_found -= 1
            if force:
                self._is_finished = True
                self._turns = float('inf')
            else:
                raise Exception

    def get_turns(self):
        """
        This method returns the numbers of turns in order to complete the match.
        @return: int, the turns to complete match
        """
        return self._turns

    def reset(self):
        """
        This method reset the match.
        """
        for knight in self._knights:
            knight._k_moves = 0
            knight._moves = 0
            knight._distance_from_target = -1
            knight._turn_from_target = -1

        self._knights_found = -1
        self._turns = 0
        self._is_finished = False

    def validate_positions(self, positions, debug=False):
        """

        @param positions:
        @param debug:
        @return:
        """
        valid = []
        for pos in positions:
            if 0 <= pos[0] <= (self._rows - 1) and 0 <= pos[1] <= (self._cols - 1):
                valid.append(pos)
        if debug:
            print("Valide positions: " + str(valid))
        return valid

    def getKnights(self):
        """
        :return: list, the list of knights' nodes
        """
        return self._knights_nodes

    def setGraph(self):
        """
        this function is used as an interface to manipulate the graph
        :return: GraphAdjacenceList, the graph related to the current match
        """
        return self._graph

    def makeGraph(self):
        """
        this function can be used to create a graph by the knights stored
        :return: None
        """
        r = self.get_rows()
        c = self.get_cols()

        #first of all... initializing the knights and storing them as initial nodes of the graph
        for k in self._knights:
            kgt = self.setGraph().insertNode(k.get_position(), k)
            self._knights_nodes.append(kgt) #storing the list of knights' nodes
            #node with a knight: knight_position + knight_weight
            k.completeTour(r, c) #calculating the complete tour for every knight
        for knight in self._knights:
            for step in knight.getMoves():
                move_from = step[0]
                move_to = step[1]
                node = self.setGraph().insertNode(move_from)
                moveNode = self.setGraph().insertNode(move_to)
                self.setGraph().linkNode(node, moveNode)
            knight.refreshBuffer() #just to free some memory...

    def makeGraphBFS(self):
        """
        this function can be used to create a graph by the knights stored
        :return: None
        """
        r = self.get_rows()
        c = self.get_cols()

        for k in self._knights:
            kgt = self.setGraph().insertNode(k.get_position(), k)
            self._knights_nodes.append(kgt)
            kgt.set_distance(0) #setting the 0-distance of the knight from its position
            k.completeTour(r, c)

        how_many = len(self.getKnights())
        minimum = float('inf')
        for knight in self._knights:
            for step in knight.getMoves():
                move_from = step[0]
                move_to = step[1]
                node = self.setGraph().insertNode(move_from)
                moveNode = self.setGraph().insertNode(move_to)
		#it is no longer necessary to link the nodes in order to accomplish the visit
		#but it is necessary to update the node deepness using the data from the moves' list
                moveNode.set_distance(step[2])
            knight.refreshBuffer()

        for node in self.setGraph().getNodes()[0].itervalues():
            if node.get_count() == how_many:
                if node.get_distance() < minimum:
                    minimum = node.get_distance()
        return minimum


    def minMovesBFS(self):
        """
        this function is the bulge of the problem. It is used to calculate the minimum number of moves
        to make all the knights converge using a previous result by the BFS forest previously build
        :return: int, the minimum moves number
        """
        #selecting knights' nodes and visiting...
        knights = self.getKnights()
        how_many = len(knights)
        forest = self.setGraph().visitNodesBFS(knights)
        #retrieving from the tuple the list of nodes
        nodes = self.setGraph().getNodes()[0]

        #finding the minimum moves number
        minimum = float('inf')
        #examining the forest generated by the visit
        for tree in forest:
            knight = tree.getRoot().getElem().get_weight()
            knight_val = knight.get_value()
            leaves = tree.getLeaves()
            for leaf in leaves:
                dist = leaf.getDistance()
                weight = knight.calculateWeight(dist)
                node = nodes[leaf.getElem().get_index()]
                node.set_distance(weight)
                if node.get_count() == how_many:
                    if node.get_distance() < minimum:
                        minimum = node.get_distance()
        return minimum


    def minMovesDijkstra(self):
        """
        this function is the bulge of the problem. It is used to calculate the minimum number of moves
        to make all the knights converge using a previous result by the forest previously build using
        a Dijkstra algorithm for the shortest path
        :return: int, the minimum moves number
        """
        #selecting knights' nodes and visiting...
        knights = self.getKnights()
        how_many = len(knights)
        forest = self.setGraph().visitDijkstra(knights)
        #retrieving from the tuple the list of nodes
        nodes = self.setGraph().getNodes()[0]

        #finding the minimum moves number
        minimum = float('inf')
        #examining the shortest-paths-tree generated by Dijkstra
        for tree in forest:
            knight = tree.getRoot().getElem().get_weight()
            knight_val = knight.get_value()
            leaves = tree.getLeaves()
            for leaf in leaves:
                dist = leaf.getDistance()
                weight = knight.calculateWeight(dist)
                node = nodes[leaf.getElem().get_index()]
                node.set_distance(weight)
                if node.get_count() == how_many:
                    if node.get_distance() < minimum:
                        minimum = node.get_distance()
        return minimum

    def minMovesFloydWarshall(self):
        """
        this function is the bulge of the problem. It is used to calculate the minimum number of moves
        to make all the knights converge using a previous result by the Floyd-Warshall algorithm
        :return: int, the minimum number of moves
        """
        INF = float('inf')
        FW = self.setGraph().FloydWarshall()
        knights = self.getKnights()
        how_many = len(knights)
        nodes = self.setGraph().getNodes()[0] #retrieving from the tuple the list of nodes

        #finding the minimum moves number
        minimum = float('inf')
        #examining the knights' paths
        for k_node in knights:
            index = k_node.get_index()
            knight = k_node.get_weight()
            knight_val = knight.get_value()

            for to_index in range(0, len(FW[index])):
                dist = FW[index][to_index]
                if dist != INF:
                    weight = knight.calculateWeight(dist)
                    node = nodes[to_index]
                    node.set_distance(weight)
                    if node.get_count() == how_many:
                        if node.get_distance() < minimum:
                            minimum = node.get_distance()
        return minimum
