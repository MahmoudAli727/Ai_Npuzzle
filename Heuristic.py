from Board import Board
import math as m
import numpy as np
import heapq


class Heuristic:
    def MisPlaced(self, board):
        heuristic = 0
        for x in range(len(board)):
            for y in range(len(board)):
                if board[y][x] and Board(len(board)).getBoard()[y][x] != board[y][x]:
                    heuristic += 1
        return heuristic

    def Euclidean(self, board):
        b = Board(len(board))
        heuristic = 0
        for x1 in range(len(board)):
            for y1 in range(len(board)):
                found = False
                for x2 in range(len(board)):
                    for y2 in range(len(board)):
                        if b.getBoard()[x1][y1] == board[x2][y2]:
                            found = True
                            dx = int(m.fabs(x2 - x1))
                            dy = int(m.fabs(y2 - y1))
                            heuristic += int(m.floor(m.sqrt(dx * dx + dy * dy)))
                            break
                    if found:
                        break
        return heuristic

    def Manhattan(self, board):
        heuristic = 0
        board = np.array(board)
        b = Board(len(board))
        goal = np.array(b.getBoard())
        for x in range(len(board)):
            for y in range(len(board)):
                if board[y][x] and goal[y][x] != board[y][x]:
                    row, col = np.where(goal == board[y][x])
                    heuristic += abs(row[0] - y) + abs(col[0] - x)
        return heuristic

    def linearConflict(self, board):
        heuristic = 0
        board = np.array(board)
        board = np.transpose(board).flatten()
        for x in range(len(board) - 1):
            for y in range(x + 1, len(board)):
                if board[x] and board[y] and board[x] > board[y]:
                    heuristic += 1

        if board[len(board) - 1]:
            heuristic += 1
        return heuristic

    def BestFirstSearch(self, start_state, goal_state, heuristic_type="Manhattan"):
        open_list = []  # Priority queue
        closed_list = set()

        def heuristic_value(board):
            if heuristic_type == "Manhattan":
                return self.Manhattan(board)
            elif heuristic_type == "Euclidean":
                return self.Euclidean(board)
            elif heuristic_type == "MisPlaced":
                return self.MisPlaced(board)
            elif heuristic_type == "Linear Conflict":
                return self.MisPlaced(board)
            else:
                raise ValueError("Invalid heuristic type")

        # Push the start state with its heuristic value
        heapq.heappush(open_list, (heuristic_value(start_state), start_state))

        while open_list:
            _, current_state = heapq.heappop(open_list)

            if current_state == goal_state:
                print("Goal reached!")
                return True

            closed_list.add(tuple(map(tuple, current_state)))

            # Generate successors
            for direction in [Board.UP, Board.DOWN, Board.LEFT, Board.RIGHT]:
                new_board = self.move(current_state, direction)
                if new_board is not None:
                    new_board_tuple = tuple(map(tuple, new_board))
                    if new_board_tuple not in closed_list:
                        heapq.heappush(open_list, (heuristic_value(new_board), new_board))

        print("No solution found.")
        return False

    def move(self, board, direction):
        # Implement logic to generate new board state after moving in the given direction
        # Return None if the move is invalid
        pass
