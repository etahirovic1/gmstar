from gmstar import GMstar
from astar_multi import Astar
from utils_my import *


def reverse(grid):
    for h in range(len(grid)):
        for w in range(len(grid[h])):
            grid[h][w] = abs(grid[h][w] - 1)
    return grid


def quit_it():
    print('Neispravan unos.')
    quit()


def run_all():

    grid, robots = choose(difficulty, num_robots)
    grid = reverse(grid)
    planner = Astar(grid, robots, given_choice, num_randoms, type_obs, num_seed, difficulty)

    routes = planner.run()

    planner = GMstar(grid, robots, routes, num_robots)

    routes, reached_goal, time_of_mstar = planner.run()

    grid = reverse(grid)
    plot_planner(routes, robots, grid, type_obs, reached_goal, difficulty, num_randoms, num_seed)
    return time_of_mstar


given_choice = input('Da li želite mjerenje performansi - 0 ili jedan sistem po izboru - 1?\n')
if given_choice != '1' and given_choice != '0':
    quit_it()

num_robots = input('Unesite broj robota (od 2 do 6):\n')
if not ('2' <= num_robots <= '6'):
    quit_it()

difficulty = input('Odaberite težinu prepreke (0 - easy, 1 - medium, 2 - hard):\n')
if not ('0' <= difficulty <= '2'):
    quit_it()

if given_choice == '1':

    num_randoms = 0
    num_seed = 0

    type_obs = input('Odaberite tip prepreke: (0 - nasumična, 1 - standardizirana, 2 - kombinirana):\n')

    if not ('0' <= type_obs <= '2'):
        quit_it()

    if int(type_obs) == 0 or int(type_obs) == 2:
        num_randoms = int(input('Unesite broj nasumičnih prepreka od (1 do 200):\n'))
        num_seed = int(input('Unesite vrijednost za seed:\n'))
        run_all()

    elif int(type_obs) == 1:
        run_all()

else:

    type_obs = input('Odaberite tip prepreke: (1 - standardizirana, 2 - kombinirana):\n')
    if not ('0' <= type_obs <= '2'):
        quit_it()

    if type_obs == '2':

        num_randoms = int(input('Unesite broj nasumičnih prepreka (40, 80, 160 ili 200):\n'))
        if num_randoms not in [40, 80, 160, 200]:
            quit_it()

        num_seeds = [2, 6, 8]

        for num_seed in num_seeds:

            fhandle = open('podaci' + str(num_robots) + '_' + str(difficulty) +
                           '_' + str(num_seed) + '_' + str(num_randoms) + '.txt', 'w')

            for it in range(0, 10):

                try:
                    time_of_m = run_all()
                except:
                    print('Putevi nisu pronađeni za seed =', num_seed)
                    break
                fhandle.write('Broj robota: ' + str(num_robots) + '\n')
                fhandle.write('Težina prepreke: ' + str(difficulty) + '\n')
                fhandle.write('Tip prepreke: ' + str(type_obs) + '\n')
                fhandle.write('Broj nasumičnih prepreka: ' + str(num_randoms) + '\n')
                fhandle.write('Seed: ' + str(num_seed) + '\n')
                fhandle.write('Vrijeme izvršavanja: ' + str(time_of_m) + '\n' + '\n')

            fhandle.close()

    elif type_obs == '1':

        num_randoms = 0
        num_seed = 0
        fhandle = open('podaci' + str(num_robots) + '_' + str(difficulty) + '.txt', 'w')
        for i in range(0, 10):
            time_of_m = run_all()
            fhandle.write('Vrijeme izvršavanja: ' + str(time_of_m) + '\n')
        fhandle.close()

    else:
        print('Nepravilan unos.')
