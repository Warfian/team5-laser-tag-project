import pygame
import sys

pygame.init()

#this sets up the window, idk what you have planned for the window so change as you must
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("30 Second Timer")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
#gets start time
start = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # calculate remaining time (30 seconds)
    seconds = 30 - (pygame.time.get_ticks() - start) // 1000
    if seconds < 0:
        seconds = 0
    
    # draw background and timer
    screen.fill((0, 0, 0))
    text = font.render(f"Time remaining: {seconds:02d}", True, (49, 225, 55)) #i just stole this green from gamescreen
    textBox = text.get_rect(center=screen.get_rect().center)
    screen.blit(text, textBox)

    pygame.display.flip()


    # stop after 30 seconds
    if seconds == 0:
        pygame.time.delay(1000)
        break

    clock.tick(60) #seconds

pygame.quit()
