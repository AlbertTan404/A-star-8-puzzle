from copy import deepcopy
import heapq


BLANK_CHAR = '_'
H_METHOD = 'h1'
TARGET = []


def input_chessboard(n):
    print('please input the initial chessboard, fill the blank with {}'.format(BLANK_CHAR))
    
    res = []
    for _ in range(n):
        temp = input().split(' ')

        if len(temp) != n:
            raise ValueError('error input length')

        res.append([int(i) for i in temp])

    return res


def get_target(n):
    arr = []
    for i in range(n):
        arr.append([0] * n)
    row = 0
    col = 0

    arr[row][col] = 1

    i = 1
    while i < n * n - 1:
        while col + 1 < n and (not arr[row][col + 1]):
            arr[row][col + 1] = i + 1
            col += 1
            i += 1
        while row + 1 < n and (not arr[row+1][col]):
            arr[row + 1][col] = i + 1
            row += 1
            i += 1
        while col - 1 > -1 and (not arr[row][col - 1]):
            arr[row][col - 1] = i + 1
            col -= 1
            i += 1
        while row - 1 > -1 and (not arr[row - 1][col]):
            arr[row - 1][col] = i + 1
            row -= 1
            i += 1

    arr[n // 2][n // 2] = '_'
    
    return arr


class Node:
    def __init__(
        self,
        chessboard,
        g_val,
        last_step=0,
        father=None
    ) -> None:
        
        self.chessboard = chessboard
        self.n = len(chessboard)

        self.g_val = g_val
        self.h_val = self.get_h()
        self.f_val = self.cal_f()
        self.last_step_flag = last_step
        self.father = father
    
    def get_h(self):
        global H_METHOD, TARGET

        h_val = 0
        if H_METHOD == 'h1':
            for x in range(self.n):
                for y in range(self.n):
                    if self.chessboard[x][y] != '_':
                        if self.chessboard[x][y] != TARGET[x][y]:
                            h_val += 1
        elif H_METHOD == 'h2':
            for x in range(self.n):
                for y in range(self.n):
                    if self.chessboard[x][y] == '_':
                        continue

                    for xx in range(self.n):
                        for yy in range(self.n):
                            if self.chessboard[x][y] == TARGET[xx][yy]:
                                h_val += abs(xx - x) + abs(yy - y)

        return h_val
    
    def cal_f(self):
        return self.g_val + self.h_val

    def __lt__(self, other):
        return self.f_val <= other.f_val

    def get_children(self):
        x, y = 0, 0
        for i in range(self.n):
            for j in range(self.n):
                if self.chessboard[i][j] == BLANK_CHAR:
                    x, y = i, j

        possible_dirs = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        dir_flags = [100, 101, 1000, 1001]
        children = []

        for (xx, yy), dir_flag in zip(possible_dirs, dir_flags):
            # don't step back
            flag_sum = dir_flag + self.last_step_flag
            if flag_sum == 201 or flag_sum == 2001:
                continue
            if 0 <= xx < self.n and 0 <= yy < self.n:
                new_chessboard = deepcopy(self.chessboard)
                new_chessboard[x][y], new_chessboard[xx][yy] = new_chessboard[xx][yy], new_chessboard[x][y]
                children.append(Node(new_chessboard, self.g_val + 1, dir_flag, id(self)))
        
        return children
    
    def draw_chessboard(self):
        print('g value: {}, h value: {}, f value: {}'.format(self.g_val, self.h_val, self.f_val))
        for i in range(self.n):
            for j in range(self.n):
                print(self.chessboard[i][j], end=' ')
            print('')


def main():
    global TARGET, H_METHOD

    print('enter the size of the chessboard:')
    n = int(input())
    if n % 2 != 1:
        raise ValueError('N must be odd!')

    print('enter the heuristic method (h1 / h2):')
    H_METHOD = input()
    if H_METHOD != 'h1' and H_METHOD != 'h2':
        raise ValueError('Heuristic method error!')

    TARGET = get_target(n)

    open_heap = []
    close_list = []

    # start_chessboard = input_chessboard(n)
    start_chessboard = [[5, 3, 6], [1, 8, 7], [4, 2, '_']]
    start_node = Node(start_chessboard, 0)
    heapq.heappush(open_heap, start_node)

    # algorithm begin
    steps = 0
    while True:
        if len(open_heap) == 0:
            print('No valid solution!')
            exit(0)
        steps += 1

        # equal f_val => smallest != to-be-popped
        # cur_node = heapq.nsmallest(1, open_heap)[0]
        cur_node = open_heap[0]
        heapq.heappop(open_heap)
        close_list.append(cur_node)
        print('----------------------------')
        print('explore:')
        cur_node.draw_chessboard()

        if cur_node.h_val == 0:
            print('Check! {} steps explored!'.format(steps))
            break

        print('children:')
        for node in cur_node.get_children():
            heapq.heappush(open_heap, node)
            node.draw_chessboard()
    # algorithm end

    # draw path
    close_list.reverse()
    father = close_list[0].father
    solution = [close_list[0]]

    for node in close_list:
        if id(node) == father:
            solution.append(node)
            father = node.father

    print('------------------')
    print('Solution with {} steps'.format(len(solution)))
    for node in reversed(solution):
        node.draw_chessboard()


if __name__ == '__main__':
    main()
