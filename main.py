import pygame

pygame.init()

# Window size
win_length = 800
win_height = 600
screen = pygame.display.set_mode((win_length, win_height))

pygame.display.set_caption("Test")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((173,250,146))
    pygame.display.flip()

pygame.quit()