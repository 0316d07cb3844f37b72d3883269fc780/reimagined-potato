from game_data.src.stance import Stance
from game_io.src.button import Button
from game_io.src.image_util import *
from game_io.src.targetable_utils import *
from game_io.src.portrait_io import get_portrait
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

    def redraw_self(self):
        image = make_stance_image(self.stance)
        self.image = image
        self.background_images = image_to_images_hovered_and_pressed(self.image)


def make_stance_image(stance: Stance):
    top_row = make_top_row(stance.name, stance.stance_id)
    middle_row = make_middle_row(stance.stability, stance.count)
    bottom_row = make_bottom_row(stance.target_list)
    return stack_vertical(top_row, middle_row, bottom_row)


def make_top_row(name, stance_id):
    name_image = make_text_field(name)
    stance_portrait = get_portrait(stance_id)
    return stack_horizontal(stance_portrait, name_image)


def make_middle_row(stability, count):
    stability_image = make_text_field("Stability :"+stability)
    count_image = make_text_field("x"+count)
    return stack_vertical(stability_image, count_image)


def make_bottom_row(targets):
    target_faces = [get_portrait(scene_id) for scene_id in targets]
    return stack_horizontal(*target_faces)