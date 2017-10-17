from pprint import pprint as pp
import random
from collections import Counter


def read_sudoku(filename):
    """ ��������� ������ �� ���������� ����� """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """����� ������ """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) +
                      ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    ������������� �������� values � ������, ��������� �� ������� �� n ���������
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i * n: i * n + n] for i in range(n)]


def get_row(values, pos):
    """ ���������� ��� �������� ��� ������ ������, ��������� � pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return values[pos[0]]


def get_col(values, pos):
    """ ���������� ��� �������� ��� ������ �������, ���������� � pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [values[i][pos[1]] for i in range(len(values))]


def get_block(values, pos):

    """ ���������� ��� �������� �� ���� ��������, � ������� ��������
    ������� pos """
    """ ���� pos ������� � ����!!! (pos = x,y � �����) """

    """ --------------------- """
    """ ���� ��� ����������� ��-�� �� 3 ������ ����� (��� �������,
    ���� ��-�� �� �������������) """
    r = 3 * (pos[0] // 3)
    c = 3 * (pos[1] // 3)
    return [values[r+i][c+j] for i in range(3) for j in range(3)]


def find_empty_positions(grid):
    """ ����� ������ ��������� ������� � �����
    >>> find_empty_positions([['1', '2', '.'], +\
    ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], +\
    ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], +\
    ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == '.':
                return (i, j)
    return -1


def find_possible_values(grid, pos):
    """ ������� ��� ��������� �������� ��� ��������� ������� """
    var = set('123456789')
    row = set(get_row(grid, pos))
    col = set(get_col(grid, pos))
    values_in_block = set(get_block(grid, pos))
    return var - set.union(values_in_block, set.union(row, col))


def solve(grid):
    """ ������� �����, ��������� � grid """
    """ ��� ������ ������?
        1. ����� ��������� �������
        2. ����� ��� ��������� ��������, ������� �����
        ���������� �� ���� �������
        3. ��� ������� ���������� ��������:
            3.1. ��������� ��� �������� �� ��� �������
            3.2. ���������� ������ ���������� ����� �����
    """
    pos = find_empty_positions(grid)
    if pos == -1:
        return grid
    values = find_possible_values(grid, pos)
    if not values:
        return None
    for i in values:
        grid[pos[0]][pos[1]] = i
        ans = solve(grid)
        if ans is not None:
            return ans
    grid[pos[0]][pos[1]] = '.'
    return None


def check_solution(solution):
    """ ���� ������� solution �����, �� ������� True,
    � ��������� ������ False """
    for i in range(9):
        var1 = set('123456789')
        var2 = set('123456789')
        var3 = set('123456789')
        row = set(get_row(solution, (i, 0)))
        col = set(get_col(solution, (0, i)))
        var1 -= row
        var2 -= col
        if var1 and var2 != set():
            return False
    for i in range(3):
        for j in range(3):
            block = set(get_block(solution, (i, j)))
            var3 -= block
            if var3 != set():
                return False
    return True


def generate_sudoku(N):
    """ ��������� ������ ������������ �� N ���������
        >>> grid = generate_sudoku(40)
        >>> sum(1 for row in grid for e in row if e == '.')
        41
        >>> solution = solve(grid)
        >>> check_solution(solution)
        True
        >>> grid = generate_sudoku(1000)
        >>> sum(1 for row in grid for e in row if e == '.')
        0
        >>> solution = solve(grid)
        >>> check_solution(solution)
        True
        >>> grid = generate_sudoku(0)
        >>> sum(1 for row in grid for e in row if e == '.')
        81
        >>> solution = solve(grid)
        >>> check_solution(solution)
        True
    """
    N = 81 - N
    grid = [['.' for i in range(9)] for j in range(9)]
    grid = solve(grid)
    for elem in range(N):
        row = random.randrange(0, 9)
        col = random.randrange(0, 9)
        while grid[row][col] == '.':
            row = random.randrange(0, 9)
            col = random.randrange(0, 9)
        grid[row][col] = '.'
    return grid

if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)
