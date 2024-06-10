#buttons
import pygame, sys

class Button:
    def __init__(self, pos_x, pos_y, image, scale):
        width = image.get_width()
        height = image.get_height() 
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = ( (pos_x, pos_y))
        self.clicked = False

    def draw(self, surface):
        action = False 
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True 
                action = True 

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False 

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action 
        