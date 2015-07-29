from math import trunc

from libs.structure import Knight


def round_int(number, precision=False):
    """

    @param number:
    @return:
    """
    if precision and 0.6 > number - trunc(number) >= 0.5:
        return trunc(number), trunc(number) + 1     # Return number rounded up and rounded down

    if trunc(number + 0.5) > trunc(number):     # If the decimal part is >= 5
        return trunc(number) + 1                # round up
    else:
        return trunc(number)                    # else round down


def calculate_targets(match, type, debug=False):
    """
    This function calculates targets positions, that is the position round the "center of mass" of the match evaluated
    among all k-knights based on them k-value.
    @param match: Match, the match to be evaluated
    @param debug: boolean, a boolean that control debug
    @return int or list of tuple: 0 in case of and list in case of
    """
    m = 0                                   # Initialization of sum of k value
    mr_row = 0                              # Initialization of sum of product row position for value
    mr_col = 0                              # Initialization of sum of product col position for value
    pieces = match.get_knights()            # Retrieve from match all knights
    max_value = match.get_max()             # Retrieve the max k-value of the chessboard
    num_pieces = len(pieces)                # Number of knights retrieved

    if num_pieces > 1:                      # There are more then one kniths
        for piece in pieces:
            if max_value != piece.get_value():      # Recalculation of k-value
                value = abs(piece.get_value() - max_value + 1)
            else:
                value = piece.get_value() - max_value + 1
            m += value                              # Sum of k value
            mr_row += piece.get_row() * value       # Sum of weighted row
            mr_col += piece.get_col() * value       # Sum of weighted col

        if debug:
            print("Target: (" + str(mr_row / m) + ", " + str(mr_col / m) + ")")
            print("Target approssimato: (" + str(round_int(mr_row / m)) + ", " + str(round_int(mr_col / m)) + ")")

        if type == 0:                               # Return only the target
            return [(round_int(mr_row / m), round_int(mr_col / m))]
        if type == 1:                               # Return the target and its neighbourhood
            targets = []
            target_row = round_int(mr_row / m)
            target_col = round_int(mr_col / m)
            for i in range(-1, 2):                  # Neighbourhood large one square
                for j in range(-1, 2):
                    targets.append((target_row + i, target_col + j))
            if debug:
                print("Targets: " + str(targets))
            return match.validate_positions(targets, debug)

        if type == 2:                               # Return the target and its neighbourhood (two squares)
            targets = []
            target_row = round_int(mr_row / m)
            target_col = round_int(mr_col / m)
            for i in range(-2, 3):                  # Neighbourhood large two squares
                for j in range(-2, 3):
                    targets.append((target_row + i, target_col + j))
            if debug:
                print("Targets: " + str(targets))
            return match.validate_positions(targets, debug)
        if type == 3:                               # Return the target, its neighbourhood and all the positions of the knight

            positions = []
            for knight in match.get_knights():
                positions.append((knight.get_row(), knight.get_col()))

            if debug:
                print("Posizioni: " + str(positions))

            targets = []
            target_row = round_int(mr_row / m, True)    # Round with "double" precision
            target_col = round_int(mr_col / m, True)
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if isinstance(target_row, tuple) and not isinstance(target_col, tuple):
                        if not (target_row[0] + i, target_col + j) in positions:
                            targets.append((target_row[0] + i, target_col + j))
                        if not (target_row[1] + i, target_col + j) in positions:
                            targets.append((target_row[1] + i, target_col + j))
                    elif isinstance(target_col, tuple) and not isinstance(target_row, tuple):
                        if not (target_row + i, target_col[0] + j) in positions:
                            targets.append((target_row + i, target_col[0] + j))
                        if not (target_row + i, target_col[1] + j) in positions:
                            targets.append((target_row + i, target_col[1] + j))
                    elif isinstance(target_col, tuple) and isinstance(target_row, tuple):
                        if not (target_row[0] + i, target_col[0] + j) in positions:
                            targets.append((target_row[0] + i, target_col[0] + j))
                        if not (target_row[0] + i, target_col[1] + j) in positions:
                            targets.append((target_row[0] + i, target_col[1] + j))
                        if not (target_row[1] + i, target_col[0] + j) in positions:
                            targets.append((target_row[1] + i, target_col[0] + j))
                        if not (target_row[1] + i, target_col[1] + j) in positions:
                            targets.append((target_row[1] + i, target_col[1] + j))
                    else:
                        if not (target_row + i, target_col + j) in positions:
                            targets.append((target_row + i, target_col + j))
            if debug:
                print("Targets: " + str(targets))

            positions.extend(match.validate_positions(targets, False))

        if type == 4:                           # Return all the chessboard
            targets = []
            for i in range(0, match.get_rows()):
                for j in range(0, match.get_cols()):
                    targets.append((i, j))
            if debug:
                print("Targets: " + str(targets))
            return targets

    elif num_pieces == 1:           # There is only one knight
        if debug:
            print("Un solo pezzo disponibile " + str(num_pieces))
        return 0
    else:                           # There are not knights
        if debug:
            print("Nessun pezzo disponibile " + str(num_pieces))
        return -1


