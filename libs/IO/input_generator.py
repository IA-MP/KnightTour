from random import randint, random
from time import time


def generate_chessboard(m, n, density, k_rand, k, debug=False):
    """
    This function generates a random chessboard from m, number of the rows, and n, number of columns.
    @param m: int, number of the rows
    @param n: int, number of the columns
    @param debug: boolean, a boolean that control debug
    @return list: a list of string that represents the chessboard
    """
    assert m >= 1, "The number of the rows must be greater then 1"
    assert n <= 10, "The number of the columns must be smaller or equal then 10"
    if k_rand:
        assert 1 <= k < 10, "If k is not random insert a k smaller then 10"

    chessboard = []
    info = [str(m), " ", str(n), "\n"]          # Info of chessboard
    chessboard.append(info)

    for i in range(0, m):                       # Creation of chessboard
        row = []
        for j in range(0, n):
            rand = randint(1, 10)

            if rand % density == 0:             # Choose knight
                if k_rand:
                    k = randint(1, 9)               # and its value
                row.append(str(k))
            else:
                row.append(".")                 # or blank position
        row.append("\n")
        chessboard.append(row)

    if debug:
        for elem in chessboard:
            print(elem)

    return chessboard


def generate_input(t, density=7, k_rand=True, k=1, debug=False):
    """
    This function generates a random input with t chessboards.
    @param t: int, the number of test to create
    @param density: int, the density of chessboard
    @param k_rand: boolean, a boolean that control random k value
    @param k: int, the k value
    @param debug: boolean, a boolean that control debug
    @return list: a list of string that represent the input
    """
    assert t <= 100, "The number of the tests must be smaller then 100"
    file = []
    info = [str(t), "\n"]                       # Numbers of test
    file.append(info)

    for i in range(0, t):
        m = int(10 * random()) + 1              # Random number of rows
        n = randint(1, 10)                      # Random number of columns (in range from 1 to 10)
        chess = generate_chessboard(m, n, density, k_rand, k)       # Generate chessboard
        file.append(chess)

    if debug:
        for elem in file:
            print(elem)

    return file


if __name__ == "__main__":
    start = time()

    #generate_input(100)

    print(time() - start)
