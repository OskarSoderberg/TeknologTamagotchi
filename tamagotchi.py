import time
import pygame


class Tamagotchi:
    def __init__(self, name, size, color):
        self.name = name
        self.size = size
        self.color = color
        self.last_actions = ['', '', '']
        self.same_action_repeat = 0
        self.last_interaction = time.time()
        self.current_animation = ''
        self.current_special_effect = ''

    img = pygame.image.load('t3.png')
    party = pygame.image.load('party.png')

    def action(self, action_type):
        """Executes the action of the given type and updates
        the information textfield."""
        self.current_animation = action_type
        self.add_to_last_actions(action_type)
        if self.same_action_repeat == 1:
            self.special_effect()
        if self.same_action_repeat >= 3:
            self.shrink()
            self.current_special_effect = 'Boring...'

    def special_effect(self):
        """Does something depending on the state of the
        last_actions list"""
        if self.last_actions == ['Study', 'Exam', 'Party']:
            self.current_special_effect = 'A+++'
            print(self.current_special_effect)
            self.grow()
        elif self.last_actions == ['Sleep', 'Party', 'Exam']:
            self.current_special_effect = 'Didn\'t study before the test. F-'
            print(self.current_special_effect)
            self.shrink()
        elif self.last_actions == ['Party', 'Sleep', 'Party']:
            self.current_special_effect = str(self.name) + ' is getting popular!'
            print(self.current_special_effect)
            self.grow()
        elif self.last_actions == ['Study', 'Party', 'Exam']:
            self.current_special_effect = 'Didn\'t remember anything on the test'
            print(self.current_special_effect)
            self.shrink()
        else:
            self.current_special_effect = ''

    def shrink(self):
        """Changes the size of the character"""
        self.size //= 2

    def grow(self):
        """Changes the size of the character"""
        self.size += 30

    def feel_alone(self):
        """Updates last interaction, updates special effect field and shrinks character"""
        self.last_interaction = time.time() - 4
        self.current_special_effect = "I'm so lonely :("
        self.shrink()

    def add_to_last_actions(self, action_type):
        """Adds an item to the last
        actions list and
        handles situations where the same button is pressed consecutively"""
        if self.last_actions[2] != action_type:
            del self.last_actions[0]
            self.last_actions.append(action_type)
            self.same_action_repeat = 1
        else:
            self.same_action_repeat += 1
        print(self.last_actions)
        print(self.same_action_repeat)

    def get_time_alone(self):
        """Returns time since last interaction in seconds"""
        return time.time() - self.last_interaction

    def get_time_alone_str(self):
        """Returns a string with the time alone divided into days, hours, minutes and seconds"""
        time_passed = time.time() - self.last_interaction
        if time_passed > 0.5:
            seconds = time_passed % 60
            time_passed = time_passed // 60
            minutes = time_passed % 600
            time_passed = time_passed // 60
            hours = time_passed % 24
            time_passed = time_passed // 24
            return str(int(time_passed)) + " days, " + str(int(hours)) + " h, " + \
                   str(int(minutes)) + " m, " + str(int(seconds)) + " s"
        else:
            return ''

    def draw_to(self, game_display):
        """Draws the tamagotchi to game_display"""
        img_copy = pygame.transform.scale(self.img, (self.size, self.size))

        img_copy.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)

        if self.size < 100:
            color = (255, 100, 100)
        elif self.size < 250:
            color = (100, 255, 100)
        else:
            color = (100, 100, 255)

        img_copy.fill(color + (0,), None, pygame.BLEND_RGBA_ADD)

        game_display.blit(img_copy, ((400 - self.size) // 2, ((600 - 200 - self.size) // 2)))

        if self.current_animation == 'Party':
            party_copy = pygame.transform.scale(self.party, (128, 128))
            game_display.blit(party_copy, (10, 100))


