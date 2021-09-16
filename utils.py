import matplotlib.pyplot as plt
from matplotlib import pylab
import json
import cv2


class Robot:
    def __init__(self, name, start, goal, wait_around=False, first_wall=None):
        self.name = name
        self.start = start
        self.goal = goal
        self.wait_around = wait_around
        self.first_wall = first_wall

    def __str__(self):
        return str("name: " + self.name + "; start: " + str(self.start) + "; goal: " + str(self.goal))


def read_config_single(filename):
    with open(filename) as f:
        data = json.load(f)
        grid = cv2.imread(data["maze"], cv2.IMREAD_GRAYSCALE)
        grid = ((grid) / 255).astype(int)
        start = tuple(data["start"])
        goal = tuple(data["goal"])
        robot = Robot("r1", start, goal)
        return grid, robot


def choose(difficulty, num_robots):
    difficulty_strings = ['easy', 'medium', 'hard']
    if '1' < num_robots <= '6' and '0' <= difficulty <= '2':
        grid, robots = read_config_multi(difficulty_strings[int(difficulty)] + '_' + num_robots + 'r.json')
        return grid, robots
    else:
        print('Not available.')


def read_config_multi(filename):
    with open(filename) as f:
        data = json.load(f)
        grid = cv2.imread(data["maze"], cv2.IMREAD_GRAYSCALE)
        grid = ((grid) / 255).astype(int)
        robots = []
        for r in data["robots"]:
            robot = Robot(r["name"], tuple(r["start"]), tuple(r["goal"]))
            robots.append(robot)
        return grid, robots


def plot_planner(routes, robots, grid, type_obs, given_choice, reached_goal=None, difficulty=None, num_randoms=None, num_seed=None):
    if reached_goal is None:
        reached_goal = []
    fig, ax = plt.subplots(figsize=(20, 20))
    ax.imshow(grid, cmap='binary_r')
    if type(robots) is list:
        for robot in robots:
            start = robot.start
            goal = robot.goal
            name = robot.name
            ax.scatter(start[1], start[0], marker="o", color="blue", s=200)
            ax.scatter(goal[1], goal[0], marker="o", color="red", s=200)
            ax.text(start[1] + 0.5, start[0], name, color='blue')
            ax.text(goal[1] + 0.5, goal[0], name, color='red')
    else:
        start = robots.start
        goal = robots.goal
        name = robots.name
        ax.scatter(start[1], start[0], marker="o", color="blue", s=200)
        ax.scatter(goal[1], goal[0], marker="o", color="red", s=200)
        ax.text(start[1] + 0.5, start[0], "r1")
        ax.text(goal[1] + 0.5, goal[0], "r1")

    if type(robots) is list:
        colors = ['y', 'c', 'r', 'm', 'b', 'g']
        for robot in reached_goal:
            route = routes[robot]
            x_coords, y_coords = get_route_coord(route)
            index = reached_goal.index(robot)
            ax.plot(y_coords, x_coords, colors[index], linewidth=len(colors) - index + 1)
            if type_obs == '2' and given_choice == '0':
                pylab.savefig('/home/emina/github/mstar_files/rezultati' + '/' + 'r' + str(len(robots)) + '/' + str(
                    difficulty) + '/' +
                              str(num_randoms) + '/' + str(num_seed) + '.png')


def get_route_coord(route):
    x_coords = []
    y_coords = []
    for i in (range(0, len(route))):
        x = route[i].position[0]
        y = route[i].position[1]
        x_coords.append(x)
        y_coords.append(y)
    return x_coords, y_coords
