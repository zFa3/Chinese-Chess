#!usr/bin/env python 3

# 中国象棋

class Chess:
    def __init__(self) -> None:

        # the cardinal directions, not mandatory,
        # only to organize the code a little
        self.U = -9,
        self.D =  9,
        self.L = -1,
        self.R =  1

        P = -1
        self.board = [
            P, P, P, P, P, P, P, P, P, P, P,
            P, P, P, P, P, P, P, P, P, P, P,
            P, 1, 2, 6, 5, 7, 5, 6, 2, 1, P,
            P, 0, 0, 0, 0, 0, 0, 0, 0, 0, P,
            P, 0, 3, 0, 0, 0, 0, 0, 3, 0, P,
            P, 4, 0, 4, 0, 4, 0, 4, 0, 4, P,
            P, 0, 0, 0, 0, 0, 0, 0, 0, 0, P,
            P, 0, 0, 0, 0, 0, 0, 0, 0, 0, P,
            P, 11, 0, 11, 0, 11, 0, 11, 0, 11, P,
            P, 0, 10, 0, 0, 0, 0, 0, 10, 0, P,
            P, 0, 0, 0, 0, 0, 0, 0, 0, 0, P,
            P, 8, 9, 13, 12, 14, 12, 13, 9, 8, P,
            P, P, P, P, P, P, P, P, P, P, P,
            P, P, P, P, P, P, P, P, P, P, P,
        ]
        # dimensions wid, hgt = 11, 14

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
        for i in range(14):
            for j in range(11):
                if self.board[i * 11 + j] != -1:
                    ending = "|" if j != 9 else "| " + chr(abs(i - 14) + 62) + "\n"
                    print(self.Pieces[self.board[i * 11 + j]], end = ending)
        for i in range(9):
            print(i + 1, end = "  ")
    
    def print_board_highlight(self, index):
        for i in range(14):
            for j in range(11):
                if self.board[i * 11 + j] != -1:
                    if self.board[i * 11 + j] == index:
                        ending = "|" if j != 9 else "| " + chr(abs(i - 14) + 62) + "\n"
                        print("X", end = ending)
                    else:
                        ending = "|" if j != 9 else "| " + chr(abs(i - 14) + 62) + "\n"
                        print(self.Pieces[self.board[i * 11 + j]], end = ending)
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
        return abs((ord(square[0])-65)-10) * 11 + int(square[1]) - 1
    
    def makeLine(self, board, move):
        # this function makes a line
        # between the (var) move endpoints
        # useful for detecting Cannon moves
        if self.notationSq(move[:2]) % 11 == self.notationSq(move[2:]) % 11:
            # if this is true, then it is a vertical move
            return [item for index, item in enumerate(board) if index % 11 == self.notationSq(move[2:]) % 11]
        else:
            # otherwise, it is a horizontal move
            return [item for index, item in enumerate(board) if index > min(self.notationSq(move[:2]), self.notationSq(move[2:])) and index < max(self.notationSq(move[:2]), self.notationSq(move[2:]))]
    
    def MakeLine(self, board, move1, move2):
        # same function as above, takes in indexes instead
        if move1 % 11 == move2 % 11:
            # if this is true, then it is a vertical move
            return [item for index, item in enumerate(board) if index % 11 == move2 % 11]
        else:
            # otherwise, it is a horizontal move
            return [item for index, item in enumerate(board) if index > min(move1, move2) and index < max(move1, move2)]

    def legal_position(self, board: list, player):
        if board.count(7) + board.count(14) != 2:
            # if there are not two kings on the board
            # then it is an illegal position
            return False
        if board.index(7) % 11 == board.index(14) % 11 and all([item == 0 for item in self.MakeLine(board, board.index(7), board.index(14))]):
            # special rule in chinese chess
            # the kings cannot face each other
            # with no pieces in between
            return False
        if board.index(7) in self.pseudo_legal(board, player) and not player:
            return False
            # if player 1's king is in
            # danger while it is player 2's turn then
            # it is an illegal position, since it would
            # be game over
        if board.index(14) in self.pseudo_legal(board, player) and player:
            # Same with the other side
            return False
        # if there are no legal positions,
        # then the game is over,
        # with !player winning
        return True
    
    def indexToNotation(self, index):
        pass

    def pseudo_legal(self, board, player):
        pseudo_legal_moves = []
        for i, t in enumerate(board):
            pieces = range(((not player)) * 7 + 1, ((not player) + 1) * 7 + 1)
            if t in pieces and t != -1:
                if t - (7 * (not player)) == 1:
                    # 1 if the piece is a 車
                    for i in (self.U, self.D, self.L, self.R):
                        pass
                if t - (7 * (not player)) == 2:
                    # 2 馬
                    pass
                if t - (7 * (not player)) == 3:
                    # 3 砲
                    pass
                if t - (7 * (not player)) == 4:
                    # 4 卒
                    pass
                if t - (7 * (not player)) == 5:
                    # 5 士
                    pass
                if t - (7 * (not player)) == 6:
                    # 6 象
                    pass
                if t - (7 * (not player)) == 7:
                    # 7 將
                    pass
        return pseudo_legal_moves

Game = Chess()
Game.print_board()

# print(Game.legal_position(Game.board, Game.Player))
print(Game.Pieces[Game.board[Game.notationSq(input())]])
