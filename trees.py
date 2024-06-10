import pygame 

class Trees(pygame.sprite.Sprite):
    """_summary_

    Args:
        pygame (_type_): _description_
    """
    def __init__(self, position, group):
        super().__init__(group)
        self.image = pygame.image.load('otherimg\árbol.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, screen, offset):
        """_summary_

        Args:
            screen (_type_): _description_
            offset (_type_): _description_
        """
        offset_pos = (self.rect.topleft[0] - offset[0], self.rect.topleft[1] - offset[1])
        screen.blit(self.image, offset_pos)
