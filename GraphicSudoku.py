# Author: Javi Barranco
# Name: GraphicSudoku

import sys
import os
import time
import random
import pygame
from Sudoku import *

pygame.init()

# Assets path:
icon_path = os.path.join("assets", "icon.png")

# Display control:
displayWidth = 462
displayHeight = 565
displayLineExtra = 12
displayFooter = displayHeight - displayWidth
displayWidthCal = displayWidth - displayLineExtra
displayHeightCal = displayHeight - displayFooter - displayLineExtra
icon = pygame.image.load(icon_path)

display = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Sudoku by JaviBT')
pygame.display.set_icon(icon)

# Colors:
white = (255,255,255)
black = (0,0,0)
grey = (200,200,200)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

# Font control:
tinyfont = pygame.font.SysFont("comicsansms",20)
smallfont = pygame.font.SysFont("helvetica", 30)
mediumfont = pygame.font.SysFont("helvetica", 40)
largefont = pygame.font.SysFont("helvetica",50)
massivefont = pygame.font.SysFont("helvetica", 65)
numberDisplayFont = pygame.font.SysFont("helvetica",30)

# FPS
clock = pygame.time.Clock()
FPS = 15

# Other variables:
numMistakes = 0

# Main sudoku:
Sudoku = [[0,0,0,2,6,0,7,0,1],
          [6,8,0,0,7,0,0,9,0],
          [1,9,0,0,0,4,5,0,0],
          [8,2,0,1,0,0,0,4,0],
          [0,0,4,6,0,2,9,0,0],
          [0,5,0,0,0,3,0,2,8],
          [0,0,9,3,0,0,0,7,4],
          [0,4,0,0,5,0,0,3,6],
          [7,0,3,0,1,8,0,0,0]]

Empty_board = [[0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0]]

# This sudoku exists for test purposes
Solved_Sudoku = [[4,3,5,3,6,9,7,8,1],
                 [6,8,2,5,7,1,4,9,3],
                 [1,9,7,8,3,4,5,6,2],
                 [8,2,6,1,9,5,3,4,7],
                 [3,7,4,6,8,2,9,1,5],
                 [9,5,1,7,4,3,6,2,8],
                 [5,1,9,3,2,6,8,7,4],
                 [2,4,8,9,5,7,1,3,6],
                 [7,6,3,4,1,8,2,5,0]]


class Grid:
    def __init__(self, Board):
        self.grid = []
        block_id = 1
        y_displacement = 0
        for i in range(len(Board)):
            x_displacement = 0
            for j in range(len(Board[i])):
                base = False
                if Board[i][j] != 0: base = True
                self.grid.append(Block(block_id,j*int(displayWidthCal/9)+x_displacement,i*int(displayHeightCal/9)+y_displacement,Board[i][j],base))
                if j%3 == 2: x_displacement += 3
                else: x_displacement += 1
                block_id += 1
            if i%3 == 2: y_displacement += 3
            else: y_displacement += 1
        self.rows = len(Board)
        self.cols = len(Board[1])

    def print(self):
        print("\n\n\nThe currend Sudoku is:\n")
        for i in range(self.rows*self.cols):
            print("{}".format(self.grid[i].value), end='')
            if i%3 == 2:
                if i%27 == 26:
                    print("\n---------------------")
                elif i%9 == 8:
                    print("")
                else:
                    print(" | ", end='')
            else:
                print(" ", end='')

    def print_block(self):
        print("\n\nThe block data: \n")
        for i in range(self.rows*self.cols):
            print("     - ", end='')
            self.grid[i].print()

class Block:
    def __init__(self,id,x_pos,y_pos,value,base):
        self.id = id
        self.x = x_pos
        self.y = y_pos
        self.value = value
        self.width = 50
        self.height = 50
        self.base = base
        self.temp = -1

    def print(self):
        print("Block {}: position ({},{}), value {}, temp {}, base {}".format(self.id,self.x,self.y,self.value,self.temp,self.base))

