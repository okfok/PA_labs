import random
import time

# Empty = object()
# UnderAttack = object()
# Queen = object()
BS = 8  # Board Size
QC = 8  # Queen Count


class Cell:
    x: int
    y: int

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x if x != 0 else random.randint(0, BS - 1)
        self.y = y if y != 0 else random.randint(0, BS - 1)

    def __eq__(self, other: 'Cell'):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}; {self.y})"


class State:
    solve_counter = 0
    queens: list[Cell]
    states: list['State']

    # exceptions: list[Cell]

    def __init__(self, queens: list[Cell] = None):  # , exceptions: list[Cell] = None
        self.states = []
        if queens is None:
            self.queens = []
            for i in range(QC):
                while (cell := Cell()) in self.queens:
                    pass
                self.queens.append(cell)
        else:
            self.queens = queens

        # self.exceptions = exceptions if exceptions is not None else []

    #
    # def print(self):
    #     print(*[x for x in range(BS + 1)])
    #
    #     for i in range(BS):
    #         print(i + 1, end=' ')
    #         for j in range(BS):
    #             if Cell(i, j) in self.queens:
    #                 print('X', end=' ')
    #             else:
    #                 print('O', end=' ')
    #
    #         print()

    def under_attack(self):
        board = [[0 for _ in range(BS)] for _ in range(BS)]
        n = 0
        for queen in self.queens:
            s = 0
            for i in range(BS):
                s += board[i][queen.y] + board[queen.x][i]

                if 0 <= (j := queen.y - queen.x + i) < BS:
                    s += board[i][j]

                if 0 <= (j := (queen.x + queen.y) - i) < BS:
                    s += board[i][j]

            if s > 0:
                n += 1

            board[queen.x][queen.y] = 1

        return n

    @property
    def is_solved(self):
        return self.under_attack() == 0

    def get_board(self, queens=None):
        if queens is None:
            queens = self.queens

        board = [[0 for _ in range(BS)] for _ in range(BS)]

        for queen in queens:
            for i in range(BS):
                if board[i][queen.y] == 0:
                    board[i][queen.y] = 1
                if board[queen.x][i] == 0:
                    board[queen.x][i] = 1

                if 0 <= (j := queen.y - queen.x + i) < BS:
                    if board[i][j] == 0:
                        board[i][j] = 1

                if 0 <= (j := (queen.x + queen.y) - i) < BS:
                    if board[i][j] == 0:
                        board[i][j] = 1

            board[queen.x][queen.y] = 2

        return board

    def solve(self, depth: int):
        State.solve_counter += 1

        if depth <= 0:
            return

        if self.is_solved:
            return self

        for queen_to_move in self.queens:
            queens = [queen for queen in self.queens if queen is not queen_to_move]

            assert QC - 1 == len(queens)
            board = self.get_board(queens)

            for i in range(BS):
                for j in range(BS):
                    if board[i][j] == 0:
                        # if (cell := Cell(i, j)) not in self.exceptions:
                        new_state = State(queens.copy())  # , self.exceptions + [queen_to_move]
                        new_state.queens.append(Cell(i, j))
                        if (res := new_state.solve(depth - 1)) is not None:
                            return res


def main():
    state = State()
    print(*state.get_board(), sep='\n')
    print(state.is_solved)
    start_time = time.time()
    state = state.solve(QC - 1)
    end_time = time.time()

    print(*state.get_board(), sep='\n')
    print(state.is_solved)

    print("Elapsed time: ", end_time - start_time)
    print("Iter:", State.solve_counter)


if __name__ == '__main__':
    main()
