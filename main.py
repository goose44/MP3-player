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

# Texts
font = pygame.font.SysFont("arial", 36)
text_surface = font.render("My MP3 Player", True, (255, 255, 255))
small_font = pygame.font.SysFont("arial", 24)

scroll_x = 0
scroll_speed = 1

paused = False
stopped = False

clock = pygame.time.Clock() 

running = True

# queue
queue_x = 550
queue_y = 60
row_height = 30
queue_width = 230
queue_height = 400
queue_text_width = queue_width - 20

def clean_name(path):
    return os.path.splitext(os.path.basename(path))[0]

def toggle_paused():
    global paused, stopped
    paused = not paused
    if not stopped:
        if paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

def play_song(index):
    global current_index, paused, stopped, scroll_x
    current_index = index
    pygame.mixer.music.load(songs[current_index])
    pygame.mixer.music.play(0)
    paused = False
    stopped = False
    scroll_x = 0

def stop_music():
    global paused, stopped
    stopped = not stopped
    if stopped:
        pygame.mixer.music.stop()
        paused = False
    else:
        pygame.mixer.music.play(0)

def next_song():
    new_index = current_index + 1
    if new_index >= len(songs):
        new_index = 0 
    play_song(new_index)

def previous_song():
    new_index = current_index - 1
    if new_index < 0:
        new_index = len(songs) - 1
    play_song(new_index)

name_box = pygame.Rect(50, 100, 240, 30)
row_rects = []
for i in range(len(songs)):
    rect = pygame.Rect(queue_x, queue_y + i * row_height, queue_text_width, row_height)
    row_rects.append(rect)

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

                for i, rect in enumerate(row_rects):
                    if rect.collidepoint(event.pos):
                        play_song(i)

    if paused:
        circle_color = GRAY
    else:
        circle_color = WHITE

    screen.fill(LIGHT_GREEN)
    song_path = songs[current_index]
    song_name = clean_name(songs[current_index])
    song_surface = small_font.render(song_name, True, WHITE)

    if song_surface.get_width() > name_box.width:
        scroll_x = scroll_x - scroll_speed
        if scroll_x < -song_surface.get_width():
            scroll_x = 0
        text_x = name_box.x + scroll_x
    else:
        text_x = name_box.x

    # Display the song name
    screen.blit(text_surface, (50, 50))

    screen.set_clip(name_box)
    screen.blit(song_surface, (text_x, name_box.y))
    screen.set_clip(None)

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

    # Queueing songs
    pygame.draw.rect(screen, DARK_GRAY, (queue_x - 10, queue_y - 10, queue_width, queue_height), border_radius=15)
    for i, path in enumerate(songs):
        if i == current_index:
            row_color = WHITE
        else:
            row_color = GRAY
        
        row_y = queue_y + i * row_height
        row_box = pygame.Rect(queue_x, row_y, queue_width - 20, row_height)
        row_surface = small_font.render(clean_name(path), True, row_color)

        screen.set_clip(row_box)
        screen.blit(row_surface, (queue_x, row_y))
        screen.set_clip(None)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()