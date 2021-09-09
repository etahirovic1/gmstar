import heapq
import random

class Node:

    def __init__(self, parent=None, position=None, value=0):
        self.parent = parent
        self.position = position
        self.value = value
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        # return self.position == other
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

class Astar:

    def __init__(self, workspace, robots, given_choice, num_randoms=0, type_obs=0, num_seed=0, difficulty=0):

        self.starts = [[] for i in range(len(robots))]

        self.paths = [[] for i in range(len(robots))]

        self.children = [[] for i in range(len(robots))]

        self.open_lists = []
        self.closed_lists = []

        self.given_choice = given_choice
        self.num_randoms = num_randoms
        self.type_obs = type_obs
        self.num_seed = num_seed
        self.difficulty = difficulty

        for num_rob in range(len(robots)):
            self.open_list_i = []
            heapq.heapify(self.open_list_i)
            self.open_lists.append(self.open_list_i)

            self.closed_list_i = []
            heapq.heapify(self.closed_list_i)
            self.closed_lists.append(self.closed_list_i)

        self.neighbors = ((-1, -1), (1, -1), (1, 1), (-1, 1), (-1, 0), (0, 1), (1, 0), (0, -1), (0, 0))

        self.workspace = workspace

        self.robots = robots

    def randomise(self):

        start_positions = []
        end_positions = []

        for robot in self.robots:
            start_positions.append(robot.start)
            end_positions.append(robot.goal)

        randoms = []
        random.seed(int(self.num_seed))

        while len(randoms) != self.num_randoms:
            num = random.randint(0, (len(self.workspace)-1) * (len(self.workspace)-1))
            w = num % (len(self.workspace) - 1)
            h = int(num / (len(self.workspace)-1))
            tapl = (h, w)
            forbidden = [[], [(12, 8), (12, 15)], [(15, 11), (15, 12)]]
            if num not in randoms and tapl not in start_positions and tapl not in end_positions and \
                    self.workspace[h][w] != 1 and tapl not in forbidden[int(self.difficulty)]:
                randoms.append(num)
                self.workspace[h][w] = 1
            else:
                continue

    def choose_course(self):
        if self.given_choice == '0':
            self.randomise()
        elif self.given_choice == '1':
            if self.type_obs == '0':
                for h in range(len(self.workspace)):
                    for w in range(len(self.workspace)):
                        self.workspace[h][w] = 0
                self.randomise()
            elif self.type_obs == '1':
                return
            elif self.type_obs == '2':
                self.randomise()

    def return_path(self, current_node):

        path = []
        current = current_node

        while current is not None:
            path.append(current)
            current = current.parent

        return path[::-1]

    def run(self):

        self.choose_course()

        for ri in range(len(self.robots)):

            start = Node(None, self.robots[ri].start, 0)
            heapq.heappush(self.open_lists[ri], start)
            self.starts[ri] = start        
            iteration = 0

            while self.open_lists[ri]:

                if iteration > 3 * len(self.robots) * len(self.workspace):
                    self.paths[ri] = self.return_path(vk)
                    print('Put za robota broj', ri, 'nije pronađen unutar prihvatljivog vremena.')
                    break

                iteration = iteration + 1

                vk = heapq.heappop(self.open_lists[ri])
                heapq.heappush(self.closed_lists[ri], vk)

                if vk.position == self.robots[ri].goal:
                    self.paths[ri] = self.return_path(vk)
                    break

                for new_position in self.neighbors:

                    node_position = (vk.position[0] + new_position[0], vk.position[1] + new_position[1])

                    if node_position[0] > (len(self.workspace) - 1) or node_position[0] < 0 or node_position[1] > (
                            len(self.workspace[len(self.workspace)-1]) -1) or node_position[1] < 0:
                        continue

                    if self.workspace[node_position[0]][node_position[1]] != 0:
                        continue

                    new_node = Node(vk, node_position, 0)
                    self.children[ri].append(new_node)

                    if new_position[0] != 1 and new_position[1] != 1:
                        new_node.g = vk.g + 1.44
                    else:
                        new_node.g = vk.g + 1

                    new_node.h = (((new_node.position[0] - self.robots[ri].goal[0]) ** 2) + (
                            (new_node.position[1] - self.robots[ri].goal[1]) ** 2))**(1/2)
                    new_node.f = new_node.g + new_node.h

                    if new_node in self.closed_lists[ri]:
                        continue

                    for open_node in self.open_lists[ri]:
                        if new_node.position == open_node.position:
                            if new_node.g < open_node.g:
                                open_node.g = new_node.g
                                open_node.parent = new_node.parent
                            break

                    if new_node not in self.open_lists[ri]:
                        heapq.heappush(self.open_lists[ri], new_node)

        for path_index in range(len(self.paths)):
            if len(self.paths[path_index]) == 0:
                print('No path for robot', path_index+1)

        return self.paths
