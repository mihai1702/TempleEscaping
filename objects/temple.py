from ursina import *
from objects.torch_fire import TorchFire
from ui import *

temple_width = 25
temple_length = 25
wall_height = 14
wall_thickness = 1

first_pressure_plate = None
second_pressure_plate = None
third_pressure_plate = None

pressed_plates = 0

class Temple(Entity):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.door_closed = False
        self.fire_timer = 0
        self.puzzle_solved = False
        self.plate1_pressed = False
        self.plate2_pressed = False
        self.plate3_pressed = False

        self.plate3_timer = 0
        self.plate3_required_time = 3
        self.plate_check_timer = 0

        self.door = Entity(
            model='cube',
            texture='assets/textures/gate_texture.jpg',
            scale=(4, 9, 0.5),
            position=(5, 8, -5),  # sus sus
            color=color.white,
            collider='box'
        )

        self.trigger_position = Vec3(5.5, 1.5, -8)
        self.trigger_radius = 3


        self.debug_trigger = Entity(
            model='sphere',
            scale=self.trigger_radius*2,
            position=self.trigger_position,
            color=color.rgba(0,0,0,0),
            visible=True
        )


        self.door_speed = 8

        self.build_floor()
        self.build_walls()
        self.build_columns()
        self.build_torches()
        self.build_pressure_plates()
        self.build_altar()
        self.build_roof()


    def build_floor(self):
        self.floor = Entity(
            parent=self,
            model='cube',
            scale=(26, 1, 26),
            position=(5, 0, -15),
            texture='assets/textures/temple_floor_texture.jpg',
            texture_scale=(15, 15),
            collider='box',
            receive_shadows=True
        )
    def build_walls(self):
        self.front_left_wall = Entity(
            parent=self,
            model='cube',
            scale=(11, wall_height, 1),
            position=(11, wall_height/2, -5),
            texture='assets/textures/wall_texture.jpg',
            collider='box',
            cast_shadows=True,
            receive_shadows=True

        )
        self.front_right_wall = Entity(
            parent=self,
            model='cube',
            scale=(11, wall_height, 1),
            position=(-2, wall_height/2, -5),
            texture='assets/textures/wall_texture.jpg',
            collider='box',
            cast_shadows=True,
            receive_shadows=True
        )
        self.front_top_wall = Entity(
            parent=self,
            model='cube',
            scale=(2, wall_height-8, 1),
            position=(4.5, 11, -5),
            texture='assets/textures/wall_texture.jpg',
            collider='box',
            cast_shadows=True,
            receive_shadows=True
        )
        self.first_side_wall = Entity(
            parent=self,
            model='cube',
            scale=(wall_thickness, wall_height, temple_length),
            position=(5- temple_width/2, wall_height/2, -15),
            texture='assets/textures/wall_texture.jpg',
            texture_scale=(1, 6),
            collider='box',
            cast_shadows=True,
            receive_shadows=True
        )
        self.second_side_wall = Entity(
            parent=self,
            model='cube',
            scale=(wall_thickness, wall_height, temple_length),
            position=(4.5+ temple_width/2, wall_height/2, -15),
            texture='assets/textures/wall_texture.jpg',
            texture_scale=(1, 6),
            collider='box',
            cast_shadows=True,
            receive_shadows=True
        )
        self.back_wall = Entity(
            parent=self,
            model='cube',
            scale=(temple_length, wall_height, wall_thickness),
            position=(17-temple_length/2, wall_height/2, -26),
            texture='assets/textures/wall_texture.jpg',
            texture_scale=(1, 6),
            collider='box',
            cast_shadows=True,
            receive_shadows=True
        )
        self.ceiling = Entity(
            parent=self,
            model='cube',
            scale=(23, 1, 20),
            position=(5, wall_height-1, -15),
            texture='assets/textures/ceiling_texture.jpg',
            texture_scale=(10,10),
            collider='box',
            cast_shadows=True,
            receive_shadows=True
        )
    def build_roof(self):
        for i in range(5):
            Entity(
                parent=self,
                model='cube',
                scale=(27 - i * 4, 2, 26 - i * 4),
                position=(5, wall_height + i, -15),
                texture='assets/textures/roof_texture.jpg'
            )
    def build_columns(self):
        z_positions = [-37.5, -30.5, -23.5]
        x_positions = [-29.5, -12.5]

        for x in x_positions:
            for z in z_positions:
                Entity(
                    parent=self,
                    model='assets/3d_models/Pillar.glb',
                    scale=0.16,
                    origin_y=0,
                    position=(x, 0, z),
                    collider='box',
                    cast_shadows=True,
                    receive_shadows=True
                )


    def build_torches(self):
        self.torches = []
        self.torch_lights = []

        torch_positions = [(0, 0, -5), (9, 0, -5)]

        for pos in torch_positions:
            torch = Entity(
                parent=self,
                model='assets/3d_models/temple_torch.glb',
                scale=5,
                origin_y=0,
                position=pos,
                cast_shadows=True,
                receive_shadows=True
            )
            self.torches.append(torch)

            light = PointLight(
                parent=self,
                color=color.orange,
                range=8,
                intensity=5,
                position = pos
            )
            self.torch_lights.append(light)

        altar_torches_positions = [(3, 0, -23.7), (6, 0, -23.7)]
        for pos in altar_torches_positions:
            torch = Entity(
                parent=self,
                model='assets/3d_models/temple_torch.glb',
                scale=3,
                origin_y=0,
                position=pos,
                rotation=(0,180,0),
                cast_shadows=True,
                receive_shadows=True
            )
            self.torches.append(torch)

            light = PointLight(
                parent=self,
                color=color.orange,
                range=8,
                intensity=5,
                position = pos
            )
            self.torch_lights.append(light)


    def build_pressure_plates(self):
        global first_pressure_plate, second_pressure_plate, third_pressure_plate
        first_pressure_plate = Entity(
            parent=self,
            model='cube',
            texture='assets/textures/stone_pressure_plate.jpg',
            scale=(1, 0.2, 1),
            position=(17-temple_length/2, 0.55, -25),
            collider='box'
        )
        second_pressure_plate = Entity(
            parent=self,
            model='cube',
            texture='assets/textures/stone_pressure_plate.jpg',
            scale=(1, 0.2, 1),
            position=(17-temple_length/2, 0.7, -23),
            collider='box'
        )
        third_pressure_plate = Entity(
            parent=self,
            model='cube',
            texture='assets/textures/stone_pressure_plate.jpg',
            scale=(1, 0.2, 1),
            position=(15, 0.55, -8),
            collider='box'
        )

    def build_altar(self):
        self.altar_floor = Entity(
            parent=self,
            model='cube',
            scale=(6, 0.3, 6),
            position=(4.5, 0.5, -21),
            texture='assets/textures/altar_floor_texture.jpg',
            texture_scale=(3,1),
            rotation=(0,180,0),
            collider='box',
        )
        self.altar_back_wall = Entity(
            parent=self,
            model='cube',
            scale=(6, 4, 0.5),
            position=(4.5, 2.5, -23.9),
            color = color.white,
            collider='box',
            texture='assets/textures/altar_walls_texture.jpg',
            texture_scale=(3,2)
        )
        self.altar_right_wall = Entity(
            parent=self,
            model='cube',
            scale=(0.5, 2, 3),
            position=(1.25, 1.5, -23),
            color = color.white,
            collider='box',
            texture='assets/textures/altar_walls_texture.jpg',
            texture_scale=(2, 2)
        )
        self.altar_left_wall = Entity(
            parent=self,
            model='cube',
            scale=(0.5, 2, 3),
            position=(7.75, 1.5, -23),
            color = color.white,
            collider='box',
            texture='assets/textures/altar_walls_texture.jpg',
            texture_scale=(2, 2)
        )


    def check_pressure_plates(self):
        global pressed_plates, first_pressure_plate, second_pressure_plate
        from ui import update_plates_counter
        plate1_distance = (self.player.position - first_pressure_plate.position).length()
        plate2_distance = (self.player.position - second_pressure_plate.position).length()
        plate3_distance = (self.player.position - third_pressure_plate.position).length()

        if plate1_distance < 1 and self.player.y < 0.8:
            if not self.plate1_pressed:
                self.plate1_pressed = True
                pressed_plates += 1
                first_pressure_plate.color = color.green

                update_plates_counter(pressed_plates)

        if plate2_distance < 1 and self.player.y < 0.8:
            if not self.plate2_pressed:
                self.plate2_pressed = True
                pressed_plates += 1
                second_pressure_plate.color = color.green

                update_plates_counter(pressed_plates)

        if plate3_distance < 1 and self.player.y < 0.8:
            if not self.plate3_pressed:
                self.plate3_timer += time.dt
                progress = self.plate3_timer / self.plate3_required_time
                third_pressure_plate.color = color.rgb(255 * (1 - progress), 255 * progress, 0)

                if self.plate3_timer >= self.plate3_required_time:
                    self.plate3_pressed = True
                    pressed_plates += 1
                    third_pressure_plate.color = color.green
                    update_plates_counter(pressed_plates)
        else:
            if not self.plate3_pressed:
                self.plate3_timer = 0
                third_pressure_plate.color = color.white

    def update(self):
        global pressed_plates, first_pressure_plate

        if not self.puzzle_solved and not self.door_closed:
            distance = (self.player.position - self.trigger_position).length()

            if distance < self.trigger_radius:
                self.close_door()
        if self.door_closed and pressed_plates == 3:
            self.open_door()
            show_finish_screen()
            self.puzzle_solved = True

        self.fire_timer += time.dt

        if self.fire_timer > 0.09:
            self.fire_timer = 0

            for torch in self.torches:
                z_offset = 0.6 if torch.z < -20 else -1
                TorchFire(
                    parent=scene,
                    position=torch.world_position + Vec3(0, torch.scale.y + 2, z_offset),
                )

        self.check_pressure_plates()


        if self.door_closed and not hasattr(self, 'counter_shown'):
            from ui import show_plates_counter
            show_plates_counter(self)
            self.counter_shown = True


    def close_door(self):
        self.door.y -= self.door_speed * time.dt

        if self.door.y <= 4:
            self.door.y = 4
            self.door_closed = True
            self.debug_trigger.visible = False
            from ui import show_door_closed_message
            show_door_closed_message(self)
            print('Usa a coborat complet!')

    def open_door(self):
        self.door.y += self.door_speed * time.dt
        if self.door.y >= 8:
            self.door.y = 8
            self.door_closed = False
            print('Usa a urcat complet!')

