from json import load
import pygame
import random


# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Tetriminojen värit
COLORS = {
    "I": (0, 255, 255),  # Cyan
    "O": (255, 255, 0),  # Yellow
    "T": (128, 0, 128),  # Purple
    "S": (0, 255, 0),  # Green
    "Z": (255, 0, 0),  # Red
    "L": (255, 165, 0),  # Orange
    "J": (0, 0, 255)  # Blue
}

# Tetriminojen muodot
SHAPES = {
    "I": [[1, 1, 1, 1]],  # I tetrimino
    "O": [[1, 1], [1, 1]],  # O tetrimino
    "T": [[0, 1, 0], [1, 1, 1]],  # T tetrimino
    "S": [[1, 1, 0], [0, 1, 1]],  # S tetrimino
    "Z": [[0, 1, 1], [1, 1, 0]],  # Z tetrimino
    "L": [[1, 1, 1], [1, 0, 0]],  # L tetrimino
    "J": [[1, 1, 1], [0, 0, 1]]  # J tetrimino
}

LOPETUS = [
    "Et voita tornilla, höpsö",
    "No hupsista, hävisit",
    "Parempi onni ensi kerralla",
    "Pystyt parempaan!",
    ":)  Oho  (:",
    "Palikat eivät pidä sinusta"
]

# Game variables
SCREEN_WIDTH = 333
SCREEN_HEIGHT = 780
GRID_SIZE = 30
fall_speed = 500  # Falling speed in milliseconds
move_speed = 100  # Movement speed in milliseconds
clock = pygame.time.Clock()
speed_increase_interval = 10000  # Speed increase interval in milliseconds
last_speed_increase_time = pygame.time.get_ticks()
last_fall_time = pygame.time.get_ticks()
last_move_time = pygame.time.get_ticks()
game_over = False

# Grid to store blocks
grid = [[0 for _ in range(SCREEN_WIDTH // GRID_SIZE)] for _ in range(SCREEN_HEIGHT // GRID_SIZE)]

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Not official Tetris")
font = pygame.font.Font(None, 36)

def draw_grid():  
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

def draw_shape(shape, offset, shape_type):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[shape_type], pygame.Rect((offset[0] + x) * GRID_SIZE, (offset[1] + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_grid_with_blocks():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x]:
                pygame.draw.rect(screen, WHITE, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                
def store_shape_in_grid(shape, offset):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[offset[1] + y][offset[0] + x] = 1

def check_for_complete_lines():
    global grid, score
    lines_cleared = 0
    for y in range(len(grid)):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [0 for _ in range(SCREEN_WIDTH // GRID_SIZE)])
            lines_cleared += 1    # Sata pistettä linjasta
    score += lines_cleared * 1  # Pisteiden kerroin per linja

# Scoring system
score = 0

def move_block_down():
    global score
    score += 1

def clear_row():
    global score
    score += 100

# Fontti
pygame.font.init()
font = pygame.font.SysFont('Arial', 27)

# Funktio pisteiden näyttämiseksi
def draw_score(screen, score):
    score_text = font.render(f'Linjoja: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def game_loop():
    global score
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def main():
    global fall_speed, move_speed, last_speed_increase_time, last_fall_time, last_move_time, game_over
    running = True
    current_shape_type, current_shape = random.choice(list(SHAPES.items()))
    shape_pos = [5, 0]
    rotation_pressed = False

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_grid_with_blocks()
        draw_shape(current_shape, shape_pos, current_shape_type)
        draw_score(screen, score)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_over:
            font = pygame.font.Font(None, 36)
            game_over_text = font.render(random.choice(LOPETUS), True, RED, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            font = pygame.font.Font(None, 36)
            prompt_text = font.render("Haluatko sulkea pelin? (K)", True, WHITE, BLACK)
            screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 - prompt_text.get_height() // 2 + 25))
            pygame.display.flip()

            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_input = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_k:
                            running = False
                            waiting_for_input = False

        else:
            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()

            if current_time - last_move_time > move_speed:
                if keys[pygame.K_LEFT] and shape_pos[0] > 0 and not any(grid[shape_pos[1] + y][shape_pos[0] - 1 + x] for y, row in enumerate(current_shape) for x, cell in enumerate(row) if cell):
                    shape_pos[0] -= 1
                if keys[pygame.K_RIGHT] and shape_pos[0] + len(current_shape[0]) < SCREEN_WIDTH // GRID_SIZE and not any(grid[shape_pos[1] + y][shape_pos[0] + 1 + x] for y, row in enumerate(current_shape) for x, cell in enumerate(row) if cell):
                    shape_pos[0] += 1
                if keys[pygame.K_DOWN] and shape_pos[1] + len(current_shape) < SCREEN_HEIGHT // GRID_SIZE and not any(grid[shape_pos[1] + 1 + y][shape_pos[0] + x] for y, row in enumerate(current_shape) for x, cell in enumerate(row) if cell):
                    shape_pos[1] += 1
                if keys[pygame.K_SPACE] and shape_pos[1] + len(current_shape) < SCREEN_HEIGHT // GRID_SIZE:
                    while shape_pos[1] + len(current_shape) < SCREEN_HEIGHT // GRID_SIZE and not any(grid[shape_pos[1] + 1 + y][shape_pos[0] + x] for y, row in enumerate(current_shape) for x, cell in enumerate(row) if cell):
                        shape_pos[1] += 1
                        
                if keys[pygame.K_UP]:
                    if not rotation_pressed:  # Tarvitaan, jotta kääntö tapahtuu vain kerran
                        rotated_shape = list(zip(*current_shape[::-1]))
                        if shape_pos[0] + len(rotated_shape[0]) <= SCREEN_WIDTH // GRID_SIZE and shape_pos[1] + len(rotated_shape) <= SCREEN_HEIGHT // GRID_SIZE:
                            current_shape = rotated_shape
                        rotation_pressed = True
                else:
                    rotation_pressed = False
                last_move_time = current_time

            if current_time - last_fall_time > fall_speed:
                shape_pos[1] += 1
                if shape_pos[1] + len(current_shape) > SCREEN_HEIGHT // GRID_SIZE or any(grid[shape_pos[1] + y][shape_pos[0] + x] for y, row in enumerate(current_shape) for x, cell in enumerate(row) if cell):
                    shape_pos[1] -= 1  # Move shape back up
                    store_shape_in_grid(current_shape, shape_pos)
                    check_for_complete_lines()
                    shape_pos = [5, 0]
                    current_shape_type, current_shape = random.choice(list(SHAPES.items()))
                    if any(grid[0]):
                        game_over = True
                last_fall_time = current_time

            if score // 2 > (score - 1) // 1:
                fall_speed = max(200, fall_speed - 100)

        pygame.display.flip()  # FPS
        clock.tick(100)

    pygame.quit()

if __name__ == "__main__":
    main()
