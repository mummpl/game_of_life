# coding=utf-8

import pygame, sys
from random import randint

pygame.init()

fps = 100
white = (255, 255, 255)
black = (0, 0, 0)

# screen size
width = 0
height = 0

if width != 0:
    size = width, height
else:
    size = 700, 700

gridSize = 70

blocksize = size[0] / gridSize

universe = []

lastSavedUniverse = ["nothing saved here"]

# randomGridInitializer
for column in range(gridSize):
    tempcolumn = []
    for row in range(gridSize):
        tempcolumn.append(randint(0, 1))
    universe.append(tempcolumn)

# print(universe)

# universe = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

screen = pygame.display.set_mode(size)

randomGame = False

menu = True

builder = False

while menu is True:

    screen.fill(black)

    # random universe button
    menuFont = pygame.font.SysFont('Helvetica', 30)
    randomSurface = menuFont.render("Random Universe", False, white)
    randomSurfaceCoord = (255, 300)
    screen.blit(randomSurface, randomSurfaceCoord)
    randomSurfaceRect = pygame.Rect(randomSurfaceCoord, (175, 50))

    # builder mode button
    builderSurface = menuFont.render("Universe Builder", False, white)
    builderSurfaceCoord = (260, 400)
    screen.blit(builderSurface, builderSurfaceCoord)
    builderSurfaceRect = pygame.Rect(builderSurfaceCoord, (170, 50))

    # proceed events
    for event in pygame.event.get():

        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            if randomSurfaceRect.collidepoint(pos[0], pos[1]):
                randomGame = True
                menu = False
                builder = False

            if builderSurfaceRect.collidepoint(pos[0], pos[1]):
                randomGame = False
                menu = False
                builder = True
        if event.type == pygame.QUIT:
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit()

    pygame.display.flip()

while randomGame is True:

    clock = pygame.time.Clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            randomGame = False
            menu = True
            builder = False

    screen.fill(black)

    # draw the latest state
    for column in range(gridSize):
        for row in range(gridSize):
            rect = pygame.Rect(column * blocksize, row * blocksize, blocksize, blocksize)
            if universe[column][row] == 1:
                pygame.draw.rect(screen, white, rect)
            else:
                pygame.draw.rect(screen, black, rect)

    # update the state
    tempUniverse = []

    for column in range(gridSize):
        tempColumn = []
        for row in range(gridSize):
            tempColumn.append(0)
        tempUniverse.append(tempColumn)

    # applying game rules
    for column in range(gridSize):
        for row in range(gridSize):
            # counting
            counter = 0

            # above
            if row > 0:
                if universe[column][row - 1] == 1:
                    counter += 1

            # below
            if row < gridSize - 1:
                if universe[column][row + 1] == 1:
                    counter += 1

            # right
            if column < gridSize - 1:
                if universe[column + 1][row] == 1:
                    counter += 1

            # left
            if column > 0:
                if universe[column - 1][row] == 1:
                    counter += 1

            # above_right
            if row > 0 and column < gridSize - 1:
                if universe[column + 1][row - 1] == 1:
                    counter += 1

            # above_left
            if row > 0 and column > 0:
                if universe[column - 1][row - 1] == 1:
                    counter += 1

            # below_right
            if row < gridSize - 1 and column < gridSize - 1:
                if universe[column + 1][row + 1] == 1:
                    counter += 1

            # below_left
            if row < gridSize - 1 and column > 0:
                if universe[column - 1][row + 1] == 1:
                    counter += 1

            # thumbs up or down
            if universe[column][row] == 0:
                if counter == 3:
                    tempUniverse[column][row] = 1
            if universe[column][row] == 1:
                if counter != 2 and counter != 3:
                    tempUniverse[column][row] = 0
                else:
                    tempUniverse[column][row] = 1

    # bring new universe into place
    universe = tempUniverse

    clock.tick(fps)
    pygame.display.flip()

# Builder module
while builder is True:

    # initialization
    clock = pygame.time.Clock()

    screen.fill(black)

    simulationMode = False
    drawMode = True

    # initialize empty universe
    universe = []
    for column in range(gridSize):
        tempColumn = []
        for row in range(gridSize):
            tempColumn.append(0)
        universe.append(tempColumn)

    # draw mode
    while drawMode is True:

        # initialization
        clock = pygame.time.Clock()

        if lastSavedUniverse != ["nothing saved here"]:
            universe = lastSavedUniverse

        # draw the latest state
        for column in range(gridSize):
            for row in range(gridSize):
                rect = pygame.Rect(column * blocksize, row * blocksize, blocksize, blocksize)
                if universe[column][row] == 1:
                    pygame.draw.rect(screen, white, rect)
                else:
                    pygame.draw.rect(screen, black, rect)

        # handle user interaction
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for column in range(gridSize):
                    for row in range(gridSize):
                        rect = pygame.Rect(column * blocksize, row * blocksize, blocksize, blocksize)
                        if rect.collidepoint(pos[0], pos[1]):
                            if universe[column][row] == 0:
                                universe[column][row] = 1
                            else:
                                universe[column][row] = 0

            # switching into simulation mode
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                lastSavedUniverse = universe
                drawMode = False
                simulationMode = True

            if event.type == pygame.QUIT:
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()

        clock.tick(fps)
        pygame.display.flip()

    while simulationMode is True:

        # initialization
        clock = pygame.time.Clock()

        # draw the latest state
        for column in range(gridSize):
            for row in range(gridSize):
                rect = pygame.Rect(column * blocksize, row * blocksize, blocksize, blocksize)
                if universe[column][row] == 1:
                    pygame.draw.rect(screen, white, rect)
                else:
                    pygame.draw.rect(screen, black, rect)

        # update the state
        tempUniverse = []

        for column in range(gridSize):
            tempColumn = []
            for row in range(gridSize):
                tempColumn.append(0)
            tempUniverse.append(tempColumn)

        # applying game rules
        for column in range(gridSize):
            for row in range(gridSize):
                # counting
                counter = 0

                # above
                if row > 0:
                    if universe[column][row - 1] == 1:
                        counter += 1

                # below
                if row < gridSize - 1:
                    if universe[column][row + 1] == 1:
                        counter += 1

                # right
                if column < gridSize - 1:
                    if universe[column + 1][row] == 1:
                        counter += 1

                # left
                if column > 0:
                    if universe[column - 1][row] == 1:
                        counter += 1

                # above_right
                if row > 0 and column < gridSize - 1:
                    if universe[column + 1][row - 1] == 1:
                        counter += 1

                # above_left
                if row > 0 and column > 0:
                    if universe[column - 1][row - 1] == 1:
                        counter += 1

                # below_right
                if row < gridSize - 1 and column < gridSize - 1:
                    if universe[column + 1][row + 1] == 1:
                        counter += 1

                # below_left
                if row < gridSize - 1 and column > 0:
                    if universe[column - 1][row + 1] == 1:
                        counter += 1

                # thumbs up or down
                if universe[column][row] == 0:
                    if counter == 3:
                        tempUniverse[column][row] = 1
                if universe[column][row] == 1:
                    if counter != 2 and counter != 3:
                        tempUniverse[column][row] = 0
                    else:
                        tempUniverse[column][row] = 1

        # bring new universe into place
        universe = tempUniverse

        # handle user interaction
        for event in pygame.event.get():

            if pygame.key.get_pressed()[pygame.K_RETURN]:
                drawMode = True
                simulationMode = False

            if event.type == pygame.QUIT:
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()

        clock.tick(fps)
        pygame.display.flip()

    clock.tick(fps)
    pygame.display.flip()
