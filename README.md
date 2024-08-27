# Chinese Chess (xiangqi) - 中国象棋
Chinese Chess, made in pure python by me (zFa3)

![image](https://github.com/user-attachments/assets/4b8f64ba-9241-4ed5-898c-5ca88f877c69)

# How to play
You can run this in any python IDE, or with the default Python IDLE
- note: no extra libraries are needed to run this program

The player on top (Player 1) goes first
you can play a move by typing in your move in the format described:
{origin square [letter-number] : destination square [letter-number]}
Example: D5E5

This project was inspired by my first chess game/engine, which
took insiration from sunfish

# Pieces
車, 馬, 砲, 卒, 士, 象, 將 --- Player 1
俥, 傌, 炮, 兵, 仕, 相, 帥 --- Player 2
_Both sides have the same types of pieces_
_Just with different chinese characters_

(you can change the caracters within the code by altering lines 44 -> 58)

First piece behaves identically to a rook
Second is a knight
Third is a cannon (moves like a rook but can only take when jumping over a piece)
Fourth is a Pawn, can only move side to side when it crosses the river
Fifth piece moves only diagonally within the palace
Sixth is the Elephant (cannot cross the river)
Lastly the king, which moves in the cardinal directions and cannot leave the palace

For full set of rules visit [this](https://www.youtube.com/watch?v=vklqOLf6mtU&t=128s) link
