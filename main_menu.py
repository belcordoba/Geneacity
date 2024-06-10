import pygame
import sys
from camera import *
from houses import *
from Players import *
from speech_bubble import *
import Buttons
from game import *
from tkinter import messagebox
global player_info

player_info = ""
player_info_text = ""

pygame.init()

def main_menu():
    """Displays the main menu and the actions for each button.
    """
    global selected_text
    global selected_id
    global player_info
    global player_info_text
    bg_color = (184, 236, 245)
    screen_size = (1000, 750)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('GeneaCity')
    clock = pygame.time.Clock()
    command = 'start'
    logo_img = pygame.image.load(r'otherimg\logo.png').convert_alpha()
    start_button_img = pygame.image.load(r'buttonsimg\play.jpg').convert_alpha()
    load_button_img = pygame.image.load(r'buttonsimg\load.jpg').convert_alpha()
    exit_button_img = pygame.image.load(r'buttonsimg\exit.jpg').convert_alpha()
    back_button_img = pygame.image.load(r'buttonsimg\back.png').convert_alpha()
    back_img = pygame.transform.scale(back_button_img, (140, 90))
    game_img = pygame.transform.scale(start_button_img, (140, 90))

    logo = Buttons.Button(350, 50, logo_img, 1)
    start_button = Buttons.Button(400, 350, start_button_img, 1)
    load_button = Buttons.Button(400, 450, load_button_img, 1)
    exit_button = Buttons.Button(400, 550, exit_button_img, 1)
    back_button = Buttons.Button(780, 600, back_img, 1)
    game_button = Buttons.Button(600, 600, game_img, 1)
    run_game_button = Buttons.Button(780, 600, game_img, 1)
    
    game_instance = Game(player_info, player_info_text)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if command == 'player':
                    game_instance.check_click(event.pos)
            elif event.type == pygame.MOUSEWHEEL:
                if command == 'player':
                    game_instance.scroll(event.y * 20)
            elif event.type == pygame.KEYDOWN:
                if command == 'player':
                    if event.key == pygame.K_UP:
                        game_instance.scroll(20)
                    elif event.key == pygame.K_DOWN:
                        game_instance.scroll(-20)
                    
        screen.fill(bg_color)
        if command == 'start':
            logo.draw(screen)
            if start_button.draw(screen):
                command = 'player'
            if load_button.draw(screen):
                command = 'load'
            if exit_button.draw(screen):
                pygame.quit()
                sys.exit()
        
        if command == 'player':
            game_instance.draw_text()
            if run_game_button.draw(screen):
                from game import selected_id
                if selected_id != "":
                    player_select_url = f"https://geneacity.life/API/selectAvailableInhabitant/?id={selected_id}"
                    player_select_api = geneacity_API_request(player_select_url)
                    player_select_api.start()
                    response = player_select_api.get_response()
                    if response['status'] == 1:
                        player_info_url = f"https://geneacity.life/API/getInhabitantInformation/?id={selected_id}"
                        player_info_api = geneacity_API_request(player_info_url)
                        player_info_api.start()
                        response = player_info_api.get_response()

                        player_id = response['inhabitant']['id']
                        name = response['inhabitant']['name']
                        gender = response['inhabitant']['gender']
                        age = response['inhabitant']['age']
                        marital_status = response['inhabitant']['marital_status']
                        father = response['inhabitant']['father']
                        mother = response['inhabitant']['mother']
                        house = response['inhabitant']['house']

                        player_info = [player_id, name, gender, age, marital_status, father, mother, house]
                        player_info_text = f"{name}, {gender}, {age} years old, {marital_status}, parents are {father} and {mother}, lives in {house}, ID is {player_id}"
                        game = Game(player_info, player_info_text)
                        game.run()
                    else:
                        messagebox.showinfo(title="Error!", message="That character is not available anymore.")
                else:
                    messagebox.showinfo(title="Error!", message="You need to choose a character to continue.")

        if command == 'load':
            if back_button.draw(screen):
                command = 'start'
            if game_button.draw(screen):
                game = Game()
                game.run()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()