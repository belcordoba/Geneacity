import pygame 

class Trees(pygame.sprite.Sprite):
    """Class used to create the tree sprites.

    Args:
        pygame (_type_): Sprites done with Pygame.
    """
    def __init__(self, position, group):
        """Creates a tree instance with the information of the tree.

        Args:
            position (_type_): Position of the tree.
            group (_type_): Group of the objects used for the camera.
        """
        super().__init__(group)
        self.image = pygame.image.load('otherimg\árbol.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, screen, offset):
        """Displays the tree on screen.

        Args:
            screen (_type_): Window where the tree will be shown.
            offset (_type_): Position where the tree will be shown.
        """
        offset_pos = (self.rect.topleft[0] - offset[0], self.rect.topleft[1] - offset[1])
        screen.blit(self.image, offset_pos)
