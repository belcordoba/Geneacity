import pygame, sys
import Buttons


def menu():
    """_summary_
    """
    pygame.init()

    screen_size = (100, 100)
    surface = pygame.display.set_mode(screen_size)
    bg_color = (184, 236, 245)
    pygame.display.set_caption('GeneaCity')
    clock = pygame.time.Clock()

    see_tree_button_img = pygame.image.load('buttonsimg/play.jpg').convert_alpha()
    back_button_img = pygame.image.load('buttonsimg/play.jpg').convert_alpha()
    save_button_img = pygame.image.load('buttonsimg/play.jpg').convert_alpha()

    see_tree_button = Buttons.Button(400, 350, see_tree_button_img, 1)
    back_button = Buttons.Button(400, 450, back_button_img, 1)
    save_button = Buttons.Button(400, 550, save_button_img, 1)
    
    command = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
       
        surface.fill(bg_color)
        if command == 1:
            if see_tree_button.draw(surface):
                command = 2
            if save_button.draw(surface):
                command = 3
            if back_button.draw(surface):
                command = 4

        if command == 2:
            pass
        if command == 3:
            pass
        
        pygame.display.flip()
        clock.tick(60)
menu()