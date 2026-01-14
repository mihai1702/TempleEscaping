from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from objects.temple import *

import copy

player = None
temple = None
trees_collection = None
pressed_pressure_plates = 0

def start_scene():
    global player, temple, trees_collection

    Sky()

    AmbientLight(color=color.rgba(120, 120, 120, 255))

    sun = DirectionalLight(color=color.rgb(255, 240, 220))
    sun.look_at(Vec3(1, -1, -1))

    player = FirstPersonController(
        position=(5, 15, 31),
        speed=8,
        jump_height=1.5,
        gravity=1
    )
    player.rotation_y = 180

    ground = Entity(
        model = 'plane',
        scale=(100, 1, 100),
        texture='assets/textures/grass_texture.jpg',
        texture_scale=(20, 20),
        collider='box',
    )
    tree1_model = load_model('assets/3d_models/trees/tree1.glb')
    tree1_model.flattenLight()

    tree2_model = load_model('assets/3d_models/trees/tree2.glb')
    tree2_model.flattenLight()

    bush1_model = load_model('assets/3d_models/bushes/bush1.glb')
    bush1_model.flattenLight()

    bush2_model = load_model('assets/3d_models/bushes/bush2.glb')
    bush2_model.flattenLight()

    tree1_m1 = Entity(
        model=copy.deepcopy(tree1_model),
        scale=1,
        position=(-18, 0, 0),
        rotation=(0, 45, 0),
        collider='box'
    )
    tree2_m1 = Entity(
        model=copy.deepcopy(tree1_model),
        scale=1,
        position=(35, 0, 25),
        collider='box'
    )
    tree1_m2 = Entity(
        model=copy.deepcopy(tree2_model),
        scale=50,
        position=(-20, 0, 28),
        rotation=(0, 90, 0),
        collider='box'
    )
    tree2_m2 = Entity(
        model=copy.deepcopy(tree2_model),
        scale=50,
        position=(40, 0, -15),
        rotation=(0, 135, 0),
        collider='box'
    )
    bush1_m1 = Entity(
        model=copy.deepcopy(bush1_model),
        scale=0.04,
        position=(15, 0, 8),
    )
    bush2_m1 = Entity(
        model=copy.deepcopy(bush1_model),
        scale=0.04,
        position=(-15, 0, 15)
    )
    bush3_m1 = Entity(
        model=copy.deepcopy(bush1_model),
        scale=0.04,
        position=(25, 0, 25)
    )
    bush4_m1 = Entity(
        model=copy.deepcopy(bush1_model),
        scale=0.04,
        position=(40, 0, 15)
    )
    bush5_m1 = Entity(
        model=copy.deepcopy(bush1_model),
        scale=0.02,
        position=(0, 0, 25)
    )
    bush6_m1 = Entity(
        model=copy.deepcopy(bush1_model),
        scale=0.02,
        position=(5, 0, 30)
    )
    bush1_m2 = Entity(
        model=copy.deepcopy(bush2_model),
        scale=0.008,
        position=(30, 0, 20)
    )
    bush2_m2 = Entity(
        model=copy.deepcopy(bush2_model),
        scale=0.008,
        position=(20, 0, 25)
    )



    temple = Temple(player)
