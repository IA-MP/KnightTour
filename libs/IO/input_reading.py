from time import time
from libs.structure import Knight, Match


def make_matches(f, debug=False):
    """
    This function reads from a txt input to create matches.
    @param f: file, the file to be read
    @param debug: boolean, a boolean that control debug
    @return : list, list of matches in the input file
    """
    assert f[len(f) - 4:] == ".txt", "No valid filename input"
    global file

    try:
        file = open(f, "r")
        settings = file.readlines()
    finally:
        file.close()

    matches = []
    count = int(settings[0])

    i = 2
    while count != 0:
        info = settings[i]
        info_l = info.split(" ")

        rows = int(info_l[0])
        cols = int(info_l[1])

        new_match = Match(rows, cols)

        for r in range(0, rows):
            line = settings[i + r + 1]
            for c in range(cols):
                if line[c].isdigit():
                    knight = Knight(r, c, int(line[c]))
                    new_match.add_knight(knight)

        matches.append(new_match)

        i = i + rows + 2
        count -= 1

    if debug:
        for match in matches:
            match.view_knights()

    return matches


if __name__ == "__main__":
    start = time()

    #filename = '../../dataset/input.txt'
    #make_matches(filename, True)

    print(time() - start)




