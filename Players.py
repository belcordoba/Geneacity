import pygame

move_right = ['images\\r.1.png', 'images\\r.2.png', 'images\\r.3.png', 'images\\r.4.png']
move_left = ['images\l.1.png', 'images\l.2.png', 'images\l.3.png', 'images\l.4.png']
move_up = ['images\d.1.png', 'images\d.2.png', 'images\d.3.png', 'images\d.4.png']
move_down = ['images\\a.1.png', 'images\\a.2.png', 'images\\a.3.png', 'images\\a.4.png']
class Player(pygame.sprite.Sprite):
    """Class used to create the image of the player in game.

    Args:
        pygame (_type_): Sprites done with Pygame.
    """
    def __init__(self, pos, group):
        """Creates the instance of the player sprite.

        Args:
            pos (_type_): Receives the position of the sprite.
            group (_type_): Group of the objects used for the camera.
        """
        super().__init__(group)
        self.images = {
            'right': [pygame.image.load(img).convert_alpha() for img in move_right],
            'left': [pygame.image.load(img).convert_alpha() for img in move_left],
            'up': [pygame.image.load(img).convert_alpha() for img in move_up],
            'down': [pygame.image.load(img).convert_alpha() for img in move_down],
        }
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.index = 0
        self.image = self.images['down'][self.index]
        self.rect = self.image.get_rect(center=pos)
        self.current_images = self.images['down']

    def handle_input(self):
        """Shows the different images according to the key pressed by the player.
        """
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.current_images = self.images['up']
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.current_images = self.images['down']
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.current_images = self.images['right']
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.current_images = self.images['left']
        else:
            self.direction.x = 0

    def update(self):
        """Update the image shown according to the direction and speed.
        """
        self.handle_input()
        self.rect.center += self.direction * self.speed

        if self.direction.x != 0 or self.direction.y != 0:
            self.index += 0.1
            if self.index >= len(self.current_images):
                self.index = 0
            self.image = self.current_images[int(self.index)]

    def draw(self, screen, offset):
        """Shows the image on the screen.

        Args:
            screen (_type_): Window where the image will be shown.
            offset (_type_): Position of the sprite on the screen.
        """
        offset_pos = (self.rect.topleft[0] - offset[0], self.rect.topleft[1] - offset[1])
        screen.blit(self.image, offset_pos)