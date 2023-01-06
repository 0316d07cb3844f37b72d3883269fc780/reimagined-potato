import game_io.src.personio as person_io
import game_data.src.persondata as person_data
import pygame

def test(allsprites):
    person = person_data.PersonData(10, "Testtype")
    try:
        image = pygame.image.load("resources/testguy.bmp")
    except pygame.error as message:
        print("Cannot load: " + "resources/testguy.bmp")
        raise SystemExit(message)
    person = person_io.PersonIO(person, [1000, 400])
    person.add(allsprites)


