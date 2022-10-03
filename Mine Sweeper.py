import pygame
import random
import os

pygame.font.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 400, 400
WINDOW = pygame.display.set_mode(
    (
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )
)

pygame.display.set_caption("Mine Sweeper")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (169, 169, 169)

FRAMES = 60
BLOCK_SIZE = 40
NUMBER_OF_MINES = 10

NEIGHBOUR_FONT = pygame.font.SysFont(
    "comicsans",
    20
)
GAME_END_FONT = pygame.font.SysFont(
    "comicsans",
    25
)

GAME_END_FLAG = pygame.USEREVENT + 1


class Block:
    """Class containing the properties we want each block in our grid to
    have."""
    
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.mine_neighbours = 0


def check_mines(x, y, grid):
    """Function counting how many mine neighbours each (non-mine) block has."""
    block = grid[x][y]
    if block.is_mine:
        # Make sure we don't count the neighbours if the block is itself a
        # mine.
        block.mine_neighbours = -1
    else:
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                # Prevent the corner pieces from trying to count mine blocks
                # that do not exist or are on the other side of the screen.
                if (x + i) < 0 or (y + j) < 0 or \
                        (x + i) >= WINDOW_WIDTH // BLOCK_SIZE or \
                        (y + j) >= WINDOW_HEIGHT // BLOCK_SIZE:
                    continue
                # Count every mine block in a 3x3 grid centered around the
                # block, since we are sure that the block is not a mine.
                if grid[x + i][y + j].is_mine:
                    block.mine_neighbours += 1


def draw_window(grid):
    """Function to handle drawing the game window at each frame."""
    # Draw the grid by filling the window with a grey background and drawing
    # white non-filled squares with line thickness 1.
    WINDOW.fill(WHITE)
    for i in range(WINDOW_WIDTH // BLOCK_SIZE):
        for j in range(WINDOW_HEIGHT // BLOCK_SIZE):
            rect = pygame.Rect(
                i * BLOCK_SIZE,
                j * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE
            )
            pygame.draw.rect(WINDOW, BLACK, rect, 1)
            if grid[i][j].is_revealed:
                rect = pygame.Rect(
                    (i + 0.05) * BLOCK_SIZE,
                    (j + 0.05) * BLOCK_SIZE,
                    BLOCK_SIZE * 0.9,
                    BLOCK_SIZE * 0.9
                )
                pygame.draw.rect(WINDOW, GREY, rect)
                if grid[i][j].is_mine:
                    pygame.draw.circle(
                        WINDOW,
                        RED,
                        (
                            (i + 0.5) * BLOCK_SIZE,
                            (j + 0.5) * BLOCK_SIZE
                        ),
                        BLOCK_SIZE * 0.25)
                elif grid[i][j].mine_neighbours > 0:
                    WINDOW.blit(
                        NEIGHBOUR_FONT.render(
                            str(grid[i][j].mine_neighbours),
                            1,
                            BLACK
                        ),
                        (
                            (i + 0.35) * BLOCK_SIZE,
                            (j + 0.1) * BLOCK_SIZE
                        )
                    )
    
    # Update the game window for it to reflect changes.
    pygame.display.update()


def floodfill_reveal(x, y, grid, revealed_count):
    grid[x][y].is_revealed = True
    revealed_count[0] += 1
    if grid[x][y].mine_neighbours == 0:
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                X = x + i
                Y = y + j
                if X < 0 or Y < 0 or \
                        X >= WINDOW_WIDTH // BLOCK_SIZE or \
                        Y >= WINDOW_HEIGHT // BLOCK_SIZE or \
                        grid[X][Y].is_revealed:
                    continue
                else:
                    floodfill_reveal(X, Y, grid, revealed_count)


def discover(click_position, grid, revealed_count):
    x = click_position[0] // BLOCK_SIZE
    y = click_position[1] // BLOCK_SIZE
    if grid[x][y].is_mine:
        return True
    elif grid[x][y].is_revealed:
        pass
    else:
        floodfill_reveal(x, y, grid, revealed_count)
    return False


def game_end(grid, clear):
    if not clear:
        for i in range(WINDOW_WIDTH // BLOCK_SIZE):
            for j in range(WINDOW_HEIGHT // BLOCK_SIZE):
                grid[i][j].is_revealed = True
        draw_window(grid)
        text = GAME_END_FONT.render(
                "Oops, you stepped on a mine!",
                1,
                BLACK
        )
        
    else:
        draw_window(grid)
        text = GAME_END_FONT.render(
            "Yay, you avoided the mines!",
            1,
            BLACK
        )
    rect = pygame.Rect(
        WINDOW_WIDTH // 2 - text.get_width() // 2,
        WINDOW_HEIGHT // 2 - text.get_height() // 2,
        text.get_width(),
        text.get_height()
    )
    pygame.draw.rect(
        WINDOW,
        YELLOW,
        rect
    )
    WINDOW.blit(
        text,
        (
            WINDOW_WIDTH // 2 - text.get_width() // 2,
            WINDOW_HEIGHT // 2 - text.get_height() // 2
        )
    )
    pygame.display.update()
    pygame.time.delay(5000)
    

def game_loop():
    """Main game loop."""
    clock = pygame.time.Clock()
    grid = []
    for i in range(WINDOW_WIDTH // BLOCK_SIZE):
        grid.append([])
        for j in range(WINDOW_HEIGHT // BLOCK_SIZE):
            grid[i].append(Block())
    
    mine_options = list(
        (x, y)
        for x in range(WINDOW_WIDTH // BLOCK_SIZE)
        for y in range(WINDOW_HEIGHT // BLOCK_SIZE)
    )
    
    for _ in range(NUMBER_OF_MINES):
        x, y = random.choice(mine_options)
        mine_options.remove((x, y))
        grid[x][y].is_mine = True
    
    for i in range(WINDOW_WIDTH // BLOCK_SIZE):
        for j in range(WINDOW_HEIGHT // BLOCK_SIZE):
            check_mines(i, j, grid)
    
    running = True
    revealed_count = [0]
    while running:
        clock.tick(FRAMES)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if discover(pos, grid, revealed_count):
                    game_end(grid, False)
                    running = False
        if revealed_count[0] == WINDOW_WIDTH//BLOCK_SIZE * \
                WINDOW_HEIGHT//BLOCK_SIZE - NUMBER_OF_MINES:
            game_end(grid, True)
            running = False
        if not running:
            break
        draw_window(grid)


if __name__ == "__main__":
    game_loop()
