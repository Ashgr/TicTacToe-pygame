
import random, pygame, sys

from pygame.locals import *

FPS = 30

WINDOWWIDTH = 640  # width of the window in pixels

WINDOWHEIGHT = 500  # height of the window in pixels

GRIDWIDTH = 3  # number of colomns in the grid

GRIDHEIGHT = 3  # number of rows in the grid

BOXSIZE = 100  # width and height of each box in pixels

GAPSIZE = 4  # gap between each box in pixels

XMARGIN = int((WINDOWWIDTH - (BOXSIZE * GRIDWIDTH + (GRIDWIDTH - 1))) / 2)

YMARGIN = int((WINDOWHEIGHT - (BOXSIZE * GRIDHEIGHT + (GRIDHEIGHT - 1))) / 2)

X = 'X'

O = 'O'

BASICFONTSIZE = 20

MSG = "Player1 is X and Player 2 is O"

#        R    G    B

GRAY = (100, 100, 100)

NAVYBLUE = (60, 60, 100)

WHITE = (255, 255, 255)

RED = (255, 0, 0)

GREEN = (0, 255, 0)

BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)

ORANGE = (255, 128, 0)

PURPLE = (255, 0, 255)

CYAN = (0, 255, 255)

BGCOLOR = NAVYBLUE

LIGHTBGCOLOR = GRAY

BOXCOLOR = WHITE

HIGHLIGHTCOLOR = BLUE

XMARK = "xmark"

OMARK = "omark"


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, WINNER, AGAIN_SURF, AGAIN_RECT, PSURF, PRECT

    WINNER = None  # this vairable will be equal to the player when the game is won and dosen't accept any clicks

    winningCoords = None

    pygame.init()

    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    BASICFONT = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)

    mousex = 0  # used to track the x coordinate of the mouse

    mousey = 0  # used to track the y coordinate of the mouse

    clickCount = 0  # used to identify the player; first if odd and second if even

    pygame.display.set_caption("TicTacToe")

    surf, rect = createText(MSG, WHITE, BGCOLOR, 5, 5)

    AGAIN_SURF, AGAIN_RECT = createText("Play Again!", NAVYBLUE, GREEN, 500, 400)

    PSURF, PRECT = createText("Player1's turn", WHITE, BGCOLOR, 3, 45)

    usedBoxes = generateUsedBoxList(False)

    usageList = generateUsedBoxList(None)

    while True:

        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)

        DISPLAYSURF.blit(surf, rect)

        DISPLAYSURF.blit(AGAIN_SURF, AGAIN_RECT)

        if clickCount < 9 and WINNER == None:
            DISPLAYSURF.blit(PSURF, PRECT)

        drawGrid(usedBoxes, usageList)

        for event in pygame.event.get():

            if event.type == QUIT:

                pygame.quit()

                sys.exit()

            elif event.type == MOUSEMOTION:

                mousex, mousey = event.pos

            elif event.type == MOUSEBUTTONUP:

                if WINNER == None:
                    mousex, mousey = event.pos

                    mouseClicked = True

                if AGAIN_RECT.collidepoint(mousex, mousey):
                    WINNER = None

                    clickCount = 0

                    usedBoxes = generateUsedBoxList(False)

                    usageList = generateUsedBoxList(None)

                    PSURF, PRECT = createText("Player1's turn", WHITE, BGCOLOR, 3, 45)

        if WINNER == None:


            boxx, boxy = getBoxAtPixel(mousex, mousey)

            if boxx != None and boxy != None:

                # mouse is over a box

                if not usedBoxes[boxx][boxy] and mouseClicked:

                    usedBoxes[boxx][boxy] = True

                    clickCount += 1

                    if clickCount % 2 == 1:

                        # clickCount is odd so first player

                        PSURF, PRECT = createText("Player2's turn", WHITE, BGCOLOR, 3, 45)

                        drawX(boxx, boxy)

                        usageList[boxx][boxy] = X

                    elif clickCount % 2 == 0:

                        # clickCount is even so second player

                        PSURF, PRECT = createText("Player1's turn", WHITE, BGCOLOR, 5, 45)

                        drawO(boxx, boxy)

                        usageList[boxx][boxy] = O

            if clickCount > 4:
                WINNER, winningCoords = checkStatus(usedBoxes, usageList, WINNER)

            if clickCount == 9 and WINNER == None:
                wsurf, wrect = createText("There is no winner", WHITE, BGCOLOR, 5, 25)

                DISPLAYSURF.blit(wsurf, wrect)

        else:


            coords = drawWinningLine(winningCoords)

            pygame.draw.lines(DISPLAYSURF, (0,0,0), False, coords, 7)

            wsurf, wrect = createText(WINNER + " is the winner", WHITE, BGCOLOR, 5, 25)

            DISPLAYSURF.blit(wsurf, wrect)

        FPSCLOCK.tick(FPS)

        pygame.display.update()


