#############################################################
# FILE : asteroids_main.py
# WRITER : Tom Tanaka, tom.tanaka, 211825872
# EXERCISE : intro2cs1 ex10 2019-2020
# DESCRIPTION: In this exercise, I create the game Asteroids
# I DISCUSSED THIS EXERCISE WITH: myself
# AUTHORS: tom.tanaka
##########################################################

from screen import Screen
import sys
import random
import ship
import asteroid
import torpedo
from math import cos
from math import sin
from math import radians

DEFAULT_ASTEROIDS_NUM = 10


class GameRunner:

    MAX_TORP_AMOUNT = 10
    MAX_TORP_TIME = 200
    SCORE_AST_3 = 20
    SCORE_AST_2 = 50
    SCORE_AST_1 = 100
    STARTING_LIVES_AMOUNT = 3
    ROTATION_AMOUNT = 7
    random_x = random.randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
    random_y = random.randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__ship1 = ship.Ship(self.random_x, 0, self.random_y, 0, 0.0)
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__can_attack = True
        self.asteroid_list = []
        self.torpedo_list = []
        self.score = 0
        self.lives = self.STARTING_LIVES_AMOUNT
        for i in range(asteroids_amount):
            self.create_asteroid()


    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        # Your code goes here
        self.__screen.set_score(self.score)
        self.update_ship()
        self.update_asteroid()
        self.update_torpedo()
        self.check_if_game_finished(self.score)

    ##------------------------General functions for manipulating objects------------------------------##
    def change_place(self, object1):
        """
        Calculates and changes the place of an object
        :param object1: ship, asteroid or torpedo
        """
        x_delta_axis = self.__screen_max_x - self.__screen_min_x
        x_new_cord = (object1.get_x_speed() + object1.get_x_location() - self.__screen_min_x)\
                     % x_delta_axis + self.__screen_min_x
        y_delta_axis = self.__screen_max_y - self.__screen_min_y
        y_new_cord = (object1.get_y_speed() + object1.get_y_location() - self.__screen_min_y) \
                     % y_delta_axis + self.__screen_min_y
        object1.change_location(x_new_cord, y_new_cord)

    def rotate(self, object1):
        """
        Rotates right or left
        :param object1: ship
        """
        if self.__screen.is_left_pressed():
            object1.set_direction(object1.get_direction() + self.ROTATION_AMOUNT)
        if self.__screen.is_right_pressed():
            object1.set_direction(object1.get_direction() - self.ROTATION_AMOUNT)

    def change_speed(self, object1):
        """
        Changes the speed of the object
        :param object1: ship, asteroid or torpedo
        """
        if self.__screen.is_up_pressed():
            object1.set_x_speed(object1.get_x_speed() + cos(radians(object1.get_direction())))
            object1.set_y_speed(object1.get_y_speed() + sin(radians(object1.get_direction())))

    ##------------------------Ship functions------------------------------##
    def update_ship(self):
        """
        Draws the ship and updates the place, rotation and speed of the ship
        """
        self.__screen.draw_ship(self.__ship1.get_x_location(), self.__ship1.get_y_location(),
                                self.__ship1.get_direction())
        self.change_place(self.__ship1)
        self.rotate(self.__ship1)
        self.change_speed(self.__ship1)

    def remove_life(self, ast):
        """
        When collided with an asteroid, removes one life and prints a message.
        :param ast: An asteroid that collided with the ship
        """
        self.__screen.remove_life()
        self.lives -= 1
        self.__screen.show_message("Collided with an asteroid!", "You have collided with an asteroid, you have "
                                   + str(self.lives) + " lives left")
        self.__screen.unregister_asteroid(ast)
        self.asteroid_list.remove(ast)

    def check_if_can_attack(self):
        """
        Checks if the ship can attack, and changes the ability to attack if necessary
        """
        if len(self.torpedo_list) > self.MAX_TORP_AMOUNT:
            self.__can_attack = False
        else:
            self.__can_attack = True

    ##------------------------Asteroid functions------------------------------##
    def update_asteroid(self):
        """
        Puts the asteroid in-game, draws and updates the asteroid and checks if the ship collided with an asteroid
        """
        self.put_asteroid_in_game()
        for ast in self.asteroid_list:
            self.__screen.draw_asteroid(ast, ast.get_x_location(), ast.get_y_location())
            if ast.has_intersection(self.__ship1):
                self.remove_life(ast)
            self.change_place(ast)

    def put_asteroid_in_game(self):
        """
        Puts all asteroids in asteroid_list on screen
        """
        for ast in self.asteroid_list:
            if ast.not_in_game():
                self.__screen.register_asteroid(ast, ast.get_size())
                ast.in_game_true()

    def create_asteroid(self):
        """
        Creates a new asteroid.
        """
        random_x_ast = random.randint(self.__screen_min_x, self.__screen_max_x)
        while random_x_ast == self.__ship1.get_x_location():  # While there is a ship in that place
            random_x_ast = random.randint(self.__screen_min_x, self.__screen_max_x)
        random_y_ast = random.randint(self.__screen_min_y, self.__screen_max_y)
        while random_y_ast == self.__ship1.get_y_location():  # While there is a ship in that place
            random_y_ast = random.randint(self.__screen_min_y, self.__screen_max_y)
        ast = asteroid.Asteroid(random_x_ast, random.randint(-4, 4), random_y_ast, random.randint(-4, 4), random.randint(1, 3))
        # ast = asteroid.Asteroid(random_x_ast, 0, random_y_ast, 0, random.randint(1, 3))  # For testing
        self.asteroid_list.append(ast)

    def asteroid_explodes(self, ast, torp):
        """
        Function that deals with the aftermath of asteroid exploding, including unregistering asteroid and torpedoes, and
        giving points.
        """
        self.asteroid_exploding_to_pieces(ast, torp)
        self.__screen.unregister_asteroid(ast)
        self.asteroid_list.remove(ast)
        self.__screen.unregister_torpedo(torp)
        self.torpedo_list.remove(torp)
        if ast.get_size() == 3:
            self.score += self.SCORE_AST_3
        elif ast.get_size() == 2:
            self.score += self.SCORE_AST_2
        elif ast.get_size() == 1:
            self.score += self.SCORE_AST_1

    def asteroid_exploding_to_pieces(self, ast, torp):
        """
        Function that is responsible for exploding the asteroid into smaller pieces.
        :param ast: asteroid
        :param torp: torpedo
        """
        if not ast.get_x_speed() ** 2 + ast.get_y_speed() ** 2:
            new_speed_x = new_speed_y = 0
        else:
            new_speed_x = (torp.get_x_speed() + ast.get_x_speed()) / ((ast.get_x_speed() ** 2 + ast.get_y_speed() ** 2) ** 0.5)
            new_speed_y = (torp.get_y_speed() + ast.get_y_speed()) / ((ast.get_x_speed() ** 2 + ast.get_y_speed() ** 2) ** 0.5)
        if ast.get_size() == 3 or ast.get_size() == 2:
            smaller_ast = asteroid.Asteroid(ast.get_x_location(), new_speed_x, ast.get_y_location(), new_speed_y,
                                              ast.get_size() - 1)
            smaller_ast_2 = asteroid.Asteroid(ast.get_x_location(), new_speed_x * -1, ast.get_y_location(), new_speed_y * -1,
                                                ast.get_size() - 1)
            self.asteroid_list.append(smaller_ast)
            self.asteroid_list.append(smaller_ast_2)

    ##------------------------Torpedo functions------------------------------##
    def update_torpedo(self):
        """
        Updates the torpedo. Checks if the user is attacking and is possible to attack, checks if the torpedo hit an
         asteroid.
        """
        self.torpedo_attack()
        self.put_torpedo_in_game()
        for torp in self.torpedo_list:
            self.change_place(torp)
            for ast in self.asteroid_list:
                if ast.has_intersection(torp):  # If there is a collision with an asteroid
                    self.asteroid_explodes(ast, torp)
            torp.add_one_to_life_time()
            if torp.get_life_time() >= self.MAX_TORP_TIME:  # If the torp stayed too long
                self.__screen.unregister_torpedo(torp)
                self.torpedo_list.remove(torp)
            self.check_if_can_attack()

    def put_torpedo_in_game(self):
        """
        Puts every torpedo in torpedo_list on the screen
        """
        for torp in self.torpedo_list:
            if torp.not_in_game():
                self.__screen.register_torpedo(torp)
                self.__screen.draw_torpedo(torp, torp.get_x_location(), torp.get_y_location(),
                                           torp.get_direction())
                torp.in_game_true()
            self.__screen.draw_torpedo(torp, torp.get_x_location(), torp.get_y_location(), torp.get_direction())

    def torpedo_attack(self):
        """
        When the attack button is pressed, this is the function that insures that the ship attacks
        """
        if self.__can_attack:
            if self.__screen.is_space_pressed():
                x_speed = self.__ship1.get_x_speed() + 2 * cos(radians(self.__ship1.get_direction()))
                y_speed = self.__ship1.get_y_speed() + 2 * sin(radians(self.__ship1.get_direction()))
                torp = torpedo.Torpedo(self.__ship1.get_x_location(), x_speed, self.__ship1.get_y_location(), y_speed,
                                         self.__ship1.get_direction())
                self.torpedo_list.append(torp)



    ##------------------------Game finishing functions------------------------------##
    def check_if_game_finished(self, score):
        """
        Checks if the game has to be finished
        :param score: score of the current GameRunner (self.score)
        """
        message_dict = {"Game over": "Game over! You have no more lives left. Try again. Your final score was: "
                                       + str(score), "Congratulations!": "Congratulations! You have won the game. Your final score was: "
                                       + str(score), "Quitting the game": "You quit the game! The window will now close"}
        if self.lives == 0:
            self.quit_game("Game over", message_dict)
        if len(self.asteroid_list) == 0:
            self.quit_game("Congratulations!", message_dict)
        if self.__screen.should_end():  # If 'q' was pressed
            self.quit_game("Quitting the game", message_dict)

    def quit_game(self, message_key, message_dict):
        """
        This function is responsible for quitting the game. Prints a fitting message depending on how the game finished.
        """
        self.__screen.show_message(message_key, message_dict[message_key])
        self.__screen.end_game()
        sys.exit()





def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