def alertMistake(block):
    global numMistakes
    pygame.draw.line(display, red, (block.x,block.y), (block.x+block.width,block.y+block.height),3)
    pygame.draw.line(display, red, (block.x+block.width,block.y), (block.x,block.y+block.height),3)
    pygame.display.update()
    numMistakes += 1
    time.sleep(0.5)

def getBlockIndex(pos, grid):
    x = pos[0]
    y = pos[1]
    for i in range(len(grid.grid)):
        if (x>=grid.grid[i].x and x<=grid.grid[i].x+grid.grid[i].width) and (y>=grid.grid[i].y and y<=grid.grid[i].y+grid.grid[i].height) and y < displayHeight - displayFooter:
            return i
    return -1

def userClick(pos,grid):
    userClick = True
    valueIntro = False
    index = getBlockIndex(pos, grid)
    block = grid.grid[index]
    if block.base == True or index == -1:
        print("Illigal click recorded at {}".format(pos))
        return
    print("Click recorded at {}".format(pos))
    pygame.draw.rect(display,red,[block.x,block.y,block.width,block.height],3)
    pygame.display.update()
    while userClick == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                userClick = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    userClick = False
                if event.key == pygame.K_c:
                    block.temp = -1
                    block.value = 0
                    userClick = False
                elif event.key == pygame.K_RETURN:
                    if block.temp != -1 and solvable(grid,index) == True:
                        block.value = block.temp
                        block.temp = -1
                        userClick = False
                    else:
                        if block.value == 0:
                            alertMistake(block)
                            block.temp = -1
                            userClick = False
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    block.temp = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    block.temp = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    block.temp = 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    block.temp = 4
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    block.temp = 5
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    block.temp = 6
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    block.temp = 7
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    block.temp = 8
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    block.temp = 9
                SketchNumberToScreen(block)
                userClick = False

def MainMenu():
    MainMenu = True

    display.fill(white)
    messageToScreen("Sudoku Project", (int(displayWidth/2),int(displayHeight/2-50)),massivefont,black)
    messageToScreen("Press 'i' to see instructions",(int(displayWidth/2),int(displayHeight/2+20)),smallfont,grey)
    messageToScreen("Press 'ENTER' to start",(int(displayWidth/2),int(displayHeight/2)),smallfont,grey)
    pygame.display.update()
    while MainMenu == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MainMenu = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_i:
                    showInstructions()
                if event.key == pygame.K_RETURN:
                    gameLoop()
    return False

def EndScreen(time1):
    EndScreen = True
    FinalTime = time.time() - time1

    display.fill(white)
    messageToScreen("CONGRATULATIONS!", (displayWidth/2,displayHeight/2-85),largefont,black)
    messageToScreen("YOU SOLVED THE SUDOKU", (displayWidth/2,displayHeight/2-50),largefont,black)
    messageToScreen(("Total Time: %.0f"%FinalTime),(displayWidth/2,displayHeight/2),mediumfont,grey)
    messageToScreen(("Total Mistakes: %d"%numMistakes),(displayWidth/2,displayHeight/2+35),mediumfont,grey)
    messageToScreen(("Press 'ENTER' to return to the"),(displayWidth/2,displayHeight/2+75),smallfont,grey)
    messageToScreen(("main menu or press 'q' to quit"),(displayWidth/2,displayHeight/2+100),smallfont,grey)
    pygame.display.update()

    while EndScreen == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EndScreen == False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    EndScreen = False
                if event.key == pygame.K_RETURN:
                    MainMenu()

    pygame.quit()
    quit()

