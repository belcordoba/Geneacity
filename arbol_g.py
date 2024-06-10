import pygame
import sys
import Buttons

pygame.init()

width, height = 1000, 750
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Árbol Binario de Búsqueda")

WHITE = (184, 236, 245)
GREEN = (0, 187, 0)
YELLOW = (255, 238, 47)
BLACK = (0, 0, 0)

node_image = pygame.image.load('otherimg\circle.png')
node_image = pygame.transform.scale(node_image, (40, 40))  

back_button_img = pygame.image.load(r'buttonsimg\back.png').convert_alpha()
back_img = pygame.transform.scale(back_button_img, (140, 90))
back_button = Buttons.Button(780, 600, back_img, 1)

class Arbol():
    """Creates the tree that will be used for the game.
    """
    def __init__(self, valor:int) -> None:
        """Creates the individual nodes for the tree.

        Args:
            valor (int): Receives the value for the node.
        """
        self.iz: Arbol = None
        self.der: Arbol = None
        self.valor = valor

    def insertar(self, nuevo_valor) -> None:
        """Inserts a new node on the tree.

        Args:
            nuevo_valor (_type_): Receives the value for the new node.
        """
        self.__insertar(nuevo_valor, self)

    def __insertar(self, nuevo_valor, raiz) -> None:
        """Inserts a new node on the tree.

        Args:
            nuevo_valor (_type_): Receives the value for the new node.
            raiz (_type_): Receives the tree where the node will be added.
        """
        if nuevo_valor <= raiz.valor:
            if raiz.iz is None:
                raiz.iz = Arbol(nuevo_valor)
            else:
                self.__insertar(nuevo_valor, raiz.iz)
        else:
            if raiz.der is None:
                raiz.der = Arbol(nuevo_valor)
            else:
                self.__insertar(nuevo_valor, raiz.der)

    def existe(self, valor) -> bool:
        """Verifies if the node already exists on the tree.

        Args:
            valor (_type_): Receives the value that will be checked.

        Returns:
            bool: Returns if the node exists or not.
        """
        return self.__existe(valor, self)

    def __existe(self, valor, raiz) -> bool:
        """Verifies if the node already exists on the tree.

        Args:
            valor (_type_): Receives the value that will be checked.
            raiz (_type_): Receives the tree where the node will be checked.

        Returns:
            bool: Returns if the node exists or not.
        """
        if raiz:
            if valor == raiz.valor:
                return True
            elif valor <= raiz.valor:
                return self.__existe(valor, raiz.iz)
            else:
                return self.__existe(valor, raiz.der)
        else:
            return False

    def ver_arbol(self, window) -> None:
        """Lets the player see the tree.

        Args:
            window (_type_): Receives the window where the image will be shown.
        """
        window.fill(WHITE)
        self.__ver_arbol(window, 0, width, 40, self)
        pygame.display.flip()

    def __ver_arbol(self, window, xmin, xmax, y, raiz) -> None:
        """Shows the tree.

        Args:
            window (_type_): Receives the window where the image will be shown.
            xmin (_type_): Receives the minimum allowed for window x size.
            xmax (_type_): Receives the maximum allowed for window x size.
            y (_type_): Receives the value for window y size.
            raiz (_type_): Receives the tree used to build the image.
        """
        if raiz:
            x = xmin + (xmax - xmin) / 2
            if raiz.iz:
                x_iz = xmin + (x - xmin) / 2
                pygame.draw.line(window, YELLOW, (x, y + 20), (x_iz, y + 80), 2)
            if raiz.der:
                x_der = x + (xmax - x) / 2
                pygame.draw.line(window, YELLOW, (x, y + 20), (x_der, y + 80), 2)
            window.blit(node_image, (x - 20, y))  # Dibujar la imagen en lugar del círculo
            font = pygame.font.Font(None, 36)
            text = font.render(str(raiz.valor), True, BLACK)
            text_rect = text.get_rect(center=(x, y + 20))
            window.blit(text, text_rect)
            self.__ver_arbol(window, xmin, x, y + 80, raiz.iz)
            self.__ver_arbol(window, x, xmax, y + 80, raiz.der)

def main():
    """Shows the tree on the game.
    """
    raiz = Arbol(valor=10)
    l = [5, 8, 4, 15, 6, 2, 1, 3, 7, 10, 15, 48, 63, 41, -2, -5]
    for x in l:
        if not raiz.existe(x):
            raiz.insertar(x)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if back_button.draw(window):
            pass 

        raiz.ver_arbol(window)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()