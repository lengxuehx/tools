# coding: utf-8


def print_location():
    #初始化二维数组
    chessboard = [[0 for x in range(8)] for y in range(8)]

    step = 0
    while 0 <= step < 8:
        ret = put_chessman(chessboard, step)
        if ret is True:
            print('{}: forward'.format(step))
            print_chessboard(chessboard)
            step += 1
        else:
            print('{}: backward'.format(step))
            print_chessboard(chessboard)
            step -= 1

    print('=================')
    print_chessboard(chessboard)


def print_chessboard(chessboard):
    for rows in chessboard:
        print(rows)


def put_chessman(chessboard, step):
    old_column = -1
    for i in range(8):
        if chessboard[step][i] == 1:
            old_column = i
            break

    if old_column == -1:
        new_column = 0
    else:
        chessboard[step][old_column] = 0
        new_column = old_column + 1
        if new_column >= 8:
            return False

    for i in range(new_column, 8):
        ret = check_locations(chessboard, step, i)
        if ret is True:
            chessboard[step][i] = 1
            return True

    return False


def check_locations(chessboard, row, column):
    leftup = column - 1
    rightup = column + 1

    for x in range(row-1, -1, -1):
        for y in range(8):
            if chessboard[x][y] == 1:
                if y == column:
                    return False

                if leftup>=0 and y==leftup:
                    return False
                elif rightup<8 and y==rightup:
                    return False

                break

        leftup = leftup - 1
        rightup = rightup + 1

    return True


if '__main__' == __name__:
    print_location()