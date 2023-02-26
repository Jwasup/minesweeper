import pygame
import random
from random import random
import math
from math import trunc
import time
from time import sleep
import os

WIDTH, HEIGHT = 750, 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Minesweeper")

FPS = 60

BLACK = (0, 0, 0)

flag = pygame.image.load(os.path.join('Assets', 'flag.png'))
flag = pygame.transform.scale(flag, (50, 50))

mine = pygame.image.load(os.path.join('Assets', 'mine.png'))
mine = pygame.transform.scale(mine, (50, 50))

blankSquare = pygame.image.load(os.path.join('Assets', 'blankSquare.png'))
blankSquare = pygame.transform.scale(blankSquare, (50, 50))

digits = ['', '', '', '', '', '', '', '', '']
for i in range(9):
    digits[i] = pygame.image.load(os.path.join('Assets', f'{str(i)}.png'))
    digits[i] = pygame.transform.scale(digits[i], (50, 50))

def printBoard(board, shownBoard):
    WIN.fill(BLACK)
    for i in range(15):
        for j in range(15):
            if shownBoard[i][j] == '':
                WIN.blit(blankSquare, (50 * j, 50 * i))
            elif shownBoard[i][j] == 'F':
                WIN.blit(flag, (50 * j, 50 * i))
            elif shownBoard[i][j] == 'R':
                if board[i][j] == 'M':
                    WIN.blit(mine, (50 * j, 50 * i))
                else:
                    WIN.blit(digits[board[i][j]], (50 * j, 50 * i))
    pygame.display.update()

def zeros(board, shownBoard, i, j):
    if shownBoard[i][j] == '':
        shownBoard[i][j] = 'R'
    for a in range(3):
        for b in range(3):
            x = i + a - 1
            y = j + b - 1
            if 0 <= x < 15 and 0 <= y < 15:
                if shownBoard[x][y] == '':
                    if board[x][y] != 0:
                        shownBoard[x][y] = 'R'
                    else:
                        zeros(board, shownBoard, x, y)

def main():
    board = [['']*15 for i in range(15)]
    for i in range(53):
        minePlaced = False
        while minePlaced == False:
            randomX = trunc(random() * 15)
            randomY = trunc(random() * 15)
            if board[randomX][randomY] == '':
                board[randomX][randomY] = 'M'
                minePlaced = True

    shownBoard = [['']*15 for i in range(15)]
    hitMine = False
    firstMove = True
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                mouseX = trunc(mouseX / 50)
                mouseY = trunc(mouseY / 50)
                if event.button == 3:
                    if shownBoard[mouseY][mouseX] == '':
                        shownBoard[mouseY][mouseX] = 'F'
                    elif shownBoard[mouseY][mouseX] == 'F':
                        shownBoard[mouseY][mouseX] = ''
                elif event.button == 1:
                    if shownBoard[mouseY][mouseX] == '':
                        if firstMove == True:
                            firstMove = False
                            for i in range(3):
                                for j in range(3):
                                    board[mouseY - 1 + i][mouseX - 1 + j] = ''
                        
                        for i in range(15):
                            for j in range(15):
                                if board[i][j] != 'M':
                                    total = 0
                                    for k in range(3):
                                        for l in range(3):
                                            x = i + k - 1
                                            y = j + l - 1
                                            if x >= 0 and y >= 0 and x < 15 and y < 15 and (x != 1 or y != 1):
                                                if board[x][y] == 'M':
                                                    total += 1
                                    board[i][j] = total

                        shownBoard[mouseY][mouseX] = 'R'
                        value = board[mouseY][mouseX]
                        if value == 'M':
                            run = False
                            hitMine = True
                        elif value == 0:
                            zeros(board, shownBoard, mouseY, mouseX)
                
                revealedTileCounter = 0
                for i in range(15):
                    for j in range(15):
                        if shownBoard[i][j] ==  'R':
                            revealedTileCounter += 1
                if revealedTileCounter >= 185:
                    run = False

        printBoard(board, shownBoard)
    if hitMine == True:
        shownBoard = [['R']*15 for i in range(15)]
    printBoard(board, shownBoard)
    sleep(4)
            


if __name__ == "__main__":
    main()