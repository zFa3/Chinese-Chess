#!usr/bin/env python 3

# 中国象棋

class Chess:
    def __init__(self) -> None:

        self.board = [
            1, 2, 6, 5, 7, 5, 6, 2, 1,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 3, 0, 0, 0, 0, 0, 3, 0,
            4, 0, 4, 0, 4, 0, 4, 0, 4,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            11, 0, 11, 0, 11, 0, 11, 0, 11,
            0, 10, 0, 0, 0, 0, 0, 10, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            8, 9, 13, 12, 14, 12, 13, 9, 8]

        # Pieces
        # 車, 馬, 砲, 卒, 士, 象, 將 --- Player 1
        # 俥, 傌, 炮, 兵, 仕, 相, 帥 --- Player 2

        self.Pieces = {
            0:"  ",
            1:"車",
            2:"馬",
            3:"砲",
            4:"卒",
            5:"士",
            6:"象",
            7:"將",
            8:"俥",
            9:"傌",
            10:"炮",
            11:"兵",
            12:"仕",
            13:"相",
            14:"帥",
        }
    
        self.Player = True # Player 1 to move

    def print_board(self):
        for i in range(10):
            for j in range(9):
                ending = "|" if j != 8 else "| " + chr(abs(i - 9) + 65)
                print(self.Pieces[self.board[i * 9 + j]], end = ending)
            print()
        for i in range(9):
            print(i + 1, end = "  ")

    def play_move(self, move, board):
        # this function doesn't test whether
        # the move is legal or not
        # play a move, on a test board
        # make shallow copy of board
        test_board = board[:]
        a, b = test_board[self.notationSq(move[:2])], test_board[self.notationSq(move[2:])]
        test_board[self.notationSq(move[2:])], test_board[self.notationSq(move[:2])] = a, b
        return test_board

    def notationSq(self, square):
        return abs((ord(square[0])-65)-9) * 9 + int(square[1]) - 1
    
    def makeLine(self, board, move):
        # this function makes a line
        # between the (var) move endpoints
        # useful for detecting Cannon moves
        if self.notationSq(move[:2]) % 9 == self.notationSq(move[2:]) % 9:
            # if this is true, then it is a vertical move
            return [item for index, item in enumerate(board) if index % 9 == self.notationSq(move[2:]) % 9]
        else:
            # otherwise, it is a horizontal move
            return [item for index, item in enumerate(board) if index > min(self.notationSq(move[:2]), self.notationSq(move[2:])) and index < max(self.notationSq(move[:2]), self.notationSq(move[2:]))]

Game = Chess()
Game.print_board()
print(Game.Pieces[Game.board[Game.notationSq(input())]])
