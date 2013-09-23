#!/usr/bin/env python
#
# 2013 CSAW Misc 300 code
# Copyright (c) 2013 Matt Hazinski <mhazinsk@vt.edu>. All rights reserved.

import socket

TCP_IP = '128.238.66.216'
TCP_PORT = 45678
BUFFER_SIZE = 1024

""" Determines the number of adjacent alive cells """
def getNeighborCount(board, row, col):
    count = 0
    if (board[row-1][col] == '*'):
        count += 1
    if (board[row+1][col] == '*'):
        count += 1
    if (board[row+1][col+1] == '*'):
        count += 1
    if (board[row-1][col-1] == '*'):
        count += 1
    if (board[row][col-1] == '*'):
        count += 1
    if (board[row][col+1] == '*'):
        count += 1
    if (board[row+1][col-1] == '*'):
        count += 1
    if (board[row-1][col+1] == '*'):
        count += 1 
    return count

""" Iterates one tick. 
    board must be a list of lists of characters """
def mutateBoard(boardList, rows, cols):
    nextBoardList = list(boardList)
    for i in range(1, rows+1):
        for j in range(1, cols+1):
            if boardList[i][j] == '*':
                if getNeighborCount(boardList, i, j) < 2:
                    nextBoardList[i][j] = ' '
                if getNeighborCount(boardList, i, j) > 3:
                    nextBoardList[i][j] = ' '
            if boardList[i][j] == ' ':
                if getNeighborCount(boardList, i, j) == 3:
                    nextBoardList[i][j] = '*'
    return nextBoardList
            

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# Get the header which contains number of generations
header = s.recv(BUFFER_SIZE).decode("utf-8")
generations = int(header.split( )[3])

# Get the actual game of life board and determine dimensions
board = s.recv(BUFFER_SIZE * 10)
print(board)
board = board.decode('utf-8').split("\n")
numCols = len(board[0]) - 2
numRows = len(board) - 3

# Convert board to a list of lists of characters so characters can be replaced
curBoardList = list()
for i in range(0, numRows+2):
    curBoardList.append(list(board[i]))
for i in range(0, numRows+2):
    print(''.join(curBoardList[i]))


print("Columns: ", numCols, " Rows: ", numRows, " Generations: ", generations)


# Mutate the board 
for i in range(generations):
    curBoardList = mutateBoard(curBoardList, numRows, numCols)
    print("Iteration", i, ":")
    print(curBoardList)
    
    
# Encode final board and send it
for i in range(0, numRows+2):
    curBoardList[i] = ''.join(curBoardList[i])
finalBoard = '\n'.join(curBoardList)

print("Final board:")
print(finalBoard)
print("Sending encoded final board...")
finalBoard += ('\n')
s.send(finalBoard.encode())
print(finalBoard.encode())


# Receive additional data
print("Waiting for additional data...")
newData = s.recv(BUFFER_SIZE).decode('utf-8').split("\n")
print(newData)
s.close()