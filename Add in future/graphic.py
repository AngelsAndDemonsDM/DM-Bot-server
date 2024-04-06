import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def main():
    pygame.init()
    pygame.display.set_mode((400, 300))
    pygame.display.set_caption("DM-Bot")
    pygame.display.set_icon(pygame.image.load("Sprites.DM-Bot\exe-main-icon.png"))
    is_run = True
    clock = pygame.time.Clock()
    FPS_limit = 60

    while is_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_run = False
            
        pygame.display.flip()
        clock.tick(FPS_limit)

if __name__ == "__main__":
    main()
