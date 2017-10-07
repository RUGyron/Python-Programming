def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
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
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    k = 0
    values_copy = []
    lenth = len(values)
    if lenth % n != 0:
        return print("Error: can't group values")
    groups = lenth // n
    for i in range(n):
        values_copy.append(values[k:groups+k])
        k = k + groups
    return values_copy


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row = values[pos[0]]
    return row


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """

    col = []
    for i in values:
        col.append(i[pos[1]])

    return col


def get_block(values, pos):

    """ Возвращает все значения из того квадрата, в который попадает
    позиция pos """
    """ Счет pos ведется с нуля!!! (pos = x,y в сетке) """

    """ --------------------- """
    """ цикл для группировки эл-ов по 3 внутри сетки (при условии,
    если эл-ты не сгруппированы) """

    row, col = pos[0] // 3 * 3, pos[1] // 3 * 3
    val_n = []
    val_n.append(values[row][col:col+3])
    val_n.append(values[row+1][col:col+3])
    val_n.append(values[row+2][col:col+3])

    val_nn = []
    for i in val_n:
        for j in i:
            if j == '.':
                continue
            val_nn.append(j)

    return val_nn


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

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
    for i in grid:
        for j in i:
            if j == '.':
                return (grid.index(i), i.index(j))
    return -1


def find_possible_values(grid, pos):
    """ Вернуть все возможные значения для указанной позиции """
    var = '123456789'
    var = set(var)
    row = set()
    col = set()
    row = set([c for c in grid[pos[0]] if c in '123456789'])
    for i in grid:
        if i[pos[1]] == '.':
            continue
        col.add(i[pos[1]])
    union = set.union(row, col)
    values_in_block = set(get_block(grid, pos))
    union = set.union(union, values_in_block)
    res = var - union
    return res


def solve(grid):
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут
        находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    """
    pos = find_empty_positions(grid)
    if pos == -1:
        return grid
    values = find_possible_values(grid, pos)
    if values == {}:
        return False
    for i in values:
        grid[pos[0]][pos[1]] = i
        ans = solve(grid)
        if ans is not None:
            return ans
    grid[pos[0]][pos[1]] = '.'
    return None


def check_solution(solution):
    """ Если решение solution верно, то вернуть True,
    в противном случае False """
    summ = 0
    for i in range(9):
        for j in range(9):
            summ += int(solution[i][j])
    if summ != 405:
        return False
    return True

if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)
