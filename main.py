import pygame
import os

pygame.init()

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

songs = []
for name in os.listdir("music"):
    if name.lower().endswith(".mp3"):
        path = os.path.join("music", name)
        songs.append(path)

current_index = 0
print(songs)

pygame.mixer.music.load(songs[current_index])
pygame.mixer.music.play(0)
pygame.mixer.music.set_volume(0.5)

# Control panel
panel_height = 100
panel_x = 0
panel_y = win_height - panel_height
control_panel_rect = pygame.Rect(panel_x, panel_y, win_length, panel_height)

# Buttons
button_gap = 20

prev_button = pygame.Rect(0, 0, button_width, button_height)
next_button = pygame.Rect(0, 0, button_width, button_height)
play_button = pygame.Rect(0, 0, button_width, button_height)

play_button.center = control_panel_rect.center
next_button.centery = play_button.centery
next_button.centerx = play_button.centerx + button_width + button_gap
prev_button.centery = play_button.centery
prev_button.centerx = play_button.centerx - button_width - button_gap

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

def toggle_paused():
    global paused, stopped
    paused = not paused
    if not stopped:
        if paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

def stop_music():
    global paused, stopped
    stopped = not stopped
    if stopped:
        pygame.mixer.music.stop()
        paused = False
    else:
        pygame.mixer.music.play(0)

def next_song():
    global current_index, paused, stopped
    current_index = current_index + 1
    if current_index >= len(songs):
        current_index = 0 
    pygame.mixer.music.load(songs[current_index])
    pygame.mixer.music.play(0)
    paused = False
    stopped = False
    print(songs[current_index])

def previous_song():
    global current_index, paused, stopped
    current_index = current_index - 1
    if current_index < 0:
        current_index = len(songs) - 1
    pygame.mixer.music.load(songs[current_index])
    pygame.mixer.music.play(0)
    paused = False
    stopped = False
    print(songs[current_index])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_paused()
            elif event.key == pygame.K_s:
                stop_music()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if play_button.collidepoint(event.pos):
                    toggle_paused()

                elif next_button.collidepoint(event.pos):
                    next_song()
                elif prev_button.collidepoint(event.pos):
                    previous_song()

            #print(paused, stopped)

    if paused:
        circle_color = GRAY
    else:
        circle_color = WHITE

    screen.fill(LIGHT_GREEN)
    screen.blit(text_surface, (50, 50))

    # CONTROL BAR
    pygame.draw.rect(screen, DARK_GRAY, (panel_x, panel_y, win_length, panel_height))

    # Draw the buttons
    pygame.draw.rect(screen, WHITE, play_button, border_radius=15)
    pygame.draw.rect(screen, WHITE, next_button, border_radius=button_width // 2)
    pygame.draw.rect(screen, WHITE, prev_button, border_radius=button_width // 2)

    # Play/Pause icon
    playx = play_button.centerx
    playy = play_button.centery
    s = 12
    if paused or stopped:
        pygame.draw.polygon(screen, DARK_GRAY, [
            (playx - s + 3, playy - s),
            (playx - s + 3, playy + s),
            (playx + s + 3, playy),
        ])
    else:
        pygame.draw.rect(screen, DARK_GRAY, (playx - 9, playy - s, 6, s * 2))
        pygame.draw.rect(screen, DARK_GRAY, (playx + 3, playy - s, 6, s * 2))

    # Next icon
    cx = next_button.centerx
    cy = next_button.centery
    s = 10
    pygame.draw.polygon(screen, DARK_GRAY, [
        (cx - s - 3, cy - s),
        (cx - s - 3, cy + s),
        (cx + s - 3, cy),
    ])
    pygame.draw.rect(screen, DARK_GRAY, (cx + s - 1, cy - s, 4, s * 2))

    # Previous icon
    px = prev_button.centerx
    py = prev_button.centery
    pygame.draw.rect(screen, DARK_GRAY, (px - s - 3, py - s, 4, s * 2))
    pygame.draw.polygon(screen, DARK_GRAY, [
        (px + s + 3, py - s),
        (px + s + 3, py + s),
        (px - s + 3, py),
    ])

    # Formula: pygame.draw.circle(surface, color, (x, y), radius)
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

    pygame.display.flip()

pygame.quit()