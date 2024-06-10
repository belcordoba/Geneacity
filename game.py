
import pygame
import sys
from random import randint
from Players import Player
from houses import House
from speech_bubble import draw_speech_bubble
from camera import Cameras
from trees import Trees
import Buttons
from api_consultas import geneacity_API_request
from arbol_g import *
from tkinter import messagebox
import random


api_x = 251
api_y = 251
house_list = []
selected_id = ""

class Game:
    def __init__(self, player_info, player_info_text):
        pygame.init()
        
        self.screen_size = (1000, 750)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('GeneaCity')
        self.clock = pygame.time.Clock()
        self.camera_group = Cameras()
        self.player = Player((400, 300), self.camera_group)
        self.background = pygame.image.load(r"tile.jpg")
        self.background = pygame.transform.scale(self.background, (300, 300))
        self.font = pygame.font.Font(None, 40)
        
        self.load_buttons()
        self.music_path = 'Sad Hamster Violin Meme.mp3'
        self.music_playing = False
        self.bg_x, self.bg_y = 0, 0
        self.options_menu_active = False
        self.load_houses()
        self.houses_data = []
        self.text_rects = []
        self.scroll_offset = 0
        self.image = pygame.image.load('play.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150)) 
        self.selected_player = player_info
        self.selected_player_text = player_info_text
        
        self.players_data = []
        self.load_names()
        self.populate_trees()
        self.show_speach_bubble = False
        self.active_player = None
        
    def load_buttons(self):
        see_tree_button_img = pygame.image.load(r'buttonsimg\resume.png').convert_alpha()
        back_button_img = pygame.image.load(r'buttonsimg\view_tree.png').convert_alpha()
        save_button_img = pygame.image.load(r'buttonsimg\exit.jpg').convert_alpha()
        view_tree_img = pygame.transform.scale(back_button_img, (220, 95))
        resume_img = pygame.transform.scale(see_tree_button_img, (220, 95))
        
        self.see_tree_button = Buttons.Button(400, 350, view_tree_img, 1)
        self.back_button = Buttons.Button(400, 450, resume_img, 1)
        self.save_button = Buttons.Button(400, 550, save_button_img, 1)
        
        options_button_img = pygame.image.load(r'buttonsimg\options.png').convert_alpha()
        opt_img = pygame.transform.scale(options_button_img, (70, 70))
        self.option_button = Buttons.Button(900, 30, opt_img, 1)
        
        mute_button_img = pygame.image.load(r'buttonsimg\mute.png').convert_alpha()
        mute_img = pygame.transform.scale(mute_button_img, (70, 70))
        self.mute_button = Buttons.Button(800, 30, mute_img, 1)
        
        music_button_img = pygame.image.load(r'buttonsimg\music.png').convert_alpha()
        music_img = pygame.transform.scale(music_button_img, (70, 70))
        self.music_button = Buttons.Button(800, 30, music_img, 1)

    def load_houses(self, player_x=0, player_y=0):
        global api_x
        global api_y
        global house_list
        url_houses = f'https://geneacity.life/API/getHouses/?x={player_x}&y={player_y}'
        consulta_casas = geneacity_API_request(url_houses)
        if (player_x-api_x) < -250 or (player_x-api_x) > 250 or (player_y-api_y) < -250 or (player_y - api_y) > 250:
                api_x = player_x
                api_y = player_y
                if len(house_list) > 10:
                    print("removing houses", len(house_list))
                    for i, house in enumerate(house_list):
                        if (house.cord_x-player_x) < -350 or (house.cord_x-player_x) > 350 or (house.cord_y-player_y) < -350 or (house.cord_y-player_y) > 350:
                            house_list.pop(i)
                consulta_casas.start()
                response = consulta_casas.get_response()
                if response:
                    print(response) 
                    if 'houses' in response:
                        for data in response['houses']:
                            house_id = data['id']
                            cord_x = data['x']  
                            cord_y = data['y']

                            url_occupants = f'https://geneacity.life/API/getHousesResidents/?houseId={house_id}'
                            consulta_occupants = geneacity_API_request(url_occupants)
                            consulta_occupants.start()
                            response_occupants = consulta_occupants.get_response()
                            self.houses_data = []
                            
                            if response_occupants:
                                for information in response_occupants['residents']:
                                    occupant_id = information['id']
                                    name = information['name']
                                    gender = information['gender']
                                    marital_status = information['marital_status']
                                    father = information['father']
                                    mother = information['mother']
                                    self.houses_data.append([occupant_id, name, gender, marital_status, father, mother])
                                house_list.append(House(house_id, cord_x, cord_y, self.houses_data, group=self.camera_group))
    
    def load_names(self):
        self.players_data = []
        
        while True:
            rand_x = random.randint(1, 100000)
            rand_y = random.randint(1, 100000)
            url_inhabitants = f'https://geneacity.life/API/getAvailableInhabitants/?x={rand_x}&y={rand_y}'
            consulta_habitantes = geneacity_API_request(url_inhabitants)
            consulta_habitantes.start()
            response = consulta_habitantes.get_response()
            if response['status'] == 1:
                break

        print(response)
        if response and response.get('status') == 1:
            if 'inhabitants' in response:
                for data in response['inhabitants']:
                    name = data['name']
                    gender = data['gender']
                    age = data['age']
                    identification = data['id']
                    self.players_data.append([name, gender, age, identification])
        print(f"Loaded players: {self.players_data}")

    def draw_text(self):
        self.screen.blit(self.image, (60, 40))
        self.text_rects = []
        y_offset = 170 + self.scroll_offset
        for player in self.players_data:
            text = self.font.render(f"{player[0]} - {player[1]} - {player[2]}", True, (0, 0, 0))  # BLACK is defined as (0, 0, 0)
            text_rect = text.get_rect()
            text_rect.topleft = (70, y_offset)
            self.screen.blit(text, text_rect)
            self.text_rects.append((text_rect, player))
            y_offset += 50

    def check_click(self, pos):
        global selected_id
        global selected_text
        for text_rect, player in self.text_rects:
            if text_rect.collidepoint(pos):
                selected_text = f"{player[0]}, {player[1]}, {player[2]}"
                selected_id = player[3]
                self.selected_player = selected_id
                messagebox.showinfo(title="Player selection:", message=f"Player selected: {selected_text}")
                draw_speech_bubble(self.screen, f" text {selected_text}", (87, 22, 3), (244, 192, 53), (170, 700), 30)
                print(f"Selected text: {selected_text}\nSelected ID: {selected_id}")
                break

    def scroll(self, dy):
        self.scroll_offset += dy
        self.scroll_offset = max(min(self.scroll_offset, 0), -len(self.players_data) * 50 + self.screen_size[1] - 100)

    def draw(self, screen, offset):
        offset_pos = self.rect.topleft - offset
        screen.blit(self.image, offset_pos)
        if self.show_speech_bubble:
            draw_speech_bubble(screen, f'people {self.occupants}', (0, 0, 0), (255, 255, 255), offset_pos, 25)
    
    def populate_trees(self):
        for num in range(20):
            random_x = randint(0, 1000)
            random_y = randint(0, 1000)
            Trees((random_x, random_y), self.camera_group)

    def run(self):
        global selected_id
        global player_info_text
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_click(event.pos)
                elif event.type == pygame.MOUSEWHEEL:
                    self.scroll(event.y * 20)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.scroll(20)
                    elif event.key == pygame.K_DOWN:
                        self.scroll(-20)

            self.update_music()
            self.player.update()
            self.check_collisions()
            player_x, player_y = self.draw()
            draw_speech_bubble(self.screen, f"Current position: ({player_x}, {player_y})", (87, 22, 3), (244, 192, 53), (170, 700), 30)
            self.load_houses(player_x, player_y)
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def update_music(self):
        if self.music_playing:
            if self.mute_button.draw(self.screen):
                pygame.mixer.music.stop()
                self.music_playing = False
        else:
            if self.music_button.draw(self.screen):
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.play(-1)
                self.music_playing = True

    def check_collisions(self):
        for sprite in self.camera_group.sprites():
            if isinstance(sprite, House):
                sprite.update(self.player.rect)

    def show_tree(self):
        tree_window = pygame.display.set_mode((width, height))  
        tree = Arbol(10)
        values = [0, 1]
        for value in values:
            if not tree.existe(value):
                tree.insertar(value)
        tree.ver_arbol(tree_window)
        pygame.display.flip()
        pygame.time.wait(5000) 

    def draw(self):
        self.screen.fill((255, 255, 255))
        player_x, player_y = self.player.rect.topleft
        bg_width, bg_height = self.background.get_size()
        offset_x = player_x % bg_width
        offset_y = player_y % bg_height

        for x in range(-bg_width, self.screen_size[0] + bg_width, bg_width):
            for y in range(-bg_height, self.screen_size[1] + bg_height, bg_height):
                self.screen.blit(self.background, (x - offset_x, y - offset_y))

        offset = (player_x - self.screen_size[0] // 2, player_y - self.screen_size[1] // 2)

        for sprite in self.camera_group:
            if sprite != self.player:
                sprite.draw(self.screen, offset)

        self.player.draw(self.screen, offset)
        
        if self.selected_player:
            draw_speech_bubble(self.screen, self.selected_player_text, (87, 22, 3), (244, 192, 53), (450, 660), 30)

        if self.music_playing:
            self.mute_button.draw(self.screen)
        else:
            self.music_button.draw(self.screen)
        
        
        if self.option_button.draw(self.screen):
            self.options_menu_active = True

        if self.options_menu_active:
            overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  
            self.screen.blit(overlay, (0, 0))
            if self.see_tree_button.draw(self.screen):
                    self.show_tree()
            if self.back_button.draw(self.screen):
                    self.options_menu_active = False 
            if self.save_button.draw(self.screen):
                    pygame.quit()
                    sys.exit()
        
        return player_x, player_y

if __name__ == '__main__':
    game = Game(player_info, player_info_text)
    game.run()