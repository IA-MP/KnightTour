import os
from time import time
import sys
from libs.IO.input_generator import generate_input

from libs.IO.input_reading import make_matches
from libs.IO.txt_generator import generate_file
from montagna import montagna

commands = dict(q=(lambda: so_long_and_thanks()),
                b=(lambda: best_algorithm()),
                g=(lambda: call_graph()),
                m=(lambda: call_maometto()))

def so_long_and_thanks():
    raise SystemExit()

def and_so_it_begins():
    print("")
    print("-------------------------------------------------------------------")
    print("              PROGETTO: 'K-CAVALLO CHE L'ERBA CRESCE!'             ")
    print("")
    print("\n"
          "        Alessio Moretti (0187698)  -  alessio.moretti@live.it\n"
          "      Claudio Pastorini (0186256)  -  pastorini.claudio@gmail.com")
    print("-------------------------------------------------------------------\n")
    inp = raw_input("Utilizzare la soluzione proposta (S) o accedere al menu' generale (N)? ")
    inp = inp.lower()
    while True:
        if inp == 's' or inp == 'n':
            break
        inp = raw_input("Utilizzare la soluzione proposta (S) o accedere al menu' generale (N)? ")
        inp = inp.lower()
    if inp == "s":
        commands['b']()
    else:
        coms = "\nInserire uno dei seguenti comandi:\ng -> soluzioni basate sul grafo delle mosse\nm -> soluzione basata sul calcolo del target\nq -> quit\n"
        while True:
            print(coms)
            choice = raw_input("Inserisci una opzione: ")
            choice = choice.lower()
            if choice in commands:
                commands[choice]()
            else:
                print("Si prega di scegliere una delle opzioni del menu'...")


def best_algorithm():
    global filename_input
    ok = False
    while not ok:
        filename_input = call_generate()
        if filename_input is not None:
            ok = True

    path_output = raw_input("Dove salvare il file di output? ")
    path_output = path_output if path_output[-1] == "/" else path_output + "/"

    matches = make_matches(filename_input)
 
    start = time()
    outs = []
    for match in matches:
        g = match.makeGraphBFS()
	if str(g) == 'inf':
           g = 'impossibile'
	outs.append(str(g))
    print "\nAlgoritmo eseguito: BFS dal grafo delle mosse"
    print "Tempo d'esecuzione:", time() - start, "secondi\n"
    generate_file(1, outs, path_output)
    raise SystemExit()

def bfs():
    global filename_input
    ok = False
    while not ok:
        filename_input = call_generate()
        if filename_input is not None:
            ok = True

    path_output = raw_input("Dove salvare il file di output? ")
    path_output = path_output if path_output[-1] == "/" else path_output + "/"

    matches = make_matches(filename_input)
 
    start = time()
    outs = []
    for match in matches:
        match.makeGraph()
	m = match.minMovesBFS()
	if str(m) == 'inf':
           m = 'impossibile'
	outs.append(str(m))
    print "\nAlgoritmo eseguito: BFS sul grafo delle mosse"
    print "Tempo d'esecuzione:", time() - start, "secondi\n"
    generate_file(1, outs, path_output)
    raise SystemExit()

def dijkstra():
    global filename_input
    ok = False
    while not ok:
        filename_input = call_generate()
        if filename_input is not None:
            ok = True

    path_output = raw_input("Dove salvare il file di output? ")
    path_output = path_output if path_output[-1] == "/" else path_output + "/"

    matches = make_matches(filename_input)
 
    start = time()
    outs = []
    for match in matches:
        match.makeGraph()
	m = match.minMovesDijkstra()
	if str(m) == 'inf':
           m = 'impossibile'
	outs.append(str(m))
    print "\nAlgoritmo eseguito: Dijkstra sul grafo delle mosse"
    print "Tempo d'esecuzione:", time() - start, "secondi\n"
    generate_file(1, outs, path_output)
    raise SystemExit()

def floyd_warshall():
    global filename_input
    ok = False
    while not ok:
        filename_input = call_generate()
        if filename_input is not None:
            ok = True

    path_output = raw_input("Dove salvare il file di output? ")
    path_output = path_output if path_output[-1] == "/" else path_output + "/"

    matches = make_matches(filename_input)
 
    start = time()
    outs = []
    for match in matches:
        match.makeGraph()
	m = match.minMovesFloydWarshall()
	if str(m) == 'inf':
           m = 'impossibile'
	outs.append(str(m))
    print "\nAlgoritmo eseguito: Floyd-Warshall sul grafo delle mosse"
    print "Tempo d'esecuzione:", time() - start, "secondi\n"
    generate_file(1, outs, path_output)
    raise SystemExit()

def graph_menu():
    print("")
    print("-------------------------------------------------------------------")
    print("               ALGORITMI BASATI SU GRAFO DELLE MOSSE               ")
    print("-------------------------------------------------------------------")
    print("\nIn questa sezione sara' possibile studiare il problema iniziale a\n"
          "partire dalla costruzione di un grafo delle possibili mosse. In particolare\n"
          "si potra' risolvere il problema con uno dei possibili algoritmi: \n"
          "\n 1.BFS by GRAPH -> grafo delle mosse come visita in ampiezza (the chosen one)"
          "\n 2.BFS on GRAPH -> visita in ampiezza del grafo delle mosse"
          "\n 3.DIJKSTRA -> ricerca del cammino minimo da un gruppo di sorgenti"
          "\n 4.FLOYD-WARSHALL -> ricerca del cammino minimo tra tutti i nodi del grafo\n")
    return


