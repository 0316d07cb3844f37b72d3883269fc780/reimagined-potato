"""For generating ressources."""

import os, re
from string_utils import read_and_clean_file, write_string_to_file, root_path
from game_data.src.persondata import PersonData
from game_data.src.person_fighting import Person_Fighting


def create_person_fighting_from_person_base(path: str):
    base_string = read_and_clean_file(path)
    base_person = PersonData.create_from_string(base_string)
    person_fighting = Person_Fighting(base_person)
    person_fighting_string = str(person_fighting)
    person_fighting_string = scrub_scene_ids(person_fighting_string)
    fighting_path = fightify_path(path)
    if not os.path.exists(fighting_path):
        write_string_to_file(person_fighting_string, fighting_path)


def scrub_scene_ids(person_fighting_string):
    person_fighting_string = re.sub(r'scene_id>\d+<', 'scene_id>auto<', person_fighting_string)
    return person_fighting_string


def fightify_path(base_path):
    fighting_path = base_path[:-11] + "person_fighting"
    return fighting_path.replace("Bases", "Fighting", 1)


def create_fighting_for_all_bases():
    base_path = root_path("resources/People/Bases")
    base_files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))]
    base_files = [f for f in base_files if f[-11:] == "person_base"]
    for file_path in base_files:
        create_person_fighting_from_person_base("resources/People/Bases/"+file_path)


def main():
    create_fighting_for_all_bases()


if __name__ == "__main__":
    main()
