import random
import pygame
import numpy

# initialize pygame so that fonts work
pygame.init()

# Colors
BG_COLOR = (54, 48, 48)
DEFAULT_SQUARE_COLOR = (227, 216, 216)
FLAG_SQUARE_COLOR = (212, 53, 53)
CLEAR_SQUARE_COLOR = (250, 245, 245)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Sizes
SQUARE_SIZE = 35  # The size of the squares in pixels
GAP_SIZE = 2  # The size of the gap between squares in pixels

# Menu Dimensions
MENU_X = 600
MENU_Y = 500
MENU_BUTTON_WIDTH = 100
MENU_BUTTON_HEIGHT = 60

# Fonts
DEFAULT_FONT = pygame.font.Font(None, 20)
MENU_FONT = pygame.font.Font(None, 50)


class BoardSquares:
    rect = None
    color = None
    value = None
    index1 = None
    index2 = None

    def __init__(self, x: int, y: int, color: tuple[int, int, int], value: int, index1: int, index2: int):
        self.rect = pygame.rect.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        self.color = color
        self.value = value
        self.index1 = index1
        self.index2 = index2

    def changeColor(self, color: tuple[int, int, int]):
        self.color = color


def generateMines(board, mines: int):
    locations = [0] * mines  # locations for mines
    squares = len(board) * len(board[0])  # total number of squares on the board
    for i in range(len(locations)):
        go = False
        while not go:
            location = random.randint(0, squares-1)
            valid = True
            for u in range(i):
                if locations[u] == location:
                    valid = False
            if valid:
                go = True
                locations[i] = location
    for location in locations:
        board[location // len(board[0])][location % len(board[0])] = -1


def generateNumbers(board):
    for i in range(len(board)):
        for u in range(len(board[0])):
            score = 0
            if board[i][u] != -1:
                # Top-Left
                if i > 0 and u > 0 and board[i-1][u-1] == -1:
                    score += 1
                # Top-Center
                if i > 0 and board[i-1][u] == -1:
                    score += 1
                # Top-Right
                if i > 0 and u < len(board[0])-1 and board[i-1][u+1] == -1:
                    score += 1
                # Left-Center
                if u > 0 and board[i][u-1] == -1:
                    score += 1
                # Right-Center
                if u < len(board[0])-1 and board[i][u+1] == -1:
                    score += 1
                # Bottom-Left
                if i < len(board)-1 and u > 0 and board[i+1][u-1] == -1:
                    score += 1
                # Bottom-Center
                if i < len(board)-1 and board[i+1][u] == -1:
                    score += 1
                # Bottom-Right
                if i < len(board)-1 and u < len(board[0])-1 and board[i+1][u+1] == -1:
                    score += 1
                board[i][u] = score


def clearSquareAndAdjacent(square: BoardSquares, board, squares: list[BoardSquares], screen: pygame.display):
    i = square.index1
    u = square.index2

    squares_per_row = len(board[0])

    if square.value == 0 and square.color == DEFAULT_SQUARE_COLOR:

        square.changeColor(CLEAR_SQUARE_COLOR)
        pygame.draw.rect(screen, square.color, square.rect)

        index = squares.index(square)
        # Top-Left
        if i > 0 and u > 0:
            clearSquareAndAdjacent(squares[index - squares_per_row - 1], board, squares, screen)
        # Top-Center
        if i > 0:
            clearSquareAndAdjacent(squares[index - squares_per_row], board, squares, screen)
        # Top-Right
        if i > 0 and u < len(board[0]) - 1:
            clearSquareAndAdjacent(squares[index - squares_per_row + 1], board, squares, screen)
        # Left-Center
        if u > 0:
            clearSquareAndAdjacent(squares[index - 1], board, squares, screen)
        # Right-Center
        if u < len(board[0]) - 1:
            clearSquareAndAdjacent(squares[index + 1], board, squares, screen)
        # Bottom-Left
        if i < len(board) - 1 and u > 0:
            clearSquareAndAdjacent(squares[index + squares_per_row - 1], board, squares, screen)
        # Bottom-Center
        if i < len(board) - 1:
            clearSquareAndAdjacent(squares[index + squares_per_row], board, squares, screen)
        # Bottom-Right
        if i < len(board) - 1 and u < len(board[0]) - 1:
            clearSquareAndAdjacent(squares[index + squares_per_row + 1], board, squares, screen)

    if square.value != 0 and square.value != -1 and square.color == DEFAULT_SQUARE_COLOR:
        square.changeColor(CLEAR_SQUARE_COLOR)
        pygame.draw.rect(screen, square.color, square.rect)
        text = DEFAULT_FONT.render(str(square.value), True, (0, 0, 0))
        screen.blit(text, square.rect)


def runMenuWindow(instructions="Select an option from below:"):
    screen = pygame.display.set_mode((MENU_X, MENU_Y))
    screen.fill(CLEAR_SQUARE_COLOR)
    pygame.display.flip()

    easy_button = pygame.rect.Rect(MENU_X/2 - MENU_BUTTON_WIDTH/2, MENU_Y/2 - MENU_BUTTON_HEIGHT/2 - MENU_BUTTON_HEIGHT - 5,
                                   MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
    medium_button = pygame.rect.Rect(
        MENU_X / 2 - MENU_BUTTON_WIDTH / 2, MENU_Y / 2 - MENU_BUTTON_HEIGHT / 2,
        MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
    hard_button = pygame.rect.Rect(
        MENU_X / 2 - MENU_BUTTON_WIDTH / 2, MENU_Y / 2 - MENU_BUTTON_HEIGHT / 2 + MENU_BUTTON_HEIGHT + 5,
        MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)

    pygame.draw.rect(screen, FLAG_SQUARE_COLOR, easy_button)
    pygame.draw.rect(screen, FLAG_SQUARE_COLOR, medium_button)
    pygame.draw.rect(screen, FLAG_SQUARE_COLOR, hard_button)

    easy_text = DEFAULT_FONT.render('Easy', True, WHITE)
    easy_text_rect = easy_text.get_rect(center=easy_button.center)
    screen.blit(easy_text, easy_text_rect)

    medium_text = DEFAULT_FONT.render('Medium', True, WHITE)
    medium_text_rect = medium_text.get_rect(center=medium_button.center)
    screen.blit(medium_text, medium_text_rect)

    hard_text = DEFAULT_FONT.render('Hard', True, WHITE)
    hard_text_rect = hard_text.get_rect(center=hard_button.center)
    screen.blit(hard_text, hard_text_rect)

    instructions_text = DEFAULT_FONT.render(instructions, True, BG_COLOR)
    instructions_text_rect = instructions_text.get_rect(center=(easy_button.center[0], easy_button.center[1]-100))
    screen.blit(instructions_text, instructions_text_rect)

    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                if pygame.rect.Rect(easy_button).collidepoint(pos):
                    return 10, 10, 8
                elif pygame.rect.Rect(medium_button).collidepoint(pos):
                    return 16, 16, 40
                elif pygame.rect.Rect(hard_button).collidepoint(pos):
                    return 30, 16, 99


# Returns true if the user wins or false if they lose
def runGameWindow(x: int, y: int, board):

    squares = []

    screen = pygame.display.set_mode((x*SQUARE_SIZE + GAP_SIZE*(x-1), y*SQUARE_SIZE + GAP_SIZE*(y-1)))
    screen.fill(BG_COLOR)
    pygame.display.flip()
    for i in range(y):
        for u in range(x):
            value = board[i][u]
            square = BoardSquares(u * SQUARE_SIZE + u * GAP_SIZE, i * SQUARE_SIZE + i * GAP_SIZE, DEFAULT_SQUARE_COLOR, value, i, u)
            pygame.draw.rect(screen, square.color, square.rect)

            # Show all scores
            # text = default_font.render(str(square.value), True, (0,0,0))
            # screen.blit(text,square.rect)

            squares.append(square)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
        pygame.display.flip()

        # Checking for win
        win = True
        for square in squares:
            if square.color != CLEAR_SQUARE_COLOR and square.value != -1:
                win = False
        if win:
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # Flagging
                    if pygame.mouse.get_pressed()[2]:
                        for square in squares:
                            if pygame.rect.Rect(square.rect).collidepoint(pos):
                                if square.color == FLAG_SQUARE_COLOR:
                                    square.changeColor(DEFAULT_SQUARE_COLOR)
                                    pygame.draw.rect(screen, square.color, square.rect)
                                elif square.color == DEFAULT_SQUARE_COLOR:
                                    square.changeColor(FLAG_SQUARE_COLOR)
                                    pygame.draw.rect(screen, square.color, square.rect)

                    # Discovering
                    if pygame.mouse.get_pressed()[0]:
                        for square in squares:
                            if pygame.rect.Rect(square.rect).collidepoint(pos):
                                if square.color == DEFAULT_SQUARE_COLOR:
                                    if square.value == -1:
                                        return False
                                    else:
                                        clearSquareAndAdjacent(square, board, squares, screen)


def runGame():
    instructions = None
    while True:
        if instructions is None:
            desired_difficulty = runMenuWindow()
        else:
            desired_difficulty = runMenuWindow(instructions)
            instructions = None
        board = [[0] * desired_difficulty[0] for i in range(desired_difficulty[1])]
        generateMines(board, desired_difficulty[2])
        generateNumbers(board)
        win = runGameWindow(desired_difficulty[0], desired_difficulty[1], board)
        if win:
            instructions = "Congratulations, you won. If you would like to play again, select an option from below:"
        else:
            instructions = "Unfortunately, you lost. If you would like to play again, select an option from below:"


if __name__ == "__main__":
    runGame()

