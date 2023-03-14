from astar import astar, get_path, Node
import random
import os


def print_table(table, direct):
    print('\n{:5s} --------------\n'.format(direct))
    for i in range(len(table)):
        for j in range(len(table[0])):
            print('{:4d}'.format(table[i][j]), end='')
        print()


def node_move(node: Node, direct: str):
    if direct == 'UP':
        if not node.x > 0:
            return node, False
        node.table = node.move('UP')
        node.x, node.y = node.x - 1, node.y
        return node, True
    if direct == 'DOWN':
        if not node.x < node.height - 1:
            return node, False
        node.table = node.move('DOWN')
        node.x, node.y = node.x + 1, node.y
        return node, True
    if direct == 'LEFT':
        if not node.y > 0:
            return node, False
        node.table = node.move('LEFT')
        node.x, node.y = node.x, node.y - 1
        return node, True
    if direct == 'RIGHT':
        if not node.y < node.width - 1:
            return node, False
        node.table = node.move('RIGHT')
        node.x, node.y = node.x, node.y + 1
        return node, True


def print_path(path_list):
    print('\n\nNum of Steps:', len(path_list) - 1)
    print('\n\nNum of Extended Nodes:', Node.extend_num)
    for path in path_list:
        p, d = path
        print('\n{:5s} --------------\n'.format(d))
        for i in range(len(p)):
            for j in range(len(p[0])):
                print('{:4d}'.format(p[i][j]), end='')
            print()
    return


def main():
    end_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    Node.end_state = end_state
    root = Node(end_state, depth=0)

    diff = input('Difficulty: s(simple)/m(medium)/h(hard) ')
    start, end = 0, 0
    if diff == 's':
        start, end, target = 10, 20, 10
    elif diff == 'm':
        start, end, target = 15, 25, 15
    elif diff == 'h':
        start, end, target = 25, 35, 25
    else:
        print('PLEASE SELECT s/m/h')
        return

    start_state = None
    num_step = random.randint(start, end)
    while True:
        step_ctr = 0
        while step_ctr < num_step:
            direct = random.random()
            result = True
            if direct < 0.25 and root.x > 0:
                root, result = node_move(root, 'UP')
            elif direct < 0.5 and root.x < root.height - 1:
                root, result = node_move(root, 'DOWN')
            elif direct < 0.75 and root.y > 0:
                root, result = node_move(root, 'LEFT')
            elif direct <= 1 and root.y < root.width - 1:
                root, result = node_move(root, 'RIGHT')
            if result:
                step_ctr += 1
        final_node = astar(root.table, root.end_state, revisit=False)
        path_list = get_path(final_node)
        if len(path_list) >= target and len(path_list) <= target + 5:
            start_state = root.table
            break

    print_table(start_state, 'INIT')

    step_ctr = 0
    while not root.is_end():
        direct = input('DIRECT (w/a/s/d) or ANSWER (p): ').strip()
        if direct == 'w':
            root, result = node_move(root, 'UP')
            if not result:
                continue
        elif direct == 's':
            root, result = node_move(root, 'DOWN')
            if not result:
                continue
        elif direct == 'a':
            root, result = node_move(root, 'LEFT')
            if not result:
                continue
        elif direct == 'd':
            root, result = node_move(root, 'RIGHT')
            if not result:
                continue
        elif direct == 'p':
            final_node = astar(root.table, root.end_state, revisit=False)
            path_list = get_path(final_node)
            print('\n\n===============ANSWER===============\n\n')
            print_path(path_list)
            return
        else:
            continue
        step_ctr += 1
        print_table(root.table, str(step_ctr))
    print('\n\nCongratulations! You have completed this task!\n\n')


if __name__ == '__main__':
    main()
    while True:
        input()
