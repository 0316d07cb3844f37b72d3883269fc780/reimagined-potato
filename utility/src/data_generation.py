"""For generating ressources."""

from string_utils import read_and_clean_file, write_string_to_file
from game_data.src.persondata import PersonData
from game_data.src.person_fighting import Person_Fighting


def create_person_fighting_from_person_base(path: str):
    base_string = read_and_clean_file(path)
    base_person = PersonData.create_from_string(base_string)
    person_fighting = Person_Fighting(base_person)
    person_fighting_string = str(person_fighting)
    fighting_path = fightify_path(path)
    write_string_to_file(fighting_path, person_fighting_string)


def fightify_path(base_path):
    fighting_path = base_path[:-11] + "person_fighting"
    return fighting_path.replace("Bases", "Fighting", 1)


def create_fighting_for_all_bases():
    pass

