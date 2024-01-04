import pygame
import random
import math

def simulate_snake_and_fly(grid_size, cell_size, initial_length, edge_buffer, fps, snake_speed):
    # Initialize pygame
    pygame.init()

    # Set up the display
    window_size = grid_size * cell_size
    screen = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption("Snake and Fly Simulation")

    # Set up the clock for FPS
    clock = pygame.time.Clock()

    # Directions
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, Down, Left, Right

    # Function to initialize a snake
    def initialize_snake():
        snake = []
        while len(snake) < initial_length:
            start_x = random.randint(edge_buffer, grid_size - edge_buffer - 1)
            start_y = random.randint(edge_buffer, grid_size - edge_buffer - 1)
            snake = [(start_x, start_y)]
            direction = random.choice(directions)
            for _ in range(1, initial_length):
                snake_x, snake_y = snake[-1]
                new_segment = (snake_x + direction[0], snake_y + direction[1])
                if 0 <= new_segment[0] < grid_size and 0 <= new_segment[1] < grid_size:
                    snake.append(new_segment)
                else:
                    break
        return {'body': snake, 'direction': direction}

    # Initialize snakes
    snakes = [initialize_snake() for _ in range(3)]

    # Function to check if a position is safe for the snake
    def is_safe_position(position, snake_body):
        return position not in snake_body and 0 <= position[0] < grid_size and 0 <= position[1] < grid_size

    # Function to draw rotated ellipse
    def draw_rotated_ellipse(surface, color, rect, angle):
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(s, color, (0, 0, *rect.size))
        surface.blit(pygame.transform.rotate(s, angle), rect.topleft)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Snake movement control
        for snake in snakes:
            head_x, head_y = snake['body'][0]
            dx, dy = snake['direction']

            # Check potential positions and change direction if needed
            potential_positions = [(dx, dy) for dx, dy in directions if is_safe_position((head_x + dx, head_y + dy), snake['body'])]
            if potential_positions:
                snake['direction'] = random.choice(potential_positions)
                dx, dy = snake['direction']

            new_head = (head_x + dx, head_y + dy)

            # Add new head and remove tail to maintain length
            snake['body'].insert(0, new_head)
            if len(snake['body']) > initial_length:
                snake['body'].pop()

        # Drawing
        screen.fill((255, 255, 255))  # White background

        # Draw each snake
        for snake in snakes:
            for i in range(len(snake['body']) - 1):
                segment = snake['body'][i]
                next_segment = snake['body'][i + 1]
                angle = math.degrees(math.atan2(next_segment[1] - segment[1], next_segment[0] - segment[0]))
                rect = pygame.Rect(segment[0] * cell_size, segment[1] * cell_size, cell_size, int(cell_size * 0.6))
                draw_rotated_ellipse(screen, (139, 69, 19), rect, angle)

        pygame.display.flip()  # Update the display
        clock.tick(fps)  # Control the frame rate

    pygame.quit()

# Example usage
simulate_snake_and_fly(grid_size=50, cell_size=20, initial_length=5, edge_buffer=5, fps=30, snake_speed=5)
