from ursina import Text, color, destroy

plates_counter_text = None

def show_door_closed_message(self):
    message = Text(
        text='DOOR CLOSED!\nYOU ARE TRAPPED INSIDE THE TEMPLE!\nFind a way out!',
        origin=(0,0),
        position=(0, 0),
        scale=1.5,
        color=color.red,
        background=True,
        backgroundColor=color.dark_gray,
    )
    destroy(message, delay=3)

def show_plates_counter(temple):
    global plates_counter_text
    from objects.temple import pressed_plates

    if plates_counter_text is None:
        plates_counter_text = Text(
            text=f'Pressure Plates: {pressed_plates}/3',
            position=(-0.85, 0.45),
            scale=2,
            color=color.white
        )

def update_plates_counter(count):
    global plates_counter_text

    if plates_counter_text is not None:
        plates_counter_text.text = f'Pressure Plates: {count}/3'
        print(f'UI Counter updated: {count}/3')

def reset_ui():
    global plates_counter_text
    if plates_counter_text:
        destroy(plates_counter_text)
        plates_counter_text = None

def show_finish_screen():
    finish_text = Text(
        text='CONGRATULATIONS!\nYOU ESCAPED THE TEMPLE!',
        origin=(0,0),
        position=(0, 0),
        scale=2,
        color=color.green,
        background=True,
        backgroundColor=color.dark_gray,
    )
    destroy(finish_text, delay=5)
