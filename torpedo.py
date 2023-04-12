class Torpedo:

    def __init__(self, x_location, x_speed, y_location, y_speed, degrees):
        self.__x_location = x_location
        self.__x_speed = x_speed
        self.__y_location = y_location
        self.__y_speed = y_speed
        self.__direction = degrees
        self.__in_game = False
        self.__radius = 4
        self.__life_time = 0

    def change_location(self, x_new_cord, y_new_cord):
        self.__x_location = x_new_cord
        self.__y_location = y_new_cord

    def not_in_game(self):
        if not self.__in_game:
            return True
        return False

    def in_game_true(self):
        self.__in_game = True

    def get_x_location(self):
        return self.__x_location

    def get_y_location(self):
        return self.__y_location

    def get_x_speed(self):
        return self.__x_speed

    def get_y_speed(self):
        return self.__y_speed

    def set_x_speed(self, new_speed):
        self.__x_speed = new_speed

    def set_y_speed(self, new_speed):
        self.__y_speed = new_speed

    def get_direction(self):
        return self.__direction

    def set_direction(self, new_direction):
        self.__direction = new_direction

    def get_life_time(self):
        return self.__life_time

    def add_one_to_life_time(self):
        self.__life_time += 1

    def get_radius(self):
        return self.__radius
