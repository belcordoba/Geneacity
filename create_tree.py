import pygame
import sys
import Buttons

pygame.init()

width, height = 1000, 750  # Aumentar el tamaño de la ventana
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Árbol Genealógico")

WHITE = (184, 236, 245)
GREEN = (0, 187, 0)
YELLOW = (255, 238, 47)
BLACK = (0, 0, 0)

node_image = pygame.image.load('otherimg/circle.png')
node_image = pygame.transform.scale(node_image, (70, 70))  # Aumentar el tamaño del nodo

back_button_img = pygame.image.load(r'buttonsimg/back.png').convert_alpha()
back_img = pygame.transform.scale(back_button_img, (140, 90))
back_button = Buttons.Button(1000, 750, back_img, 1)

class Nodo:
    def __init__(self, nivel, posicion, padre=None):
        self.valor = None
        self.nivel = nivel
        self.padre = padre
        self.posicion = posicion

class ArbolGenealogico:
    def __init__(self):
        self.nodos = []

    def crear_nodos(self):
        niveles = 5  # Número de niveles en el árbol
        nodos_por_nivel = [1, 2, 4, 8, 16]  # Nodos por nivel
        for nivel in range(niveles):
            y = 100 + nivel * 150  # Separación vertical
            x_inicial = (width - nodos_por_nivel[nivel] * 150) / 2  # Aumentar la separación horizontal
            for i in range(nodos_por_nivel[nivel]):
                x = x_inicial + i * 150
                padre = None
                if nivel > 0:
                    padre = self.nodos[(2**nivel - 1) // 2 + i // 2]
                self.nodos.append(Nodo(nivel, (x, y), padre))

    def agregar_valor(self, valor, nivel, nodo_index):
        nodo = self.nodos[nivel * (nivel + 1) // 2 + nodo_index]
        nodo.valor = valor

    def ver_arbol(self, window):
        window.fill(WHITE)

        # Dibujar las líneas primero
        for nodo in self.nodos:
            if nodo.padre and nodo.valor is not None:
                pygame.draw.line(window, YELLOW, nodo.posicion, nodo.padre.posicion, 4)

        # Dibujar los nodos al frente
        for nodo in self.nodos:
            x, y = nodo.posicion
            if nodo.valor is not None:
                window.blit(node_image, (x - 35, y - 35))  # Ajustar la posición para el nuevo tamaño del nodo
                font = pygame.font.Font(None, 48)  # Aumentar el tamaño de la fuente
                text = font.render(str(nodo.valor), True, BLACK)
                text_rect = text.get_rect(center=(x, y))
                window.blit(text, text_rect)

        pygame.display.flip()

def main():
    arbol = ArbolGenealogico()
    arbol.crear_nodos()
     
    arbol.agregar_valor(1, 0, 0)  # Nivel 0, nodo 0
    arbol.agregar_valor(2, 1, 0)  # Nivel 1, nodo 0
    arbol.agregar_valor(3, 1, 1)  # Nivel 1, nodo 1
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if back_button.draw(window):
            pass 

        arbol.ver_arbol(window)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
