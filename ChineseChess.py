#!usr/bin/env python 3

# 中国象棋

class Chess:
    def __init__(self) -> None:

        # the cardinal directions, not mandatory,
        # only to organize the code a little
        self.U = -11
        self.D =  11
        self.L = -1
        self.R =  1

        P = -1
        self.board = [
            # Player 1
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
            P, P, P, P, P, P, P, P, P, P, P
            # Player 2
        ]
        self.board = [
            # Player 1
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
            P, P, P, P, P, P, P, P, P, P, P
            # Player 2
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
            if i == 6:
                print("--------------------------")
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
        # removed the -1 to compensate for left padding
        return (abs((ord(square[0])-65) - 9) + 2) * 11 + int(square[1])
    
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
            return [item for index, item in enumerate(board) if index % 11 == move2 % 11 and item != -1 and index > min(move1, move2) and index < max(move1, move2)]
        else:
            # otherwise, it is a horizontal move
            return [item for index, item in enumerate(board) if index > min(move1, move2) and index < max(move1, move2) and item != -1]

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
    
    def pseudo_legal(self, board, player):
        pseudo_legal_moves = []
        for i, t in enumerate(board):
            # pieces = range(1, 8) if player else range(8, 15)
            pieces = range(((not player)) * 7 + 1, ((not player) + 1) * 7 + 1)
            # we could actually do a out of bounds check more efficiently by
            # adding the padding block (-1) as a friendly piece for both sides,
            # which essentially does the same thing as what it currently does
            if t in pieces and t != -1:
                if t - (7 * (not player)) == 1:
                    # if the piece is a 車
                    for j in (self.U, self.D, self.L, self.R):
                        # create a ray for the piece
                        for ray_dist in range(1, 10):
                            # max length between the width and height
                            piece = board[i + j * ray_dist]
                            if piece == -1:
                                # if we have hit an edge, dont continue
                                break # break from the ray loop
                            elif piece == 0:
                                # if it is an empty square, then we can go here or
                                # choose to go further
                                pseudo_legal_moves.append((i, i + j * ray_dist))
                            elif not piece in pieces:
                                # if it is an enemy piece, then the rook can take it,
                                # but it cannot continue further, so we break
                                pseudo_legal_moves.append((i, i + j * ray_dist))
                            else:
                            # otherwise, we break, to prevent jumping over pieces
                                break

                if t - (7 * (not player)) == 2:
                    # if the piece is a (knight) 馬
                    for j in [[self.U, self.U, self.R], [self.U, self.U, self.L], [self.D, self.D, self.R], [self.D, self.D, self.L], [self.L, self.L, self.U], [self.L, self.L, self.D], [self.R, self.R, self.U], [self.R, self.R, self.D]]:
                        # all the moves the knight can make
                        piece = board[i + sum(j)]
                        if piece == -1 or piece in pieces or board[i + j[1]] != 0:
                            # if the spot we are checking is out of bounds or is our own piece
                            # OR, it being blocked by another piece (Special rule in chinese chess)
                            continue # since this isnt a raying piece, we can cont. instead of breaking
                        # otherwise we can add it to the list of (pseudo) legal moves
                        pseudo_legal_moves.append((i, i + sum(j)))

                if t - (7 * (not player)) == 3:
                    # 3 砲
                    pass
                if t - (7 * (not player)) == 4:
                    # 4 卒
                    if (player and i > 77) or (not player and i < 67):
                        # if the pawn has crossed the river
                        # then it can now capture to the side
                        pass
                    elif board[i + (self.D if player else self.U)] not in pieces and board[i + (self.D if player else self.U)] != -1:
                        pseudo_legal_moves.append((i, i + (self.D if player else self.U)))
                        # then it can only capture the square infront of it
                        
                if t - (7 * (not player)) == 5:
                    # 5 士
                    for m in [self.U + self.R, self.U + self.L, self.D + self.R, self.D + self.L]:
                        if not board[i + m] in pieces and board[i + m] != -1 and ((i + m in [26, 27, 28, 37, 38, 39, 48, 49, 50] and player) or (i + m in [103, 104, 105, 114, 115, 116, 125, 126, 127] and not player)):
                            pseudo_legal_moves.append((i, i + m))
                if t - (7 * (not player)) == 6:
                    # 6 象
                    for j in [[self.U, self.R, self.U, self.R], [self.U, self.L, self.U, self.L], [self.D, self.R, self.D, self.R], [self.D, self.L, self.D, self.L]]:
                        # all the moves the knight can make
                        piece = board[i + sum(j)]
                        if piece == -1 or piece in pieces or board[i + sum(j[:2])] != 0 or ((i + sum(j)) < 70 and not player) or ((i + sum(j)) > 60 and player):
                            # Very similar to the knight, however it can't cross the river
                            continue # since this isnt a raying piece, we can cont. instead of breaking
                        # otherwise we can add it to the list of (pseudo) legal moves
                        pseudo_legal_moves.append((i, i + sum(j)))
                if t - (7 * (not player)) == 7:
                    # 7 將
                    for m in (self.U, self.D, self.L, self.R):
                        piece = board[i + m]
                        if piece == -1 or piece in pieces: continue
                        # the king has to stay within his palace
                        if (i + m in [26, 27, 28, 37, 38, 39, 48, 49, 50] and player) or (i + m in [103, 104, 105, 114, 115, 116, 125, 126, 127] and not player):
                            pseudo_legal_moves.append((i, i + m))
        return pseudo_legal_moves

    def indexNotation(self, index):
        index = abs(index - 14 * 11) - 23
        row, col = index // 11, index % 11
        return str(chr(row + 65) + str(col))

def main():
    Game = Chess()
    Game.print_board()
    # Game.Player = not Game.Player

    print("\n\n", list(map(lambda x: Game.indexNotation(x[0]) + Game.indexNotation(x[1]),Game.pseudo_legal(Game.board, Game.Player))))
    print(Game.pseudo_legal(Game.board, Game.Player))

    print("Moves:", len(Game.pseudo_legal(Game.board, Game.Player)))
    print(Game.legal_position(Game.board, Game.Player))

    print(Game.notationSq(input()))
    # print(Game.Pieces[Game.board[Game.notationSq(input())]])
    # print(Game.Pieces[Game.board[int(input())]])


if __name__ == "__main__":
    main()
