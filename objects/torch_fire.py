import timeit

from ursina import *
from ursina import color as ucolor
from random import uniform, choice

class TorchFire(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='quad',
            billboard = True,
            texture='assets/textures/fire_texture.png',
            **kwargs
        )
        self.life = uniform(0.3, 0.6)
        self.speed = uniform(1.2, 2.2)
        self.drift = Vec3(uniform(-0.3, 0.3), 1, uniform(-0.3, 0.3))


    def update(self):
        self.position += self.drift * self.speed * time.dt
        self.scale *= 0.6
        self.life -=time.dt


        if self.life <= 0:
            destroy(self)