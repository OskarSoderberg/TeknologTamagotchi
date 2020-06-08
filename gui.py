import pygame
import time


class TextField:
    """Contains the TextField's properties such as background
    color, text size, coordinates and a print function"""
    def __init__(self, text, size, x, y, width, height, text_color, background_color):
        self.text = text
        self.size = size
        self.coordinates = [x, y]
        self.measures = [width, height]
        self.text_color = text_color
        self.background_color = background_color

    def get_middle_coordinates(self):
        """Returns the center coordinates of the textfield"""
        return [self.coordinates[0] + (self.measures[0] // 2),
                self.coordinates[1] + (self.measures[1] // 2)]

    def print_to(self, game_display, correction_x=0, correction_y=0):
        """Prints TextField to game_display"""
        if self.background_color:
            pygame.draw.rect(game_display, self.background_color, self.coordinates + self.measures)
        text_surface = pygame.font.Font('BalsamiqSans-Regular.ttf', self.size).render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.get_middle_coordinates()[0] + correction_x, self.get_middle_coordinates()[1] + correction_y)
        game_display.blit(text_surface, text_rect)


class Button:
    """Contains the Button's properties such as colors in
    different states, a TextField, size and coordinates. Also
    Has functions such as get_current_state"""
    def __init__(self, text, x, y, width, height, text_color, button_colors, the_function):
        self.textfield = TextField(text, (height // 2), x, y, width, height, text_color, False)
        self.coordinates = [x, y]
        self.measures = [width, height]
        self.button_colors = button_colors
        self.the_function = the_function

    def set_text(self, new_text):
        self.textfield.text = new_text

    def get_text(self):
        return self.textfield.text

    def get_middle_coordinates(self):
        """Returns the center coordinates of the button"""
        return [self.coordinates[0] + (self.measures[0] // 2),
                self.coordinates[1] + (self.measures[1] // 2)]

    def get_state(self):
        """Returns the state of the button as a string"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.coordinates[0] < mouse_pos[0] < self.coordinates[0] + self.measures[0] \
                and self.coordinates[1] < mouse_pos[1] < self.coordinates[1] + self.measures[1]:
            if mouse_pressed:
                return 'pressed'
            else:
                return 'hover'
        else:
            return 'standard'

    def print_to(self, game_display):
        """Prints Button to game_display"""
        if self.get_state() == 'pressed':
            pygame.draw.rect(game_display, (0, 0, 0), self.coordinates + self.measures)
            pygame.draw.rect(game_display, self.button_colors[2], [self.coordinates[0] + 5,
                                                                   self.coordinates[1] + 5,
                                                                   self.measures[0],
                                                                   self.measures[1]])
            self.textfield.print_to(game_display, 3, 3)
        elif self.get_state() == 'hover':
            pygame.draw.rect(game_display, self.button_colors[1], self.coordinates + self.measures)
            self.textfield.print_to(game_display)
        else:
            pygame.draw.rect(game_display, self.button_colors[0], self.coordinates + self.measures)
            self.textfield.print_to(game_display)


class Gui1:
    """Generates a GUI for tamagotchi"""
    def __init__(self, tamagotchi):
        self.tamagotchi = tamagotchi

        pygame.init()
        self.game_display = pygame.display.set_mode((400, 600))
        pygame.display.set_caption('Technology Tamagotchi - Version 4.1')

        white = (255, 255, 255)
        lightgray = (200, 200, 200)
        gray = (100, 100, 100)
        darkgray = (90, 90, 90)
        black = (0, 0, 0)

        self.my_button1 = Button("Sleep", 0, 400, 200, 100, black, (lightgray, gray, darkgray),
                                 lambda: tamagotchi.action('Sleep'))
        self.my_button2 = Button("Study", 200, 400, 200, 100, black, (lightgray, gray, darkgray),
                                 lambda: tamagotchi.action('Study'))
        self.my_button3 = Button("Exam", 0, 500, 200, 100, black, (lightgray, gray, darkgray),
                                 lambda: tamagotchi.action('Exam'))
        self.my_button4 = Button("Party", 200, 500, 200, 100, black, (lightgray, gray, darkgray),
                                 lambda: tamagotchi.action('Party'))

        self.textfield_size = TextField("Size: " + str(self.tamagotchi.size), 30, 200, 350, 200, 50, white, black)
        self.textfield_name = TextField(self.tamagotchi.name, 40, 0, 350, 200, 50, white, black)

        self.action_field = TextField("Hello my friend!", 30, 0, 0, 400, 50, white, black)
        self.special_effect_field = TextField(self.tamagotchi.get_time_alone_str(), 25, 0, 50, 400, 50, black, False)

    def trigger_pressed_button(self):
        """Activates the function of the pressed button"""
        if self.my_button1.get_state() == 'pressed':
            self.my_button1.the_function()
        elif self.my_button2.get_state() == 'pressed':
            self.my_button2.the_function()
        elif self.my_button3.get_state() == 'pressed':
            self.my_button3.the_function()
        elif self.my_button4.get_state() == 'pressed':
            self.my_button4.the_function()
        self.tamagotchi.last_interaction = time.time()

    def update_fields(self):
        """Updates game_display to changed values"""
        self.textfield_size.text = "Size: " + str(self.tamagotchi.size)
        self.textfield_name.text = self.tamagotchi.name

        if self.tamagotchi.current_animation == 'Sleep':
            self.action_field.text = "Sleeping..."
        elif self.tamagotchi.current_animation == 'Study':
            self.action_field.text = "Studying..."
        elif self.tamagotchi.current_animation == 'Exam':
            self.action_field.text = "Writing test..."
        elif self.tamagotchi.current_animation == 'Party':
            self.action_field.text = "Partying!!!"

        self.special_effect_field.text = self.tamagotchi.current_special_effect

    def update_graphics(self):
        """Prints everything to game_display"""
        self.game_display.fill((255, 255, 255))

        self.tamagotchi.draw_to(self.game_display)

        self.my_button1.print_to(self.game_display)
        self.my_button2.print_to(self.game_display)
        self.my_button3.print_to(self.game_display)
        self.my_button4.print_to(self.game_display)

        self.textfield_size.print_to(self.game_display)
        self.textfield_name.print_to(self.game_display)
        self.action_field.print_to(self.game_display)
        self.special_effect_field.print_to(self.game_display)

        pygame.display.update()
