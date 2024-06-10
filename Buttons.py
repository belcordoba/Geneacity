#buttons
import pygame, sys

class Button:
    """Creates buttons so they can be shown on the game.
    """
    def __init__(self, pos_x, pos_y, image, scale):
        """Receives the values needed to create the button.

        Args:
            pos_x (_type_): Receives the x position for the button.
            pos_y (_type_): Receives the y position for the button.
            image (_type_): Receives the image for the button.
            scale (_type_): Receives the scale for the image of the button.
        """
        width = image.get_width()
        height = image.get_height() 
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = ( (pos_x, pos_y))
        self.clicked = False

    def draw(self, surface):
        """Shows the button on the game window.

        Args:
            surface (_type_): Window where the button will be shown.

        Returns:
            _type_: Return the action done by the button when clicked.
        """
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
        