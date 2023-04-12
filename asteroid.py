class Asteroid:

    def __init__(self, x_location, x_speed, y_location, y_speed, size):
        self.__x_location = x_location
        self.__x_speed = x_speed
        self.__y_location = y_location
        self.__y_speed = y_speed
        self.__size = size
        self.__in_game = False
        self.__radius = (self.__size * 10) - 5

    def change_location(self, x_new_cord, y_new_cord):
        self.__x_location = x_new_cord
        self.__y_location = y_new_cord

    def has_intersection(self, obj):
        distance = ((obj.get_x_location() - self.__x_location)**2 + (obj.get_y_location() - self.__y_location)**2)**0.5
        if distance <= (self.__radius + obj.get_radius()):
            return True
        else:
            return False

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

    def get_size(self):
        return self.__size
