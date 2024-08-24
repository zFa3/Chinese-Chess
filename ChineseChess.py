#!usr/bin/env python 3
# zFa3 - Chinese Chess
# 中国象棋

class Chess:
    def __init__(self) -> None:
        # the directions
        self.Dirs = (-11, 11, -1, 1)
        # padding
        P = self.Dirs[2]
        # the board, with a 2 layer padding
        # on each side (left and right wrap around)
        # to prevent pieces that can jump
        # like the knight/elephant from
        # moving out of bounds
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

        self.Pieces = { 0:"  ", 1:"車", 2:"馬", 3:"砲", 4:"卒", 5:"士", 6:"象", 7:"將", 8:"俥", 9:"傌", 10:"炮", 11:"兵", 12:"仕", 13:"相", 14:"帥"}
        self.pr_legal_mvs = True
        self.clear = False
        self.Player = True # Player 1 to move

    def print_board(self):
        if self.clear: print("\033c")
        for i in range(14):
            for j in range(11):
                if self.board[i * 11 + j] != -1:
                    ending = "|" if j != 9 else "| " + chr(abs(i - 14) + 62) + "\n"
                    print(self.Pieces[self.board[i * 11 + j]], end = ending)
            if i == 6:
                print("-" * 26)
        for i in range(9):
            print(i + 1, end = "  ")
        print("\n")

    def play_move(self, move, board):
        # this function doesn't test whether
        # the move is legal or not
        # play a move, on a test board
        # make shallow copy of board
        # * deep copy isnt neccessary, since
        # we are only storing integer values
        test_board = board[:]
        test_board[self.notationSq(move[2:])] = test_board[self.notationSq(move[:2])]
        test_board[self.notationSq(move[:2])] = 0
        return test_board
    
    def Play_Move(self, move, board):
        # same as above but takes in indexes instead
        test_board = board[:]
        # a, b = test_board[move[0]], test_board[move[1]]
        # test_board[move[1]], test_board[move[0]] = a, b
        test_board[move[1]] = test_board[move[0]]
        test_board[move[0]] = 0
        return test_board

    def notationSq(self, square):
        # +2 to compensate for side padding
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

    def is_being_checked(self, board, player):
        # making sure the kings cant see each other
        # (before checking anything else do it doesn't get overwritten)
        if board.index(7) % 11 == board.index(14) % 11 and all([item == 0 for item in self.MakeLine(board, board.index(7), board.index(14))]):
            return True
        # input -> copy of the board
        # input -> the player who is currently to move
        if not player:
            # if the player is == 0
            # so if it is player 2
            return board.index(14) in list(map(lambda x:x[1], self.pseudo_legal(board, 1)))
        else:
            # player 1 being checked?
            return board.index(7) in list(map(lambda x:x[1], self.pseudo_legal(board, 0)))
        
        return False

    def pseudo_legal(self, board, player):
        pseudo_lm = []
        for i, t in enumerate(board):
            # pieces = range(1, 8) if player else range(8, 15)
            pieces = range(((not player)) * 7 + 1, ((not player) + 1) * 7 + 1)
            # we could actually do a out of bounds check more efficiently by
            # adding the padding block (-1) as a friendly piece for both sides,
            # which essentially does the same thing as what it currently does
            if t in pieces and t != -1:
                if t - (7 * (not player)) == 1:
                    # if the piece is a 車
                    for j in (self.Dirs[0], self.Dirs[1], self.Dirs[2], self.Dirs[3]):
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
                                pseudo_lm.append((i, i + j * ray_dist))
                            elif not piece in pieces:
                                # if it is an enemy piece, then the rook can take it,
                                # but it cannot continue further, so we break
                                pseudo_lm.append((i, i + j * ray_dist))
                                break
                            else:
                            # otherwise, we break, to prevent jumping over pieces
                                break

                if t - (7 * (not player)) == 2:
                    # if the piece is a (knight) 馬
                    for j in [[self.Dirs[0], self.Dirs[0], self.Dirs[3]], [self.Dirs[0], self.Dirs[0], self.Dirs[2]], [self.Dirs[1], self.Dirs[1], self.Dirs[3]], [self.Dirs[1], self.Dirs[1], self.Dirs[2]], [self.Dirs[2], self.Dirs[2], self.Dirs[0]], [self.Dirs[2], self.Dirs[2], self.Dirs[1]], [self.Dirs[3], self.Dirs[3], self.Dirs[0]], [self.Dirs[3], self.Dirs[3], self.Dirs[1]]]:
                        # all the moves the knight can make
                        piece = board[i + sum(j)]
                        if piece == -1 or piece in pieces or board[i + j[1]] != 0:
                            # if the spot we are checking is out of bounds or is our own piece
                            # OR, it being blocked by another piece (Special rule in chinese chess)
                            continue # since this isnt a raying piece, we can cont. instead of breaking
                        # otherwise we can add it to the list of (pseudo) legal moves
                        pseudo_lm.append((i, i + sum(j)))

                if t - (7 * (not player)) == 3:
                    # if the piece is a cannon 砲
                    for j in (self.Dirs[0], self.Dirs[1], self.Dirs[2], self.Dirs[3]):
                        skip = False
                        # create a ray for the piece
                        for ray_dist in range(1, 10):
                            # Furthest the piece can go before leaving the board
                            piece = board[i + j * ray_dist]
                            if piece == -1: break # similar code to the 車 (chess rook equivalent)
                            if not skip:
                                if piece == 0:
                                    pseudo_lm.append((i, i + j * ray_dist))
                                elif piece:
                                    skip = True
                            elif piece:
                                pseudo_lm.append((i, i + j * ray_dist)); break
                    
                if t - (7 * (not player)) == 4:
                    # 4 卒
                    if (player and i > 77) or (not player and i < 67):
                        # if the pawn has crossed the river
                        # then it can now capture to the side
                        for m in [self.Dirs[2], self.Dirs[3], (self.Dirs[1] if player else self.Dirs[0])]:
                            if (not board[i + m] in pieces) and board[i + m] != -1:
                                pseudo_lm.append((i, i + m))
                    elif board[i + (self.Dirs[1] if player else self.Dirs[0])] not in pieces and board[i + (self.Dirs[1] if player else self.Dirs[0])] != -1:
                        pseudo_lm.append((i, i + (self.Dirs[1] if player else self.Dirs[0])))
                        # then it can only capture the square in front of it
                        
                if t - (7 * (not player)) == 5:
                    # 5 士
                    for m in [self.Dirs[0] + self.Dirs[3], self.Dirs[0] + self.Dirs[2], self.Dirs[1] + self.Dirs[3], self.Dirs[1] + self.Dirs[2]]:
                        if (not board[i + m] in pieces) and board[i + m] != -1 and ((i + m in [26, 27, 28, 37, 38, 39, 48, 49, 50] and player) or (i + m in [103, 104, 105, 114, 115, 116, 125, 126, 127] and not player)):
                            pseudo_lm.append((i, i + m))
                if t - (7 * (not player)) == 6:
                    # 6 象
                    for j in [[self.Dirs[0], self.Dirs[3], self.Dirs[0], self.Dirs[3]], [self.Dirs[0], self.Dirs[2], self.Dirs[0], self.Dirs[2]], [self.Dirs[1], self.Dirs[3], self.Dirs[1], self.Dirs[3]], [self.Dirs[1], self.Dirs[2], self.Dirs[1], self.Dirs[2]]]:
                        # all the moves the knight can make
                        piece = board[i + sum(j)]
                        if piece == -1 or piece in pieces or board[i + sum(j[:2])] != 0 or ((i + sum(j)) < 70 and not player) or ((i + sum(j)) > 60 and player):
                            # Very similar to the knight, however it can't cross the river
                            continue # since this isnt a raying piece, we can cont. instead of breaking
                        # otherwise we can add it to the list of (pseudo) legal moves
                        pseudo_lm.append((i, i + sum(j)))
                if t - (7 * (not player)) == 7:
                    # 7 將
                    for m in (self.Dirs[0], self.Dirs[1], self.Dirs[2], self.Dirs[3]):
                        piece = board[i + m]
                        if piece == -1 or piece in pieces: continue
                        # the king has to stay within his palace
                        if (i + m in [26, 27, 28, 37, 38, 39, 48, 49, 50] and player) or (i + m in [103, 104, 105, 114, 115, 116, 125, 126, 127] and not player):
                            pseudo_lm.append((i, i + m))
        return pseudo_lm

    def legal_moves(self, board, player):
        # this function returns the legal moves that the player (to move) has
        player_legal_moves = []
        test_board = board[:]
        for i in self.pseudo_legal(test_board, player):
            test_board = board[:]
            test_board = self.Play_Move(i, test_board)
            try:
                if not self.is_being_checked(test_board, player):
                    player_legal_moves.append(i)
            except ValueError:
                continue
                # whoops one of the pseudolegal moves that was generated was a piece
                # capturing a king, which results in an error since we are asking for
                # an index which doesn't exist
        return player_legal_moves

    def indexNotation(self, index):
        # Brute force because speed isn't priority
        for i in range(10):
            for j in range(1, 10):
                if self.notationSq(chr(i + 65) + str(j)) == index:
                    return chr(i + 65) + str(j)

def main():
    Game = Chess()
    Game.print_board()
    while True:
        if Game.pr_legal_mvs:
            # print the list of legal moves?
            print(list(map(lambda x: Game.indexNotation(x[0]) + Game.indexNotation(x[1]), Game.legal_moves(Game.board, Game.Player))))
            print()
        
        move = input(f"{'PLAYER 1 -' if Game.Player else 'PLAYER 2 -'} Move:").upper()

        if move in list(map(lambda x: Game.indexNotation(x[0]) + Game.indexNotation(x[1]), Game.legal_moves(Game.board, Game.Player))):
            Game.board = Game.play_move(move, Game.board)
            # if the move is legal
            # then we play the move
            # and print the board
            Game.print_board()
            Game.Player = not Game.Player
            # set player to !player
            if len(Game.legal_moves(Game.board, Game.Player)) == 0:
                break
        else:
            print("INVALID MOVE")
            # if the move isnt valid then we
            # let the player know and ask for a new move
    print("CHECKMATE:")
    print(f"PLAYER {Game.Player + 1} WON")

if __name__ == "__main__":
    main()
