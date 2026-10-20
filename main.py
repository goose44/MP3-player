import pygame

pygame.init()

# Hardcoded mp3 files (Will change to be more flexible later!)
pygame.mixer.music.load("song1.mp3")
pygame.mixer.music.play(0)
pygame.mixer.music.set_volume(0.5)

# Window size
win_length = 800
win_height = 600
screen = pygame.display.set_mode((win_length, win_height))

# Button size
button_width = 60
button_height = 60

pygame.display.set_caption("Test")

DARK_GRAY = (40, 40, 40)
GRAY = (103, 108, 144)
WHITE = (255, 255, 255)
LIGHT_GREEN = (173,250,146)
GOLD = (226,190,98)

# Control panel
panel_height = 100
panel_x = 0
panel_y = win_height - panel_height
control_panel_rect = pygame.Rect(panel_x, panel_y, win_length, panel_height)

#Circle
circle_radius = 100
circle_x = win_length // 2
circle_y = panel_y  // 2

running = True

# Texts
font = pygame.font.SysFont("arial", 36)
text_surface = font.render("My MP3 Player", True, (255, 255, 255))

paused = False
stopped = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                if not stopped:
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            elif event.key == pygame.K_s:
                stopped = not stopped
                if stopped:
                    pygame.mixer.music.stop()
                    paused = False
                else:
                    pygame.mixer.music.play(0)

            #print(paused, stopped)

    if paused:
        circle_color = GRAY
    else:
        circle_color = WHITE

    screen.fill(LIGHT_GREEN)
    screen.blit(text_surface, (50, 50))

    # CONTROL BAR
    pygame.draw.rect(screen, DARK_GRAY, (panel_x, panel_y, win_length, panel_height))

    # Buttons
    button_gap = 20

    prev_button = pygame.Rect(0, 0, button_width, button_height)
    next_button = pygame.Rect(0, 0, button_width, button_height)
    play_button = pygame.Rect(0, 0, button_width, button_height)

    # Play/Pause button
    play_button.center = control_panel_rect.center
    pygame.draw.rect(screen, WHITE, play_button, border_radius=15)

    # Next button
    next_button.centery = play_button.centery
    next_button.centerx = play_button.centerx + button_width + button_gap
    pygame.draw.rect(screen, WHITE, next_button, border_radius = button_width // 2)

    # Previous button
    prev_button.centery = play_button.centery
    prev_button.centerx = play_button.centerx - button_width - button_gap
    pygame.draw.rect(screen, WHITE, prev_button, border_radius = button_width // 2)

    # Formula: pygame.draw.circle(surface, color, (x, y), radius)
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

    pygame.display.flip()

pygame.quit()