from game_data.src.stance import Stance
from game_io.src.button import Button
from game_io.src.image_util import *
from game_io.src.targetable_utils import *
from game_io.src.portrait_io import Portrait
from game_io.src.getter_io import getter


class StanceIO(Button):

    def __init__(self, stance: Stance, position=None):
        self.stance = stance
        image = make_stance_image(stance)
        self.rect = image.get_rect()
        if position is not None:
            self.rect.center = position
        getter[stance.scene_id] = self
        super(StanceIO, self).__init__(image_to_images_hovered_and_pressed(image), self.rect)


def make_stance_image(stance: Stance):
    name_image = make_text_field(stance.name)
    stance_portrait = Portrait(stance.stance_id)
    return stack_horizontal(stance_portrait, name_image)
