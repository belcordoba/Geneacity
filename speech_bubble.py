import pygame

def draw_speech_bubble(screen, text, text_color, bg_color, pos, size):
    """_summary_

    Args:
        screen (_type_): _description_
        text (_type_): _description_
        text_color (_type_): _description_
        bg_color (_type_): _description_
        pos (_type_): _description_
        size (_type_): _description_
    """
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=pos)

    bg_rect = text_rect.copy()
    bg_rect.inflate_ip(10, 10)

    frame_rect = bg_rect.copy()
    frame_rect.inflate_ip(4, 4)

    pygame.draw.rect(screen, text_color, frame_rect)
    pygame.draw.rect(screen, bg_color, bg_rect)
    screen.blit(text_surface, text_rect)