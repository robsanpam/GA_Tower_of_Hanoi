import random
import numpy as np
import sys
from tqdm import tqdm


def main(argv):

    try:
        assert int(argv[6].split('=')[1].replace(" ", "")) <= int(
            argv[5].split('=')[1].replace(
                " ", "")), "Number of disks should be <= number of towers"
    except AssertionError as e:
        raise

    if str(argv[4].split('=')[1].replace(" ", "")) == 'ran':
        seed = random.random()
    else:
        seed = int(argv[4].split('=')[1].replace(" ", ""))

    geneticAlgorithm(
        populationSize=int(argv[0].split('=')[1].replace(" ", "")),
        generations=int(argv[1].split('=')[1].replace(" ", "")),
        cRate=float(argv[2].split('=')[1].replace(" ", "")),
        mRate=float(argv[3].split('=')[1].replace(" ", "")),
        seed=seed,
        towers=int(argv[5].split('=')[1].replace(" ", "")),
        disks=int(argv[6].split('=')[1].replace(" ", "")),
        max_moves=int(argv[7].split('=')[1].replace(" ", "")))


def geneticAlgorithm(populationSize, generations, cRate, mRate, seed, towers,
                     disks, max_moves):
    global nbBits
    global population
    global fitness
    global nb_bits_move
    global possible_moves

    pbar = tqdm(total=generations)
    nb_bits_move, nbBits, possible_moves = get_moves(towers, max_moves)

    population = ["" for x in range(populationSize)]
    fitness = [0 for x in range(populationSize)]
    random.seed(seed)
    bFitness = -9999
    solution = ""

    # Creates the initial population.
    for i in range(populationSize):
        population[i] = createIndividual()
        evaluate(i, towers, int(disks), 0)

    # Runs the genetic algorithm process
    for i in range(generations):
        pbar.update(1)
        tmpPopulation = ["" for x in range(populationSize)]

        for j in range(populationSize // 2):
            offspring = cross(select(5), select(5), cRate)
            tmpPopulation[j * 2] = offspring[0]
            tmpPopulation[j * 2 + 1] = offspring[1]

        population = tmpPopulation
        for j in range(populationSize):
            mutate(j, mRate)
            evaluate(j, towers, int(disks), 0)

        for j in range(populationSize):
            if fitness[j] > bFitness:
                bFitness = fitness[j]
                solution = population[j]
    print()
    print('Gene Solution')
    print(solution)
    print('Fitness')
    print(bFitness)
    evaluate(0, towers, disks, 1, sol=solution)


def createIndividual():
    individual = ""
    for i in range(nbBits):
        if random.random() < 0.5:
            individual = individual + "1"
        else:
            individual = individual + "0"
    return individual


def evaluate(index, towers, disks, visualize, sol=None):
    eval = 0
    game = np.full((disks, towers), '-')
    for i in range(disks):
        game[i][0] = i
    if visualize:
        print('-------------------------------')
        print("Game Start")
        print(game)
        element = sol
    element = population[index]
    for slice in range(len(element) // nb_bits_move):
        code = element[slice * nb_bits_move:
                       slice * nb_bits_move + nb_bits_move]
        if code in possible_moves.keys():
            move = possible_moves[code]
            if visualize:
                print('-------------------------------')
                print(move)
            game = doMove(game, move, disks, visualize)
            if visualize:
                print(game)
    if not visualize:
        for row in game:
            if row[-1] != '-':
                eval = eval + 1
        fitness[index] = eval


def doMove(game, move, disks, visualize):
    start_tower = int(move[0])
    end_tower = int(move[-1])
    start_disk = None
    index_start_disk = None

    # Look if game is completed
    completed = True
    for row in game:
        if row[-1] == '-':
            completed = False

    if completed:
        if visualize:
            print("Game completed, move ignored.")

    else:
        # Look if start_tower is empty
        if game[disks - 1][start_tower] == '-':
            if visualize:
                print("empty tower")

        else:
            # Look for the starting disk
            for i in range(disks):
                if game[i][start_tower] != '-':
                    start_disk = int(game[i][start_tower])
                    index_start_disk = i
                    break

            # Look if end_tower is empty
            if game[disks - 1][end_tower] == '-':
                game[disks - 1][end_tower] = start_disk
                game[index_start_disk][start_tower] = '-'

            else:
                # Look if disk can be put at end_tower
                for i in range(disks - 1):
                    if game[i][end_tower] == '-':
                        if game[i + 1][end_tower] != '-':
                            if int(game[i + 1][end_tower]) > start_disk:
                                game[i][end_tower] = str(start_disk)
                                game[index_start_disk][start_tower] = '-'
                                break
                            else:
                                if visualize:
                                    print("invalid move")
    return game


def select(tournamentSize):
    pSize = len(population)
    best = random.randint(0, pSize - 1)
    for i in range(tournamentSize - 1):
        candidate = random.randint(1, pSize - 1)
        if (fitness[candidate] > fitness[best]):
            best = candidate
    return best


def cross(indexA, indexB, cRate):
    parentA = population[indexA]
    parentB = population[indexB]
    if random.random() < cRate:
        cPoint = random.randint(1, nbBits - 1)
        offspring = ["" for x in range(2)]
        offspring[0] = parentA[:cPoint] + parentB[cPoint:]
        offspring[1] = parentB[:cPoint] + parentA[cPoint:]
    else:
        offspring = [parentA, parentB]
    return offspring


def get_moves(towers, max_moves):
    nb_poss_moves = towers * (towers - 1)
    nb_bits_move = np.int(np.ceil(np.log2(nb_poss_moves)))
    possible_moves = {}
    nbBits = np.ceil(max_moves * nb_bits_move)

    move = 0
    for tower in range(towers):
        a_other_towers = np.delete(np.arange(towers), tower)
        for other in range(towers - 1):
            possible_moves[np.binary_repr(
                move, nb_bits_move)] = "%d -> %d" % (tower,
                                                     a_other_towers[other])
            move += 1
    return int(nb_bits_move), int(nbBits), possible_moves


def mutate(index, mRate):
    tmp = ""
    for i in range(nbBits):
        if random.random() < mRate:
            if population[index][i] == '1':
                tmp = tmp + "0"
            else:
                tmp = tmp + "1"
        else:
            tmp = tmp + population[index][i]
    population[index] = tmp


if __name__ == '__main__':
    main(sys.argv[1:])
