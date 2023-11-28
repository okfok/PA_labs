import functools
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

    def __init__(self, x: int = None, y: int = None):
        self.x = x if x is not None else random.randint(0, BS - 1)
        self.y = y if y is not None else random.randint(0, BS - 1)

    def __eq__(self, other: 'Cell'):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Cell({self.x}, {self.y})"


class State:
    solve_counter = 1
    memory = 0
    max_depth = 0
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

    @property
    def under_attack(self):  # F2 function
        board = [[0 for _ in range(BS)] for _ in range(BS)]

        for queen in self.queens:
            for i in range(BS):
                if i != queen.x:
                    board[i][queen.y] += 1
                if i != queen.y:
                    board[queen.x][i] += 1

                if 0 <= (j := queen.y - queen.x + i) < BS:
                    if not (i == queen.x and j == queen.y):
                        board[i][j] += 1

                if 0 <= (j := (queen.x + queen.y) - i) < BS:
                    if not (i == queen.x and j == queen.y):
                        board[i][j] += 1

        n = 0

        for queen in self.queens:
            n += board[queen.x][queen.y]

        return n // 2

    @property
    def is_solved(self):
        return self.under_attack == 0

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

    def draw_board(self):
        board = [['#' for _ in range(BS)] for _ in range(BS)]

        for queen in self.queens:
            board[queen.x][queen.y] = '&'
        return '\n'.join([' '.join(i) for i in board])

    @staticmethod
    def create_new_states(state: 'State'):
        states = []

        for queen_to_move in state.queens:
            queens = [queen for queen in state.queens if queen is not queen_to_move]

            assert QC - 1 == len(queens)
            board = state.get_board(queens)

            for i in range(BS):
                for j in range(BS):
                    if board[i][j] == 0:
                        new_state = State(queens.copy())
                        new_state.queens.append(Cell(i, j))
                        states.append(new_state)
                        assert state.under_attack >= new_state.under_attack
        return states

    def solve_NSA(self, depth: int = QC - 1):
        State.solve_counter += 1

        if depth < 0:
            return

        if self.is_solved:
            State.max_depth = depth
            return self

        new_states = State.create_new_states(self)
        State.solve_counter += len(new_states)
        for state in new_states:
            if (res := state.solve_NSA(depth - 1)) is not None:
                return res

        State.memory += len(new_states)

    def solve_ISA(self):

        if self.is_solved:
            return self

        states = [(0, self)]

        iterations = 0
        states_total = 1

        while True:

            states.sort(key=lambda x: x[0] + x[1].under_attack, reverse=True)  # A*
            iterations += 1

            price, state = states.pop()
            # print(len(states), price, state.under_attack)

            new_states = [(price + 1, state) for state in State.create_new_states(state)]
            states_total += len(new_states)

            states += new_states

            for pr, st in states:
                if st.is_solved:
                    print("Iter: ", iterations)
                    print("States: ", states_total)
                    print("Memory: ", len(states))
                    return st


DEPTH = 7


def NSA():
    state = State()
    print(state.draw_board(), end='\n\n')
    print("Solved: ", state.is_solved)
    print("Func:", state.under_attack)
    start_time = time.time()
    solved_state = state.solve_NSA(DEPTH)
    end_time = time.time()

    if solved_state is not None:
        print(solved_state.draw_board(), end='\n\n')
        print("Solved: ", solved_state.is_solved)

    print("Elapsed time: ", end_time - start_time)
    print("Iter:", State.solve_counter)
    print("Memory:", State.solve_counter - State.memory)
    print("Depth : ", DEPTH - State.max_depth)


def ISA():
    state = State()
    print(state.draw_board(), end='\n\n')
    print("Solved: ", state.is_solved)
    print("Func:", state.under_attack)
    start_time = time.time()
    solved_state = state.solve_ISA()
    end_time = time.time()

    if solved_state is not None:
        print(solved_state.draw_board(), end='\n\n')
        print("Solved: ", solved_state.is_solved)

    print("Elapsed time: ", end_time - start_time)


if __name__ == '__main__':
    NSA()
    # ISA()
