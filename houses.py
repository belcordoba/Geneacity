import pygame 
from speech_bubble import draw_speech_bubble
from tkinter import messagebox
import json 
from arbol_g import *

def read_json_file():
    with open('players_data.json', 'r') as file:
        data = json.load(file)
    return data

def process_family_data(father, mother):
    print(f"Processing family data for father ID: {father}, mother ID: {mother}")
    for family in House.family_data:
        for key, relationships in family.items():
            for relation, ids in relationships.items():
                print(f"Checking relation {relation} in category {key} with IDs {ids}")
                if int(father) in map(int, ids) or int(mother) in map(int, ids):
                    print(f"Found parent ID {father if father in ids else mother} in category {key}, relation {relation}")
                    if relation == 'mother' or relation == 'father':
                        messagebox.showinfo(title='family', message=f'You have found one of your siblings')
                    elif relation == 'children':
                        messagebox.showinfo(title='family', message=f'You have found one of your nieces/nephews')
                    elif relation == 'grandmother' or relation == 'grandfather':
                        messagebox.showinfo(title='family', message=f'You have found one of your aunts/uncles')

                    return True
    return False

class House(pygame.sprite.Sprite):
    def __init__(self, ID, cord_x, cord_y, occupants, group):
        super().__init__(group)
        self.id = ID
        self.cord_x = int(cord_x)
        self.cord_y = int(cord_y)
        self.occupants = occupants 
        self.image = pygame.image.load('otherimg\houses.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))  
        self.rect = self.image.get_rect(topleft=(self.cord_x, self.cord_y))
        self.show_speech_bubble = False
        self.houses_data = []

    def update(self, player_rect):
        if self.rect.colliderect(player_rect):
            self.show_speech_bubble = True
        else:
            self.show_speech_bubble = False


    import pygame 
from speech_bubble import draw_speech_bubble
import Buttons
from tkinter import messagebox

class House(pygame.sprite.Sprite):
    def __init__(self, ID, cord_x, cord_y, occupants, group):
        super().__init__(group)
        self.id = ID
        self.cord_x = int(cord_x)
        self.cord_y = int(cord_y)
        self.occupants = occupants 
        self.image = pygame.image.load('otherimg\houses.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))  
        self.rect = self.image.get_rect(topleft=(self.cord_x, self.cord_y))
        self.show_speech_bubble = False
        self.houses_data = []

    def update(self, player_rect):
        if self.rect.colliderect(player_rect):
            self.show_speech_bubble = True
        else:
            self.show_speech_bubble = False

    def draw(self, screen, offset):
        get_parents_button_img = pygame.image.load(r'buttonsimg\get_parents.png').convert_alpha()
        marry_button_img = pygame.image.load(r'buttonsimg\marry.png').convert_alpha()
        offset_pos = (self.rect.topleft[0] - offset[0], self.rect.topleft[1] - offset[1])
        screen.blit(self.image, offset_pos)
        if self.show_speech_bubble:
            for i, occupant in enumerate(self.occupants):
                text_bubble = f'Name: {occupant[1]}, Gender: {occupant[2]}, Status: {occupant[3]}, ID: {occupant[0]}'
                draw_speech_bubble(screen, text_bubble, (87, 22, 3), (244, 192, 53), (offset_pos[0], offset_pos[1] + (i * -30)), 25)
                offset_buttons = len(text_bubble)* 5 - 25
                get_parents_button = Buttons.Button((offset_pos[0]+offset_buttons), (offset_pos[1] + (i * -30) - 14), get_parents_button_img, 0.3)
                if get_parents_button.draw(screen):
                    parents_info = f"My parents are {occupant[4]} and {occupant[5]}" 
                    print(parents_info)
                    messagebox.showinfo(title=f"{occupant[1]}'s response:", message=parents_info)
                    print(f"Button pressed for occupant: {occupant}")
                    found = process_family_data(occupant[4], occupant[5])
                    
                    if not found:
                        messagebox.showinfo(title=f'Not family', message='They are not part of your family tree')
    
                if occupant[3] == "Single":
                    marry_button = Buttons.Button((offset_pos[0]+offset_buttons+35), (offset_pos[1] + (i * -30) - 14), marry_button_img, 0.3)
                    marry_button.draw(screen)
                        #


House.family_data = read_json_file()
print("Loaded family data:", House.family_data)