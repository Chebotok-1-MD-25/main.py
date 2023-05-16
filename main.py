import math
import random

import arcade
from arcade.gui import UIManager, UIFlatButton, UIOnClickEvent

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Platformer"



# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.1
TILE_SCALING = 0.05


class StartGameButton(UIFlatButton):

    def __init__(self, center_x, center_y, ui_manager: UIManager):
        super().__init__(
            text="Start Game",
            x=center_x,
            y=center_y,
            # center_x=center_x,
            # center_y=center_y,
            width=200,
            height=50,

            id="start_game_button",
        )
        self.ui_manager = ui_manager


    def on_click(self, click):
        # print(click)
        self.ui_manager.clear()
        game_view = MyGame()
        game_view.setup()
        self.ui_manager.window.show_view(game_view)


class Coin(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)  # хранение картинки с масштабом


class MainMenu(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BANANA_MANIA)

        # Create a UIManager
        self.ui_manager = UIManager()
        self.ui_manager.enable()
        # Create the StartGameButton and register it with the UIManager
        start_game_button = StartGameButton(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2, self.ui_manager)
        self.ui_manager.add(start_game_button)

    def on_hide_view(self):
        self.ui_manager.remove_handlers()

    def on_draw(self):
        arcade.start_render()
        self.ui_manager.draw()
        arcade.draw_text("Dragon fly", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100,
                         arcade.color.BLUE, font_size=50, anchor_x="center")

    # def on_key_press(self, symbol: int, modifiers: int):
    #     self.ui_manager.on_key_press(symbol, modifiers)
    #
    # def on_key_release(self, symbol: int, modifiers: int):
    #     self.ui_manager.on_key_release(symbol, modifiers)

    # запуск игры
    # def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
    #     game_view = MyGame()
    #     game_view.setup()
    #     self.window.show_view(game_view)

class MyGame(arcade.View):
    """
    Main application class.
    """
#генерируем облака случайным образом
    def generate_clouds(self):
        while len(self.clouds_list) < 10:
            clouds = arcade.Sprite("images/cloud.png", TILE_SCALING)
            clouds.position = [random.randint(SCREEN_WIDTH + self.camera_pos[0], SCREEN_WIDTH * 2 + self.camera_pos[0]),
                               random.randint(0, SCREEN_HEIGHT)]
            self.clouds_list.append(clouds)

    def generate_coins(self):
        while len(self.coin_sprite_list) < 10:
            coins = arcade.Sprite("images/coin.png", 0.025)
            random_x = random.randint(SCREEN_WIDTH + self.camera_pos[0], SCREEN_WIDTH * 2 + self.camera_pos[0])
            random_y = random.randint(0, SCREEN_HEIGHT)
            coins.position = [random_x, random_y]
            #self.coin_sprite_list.append(coins)

            # Условие, чтобы монетки не накладывались на облака
            while arcade.check_for_collision_with_list(coins, self.clouds_list):
                random_x = random.randint(SCREEN_WIDTH + self.camera_pos[0], SCREEN_WIDTH * 2 + self.camera_pos[0])
                random_y = random.randint(0, SCREEN_HEIGHT)
                coins.center_x = random_x
                coins.center_y = random_y


            self.coin_sprite_list.append(coins)  # добавление картинки монеток


    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.clouds_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        #Очки
        self.score = 0

        self.camera_pos = [0,0]

        self.game_over = False

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)




    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Camera
        self.camera = arcade.Camera(self.window.width, self.window.height)

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "images/dragon.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 350
        self.player_list.append(self.player_sprite)

        self.coin_sprite_list = arcade.SpriteList() #монеты


        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        # coordinate_list = [[512, 502], [256, 81], [768, 403], [1005, 154], [1502, 403]]
        #
        # for coordinate in coordinate_list:
        #     # Add a crate on the ground
        #     clouds = arcade.Sprite(
        #         "images/cloud.png", TILE_SCALING
        #     )
        #     clouds.position = coordinate
        #     self.clouds_list.append(clouds)


        # for _ in range (10):
        #     coin = Coin("images/coin.png", 0.02)
        #     coin.center_x = random.randint(100, SCREEN_WIDTH)
        #     coin.center_y = random.randint(0, SCREEN_HEIGHT)





    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 8)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height)

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)


    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        self.clouds_list.draw()
        self.player_list.draw()

        # Activate our Camera
        self.camera.use()

        # Отображение очков на экране
        self.coin_sprite_list.draw()
        arcade.draw_text(f"Очки: {self.score}", self.camera_pos[0], 10, arcade.color.BANANA_MANIA, 14)

        # Отображение об окончании игры
        if self.game_over:
            arcade.draw_text("Game over", self.camera_pos[0]+480, 300, arcade.color.RED, font_size=50, anchor_x="center")
            arcade.draw_text(f"Количество очков: {self.score}", self.camera_pos[0] + 480, 250,
                             arcade.color.TAN, font_size=35, anchor_x="center")

    def on_update(self, delta_time):
        """Movement and game logic"""

        if not self.game_over:

            # Move the player with the physics engine
            self.player_sprite.center_x += 1

            # позиция камеры
            self.center_camera_to_player()

            # позиция счетчика очков
            self.camera_pos[0] += 1

            # сбор монеточек
            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_sprite_list)
            for coin in coin_hit_list:
                self.score += 1
                coin.kill()

            # столкновение с препятствием и конец игры
            cloud_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.clouds_list)
            for cloud in cloud_hit_list:
                self.player_sprite.kill()
                self.game_over = True

            for cloud in self.clouds_list:
                if cloud.center_x == self.camera_pos[0] - 50:
                    self.clouds_list.remove(cloud)

            while len(self.clouds_list) < 10:
                self.generate_clouds()

            for coin in self.coin_sprite_list:
                if coin.center_x == self.camera_pos[0] - 50:
                    self.coin_sprite_list.remove(coin)

            while len(self.coin_sprite_list) < 10:
                self.generate_coins()



    def on_key_press(self, key, modifiers):

        '''Перемещение по кнопкам'''
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.center_y += 8
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.center_y -= 8





def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_menu = MainMenu()
    window.show_view(main_menu)
    arcade.run()


if __name__ == "__main__":
    main()