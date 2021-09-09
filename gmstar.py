from astar_multi import Node
import heapq
from timeit import default_timer as timer
from datetime import timedelta
from itertools import product

class Configuration:

    def __init__(self, nodes=None, back_ptr=None, cost=0, collision_set=None, backprop_set=None):
        if collision_set is None:
            collision_set = set()
        if backprop_set is None:
            backprop_set = set()
        self.nodes = nodes
        self.back_ptr = back_ptr
        self.cost = cost
        self.collision_set = collision_set
        self.backprop_set = backprop_set

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost


class GMstar:

    def __init__(self, workspace, robots, paths, num_robots):

        self.workspace = workspace
        self.robots = robots
        self.paths = paths
        self.num_robots = num_robots

        self.open_list = []
        heapq.heapify(self.open_list)

        self.all_configurations = []
        self.intersection = False
        self.MAX_COST = 0
        self.collided = False
        self.longest_path_length = 0

        self.forbid = [[] for i in range(int(self.num_robots))]

        self.goal_config = []
        self.start_config = []

        self.reached_goal = []

        self.neighbors = (
            (1, 1), (0, 1), (1, -1), (-1, -1), (-1, 1), (-1, 0), (1, 0), (0, -1), (0, 0))

    def repeat(self, temp_config, route, short):

        temp_config = temp_config.back_ptr
        forbid = short
        short = temp_config.nodes[route].position

        return temp_config, short, forbid

    def unstuck(self, problem_config):

        for route in range(int(self.num_robots)):

            temp_config = Configuration(problem_config.nodes, problem_config.back_ptr)

            if problem_config.nodes[route].position != self.goal_config.nodes[route].position:

                _, short, temp = self.repeat(temp_config, route, None)

                while short != self.robots[route].first_wall[1]:
                    temp_config, short, temp = self.repeat(temp_config, route, short)

                self.forbid[route].append(temp)
                self.open_list = []
                heapq.heapify(self.open_list)
                heapq.heappush(self.open_list, temp_config)

    def back_track(self, current_config, start):

        end = timer()

        time_of_mstar = timedelta(seconds=end-start)

        print('Vrijeme za koje je pronađen put: ', time_of_mstar)

        self.paths = [[] for i in range(int(self.num_robots))]

        for path_index in range(int(self.num_robots)):

            current = current_config

            while current is not None:
                self.paths[path_index].append(current.nodes[path_index])
                current = current.back_ptr

            self.paths[path_index] = self.paths[path_index][::-1]
            '''it = 0
            print('path ', path_index, ': ')
            for p in self.paths[path_index]:
                print('point ', it, ': ', p)
                it = it + 1'''

        return self.paths, self.reached_goal, time_of_mstar

    def assemble_configurations(self):

        for path in self.paths:
            if len(path) > self.longest_path_length:
                self.longest_path_length = len(path)

        previous_config = None

        for i in range(self.longest_path_length):

            temp_config = [() for c in range(int(self.num_robots))]
            cost = 0

            for j in range(int(self.num_robots)):
                if len(self.paths[j]) - 1 > i:
                    node = self.paths[j][i]
                else:
                    node = self.paths[j][len(self.paths[j]) - 1]

                temp_config[j] = node
                cost = cost + node.f

            if cost > self.MAX_COST:
                self.MAX_COST = cost

            previous_config = Configuration(temp_config, previous_config, cost)
            self.all_configurations.append(previous_config)

    def find_node_cost(self, node, parent, config, node_index):

        if parent is None:
            node.g = 0
            node.h = 0
        else:
            c = config.back_ptr
            do_not_use = False
            while c is not None:
                if c.nodes[node_index].position == config.nodes[node_index].position and \
                        c.nodes[node_index].position != self.goal_config.nodes[node_index].position and \
                        self.robots[node_index].wait_around is not True:
                    node.g = parent.nodes[node_index].g + 1000
                    do_not_use = True
                    break
                c = c.back_ptr
            if not do_not_use:
                if node.position != parent.nodes[node_index].position:
                    node.g = parent.nodes[node_index].g + 1
                else:
                    node.g = parent.nodes[node_index].g
            node.h = ((node.position[0] - self.robots[node_index].goal[0]) ** 2 +
                      (node.position[1] - self.robots[node_index].goal[1]) ** 2) ** (1 / 2)
        node.f = node.g + node.h

    def find_config_cost(self, parent, config):
        cost = 0
        for node_index in range(len(config.nodes)):
            self.find_node_cost(config.nodes[node_index], parent, config, node_index)
            cost = cost + config.nodes[node_index].f
        config.cost = cost

    def generate_neighbors_with_colls(self, all_neighbors, vm):

        all_neighbors_nodes = [[] for i in range(len(all_neighbors))]
        all_neighbors_with_cost = []
        heapq.heapify(all_neighbors_with_cost)

        for neighbor in range(len(all_neighbors)):

            for n in range(len(all_neighbors[neighbor])):
                node = Node(vm.nodes[n], all_neighbors[neighbor][n], 0)
                all_neighbors_nodes[neighbor].append(node)

            conf = Configuration(all_neighbors_nodes[neighbor], vm)
            self.find_config_cost(vm, conf)
            heapq.heappush(all_neighbors_with_cost, conf)

        return all_neighbors_with_cost

    def generate_node_neighbors(self, node, i):

        all_children_of_node = []

        for new_position in self.neighbors:

            node_position = (node.position[0] + new_position[0], node.position[1] + new_position[1])

            if node_position[0] > (len(self.workspace) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(self.workspace[len(self.workspace) - 1]) - 1) or node_position[1] < 0:
                continue

            if self.workspace[node_position[0]][node_position[1]] != 0:
                if self.robots[i].first_wall is None:
                    self.robots[i].first_wall = [node_position, node.position]
                continue

            pos = (node_position[0], node_position[1])

            if node_position in self.forbid[i]:
                continue

            all_children_of_node.append(pos)

        return all_children_of_node

    def generate_neighbors(self, vm):

        all_children_list = [[] for c in range(len(vm.nodes))]

        for i in range(len(vm.nodes)):

            node = vm.nodes[i]

            if node.position == self.goal_config.nodes[i].position:
                all_children_list[i] = [node.position]
                for element in self.open_list:
                    element.nodes[i] = node
                continue

            all_children_list[i] = self.generate_node_neighbors(node, i)

        all_neighbors = list(product(*all_children_list))
        all_neighbors_with_cost = self.generate_neighbors_with_colls(all_neighbors, vm)

        return all_neighbors_with_cost

    def update_collision_sets(self, config):

        config.collision_set = set()
        for c in range(int(self.num_robots)):
            for c1 in range(c + 1, int(self.num_robots)):
                if config.nodes[c].position == config.nodes[c1].position:
                    config.collision_set.add(c)
                    config.collision_set.add(c1)

    def zero_check(self, a, b, c, d):
        if (a - b) == 0:
            return 0
        else:
            return (c - d) / (a - b)

    def find_intersections(self, vk, vl):

        for r1 in range(int(self.num_robots)):
            for r2 in range(r1 + 1, int(self.num_robots)):

                vk_1 = vk.nodes[r1].position; vk_2 = vk.nodes[r2].position
                vl_1 = vl.nodes[r1].position; vl_2 = vl.nodes[r2].position

                if vk_1 == vl_2 and vk_2 == vl_1:
                    self.intersection = True
                    self.robots[r1].wait_around = True
                    return

                if vk_1 == vl_2 or vk_2 == vl_1:
                    continue

                if (vk_1 == vl_1 and vk_1 != vl_2 or vk_2 == vl_2 and vk_2 != vl_1) and vk_2 != vk_1:
                    continue

                y1 = vk_1[0]; x1 = vk_1[1]
                y2 = vk_2[0]; x2 = vk_2[1]
                y3 = vl_1[0]; x3 = vl_1[1]
                y4 = vl_2[0]; x4 = vl_2[1]

                if y1 == y4 and y2 == y3 and x1 == x2 and x3 == x4 or y1 == y2 and y3 == y4 and x1 == x4 and x2 == y3:
                    self.intersection = True
                    self.robots[r1].wait_around = True

    def keep_optimal_paths(self, vk):

        vl = self.all_configurations[self.all_configurations.index(vk) + 1]

        self.update_collision_sets(vl)
        self.find_intersections(vk, vl)

        if len(vl.collision_set) == 0 and not self.intersection:
            vl.back_ptr = vk
            if vl not in self.open_list:
                heapq.heappush(self.open_list, vl)
                return True

        return False

    def robot_reached_goal(self, vk):
        for node in vk.nodes:
            if node.position == self.goal_config.nodes[vk.nodes.index(node)].position:
                if vk.nodes.index(node) not in self.reached_goal:
                    self.reached_goal.append(vk.nodes.index(node))

    def run(self):

        self.assemble_configurations()
        self.start_config = self.all_configurations[0]
        self.goal_config = self.all_configurations[len(self.all_configurations)-1]
        heapq.heappush(self.open_list, self.start_config)

        iteration = 0

        start = timer()

        while len(self.open_list) != 0:  # open_list is on the level of configurations

            vk = heapq.heappop(self.open_list)
            self.robot_reached_goal(vk)

            iteration = iteration + 1

            if vk.nodes == self.goal_config.nodes:
                return self.back_track(vk, start)

            if iteration > int(self.num_robots) * len(self.workspace):
                print('Putevi nisu pronađeni')
                break

            if not self.collided:
                if self.keep_optimal_paths(vk):
                    continue

            vk_nbh = self.generate_neighbors(vk)
            self.collided = True

            while len(vk_nbh) != 0:

                vl = heapq.heappop(vk_nbh)

                self.update_collision_sets(vl)
                self.find_config_cost(vk.back_ptr, vk)
                self.find_config_cost(vk, vl)

                if len(vl.collision_set) == 0:
                    self.find_intersections(vk, vl)
                    if self.intersection:
                        self.intersection = False
                        for robot_index in range(int(self.num_robots)):
                            self.robots[robot_index].wait_around = False
                        continue

                    vl.back_ptr = vk
                    if vl not in self.open_list:
                        heapq.heappush(self.open_list, vl)
                        break

        return
