from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

player = None

def start_scene():
    global player

    Sky()

    AmbientLight(color=color.rgba(120, 120, 120, 255))

    sun = DirectionalLight(color=color.rgb(255, 240, 220))
    sun.look_at(Vec3(1, -1, -1))

    player = FirstPersonController(
        position=(0, 2, -5),
        speed=5,
        jump_height=1.5,
        gravity=1
    )

    ground = Entity(
        model = 'plane',
        scale=(100, 1, 100),
        texture='grass_texture.jpg',
        texture_scale=(20, 20),
        collider='box',
    )