def call_graph():
    graph_menu()
    algorithms = dict([('1', lambda: best_algorithm()), 
		       ('2', lambda: bfs()), 
                       ('3', lambda: dijkstra()), 
                       ('4', lambda: floyd_warshall())])
    alg = raw_input("Scegliere un algoritmo (da 1 a 4): ")
    while alg not in algorithms:
         print("Si prega di scegliere entro i limiti delle opzioni proposte")
         alg = raw_input("Scegliere un algoritmo (da 1 a 4): ")
    algorithms[alg]()
    return



def maometto_menu():
    print("")
    print("-------------------------------------------------------------------")
    print("                     ALGORITMO DELLA MONTAGNA                      ")
    print("          (ovvero, 'come far incontrare degli amici al bar')       ")
    print("-------------------------------------------------------------------")


def call_maometto():
    maometto_menu()
    global filename_input
    ok = False
    while not ok:
        filename_input = call_generate()
        if filename_input is not None:
            ok = True

    path_output = raw_input("Dove salvare il file di output? ")
    path_output = path_output if path_output[-1] == "/" else path_output + "/"

    print("")
    print("-------------------------------------------------------------------")
    print("             TARGET della DISTRIBUZIONE - ISTRUZIONI               ")
    print("-------------------------------------------------------------------")
    print("\nCome spiegato nella relazione abbiamo implementato piu'\n"
	     "generatori di targetes. Quale generatore di targets usare?\n"
	     "(0 per avere un solo target, 1 per avere target con un intorno\n"
	     "di 1 casella (default), 2 per avere con un intorno di 2 caselle,\n"
	     "3 per avere target con target e le posizioni dei cavalli e \n"
	     "4 per avere tutta la scacchiera\n")
    type = int(raw_input("Inserire una tipologia di target: "))
    if type < 0 or type > 4:
        type = 1
	print("Abbiamo scelto per te il generatore di default!\n")
    
    matches = make_matches(filename_input)

    start = time()
    outs = []
    for match in matches:
        montagna(match, int(type), outs, False)
    print "\nAlgoritmo eseguito: Montagna"
    print "Tempo d'esecuzione:", time() - start, "secondi\n"
    generate_file(1, outs, path_output)
    raise SystemExit()


def generate_menu():
    print("")
    print("-------------------------------------------------------------------")
    print("                  GENERATORE DI INPUT - ISTRUZIONI                 ")
    print("-------------------------------------------------------------------")
    print("\nGli input che e' possibile creare in questa sezione variano sia per\n"
          "numero di casi presenti, variando sia la densita' dei cavalli presenti\n"
          "sulla scacchiera, sia il valore dei k-cavalli. Ricordiamo che un k-cavallo\n"
          "e' un cavallo particolare che puo' eseguire al piu' k mosse in un turno.\n"
          "Una serie di passaggi vi guidera' nella scelta del caso da generare\n")
    return

def call_generate():
    global density, k
    density = 7
    k = 1
    generate = raw_input("Generare un nuovo input? (S/N) ")
    generate = generate.lower()
    if generate == "s":
        generate_menu()
        num = raw_input("Quanti casi generare? (<= 100) ")
	if int(num) < 1 or int(num) > 100:
		print("Si prega di seguire le istruzioni, scegliere una opzione valida (da 1 a 100)")
		return None
        path_input = raw_input("Dove salvare il file? ")
        path_input = path_input if path_input[-1] == "/" else path_input + "/"
        re_density = raw_input("Generare le scacchiere con una densita' prefissata? (S/N) ")
        re_density = re_density.lower()
        if re_density == "n":
            req_density = raw_input("Con quale densita' generare le scacchiere? (Disponibili 1:10% 2:20% 3:30% 4:40% 5:100%) ")
            if req_density == "1":
                density = 6
            elif req_density == "2":
                density = 5
            elif req_density == "3":
                density = 3
            elif req_density == "4":
                density = 2
            elif req_density == "5":
                density = 1
	    else:
            	print("Si prega di seguire le istruzioni, scegliere una opzione valida (da 1 a 5)")
            	return None
        elif re_density == "s":
            density = 7
        else:
            print("Si prega di seguire le istruzioni, inserire o S (o s) o N (o n)")
            return None
        re_k_rand = raw_input("Generare il match con un k casuale? (S/N) ")
        re_k_rand = re_k_rand.lower()
        if re_k_rand == "n":
            k_rand = False
            k = raw_input("Scegliere un k da 1 a 9 ")
            if len(k) > 1:
		k = k[0]
            k = int(k)
	    if k < 0  or k > 9:
		print("Si prega di seguire le istruzioni, inserire una opzione valide (da 1 a 9)")
                return None
        elif re_k_rand == "s":
            k_rand = True
            k = 1
        else:
            print("Si prega di seguire le istruzioni, inserire o S (o s) o N (o n)")
            return None
        filename_input = generate_file(0, generate_input(int(num), density, k_rand, k, False), path_input)

    elif generate == "n":
        ok = False
        while not ok:
            filename_input = raw_input("Quale file usare? ")
            filename_input = filename_input if filename_input[-4:] == ".txt" else filename_input + ".txt"
	    if not os.path.exists(filename_input):
                print("Non esiste nessun file con questo nome!")
            else:
                ok = True
    else:
        print("Si prega di seguire le istruzioni, inserire o S (o s) o N (o n)")
        return None

    return filename_input


if __name__ == "__main__":
    and_so_it_begins()