def generateUsedBoxList(val):
    usedboxes = []

    for i in range(GRIDWIDTH):
        usedboxes.append([val] * GRIDHEIGHT)

    return usedboxes


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates

    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN

    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN

    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(GRIDWIDTH):

        for boxy in range(GRIDHEIGHT):

            left, top = leftTopCoordsOfBox(boxx, boxy)

            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)

            if boxRect.collidepoint(x, y):
                return (boxx, boxy)

    return (None, None)


def checkStatus(usedBoxes, usageList, WINNER):
    simulX = 0

    simulO = 0

    simulBoxX = []

    simulBoxO = []

    # check all the rows

    for x in range(GRIDWIDTH):

        for y in range(GRIDHEIGHT):

            if usedBoxes[x][y]:

                if usageList[x][y] == X:

                    simulX += 1

                    simulBoxX.append((x, y))

                elif usageList[x][y] == O:

                    simulO += 1

                    simulBoxO.append((x, y))

        if simulX == 3:

            print("player1 is winner!")

            WINNER = "player1"

            return (WINNER, simulBoxX)

        elif simulO == 3:

            print("player2 is winner!")

            WINNER = "player2"

            return (WINNER, simulBoxO)

        else:

            simulX = 0

            simulO = 0

            simulBoxX = []

            simulBoxO = []

    # check all the columns

    for y in range(GRIDHEIGHT):

        for x in range(GRIDWIDTH):

            if usedBoxes[x][y]:

                if usageList[x][y] == X:

                    simulX += 1

                    simulBoxX.append((x, y))

                elif usageList[x][y] == O:

                    simulO += 1

                    simulBoxO.append((x, y))

        if simulX == 3:

            print("player1 is winner!")

            WINNER = "player1"

            return (WINNER, simulBoxX)

        elif simulO == 3:

            print("player2 is winner!")

            WINNER = "player2"

            return (WINNER, simulBoxO)

        else:

            simulX = 0

            simulO = 0

            simulBoxX = []

            simulBoxO = []

    # check diagonals

    # cheking first diagonal '\'

    for i in range(GRIDWIDTH):

        if usedBoxes[i][i]:

            if usageList[i][i] == X:

                simulX += 1

                simulBoxX.append((i, i))

            elif usageList[i][i] == O:

                simulO += 1

                simulBoxO.append((i, i))

    if simulX == 3:

        print("player1 is winner!")

        WINNER = "player1"

        return (WINNER, simulBoxX)

    elif simulO == 3:

        print("player2 is winner!")

        WINNER = "player2"

        return (WINNER, simulBoxO)

    else:

        simulX = 0

        simulO = 0

        simulBoxX = []

        simulBoxO = []

    # checking second diagonal '/'

    if usedBoxes[0][2] and usedBoxes[1][1] and usedBoxes[2][0]:

        if usageList[0][2] == X:

            simulX += 1

            simulBoxX.append((0, 2))

        else:

            simulO += 1

            simulBoxO.append((0, 2))

        if usageList[1][1] == X:

            simulX += 1

            simulBoxX.append((1, 1))

        else:

            simulO += 1

            simulBoxO.append((1, 1))

        if usageList[2][0] == X:

            simulX += 1

            simulBoxX.append((2, 0))

        else:

            simulO += 1

            simulBoxO.append((2, 0))

        if simulX == 3:

            print("player1 is winner!")

            WINNER = "player1"

            return (WINNER, simulBoxX)

        elif simulO == 3:

            print("player2 is winner!")

            WINNER = "player2"

            return (WINNER, simulBoxO)

        else:

            simulX = 0

            simulO = 0

            simulBoxX = []

            simulBoxO = []

    return (None, None)


