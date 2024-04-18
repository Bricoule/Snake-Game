import getpass
import os
import random
import sys

import pygame

snake_speed = 15

# Defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Get the screen dimensions
screen_info = pygame.display.Info()
window_x = screen_info.current_w
window_y = screen_info.current_h

# Set the window size
game_window = pygame.display.set_mode((window_x, window_y), pygame.FULLSCREEN)

# FPS (frames per second) controller
fps = pygame.time.Clock()

# Block size of the snake and fruit
block_size = 30

# Defining snake default position
snake_position = [100, 50]

# Defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]
# fruit position
fruit_position = [random.randrange(1, (window_x // block_size)) * block_size,
                  random.randrange(1, (window_y // block_size)) * block_size]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

# highest score
highest_score = 0


def load_highest_score():
    global highest_score
    username = getpass.getuser()
    directory_path = r"C:\Users\fnieslanik\AppData\Roaming"

    # Check if the directory exists
    if os.path.exists(directory_path):
        with os.scandir(directory_path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name == "Score.txt":
                    with open(entry.path, 'r') as file:
                        lines = file.readlines()

                    for line in lines:
                        if username in line:
                            # Extract the highest score from the line
                            highest_score = int(line.split(":")[1])
                            break  # Exit the loop once the highest score is found
                    else:
                        highest_score = 0  # Set highest score to 0 if the username is not found
                    break  # Exit the loop once the score file is found

    if highest_score is None:
        highest_score = 0  # Set highest score to 0 if the file is not found


# Flag to check if the game is over
game_over_flag = False

# Flag to check if the game over text should be displayed
show_game_over_text = False

# Set the initial value of show_score_flag to True
show_score_flag = True

# Set the interval (in frames) for updating the highest score
highest_score_refresh_interval = 60  # Update every 60 frames

# Counter to keep track of frame count
frame_count = 0


# Reset the game variables
def reset_game():
    global snake_position, snake_body, fruit_position, \
        fruit_spawn, direction, change_to, score, game_over_flag, show_score_flag
    snake_position = [100, 50]
    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]
                  ]
    fruit_position = [random.randrange(1, (window_x // block_size)) * block_size,
                      random.randrange(1, (window_y // block_size)) * block_size]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    game_over_flag = False
    show_score_flag = True
    game_window.fill(black)  # Clear the game window
    pygame.display.update()  # Update the display


# Display the score and highest score
def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score: ' + str(score), True, color)
    highest_score_surface = score_font.render('Highest Score: ' + str(highest_score), True, color)
    score_rect = score_surface.get_rect()
    highest_score_rect = highest_score_surface.get_rect()
    score_rect.midtop = (window_x // 2, 10)
    highest_score_rect.midtop = (window_x // 2, score_rect.bottom + 10)
    game_window.blit(score_surface, score_rect)
    game_window.blit(highest_score_surface, highest_score_rect)


# Game over function
def game_over():
    global game_over_flag, show_game_over_text, highest_score

    # Set the game_over_flag to True
    game_over_flag = True
    show_game_over_text = True

    # Update the highest score if the current score is higher
    if score > highest_score:
        highest_score = score

        # Save the highest score to a text file
        username = getpass.getuser()
        data = username + ": " + str(highest_score)

        # Define the path to the text file
        file_path = "C:\\Users\\fnieslanik\\AppData\\Roaming\\Score.txt"

        # Check if the file already exists
        if os.path.exists(file_path):
            # Read the existing file content
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Update the record for the user if it exists
            updated_lines = []
            record_exists = False
            for line in lines:
                if username in line:
                    updated_lines.append(data + "\n")
                    record_exists = True
                else:
                    updated_lines.append(line)

            # If the record does not exist, add it to the end of the file
            if not record_exists:
                updated_lines.append(data + "\n")

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.writelines(updated_lines)
        else:
            # Create a new file and write the score
            with open(file_path, 'w') as file:
                file.write(data + "\n")

    # Create font objects
    game_over_font = pygame.font.SysFont('Comic Sans', 40)
    score_font = pygame.font.SysFont('Comic Sans', 30)
    message_font = pygame.font.SysFont('Comic Sans', 25)

    # Create text surfaces for game over, score, and play again message
    game_over_surface = game_over_font.render("Game Over", True, red)
    score_surface = score_font.render('Score: ' + str(score), True, white)
    message_surface = message_font.render('Play Again? (Press "Space Key") or Quit the Game (Press "Esc Key")',
                                          True,
                                          white)

    # Create rectangles for the text surfaces
    game_over_rect = game_over_surface.get_rect()
    score_rect = score_surface.get_rect()
    message_rect = message_surface.get_rect()

    # Position the text surfaces on the screen
    game_over_rect.midtop = (window_x // 2, window_y // 4)
    score_rect.midtop = (window_x // 2, game_over_rect.bottom + 20)
    message_rect.midtop = (window_x // 2, score_rect.bottom + 20)

    # Blit will draw the text surfaces on the screen
    game_window.blit(game_over_surface, game_over_rect)
    game_window.blit(score_surface, score_rect)
    game_window.blit(message_surface, message_rect)

    pygame.display.flip()


# Set the initial value of start_game and key_pressed to False
start_game = False
key_pressed = False

# Main Function
while True:
    if not start_game:
        game_window.fill(black)
        welcome_font = pygame.font.SysFont('Comic Sans', 40)
        welcome_text = welcome_font.render("Welcome to The Snake Game, " + getpass.getuser(), True, white)
        start_message_font = pygame.font.SysFont('Comic Sans', 30)
        start_message_text = start_message_font.render("Press any key to start the game", True, white)
        welcome_rect = welcome_text.get_rect()
        start_message_rect = start_message_text.get_rect()
        welcome_rect.midtop = (window_x // 2, window_y // 4)
        start_message_rect.midtop = (window_x // 2, window_y // 2)
        game_window.blit(welcome_text, welcome_rect)
        game_window.blit(start_message_text, start_message_rect)
        pygame.display.flip()

        # Call the load_highest_score() function to load the highest score
        load_highest_score()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                start_game = True  # Set start_game to True when any key is pressed
                key_pressed = True  # Set key_pressed to True when any key is pressed
                pygame.time.wait(500)  # Wait for 500 milliseconds (0.5 seconds)
                break  # Exit the loop after handling the first keydown event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Exit the game when the window is closed

    if start_game:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  # Use sys.exit() to exit the game
                if game_over_flag:
                    if event.key == pygame.K_SPACE:
                        reset_game()  # Restart the game
                        game_over_flag = False
                        show_game_over_text = False

        # Check if any key has been pressed before moving the snake
        if key_pressed and not game_over_flag:
            # If two keys pressed simultaneously
            # we don't want snake to move into two
            # directions simultaneously
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'

            # Moving the snake
            if direction == 'UP':
                snake_position[1] -= block_size
            if direction == 'DOWN':
                snake_position[1] += block_size
            if direction == 'LEFT':
                snake_position[0] -= block_size
            if direction == 'RIGHT':
                snake_position[0] += block_size

            # Snake body growing mechanism
            # if fruits and snakes collide then scores will be incremented by 1
            snake_body.insert(0, list(snake_position))
            if abs(snake_position[0] - fruit_position[0]) < block_size and abs(
                    snake_position[1] - fruit_position[1]) < block_size:
                score += 1
                fruit_spawn = False
            else:
                snake_body.pop()

            if not fruit_spawn:
                fruit_position = [random.randrange(1, (window_x // block_size)) * block_size,
                                  random.randrange(1, (window_y // block_size)) * block_size]
                fruit_spawn = True

            game_window.fill(black)

            # Drawing the snake body
            for pos in snake_body:
                pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], block_size, block_size))

            # Drawing the fruit
            pygame.draw.rect(game_window, red,
                             pygame.Rect(fruit_position[0], fruit_position[1], block_size, block_size))

            # Game Over conditions
            # if snake is outside the boundaries of the window
            if snake_position[0] < 0 or snake_position[0] >= window_x or \
                    snake_position[1] < 0 or snake_position[1] >= window_y:
                game_over()

            # if snake hits itself
            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    game_over()

            # Show the score and highest score
            if show_score_flag and not game_over_flag:
                show_score(white, 'Comic Sans', 30)

            # Refresh game screen
            pygame.display.update()

            # Refresh rate
            fps.tick(snake_speed)
