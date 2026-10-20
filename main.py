import pygame

pygame.init()

# Window size
win_length = 800
win_height = 600
screen = pygame.display.set_mode((win_length, win_height))

pygame.display.set_caption("Test")

DARK_GRAY = (40, 40, 40)
WHITE = (255, 255, 255)
LIGHT_GREEN = (173,250,146)

# Control panel
panel_height = 100
panel_x = 0

panel_y = win_height - panel_height

#Circle
circle_radius = 100
circle_x = win_length // 2

circle_y = panel_y  // 2

running = True

font = pygame.font.SysFont("arial", 36)
text_surface = font.render("My MP3 Player", True, (255, 255, 255))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(LIGHT_GREEN)
    screen.blit(text_surface, (50, 50))

    # Formula: pygame.draw.rect(surface, color, (x, y, width, height))
    pygame.draw.rect(screen, DARK_GRAY, (panel_x, panel_y, win_length, panel_height))

    # Formula: pygame.draw.circle(surface, color, (x, y), radius)
    pygame.draw.circle(screen, WHITE, (circle_x, circle_y), circle_radius)

    pygame.display.flip()

pygame.quit()