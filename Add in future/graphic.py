import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Забей хуй и используй pyqt5

def main_window():
    # Main
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("DM-Bot")
    pygame.display.set_icon(pygame.image.load("Sprites.DM-Bot\exe-main-icon.png"))

    # Fronts
    base_font = pygame.font.Font("Data.DM-Bot\\Fonts\\base_font.otf", 40)
    text_surface = base_font.render("????", False, "black")

    # Main loop
    is_run = True
    clock = pygame.time.Clock()
    FPS_limit = 60

    while is_run:
        screen.blit(text_surface, (0, 0))

        clock.tick(FPS_limit)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_run = False
    
    pygame.quit()

if __name__ == "__main__":
    main_window()
