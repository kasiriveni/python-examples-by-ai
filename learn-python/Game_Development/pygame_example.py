# Pygame minimal example (requires pygame)
import sys
try:
    import pygame
except Exception:
    print('pygame not installed')
    sys.exit(0)

pygame.init()
size = (320,240)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30,30,30))
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
