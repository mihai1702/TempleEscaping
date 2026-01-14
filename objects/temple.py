from ursina import *
from objects.torch_fire import TorchFire

temple_width = 25
temple_length = 25
wall_height = 14
wall_thickness = 1

first_pressure_plate = None

pressed_plates = 0
plate_1_pressed = False
plate_2_pressed = False
plate_3_pressed = False

class Temple(Entity):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.door_closed = False
        self.fire_timer = 0
        self.plate1_pressed = False
        self.plate_check_timer = 0  # Add timer for pressure plate checks

        # Ușa templului (sus la început)
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

        # Debug vizual (poți ascunde după test)
        self.debug_trigger = Entity(
            model='sphere',
            scale=self.trigger_radius*2,
            position=self.trigger_position,
            color=color.rgba(0,0,0,0),
            visible=True
        )

        # viteza de coborâre a ușii
        self.door_speed = 8  # unități pe secundă

        self.build_floor()
        self.build_walls()
        self.build_columns()
        self.build_torches()
        self.build_pressure_plates()


    def build_floor(self):
        self.floor = Entity(
            parent=self,
            model='cube',
            scale=(26, 1, 26),
            position=(5, 0, -15),
            texture='assets/textures/temple_floor_texture.jpg',
            texture_scale=(15, 15),
            collider='box',
        )
    def build_walls(self):
        self.front_left_wall = Entity(
            parent=self,
            model='cube',
            scale=(11, wall_height, 1),
            position=(11, wall_height/2, -5),
            texture='assets/textures/wall_texture.jpg',
            collider='box',
        )
        self.front_right_wall = Entity(
            parent=self,
            model='cube',
            scale=(11, wall_height, 1),
            position=(-2, wall_height/2, -5),
            texture='assets/textures/wall_texture.jpg',
            collider='box'
        )
        self.front_top_wall = Entity(
            parent=self,
            model='cube',
            scale=(2, wall_height-8, 1),
            position=(4.5, 11, -5),
            texture='assets/textures/wall_texture.jpg',
            collider='box'
        )
        self.first_side_wall = Entity(
            parent=self,
            model='cube',
            scale=(wall_thickness, wall_height, temple_length),
            position=(5- temple_width/2, wall_height/2, -15),
            texture='assets/textures/wall_texture.jpg',
            texture_scale=(1, 6),
            collider='box'
        )
        self.second_side_wall = Entity(
            parent=self,
            model='cube',
            scale=(wall_thickness, wall_height, temple_length),
            position=(4.5+ temple_width/2, wall_height/2, -15),
            texture='assets/textures/wall_texture.jpg',
            texture_scale=(1, 6),
            collider='box'
        )
        self.back_wall = Entity(
            parent=self,
            model='cube',
            scale=(temple_length, wall_height, wall_thickness),
            position=(17-temple_length/2, wall_height/2, -26),
            texture='assets/textures/wall_texture.jpg',
            texture_scale=(1, 6),
            collider='box'
        )
        self.ceiling = Entity(
            parent=self,
            model='cube',
            scale=(26, 1, 26),
            position=(5, wall_height, -15),
            texture='assets/textures/ceiling_texture.jpg',
            collider='box'
        )

    def build_columns(self):
        z_positions = [-35.5, -28.5, -21.5]
        x_positions = [-27, -10]

        for x in x_positions:
            for z in z_positions:
                Entity(
                    parent=self,  # important! rămâne copil al templului
                    model='assets/3d_models/Pillar.glb',
                    scale=0.14,
                    origin_y=0,  # baza coloanei pe podea
                    position=(x, 0, z),  # poziție relativă la templu
                    collider='box'
                )

    def build_torches(self):
        self.torches = []  # Store all torches in a list

        torch_positions = [(0, 0, -5), (9, 0, -5)]



        for pos in torch_positions:
            torch = Entity(
                parent=self,
                model='assets/3d_models/temple_torch.glb',
                scale=5,
                origin_y=0,
                position=pos,
            )
            self.torches.append(torch)

    def build_pressure_plates(self):
        global first_pressure_plate
        first_pressure_plate = Entity(
            parent=self,
            model='cube',
            texture='assets/textures/stone_pressure_plate.jpg',
            scale=(1, 0.2, 1),
            position=(17-temple_length/2, 0.55, -25),
            collider='box',
        )

    def check_pressure_plates(self):
        """Check pressure plates separately from main update loop"""
        global pressed_plates, first_pressure_plate

        plate1_distance = (self.player.position - first_pressure_plate.position).length()
        if plate1_distance < 2 and self.player.y < 1:
            if not self.plate1_pressed:
                self.plate1_pressed = True
                pressed_plates += 1
                first_pressure_plate.color = color.green

                # Update UI counter immediately
                from ui import update_plates_counter
                update_plates_counter(pressed_plates)

    def update(self):
        global pressed_plates, first_pressure_plate

        if not self.door_closed:
            distance = (self.player.position - self.trigger_position).length()

            if distance < self.trigger_radius:
                self.close_door()

        self.fire_timer += time.dt

        if self.fire_timer > 0.09:
            self.fire_timer = 0

            for torch in self.torches:
                TorchFire(
                    parent=scene,
                    position=torch.world_position + Vec3(0, 7, -1),
                )

        self.plate_check_timer += time.dt
        if self.plate_check_timer > 0.1:
            self.plate_check_timer = 0
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
