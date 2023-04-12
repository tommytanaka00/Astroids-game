class Ship:

    def __init__(self, x_location, x_speed, y_location, y_speed, degrees):
        self.__x_location = x_location
        self.__x_speed = x_speed
        self.__y_location = y_location
        self.__y_speed = y_speed
        self.__direction = degrees
        self.__radius = 2

    def change_location(self, x_new_cord, y_new_cord):
        self.__x_location = x_new_cord
        self.__y_location = y_new_cord

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

    def get_radius(self):
        return self.__radius