from ursina import *


def clear_ui():
    for e in scene.entities[:]:
        if isinstance(e, (Button, Text)) or e.model =='quad':
            destroy(e)