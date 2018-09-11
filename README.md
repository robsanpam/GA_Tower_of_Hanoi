# GA for Tower of Hanoi

Solving the tower of hanoi problem with a genetic algorithm (GA). The goal of the problem is to move all disks from the first tower to the last, but you cannot place a larger disk onto a smaller disk.

## Requirements

Please make sure to install the following packages:

    pip install tqdm
    pip install numpy

## Running the algorithm

Please define the following execution parameters upon calling the script:

- populationSize: Integer number of chromosomes for each generation.
- generations: Integer number of generations to run the GA.
- cRate: Float probability of performing crossover with two chromosomes.
- mRate: Float probability of performing mutation on a chromosome.
- seed: Integer seed number for the pseudo-random number generator. If you write _ran_, the seed will be selected at random.
- towers: Integer number of towers for the tower of hanoi problem.
- disks: Intenger number of disks for the tower of hanoi problem.
- max_moves: Integer number of maximum moves allowed for the GA to solve the tower of hanoi problem.

For example:

    python hanoi_tower.py -populationSize=100 -generations=100 -cRate=1.0 -mRate=0.01 -seed=ran -towers=3 -disks=3 -max_moves=20

## Results

Each column represents a tower and each number a disk. Empty positions are represented with a '-'. The value of the number represents the size of the disk. In this way, a disk of size 2 cannot be on top of a disk size 1.

The script will print the step-by-step solution of the best chromosome. The fitness function is defined as the number of disks on the rightmost tower.
