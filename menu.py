#menu
import pygame, sys
import Buttons

pygame.init()

pygame.init()

bg_color = (184, 236, 245)
screen_size = (1000, 750)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('GeneaCity')
clock = pygame.time.Clock()

start_button_img = pygame.image.load('buttons img\buttons1.png').convert_alpha()
start_button = Buttons.Button(304,125, start_button_img, 1)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    start_button.draw(screen)
    screen.fill(bg_color)
    pygame.display.flip()
    clock.tick(60)