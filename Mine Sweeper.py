import pygame
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
GREY = (144, 144, 144)

FRAMES = 60
BLOCK_SIZE = 40


class Block:
    """Class containing the properties we want each block in our grid to
    have."""
    
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.mine_neighbours = 0


def check_mines(block, x, y, grid):
    """Function counting how many mine neighbours each (non-mine) block has."""
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
    WINDOW.fill(GREY)
    for i in range(WINDOW_WIDTH // BLOCK_SIZE):
        for j in range(WINDOW_HEIGHT // BLOCK_SIZE):
            rect = pygame.Rect(
                i * BLOCK_SIZE,
                j * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE
            )
            pygame.draw.rect(WINDOW, WHITE, rect, 1)
            if grid[i][j].is_revealed:
                if grid[i][j].is_mine:
                    pygame.draw.circle(WINDOW, RED, ((i + 0.5) * BLOCK_SIZE,
                                                     (j + 0.5) * BLOCK_SIZE),
                                       BLOCK_SIZE * 0.25)
                else:
                    # Non mine conditions
                    pass
    
    # Update the game window for it to reflect changes.
    pygame.display.update()


def game_loop():
    """Main game loop."""
    clock = pygame.time.Clock()
    grid = []
    for i in range(WINDOW_WIDTH // BLOCK_SIZE):
        grid.append([])
        for j in range(WINDOW_HEIGHT // BLOCK_SIZE):
            grid[i].append(Block())
    
    running = True
    while running:
        clock.tick(FRAMES)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                break
        if not running:
            break
        draw_window(grid)


if __name__ == "__main__":
    game_loop()
