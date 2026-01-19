from utils import *
from ursina import *

app = Ursina(
    title='Temple Escaping',
    icon='assets/temple_escaping_icon.ico'
)


start_label = None
start_button = None
exit_button = None

exit_label = None
exit_yes_button = None
exit_no_button = None

background = None

game_running = False
title_bg = None

window.shadow_map_enabled = True
window.shadow_map_resolution = 2048

def show_main_menu():
    global start_label, start_button, exit_button, background, game_running, title_bg
    game_running = False
    clear_ui()

    background = Entity(
        parent=camera.ui,
        model='quad',
        texture='assets/textures/background.png',
        scale=(1.777, 1),
        z=1
    )

    start_label = Text(
        parent=camera.ui,
        text='Temple Escaping',
        origin=(0, 0),
        scale=3,
        y=0.3,
        background=True,
        backgroundColor=color.rgba(0, 0, 0, 0.3),
        z=-0.02
    )

    start_button = Button(
        parent=camera.ui,
        text='Start',
        color=color.azure,
        scale=(0.4, 0.1),
        position=(-0.25, 0)
    )
    start_button.on_click = start_game

    exit_button = Button(
        parent=camera.ui,
        text='Quit',
        color=color.red,
        scale=(0.4, 0.1),
        position=(0.25, 0)
    )
    exit_button.on_click = quit_game

    game_rules = Text(
        parent=camera.ui,
        text='Find a way to escape the temple by searching for 3 pressure plates hidden around the temple\nUse mouse to look around and WASD to move\nPress ESC to pause the game',
        origin=(0, 0),
        scale=1.5,
        y=-0.3,
        background=True,
        backgroundColor=color.rgba(0, 0, 0, 0.3),
        z=-0.02
    )



def start_game():
    global game_running, background, title_bg
    clear_ui()


    if background:
        destroy(background)
        background = None

    if title_bg:
        destroy(title_bg)
        title_bg = None

    mouse.locked = True
    game_running = True
    from game_logic import start_scene
    start_scene()

def show_exit_screen():
    global exit_label, exit_yes_button, exit_no_button, background, game_running
    game_running = False
    mouse.locked = False

    exit_label = Text(
        text='Are you sure?',
        scale=3,
        origin=(0, 0),
        y=0.2,
        background=True,
        backgroundColor=color.rgba(0,0,0,0.3)
    )
    exit_yes_button = Button(
        text='Exit Game',
        scale=(0.4,0.1),
        y=0,
        color=color.red
    )
    exit_yes_button.on_click = application.quit
    exit_no_button = Button(
        text='Continue Playing',
        scale=(0.4,0.1),
        y=-0.2,
        color=color.rgb(58/255,194/255,0/255)
    )
    exit_no_button.on_click = resume_game

def resume_game():
    global exit_label, exit_yes_button, exit_no_button, game_running

    if exit_label:
        exit_label.enabled = False
    if exit_yes_button:
        exit_yes_button.enabled = False
    if exit_no_button:
        exit_no_button.enabled = False

    mouse.locked = True
    game_running = True

def quit_game():
    application.quit()


show_main_menu()

def input(key):
    if key == 'escape':
        if game_running:
            mouse.locked = False

            if exit_label and exit_yes_button and exit_no_button:
                exit_label.enabled = True
                exit_yes_button.enabled = True
                exit_no_button.enabled = True
            else:
                show_exit_screen()


app.run()