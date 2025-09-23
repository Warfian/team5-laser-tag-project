import pygame
import sys
import time

def splash_screen():
    pygame.init()

    screen = pygame.display.set_mode((920, 420))
    
    try:
        logo = pygame.image.load("logo.jpg")
    except pygame.error:
        print("Error: Could not load image.")
        pygame.quit()
        sys.exit()

    logo = pygame.transform.smoothscale(logo, (320, 320))
    logorect = logo.get_rect()


    screen.fill((0, 0, 0)) #balck to match logo
    window_width, window_height = screen.get_size()

    logorect.center = (window_width // 2, (window_height // 2)-20)
    screen.blit(logo, logorect)
    pygame.display.flip()

    start_time = time.time()
    while time.time() - start_time < 8:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    pygame.quit()

def main():
    splash_screen() 
    print("Splash Screen Done")

if __name__ == "__main__":
    main()