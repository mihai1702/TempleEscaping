from utils import *
app = Ursina()

start_label = None
start_button = None
exit_button = None

exit_label = None
exit_yes_button = None
exit_no_button = None

background = None

game_running = False
title_bg = None


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
    title_bg = Entity(
        parent=camera.ui,
        model='quad',
        scale=(0.6, 0.15),
        color = color.rgba(0,0,0,0.3),
        y=0.3,
        z=-0.01
    )
    start_label = Text(
        parent=camera.ui,
        text='Jocul templului',
        origin=(0, 0),
        scale=3,
        y=0.3,
        z=-0.02
    )

    start_button = Button(
        parent=camera.ui,
        text='Start',
        color=color.azure,
        scale=(0.4, 0.1),
        position=(0, 0)
    )
    start_button.on_click = start_game

    exit_button = Button(
        parent=camera.ui,
        text='Quit',
        color=color.red,
        scale=(0.4, 0.1),
        position=(0, -0.2)
    )
    exit_button.on_click = quit_game


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
    clear_ui()
    exit_label = Text(
        text='Ești sigur?',
        scale=3,
        y=0.2
    )

    exit_yes_button = Button(
        text='Exit Game',
        scale=0.1,
        y=0,
        color=color.red
    )
    exit_yes_button.on_click = application.quit

    exit_no_button = Button(
        text='Start Over',
        scale=0.1,
        y=-0.2,
        color=color.azure
    )
    exit_no_button.on_click = show_main_menu

def quit_game():
    application.quit()


show_main_menu()

def input(key):
    if key == 'escape':
        if game_running:
            mouse.locked = False
            show_exit_screen()

app.run()