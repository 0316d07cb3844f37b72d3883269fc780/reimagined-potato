import game_io.person_io as person_io
import game_data.src.person_data as person_data
import pygame

def test(allsprites):
    person = person_data.Person_Data(10, "Testtype")
    try:
        image = pygame.image.load("resources/testguy.bmp")
    except pygame.error as message:
        print("Cannot load: " + "resources/testguy.bmp")
        raise SystemExit(message)
    person = person_io.Person_IO(person, [1000,400])
    person.add(allsprites)