def showInstructions():
    showInstructions = True

    display.fill(white)
    messageToScreen("Instructions", (int(displayWidth/2),int(displayHeight/2-50)-175),massivefont,black)
    messageToScreen("To select a cell from the grid click on it",(int(displayWidth/2),int(displayHeight/2-160)),tinyfont,grey)
    messageToScreen("Once selected the cell will have a red border",(int(displayWidth/2),int(displayHeight/2-140)),tinyfont,grey)
    messageToScreen("When a cell is selected you can:                                          ",(int(displayWidth/2),int(displayHeight/2-110)),tinyfont,grey)
    messageToScreen("- Press 'v': Deselects the cell                                            ",(int(displayWidth/2),int(displayHeight/2-90)),tinyfont,grey)
    messageToScreen("- Press 'c': Clear the content of the cell                             ",(int(displayWidth/2),int(displayHeight/2-70)),tinyfont,grey)
    messageToScreen("- Press Number: Will sketch that number on the cell           ",(int(displayWidth/2),int(displayHeight/2-50)),tinyfont,grey)
    messageToScreen("- Press ENTER: Will draw the current sketch on the cell     ",(int(displayWidth/2),int(displayHeight/2-30)),tinyfont,grey)
    messageToScreen("The game checks whether the sudoku is still solvable after",(int(displayWidth/2),int(displayHeight/2+30)),tinyfont,grey)
    messageToScreen("drawing a number rather than whether the number is valid",(int(displayWidth/2),int(displayHeight/2+50)),tinyfont,grey)
    messageToScreen("While you are at a menu, pressing 'Enter'",(int(displayWidth/2),int(displayHeight/2+100)),tinyfont,grey)
    messageToScreen("will move you on to the next menu.",(int(displayWidth/2),int(displayHeight/2+120)),tinyfont,grey)
    messageToScreen("Pressing 'j' during a game will complete the sudoku",(int(displayWidth/2),int(displayHeight/2+170)),tinyfont,grey)
    pygame.display.update()

    while showInstructions == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showInstructions = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    showInstructions = False
                    MainMenu()
                if event.key == pygame.K_q:
                    showInstructions = False
    pygame.quit()
    quit()
# Calling this function every loop of gameLoop is not efficient.
def checkComplete(grid,Autocomplete):
    tempgrid = Empty_board
    i = 0
    for j in range(len(grid.grid)):
        tempgrid[i][j%9] = grid.grid[j].value
        if j%9 == 8:
            i += 1
    for i in range(len(tempgrid)):
        for j in range(len(tempgrid[i])):
            if tempgrid[i][j] == 0:
                return False
    pygame.draw.rect(display,green,[0,0,displayWidth,displayHeight-displayFooter],10)
    textSurface = largefont.render("COMPLETED",True,green)
    textRect = textSurface.get_rect()
    textRect.center = ((displayWidth/2),((displayHeight-displayFooter + displayHeight)/2))
    pygame.draw.rect(display,white,[0,displayHeight-displayFooter,displayWidth,displayFooter],0)
    display.blit(textSurface,textRect)
    if Autocomplete == True:
        messageToScreen("Press 'ENTER' to return to main menu",(int(displayWidth/2),int(displayHeight-displayFooter + displayHeight)/2+30),tinyfont,grey)
        pygame.display.update()
        while Autocomplete == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Autocomplete = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Autocomplete = False
                    if event.key == pygame.K_q:
                        Autocomplete = False
                        pygame.quit()
                        quit()
    pygame.display.update()
    if Autocomplete == False: time.sleep(3)
    return True

def messageToScreen(msg, pos, fontType, color):
    textSurface = fontType.render(msg,True,color)
    textRect = textSurface.get_rect()
    textRect.center = (pos[0],pos[1])
    display.blit(textSurface, textRect)

def timeToScreen(time1):
    currentTime = time.time() - time1
    M = 0.85
    if currentTime > 9: M += 0.02
    if currentTime > 99: M += 0.02
    msg1 = ("Time: ")
    msg2 = ("%.0f" % currentTime)
    textSurface1 = mediumfont.render(msg1,True,black)
    textSurface2 = mediumfont.render(msg2,True,black)
    textRect1 = textSurface1.get_rect()
    textRect2 = textSurface2.get_rect()
    textRect1.center = (displayWidth*0.75,(displayHeight-displayFooter + displayHeight)/2)
    textRect2.center = (displayWidth*M,(displayHeight-displayFooter + displayHeight)/2)
    display.blit(textSurface1,textRect1)
    display.blit(textSurface2,textRect2)

def numberToScreen(block):
    if block.value != 0:
        textSurface = numberDisplayFont.render(str(block.value),True,black)
    elif block.temp != -1 and block.temp != 0:
        textSurface = numberDisplayFont.render(str(block.temp),True,grey)
    else:
        return
    textRect = textSurface.get_rect()
    textRect.center = ((block.x+block.x+block.width)/2),((block.y+block.y+block.height)/2) # Centers the textRect at the given coordinates x,y
    display.blit(textSurface,textRect)

