import pygame

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong-ish v3 - Created by PlayDough")
# Colors
white = (255, 255, 255)
black = (0, 0, 0)
light_green = (0, 255, 0)
sBlue = (85, 144, 237)
red = (255, 17, 0)
green = (102, 255, 0)

# Paddle and ball dimensions
p_paddle_width = 10
p_paddle_height = 100
a_paddle_width = 10
a_paddle_height = 100
ball_size = 10

# Initial positions
player_paddle_x = 20
player_paddle_y = screen_height // 2 - p_paddle_height // 2
ai_paddle_x = screen_width - a_paddle_width - 20
ai_paddle_y = screen_height // 2 - a_paddle_height // 2
ball_x = screen_width // 2 - ball_size // 2
ball_y = screen_height // 2 - ball_size // 2

# Initial speeds
ball_x_speed = 0.09
ball_y_speed = 0.09
paddle_speed = 0.07

# Scores
player_score = 0
ai_score = 0

# Game state
game_state = "menu1"  # Can be "menu1", "menu2", "game", or "game_over"

# Iniial Menu options
menu1_options = ["Play", "Quit"]
selected_option = 0

# Game Over Options
menu2_options = ["Play Again", "Quit"]
selected_option = 0

def draw_menu1():
    screen.fill(black)
    font = pygame.font.Font(None, 36)
    for i, option in enumerate(menu1_options):
        text = font.render(option, True, sBlue)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + i * 50))
        if i == selected_option:
            pygame.draw.rect(screen, red, text_rect, 2)
        screen.blit(text, text_rect)

def draw_menu2():
    screen.fill(black)
    font = pygame.font.Font(None, 36)
    for i, option in enumerate(menu2_options):
        text = font.render(option, True, sBlue)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + i * 50))
        if i == selected_option:
            pygame.draw.rect(screen, red, text_rect, 2)
        screen.blit(text, text_rect)

def draw_score():
    font = pygame.font.Font(None, 36)
    player_score_text = font.render(f"Player: {player_score}", True, green)
    ai_score_text = font.render(f"AI: {ai_score}", True, red)
    screen.blit(player_score_text, (20, 20))
    screen.blit(ai_score_text, (screen_width - 200, 20))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if game_state == "menu1":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            selected_option = (selected_option - 1) % len(menu1_options)
        elif keys[pygame.K_s]:
            selected_option = (selected_option + 1) % len(menu1_options)
        elif keys[pygame.K_RETURN]:
            if selected_option == 0:
                game_state = "game"
                player_score = 0
                ai_score = 0
                ball_speed_x = 0.09
                ball_speed_y = 0.09
                paddle_speed = 0.07
            else:
                pygame.quit()
                quit()

        draw_menu1()

    if game_state == "menu2":
        keys2 = pygame.key.get_pressed()
        if keys2[pygame.K_w]:
            selected_option = (selected_option - 1) % len(menu2_options)
        elif keys2[pygame.K_s]:
            selected_option = (selected_option + 1) % len(menu2_options)
        elif keys2[pygame.K_RETURN]:
            if selected_option == 0:
                game_state = "game"
                player_score = 0
                ai_score = 0
                ball_speed_x = 0.09
                ball_speed_y = 0.09
                paddle_speed = 0.07
            else:
                pygame.quit()
                quit()

        draw_menu2()

    elif game_state == "game":
        # Move the player paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_paddle_y -= paddle_speed
        if keys[pygame.K_s]:
            player_paddle_y += paddle_speed

        # Keep the player paddle within the screen
        player_paddle_y = max(0, min(player_paddle_y, screen_height - p_paddle_height))

        # Move the AI paddle
        if ball_x > screen_width // 2:
            if ai_paddle_y < ball_y:
                ai_paddle_y += paddle_speed
            elif ai_paddle_y > ball_y:
                ai_paddle_y -= paddle_speed

        # Keep the AI paddle within the screen
        ai_paddle_y = max(0, min(ai_paddle_y, screen_height - a_paddle_height))

        # Move the ball
        ball_x += ball_x_speed
        ball_y += ball_y_speed

        # Ball collision with walls
        if ball_y <= 0 or ball_y + ball_size >= screen_height:
            ball_y_speed *= -1

        # Ball collision with paddles
        if (ball_x <= player_paddle_x + p_paddle_width and ball_y >= player_paddle_y and ball_y <= player_paddle_y + p_paddle_height) or (ball_x + ball_size >= ai_paddle_x and ball_y >= ai_paddle_y and ball_y <= ai_paddle_y + a_paddle_height):
            ball_x_speed *= -1

        # Game over conditions
        if ball_x < 0:
            ai_score += 1
            if ai_score == 5:
                game_state = "menu2"
            else:
                ball_x = screen_width // 2 - ball_size // 2
                ball_y = screen_height // 2 - ball_size // 2
                ball_speed_x *= 1.02
                ball_speed_y *= 1.02
                paddle_speed *= 1.02
                if player_score > 0:
                    player_score -= 1
                    p_paddle_height -= 10
        elif ball_x > screen_width:
            player_score += 1
            if player_score == 5:
                game_state = "menu2"
            else:
                ball_x = screen_width // 2 - ball_size // 2
                ball_y = screen_height // 2 - ball_size // 2
                ball_speed_x *= 1.02
                ball_speed_y *= 1.02
                paddle_speed *= 1.02
                if ai_score > 0:
                    ai_score -= 1
                    a_paddle_height -= 10

        # Draw everything
        screen.fill(black)
        draw_score()
        pygame.draw.rect(screen, green, (player_paddle_x, player_paddle_y, p_paddle_width, p_paddle_height))
        pygame.draw.rect(screen, red, (ai_paddle_x, ai_paddle_y, a_paddle_width, a_paddle_height))
        pygame.draw.rect(screen, sBlue, (ball_x, ball_y, ball_size, ball_size))

    elif game_state == "menu2":
        screen.fill(black)
        font = pygame.font.Font(None, 36)
        if player_score == 5:
            text = font.render("Player Wins!", True, white)
        else:
            text = font.render("AI Wins!", True, white)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

        # Add a delay before returning to the menu
        pygame.time.delay(1000)
        game_state = "menu2"

    pygame.display.flip()

pygame.quit()