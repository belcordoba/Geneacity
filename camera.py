import pygame

class Cameras(pygame.sprite.Group):
    """Class used to create the camera view for the player.

    Args:
        pygame (_type_): Group of sprites done with Pygame.
    """
    def __init__(self):
        """Creates the camera that will show the objects in the game.
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        self.offset = pygame.math.Vector2(0, 0)
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.camera_borders = {'right': 100, 'left': 100, 'top': 100, 'width': 100}
        top = self.camera_borders['top']
        left = self.camera_borders['left']
        height = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['width'])
        width = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        self.camera_rect = pygame.Rect(top, left, width, height)

    def box_movement(self, target):
        """Allows the movement of the objects according to the player's position.

        Args:
            target (_type_): Uses the player to move the objects.
        """
        self.offset.x = target.rect.centerx - self.half_w 
        self.offset.y = target.rect.centery - self.half_h

    def draw_right(self, player):
        """Draws the objects according to the player position.

        Args:
            player (_type_): Receives the information of the player to use it as reference.
        """
        self.box_movement(player)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.y):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)