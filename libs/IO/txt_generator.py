import os
from time import time

from libs.IO.input_generator import generate_input


def generate_name_file(kind, path):
    """
    This function allows to generate sequential input file name
    @param kind: int, 0 if input, 1 if output
    @param path: string, the path where generate file
    @return: string, the name file with an incremental number
    """
    global filename
    i = 0
    while True:
        if kind == 0:
            filename = "input_%d" % i
        elif kind == 1:
            filename = "output_%d" % i
        if not os.path.exists(path + filename + ".txt"):
            return filename
        i += 1


def generate_file(kind, text, path, num=None):
    """
    This function generates input or output txt file.
    @param kind: int, the int that represent the kind of file to be generated. 0 for input, 1 for output
    @param text: string, the string to store in the file
    @param path: string, the path where we want generate file
    @param num: int, the incremental value, if there is not it override the file
    """
    global file
    file = None
    final_path = ""
    if kind == 0:                               # Generate input file
        try:
            if num is None:
                name = generate_name_file(0, path)
                final_path = path + name + '.txt'
                file = open(final_path, 'w')
            else:
                final_path = path + 'input_' + str(num) + '.txt'
                file = open(final_path, 'w')
            for row in text:
                for col in row:
                    for elem in col:
                        file.writelines(str(elem))
                file.write("\n")
        except Exception:
            print("Si e' verificato un problema con il path, seguire le istruzioni per favore e scrivere un path regolare")
            raise SystemExit()
        finally:
            if file != None:
		file.close()
    elif kind == 1:                             # Generate output file
        try:
            if num is None:
                name = generate_name_file(1, path)
                final_path = path + name + '.txt'
                file = open(final_path, 'w')
            else:
                final_path = path + 'output_' + str(num) + '.txt'
                file = open(final_path, 'w')
            i = 1
            for elem in text:
                file.write("Caso " + str(i) + ": " + elem + "\n")
                i += 1
        finally:
            file.close()
    return final_path

if __name__ == "__main__":
    start = time()

    #generate_file(0, generate_input(100, False), "../../dataset/")
    #generate_file(1, ["0", "4", "14", "impossibile", "150"], "../../dataset/")

    print(time() - start)
