from bisect import insort
import copy
import time


class Node:
    end_state = None
    width, height = 0, 0
    extend_num = 0
    scale = 0.6

    def __init__(self, table: list, x: int = -1, y: int = -1, depth: int = 0, parent=None, direct=None) -> None:
        self.x, self.y = -1, -1
        if Node.width == Node.height == 0:
            Node.width, Node.height = len(table), len(table[0])
        if x != -1 and y != -1:
            self.x, self.y = x, y
        else:
            for i in range(Node.width):
                for j in range(Node.height):
                    if table[i][j] == 0:
                        self.x, self.y = i, j
        self.table = table
        self.depth = depth
        self.parent = parent
        self.direct = direct
        self.id = '-'.join(map(str, table))
        self.f = self.F()

    def __eq__(self, other):
        return self.id == other.id if other is not None else False

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self) -> str:
        return str(self.f)

    def extend(self):
        table_list = []
        if self.x > 0:
            table_list.append(Node(self.move('UP'), self.x - 1, self.y, self.depth + 1, self, 'UP'))
        if self.x < self.height - 1:
            table_list.append(Node(self.move('DOWN'), self.x + 1, self.y, self.depth + 1, self, 'DOWN'))
        if self.y > 0:
            table_list.append(Node(self.move('LEFT'), self.x, self.y - 1, self.depth + 1, self, 'LEFT'))
        if self.y < self.width - 1:
            table_list.append(Node(self.move('RIGHT'), self.x, self.y + 1, self.depth + 1, self, 'RIGHT'))
        Node.extend_num += len(table_list)
        return table_list

    def move(self, direct):
        new_table = copy.deepcopy(self.table)
        if direct == 'LEFT':
            new_table[self.x][self.y], new_table[self.x][self.y - 1] = new_table[self.x][self.y - 1], new_table[self.x][self.y]
        elif direct == 'RIGHT':
            new_table[self.x][self.y], new_table[self.x][self.y + 1] = new_table[self.x][self.y + 1], new_table[self.x][self.y]
        elif direct == 'UP':
            new_table[self.x][self.y], new_table[self.x - 1][self.y] = new_table[self.x - 1][self.y], new_table[self.x][self.y]
        elif direct == 'DOWN':
            new_table[self.x][self.y], new_table[self.x + 1][self.y] = new_table[self.x + 1][self.y], new_table[self.x][self.y]
        return new_table

    def F(self):
        return Node.scale * M_dist(self.table, Node.end_state, Node.width, Node.height) + (1 - Node.scale) * self.depth

    def is_end(self):
        return self.table == Node.end_state


def M_dist(a: list, b: list, width: int, height: int):
    a_dict, total = dict(), 0
    for i in range(height):
        for j in range(width):
            a_dict[a[i][j]] = (i, j)
    for i in range(height):
        for j in range(width):
            ax, ay = a_dict[b[i][j]]
            total += (abs(i - ax) + abs(j - ay))
    return total


def E_dist(a: list, b: list, width: int, height: int):
    a_dict, total = dict(), 0
    for i in range(height):
        for j in range(width):
            a_dict[a[i][j]] = (i, j)
    for i in range(height):
        for j in range(width):
            ax, ay = a_dict[b[i][j]]
            total += ((i - ax)**2 + (j - ay)**2)
    return total


def E_count(a: list, b: list, width: int, height: int):
    a_dict, total = dict(), 0
    for i in range(height):
        for j in range(width):
            a_dict[a[i][j]] = (i, j)
    for i in range(height):
        for j in range(width):
            ax, ay = a_dict[b[i][j]]
            if i != ax or j != ay:
                total += 1
    return total


def astar(start_state, end_state, revisit=True):
    start_time = time.perf_counter_ns()
    Node.scale = 0.6
    Node.end_state = end_state
    root = Node(start_state, depth=0)
    opened_list, closed_list = [], []
    # use dict to find specific table
    opened_dict, closed_dict = dict(), dict()
    # insert root node into open_list
    insort(opened_list, root)
    opened_dict[root.id] = root
    while True:
        # opened_list is empty means NoAnswer
        if len(opened_list) == 0:
            raise Exception('NoAnswer')
        # pop the first element from opened_list
        current = opened_list.pop(0)
        opened_dict.pop(current.id)
        # push it into closed_list
        insort(closed_list, current)
        closed_dict[current.id] = current
        # Is current node the answer
        if current.is_end():
            # TODO
            # print('\nUsing Time: {} ms'.format((time.perf_counter_ns() - start_time) / 1000000))
            return current
        # extend current node
        nodes = current.extend()
        for node in nodes:
            if node.id not in closed_dict:
                if node.id not in opened_dict:
                    # node is in neither opened_list nor closed_list
                    insort(opened_list, node)
                    opened_dict[node.id] = node
                else:
                    # node is in opened_list
                    old = opened_dict[node.id]
                    if node.f < old.f:
                        # refresh table's node
                        opened_list.remove(old)
                        insort(opened_list, node)
                        opened_dict[node.id] = node
            else:
                if not revisit:
                    continue
                # node is in closed_list
                closed_list.remove(node)
                closed_dict.pop(node.id)
                insort(opened_list, node)
                opened_dict[node.id] = node
        # TODO
        # print('\ropen_list: {}, closed_list: {}, extended: {}, current depth: {}'.format(len(opened_list), len(closed_list), Node.extend_num, current.depth), end='')


def get_path(final_node):
    path_list = []
    while (1):
        if final_node.direct == None:
            path_list.insert(0, [final_node.table, 'INIT'])
            break
        path_list.insert(0, [final_node.table, final_node.direct])
        final_node = final_node.parent
    return path_list


def print_path(path_list):
    print('\n\nNum of Steps:', len(path_list) - 1)
    print('\n\nNum of Extended Nodes:', Node.extend_num)
    for path in path_list:
        p, d = path
        print('\n{:5s} --------------\n'.format(d))
        for i in range(len(start_state)):
            for j in range(len(start_state[0])):
                print('{:4d}'.format(p[i][j]), end='')
            print()
    return


if __name__ == '__main__':
    start_state = [[11, 9, 4, 15], [1, 3, 0, 12], [7, 5, 8, 6], [13, 2, 10, 14]]  # ppt
    # start_state = [[11, 5, 9, 13], [2, 6, 10, 14], [3, 7, 0, 15], [4, 8, 12, 1]]  # impossible
    # start_state = [[2, 5, 4, 8], [1, 7, 0, 3], [10, 6, 15, 14], [9, 13, 12, 11]]  # very hard
    # start_state = [[5, 1, 2, 4], [9, 6, 3, 8], [13, 15, 10, 11], [0, 14, 7, 12]]  # hard
    end_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

    # start_state = [[2, 8, 3], [1, 0, 4], [7, 6, 5]]
    # end_state = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

    final_node = astar(start_state, end_state, revisit=False)
    path_list = get_path(final_node)
    print_path(path_list)