def drawGrid(usedBoxes, usageList):
    for x in range(GRIDWIDTH):

        for y in range(GRIDHEIGHT):

            xcoord = (x * (BOXSIZE + GAPSIZE)) + XMARGIN

            ycoord = (y * (BOXSIZE + GAPSIZE)) + YMARGIN

            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (xcoord, ycoord, BOXSIZE, BOXSIZE), 0)

            if usedBoxes[x][y]:

                if usageList[x][y] == X:

                    drawX(x, y)

                elif usageList[x][y] == O:

                    drawO(x, y)


def drawX(boxx, boxy):
    ltx, lty = leftTopCoordsOfBox(boxx, boxy)

    startPoint1 = (ltx, lty)

    endPoint1 = (ltx + BOXSIZE, lty + BOXSIZE)

    startPoint2 = (ltx + BOXSIZE, lty)

    endPoint2 = (ltx, lty + BOXSIZE)

    pygame.draw.line(DISPLAYSURF, BLUE, startPoint1, endPoint1, 6)

    pygame.draw.line(DISPLAYSURF, BLUE, startPoint2, endPoint2, 6)

    return 0


def drawO(boxx, boxy):
    ltx, lty = leftTopCoordsOfBox(boxx, boxy)

    center = (int(ltx + (BOXSIZE / 2)), int(lty + (BOXSIZE / 2)))

    pygame.draw.circle(DISPLAYSURF, RED, center, int((BOXSIZE / 2) - 5), 6)

    return 0


def drawWinningLine(winningCoords):
    coords = []

    if winningCoords[0][0] == winningCoords[1][0]:

        # x coords are equal so its a column

        for i in range(3):
            coordx, coordy = leftTopCoordsOfBox(winningCoords[i][0], winningCoords[i][1])

            coords.append((coordx + (BOXSIZE / 2), coordy))

            coords.append((coordx + (BOXSIZE / 2), coordy + BOXSIZE))

    elif winningCoords[0][1] == winningCoords[1][1]:

        # y coords are equal so its a row

        for i in range(3):
            coordx, coordy = leftTopCoordsOfBox(winningCoords[i][0], winningCoords[i][1])

            coords.append((coordx, coordy + (BOXSIZE / 2)))

            coords.append((coordx + BOXSIZE, coordy + (BOXSIZE / 2)))

    else:  # diagonals

        if winningCoords[0][0] == winningCoords[0][1]:

            for i in range(3):
                coordx, coordy = leftTopCoordsOfBox(winningCoords[i][0], winningCoords[i][1])

                coords.append((coordx, coordy))

                coords.append((coordx + BOXSIZE, coordy + BOXSIZE))

        else:

            for i in range(3):
                coordx, coordy = leftTopCoordsOfBox(winningCoords[i][0], winningCoords[i][1])

                coords.append((coordx + BOXSIZE, coordy))

                coords.append((coordx, coordy + BOXSIZE))

    return coords


def createText(message, color, bgcolor, xcoord, ycoord):
    messageSurf = BASICFONT.render(message, True, color, bgcolor)

    messageRect = messageSurf.get_rect()

    messageRect.topleft = (xcoord, ycoord)

    return (messageSurf, messageRect)


if __name__ == "__main__": main()