def SketchNumberToScreen(block):
    if block.temp == -1:
        return
    textSurface = numberDisplayFont.render(str(block.temp),True,grey)
    textRect = textSurface.get_rect()
    textRect.center = ((block.x+block.x+block.width)/2),((block.y+block.y+block.height)/2) # Centers the textRect at the given coordinates x,y
    display.blit(textSurface,textRect)
    pygame.display.update()

def solvable(grid,index):
    tempgrid = Empty_board
    i = 0
    for j in range(len(grid.grid)):
        tempgrid[i][j%9] = grid.grid[j].value
        if j == index:
            if valid(tempgrid,grid.grid[index].temp,i,j%9):
                 tempgrid[i][j%9] = grid.grid[index].temp
            else:
                return False
        if j%9 == 8:
            i += 1
    if solve(tempgrid) == True:
        return True
    else: return False

def Autocomplete(grid,time1):
    tempgrid = Empty_board
    i = 0
    for j in range(len(grid.grid)):
        tempgrid[i][j%9] = grid.grid[j].value
        if j%9 == 8:
            i += 1
    if solve(tempgrid) == True:
        insertIndex = 0
        for i in range(len(tempgrid)):
            for j in range(len(tempgrid[i])):
                grid.grid[insertIndex].value = tempgrid[i][j]
                insertIndex += 1
        updateScreen(grid,time1)
        checkComplete(grid,True)
        MainMenu()
    else: MainMenu()

def updateScreen(grid, time1):
    # Frame Update
    display.fill(white)
    # Creates the sudoku grid
    j = 1
    for i in range(1,9):
        # Draws 2 grey lines followed by a thicker black line (In both the x and y axis)
        if i%3 == 0:
            pygame.draw.line(display, black, (i*(displayWidthCal/9)+j,0), (i*(displayWidthCal/9)+j,displayHeight-displayFooter), 3)
            pygame.draw.line(display, black, (0,i*(displayHeightCal/9)+j), (displayWidth,i*(displayHeightCal/9)+j), 3)
            j += 3
        else:
            pygame.draw.line(display, grey, (i*(displayWidthCal/9)+j,0), (i*(displayWidthCal/9)+j,displayHeight-displayFooter), 1)
            pygame.draw.line(display, grey, (0,i*(displayHeightCal/9)+j), (displayWidth,i*(displayHeightCal/9)+j), 1)
            j += 1
    # Draws the line that separates the grid from the footer
    pygame.draw.line(display,black,(0,displayHeight-displayFooter+1),(displayWidth,displayHeight-displayFooter+1),3)
    # Displays time and mistakes in the footer
    timeToScreen(time1)
    messageToScreen(("Mistakes: %d"%numMistakes),(displayWidth*0.225,(displayHeight-displayFooter + displayHeight)/2),mediumfont,black)
    # Displays the numbers
    for i in range(0,len(grid.grid)):
        numberToScreen(grid.grid[i])
    pygame.display.update()
    clock.tick(FPS)

def gameLoop():
    global numMistakes
    # Flags:
    gameExit = True
    time1 = time.time()

    grid = Grid(Sudoku)
    grid.print_block()
    grid.print()

    # GameLoop
    while gameExit == True:
        if checkComplete(grid,False) == True:
            EndScreen(time1)
        for event in pygame.event.get():
            # Checks quit from pressing EXIT from window
            if event.type == pygame.QUIT:
                gameExit = False
            # Checks quit from pressing 'k'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameExit = False
                if event.key == pygame.K_j:
                    Autocomplete(grid, time1)

        # Checks mouse clicks
        mouse_state = pygame.mouse.get_pressed()
        if mouse_state[0] == True:
            posClick = pygame.mouse.get_pos()
            userClick(posClick, grid)
        # Update Screen:
        updateScreen(grid,time1)

    # Quit
    pygame.quit()
    quit()

#################

MainMenu()
pygame.quit()
quit()