def montagna(match, type, outs, debug=False):
    """

    @param match:
    @param debug:
    """
    if debug:
        print("Match: (" + str(match.get_rows()) + ", " + str(match.get_cols()) +")")
    targets = calculate_targets(match, type, debug)                 # We calculate targets
    if isinstance(targets, list):                                   # If there are more the one
        turns = float('inf')                                        # Inizializate number of turns with the highest number in Python
        for target in targets:                                      # For all targetes
            target_knight = Knight(target[0], target[1], 1)         # we create a fake knight

            force = False

            while not match.is_finished():                          # While the match is not finished
                list_moves = target_knight.get_moves(match.get_rows(), match.get_cols(), debug) if target_knight.get_value() == 1 else target_knight.get_other_moves(match.get_rows(), match.get_cols(), debug)     # generate moves
                if len(list_moves) != 0:                            # If there are some moves
                    for knight in match.get_knights():              # For all knigths
                        if target == knight.get_position() and not knight.is_found():   # If the target is equal to position of a knight and it is not yet founded
                            match.knight_found(knight, 0)           # We found a knight
                            if match.get_turns() > turns:           # Optimization: if the actual match have already turns greater then previous
                                break                               # Break and skip target
                        for move in list_moves:                     # For all moves
                            if move == knight.get_position() and not knight.is_found(): # if the move is equal to position of a knight and it is not yet founded
                                match.knight_found(knight, target_knight.get_value())   			     # we found a new knight
                                if match.get_turns() > turns:       # Optimization: if the actual match have already turns greater then previous
                                    break                           # Break and skip target
                else:       # Otherwise there is not moves
                    force = True            # We force the closure of the match
                    if debug:
                        print("Non ci sono mosse possibili, forzo chiusura match")
                try:
                    match.finish(force)
                except Exception:
                    if debug:
                        print("Non posso chiudere match!")
                    pass

                target_knight.set_value(target_knight.get_value() + 1)
            if match.get_turns() < turns:       # Find if this match have got less turns in order to complete
                turns = match.get_turns()
                if debug:
                    print("Con il cavallo: " + str(target_knight.get_position()) + " ho impiegato " + str(turns) + " turni.")
                if turns == len(match.get_knights()) -1:
                    break

            match.reset()
        if turns != float('inf'):
            if debug:
                print("Ho impiegato " + str(turns) + " turno(i)!")      # We could complete
            outs.append(str(turns))
        else:
            if debug:
                print("Impossibile!")                                   # We could not complete
            outs.append("impossibile")
    else:
        if targets == 0:                                                # There is only one knight
            if debug:
                print("Ho impiegato 0 turni!")
            outs.append(str(0))
        else:                                                           # There are not knights
            if debug:
                print("Impossibile")
            outs.append("impossibile")
