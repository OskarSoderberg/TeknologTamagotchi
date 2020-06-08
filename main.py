from gui import *
from tamagotchi import *
import pickle


def save(number, the_object):
    """Saves the_object to a file"""
    the_object.last_interaction = time.time()
    save_file = open('save' + str(number) + '.txt', 'wb')
    pickle.dump(the_object, save_file)


def load(number):
    """Loads saved data from file"""
    try:
        save_file = open('save' + str(number) + '.txt', 'rb')
        my_tamagotchi = pickle.load(save_file)
    except FileNotFoundError:
        my_tamagotchi = Tamagotchi("Olof", 150, (50, 123, 233))
    return my_tamagotchi


def main():
    """Creates GUI, loads saved data, alternatively creates a new
    tamagotchi if a saved one doesn't exist. Runs a loop that handles
    events and animations."""

    my_tamagotchi = load(1)
    my_gui = Gui1(my_tamagotchi)
    my_gui.update_graphics()
    my_tamagotchi.last_interaction = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                save(1, my_tamagotchi)
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                my_gui.trigger_pressed_button()
                my_gui.update_fields()

        if my_tamagotchi.get_time_alone() > 5:
            my_tamagotchi.feel_alone()
            my_gui.update_fields()

        my_gui.update_graphics()


if __name__ == '__main__':
    main()