# Shalom Yemane
# CPSC 386-01
# 2021-11-29
# syemane@csu.fullerton.edu
# @S-Yemane
#
# Lab 04-00
#
# This file is the executable for the entire program.
#

"""This module holds the Scene classes."""

import random
import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Scene:
    """The default Scene class."""

    def __init__(self, screen, background_color):
        self._is_valid = True
        self._game_is_valid = True
        self._go_to_title_screen = False
        self._go_to_game_screen = False
        self._framerate = 60
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background_color = background_color
        self._background.fill(self._background_color)
        self._font = pygame.freetype.SysFont('arial', 24)

    def is_valid(self):
        """Returns whether the current scene should continue to be displayed or not."""
        return self._is_valid

    def game_is_valid(self):
        """Returns whether the game is being exited out of or not."""
        return self._game_is_valid

    def go_to_title_screen(self):
        """Returns if the next scene should be the title screen."""
        return self._go_to_title_screen

    def go_to_game_screen(self):
        """Returns if the next scene should be the title screen."""
        return self._go_to_game_screen

    def reset_flags(self):
        """Resets all the boolean flags to default values."""
        self._is_valid = True
        self._game_is_valid = True
        self._go_to_title_screen = False
        self._go_to_game_screen = False

    def framerate(self):
        """Returns the framerate."""
        return self._framerate

    def start(self):
        """Start the scene."""
        pass

    def end(self):
        """End the scene."""
        pass

    def update(self):
        """Update the scene."""
        pass

    def draw(self):
        """Draws onto the window screen."""
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Processes a given event for potential input/actions."""
        if event.type == pygame.QUIT:
            print('Quit')
            self._is_valid = False
            self._game_is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print('Quit')
            self._is_valid = False
            self._game_is_valid = False


class TitleScene(Scene):
    """The Title Scene class."""

    def __init__(self, screen, background_color):
        super().__init__(screen, background_color)
        self._start_button = pygame.Rect(350, 500, 100, 50)
        self._quit_button = pygame.Rect(350, 600, 100, 50)

    def draw(self):
        super().draw()
        title_surface, unused_rect = self._font.render('Snek', WHITE)
        start_button_surface, unused_rect = self._font.render('Start', BLACK)
        quit_button_surface, unused_rect = self._font.render('Quit', BLACK)
        self._screen.blit(title_surface, (400, 250))
        pygame.draw.rect(self._screen, WHITE, self._start_button)
        pygame.draw.rect(self._screen, WHITE, self._quit_button)
        self._screen.blit(
            start_button_surface,
            (self._start_button.x + 25, self._start_button.y + 15),
        )
        self._screen.blit(
            quit_button_surface,
            (self._quit_button.x + 27, self._quit_button.y + 15),
        )

    def process_event(self, event):
        super().process_event(event)
        # Hitting the "Enter" key starts the game.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._is_valid = False
            self._go_to_game_screen = True
        # Handling for clicking on the title screen buttons.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseposition = pygame.mouse.get_pos()
            if self._start_button.collidepoint(mouseposition):
                self._is_valid = False
                self._go_to_game_screen = True
            if self._quit_button.collidepoint(mouseposition):
                self._is_valid = False
                self._game_is_valid = False


class GameScene(Scene):
    """The Game Scene class."""

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self, screen, background_color):
        super().__init__(screen, background_color)
        self._framerate = 10
        self._is_playing = True
        self._button_font = pygame.freetype.SysFont('arial', 12)
        self._up_button = pygame.Rect(375, 675, 50, 25)
        self._down_button = pygame.Rect(375, 725, 50, 25)
        self._left_button = pygame.Rect(300, 700, 50, 25)
        self._right_button = pygame.Rect(450, 700, 50, 25)

        self._direction = GameScene.UP
        self._snake_part_coords = [(12, 12), (12, 13), (12, 14)]
        self._snake_growing = False
        self._apple_coords = (12, 5)
        self._score = 0
        # Note: Grid coordinates start at zero.

    def update(self):
        if self._is_playing:
            self.check_for_collision()
            self.check_ate_apple()

    def draw(self):
        super().draw()
        self.draw_grid()
        self.draw_buttons()
        self.draw_apple()
        self.draw_snake_parts()
        self.draw_score()

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseposition = pygame.mouse.get_pos()
            if (
                self._up_button.collidepoint(mouseposition)
                and self._direction != GameScene.DOWN
            ):
                self._direction = GameScene.UP
            if (
                self._down_button.collidepoint(mouseposition)
                and self._direction != GameScene.UP
            ):
                self._direction = GameScene.DOWN
            if (
                self._left_button.collidepoint(mouseposition)
                and self._direction != GameScene.RIGHT
            ):
                self._direction = GameScene.LEFT
            if (
                self._right_button.collidepoint(mouseposition)
                and self._direction != GameScene.LEFT
            ):
                self._direction = GameScene.RIGHT
        if event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP or event.key == pygame.K_w
            ) and self._direction != GameScene.DOWN:
                self._direction = GameScene.UP
            if (
                event.key == pygame.K_DOWN or event.key == pygame.K_s
            ) and self._direction != GameScene.UP:
                self._direction = GameScene.DOWN
            if (
                event.key == pygame.K_LEFT or event.key == pygame.K_a
            ) and self._direction != GameScene.RIGHT:
                self._direction = GameScene.LEFT
            if (
                event.key == pygame.K_RIGHT or event.key == pygame.K_d
            ) and self._direction != GameScene.LEFT:
                self._direction = GameScene.RIGHT

    def check_ate_apple(self):
        """Check if the snake reached an apple."""
        if self._snake_part_coords[0] == self._apple_coords:
            self._snake_growing = True
            self._score = self._score + 1
            self.grow_new_apple()

    def check_for_collision(self):
        """Check if the snake has died."""
        pos_to_move = self._snake_part_coords[0]
        if self._direction == GameScene.UP:
            pos_to_move = (pos_to_move[0], pos_to_move[1] - 1)
        if self._direction == GameScene.DOWN:
            pos_to_move = (pos_to_move[0], pos_to_move[1] + 1)
        if self._direction == GameScene.LEFT:
            pos_to_move = (pos_to_move[0] - 1, pos_to_move[1])
        if self._direction == GameScene.RIGHT:
            pos_to_move = (pos_to_move[0] + 1, pos_to_move[1])

        if (
            pos_to_move[0] < 0
            or pos_to_move[0] > 24
            or pos_to_move[1] < 0
            or pos_to_move[1] > 24
        ):
            self._is_playing = False
        for coords in self._snake_part_coords:
            if pos_to_move[0] == coords[0] and pos_to_move[1] == coords[1]:
                self._is_playing = False

        self._snake_part_coords.insert(0, pos_to_move)
        if self._snake_growing:
            self._snake_growing = False
        else:
            self._snake_part_coords.pop()

    def grow_new_apple(self):
        """Chooses a new coordinate on the grid for an apple."""
        self._apple_coords = (random.randint(0, 24), random.randint(0, 24))
        # If the new coords are inside a snake part, get a new random coordinate.
        for coord in self._snake_part_coords:
            if self._apple_coords == coord:
                self.grow_new_apple()

    def draw_grid(self):
        """Draws a 25x25 grid of squares, 20 pixels squared in size."""
        for x_coord in range(150, 651, 20):
            pygame.draw.line(
                self._screen, WHITE, (x_coord, 150), (x_coord, 650)
            )
        for y_coord in range(150, 651, 20):
            pygame.draw.line(
                self._screen, WHITE, (150, y_coord), (650, y_coord)
            )

    def draw_buttons(self):
        """Draws 4 buttons for use in controlling the snake."""
        pygame.draw.rect(self._screen, WHITE, self._up_button)
        pygame.draw.rect(self._screen, WHITE, self._down_button)
        pygame.draw.rect(self._screen, WHITE, self._left_button)
        pygame.draw.rect(self._screen, WHITE, self._right_button)
        up_surface, rect = self._button_font.render('UP', BLACK)
        down_surface, rect = self._button_font.render('DOWN', BLACK)
        left_surface, rect = self._button_font.render('LEFT', BLACK)
        right_surface, rect = self._button_font.render('RIGHT', BLACK)
        self._screen.blit(
            up_surface, (self._up_button.x + 17, self._up_button.y + 8)
        )
        self._screen.blit(
            down_surface, (self._down_button.x + 7, self._down_button.y + 8)
        )
        self._screen.blit(
            left_surface, (self._left_button.x + 11, self._left_button.y + 8)
        )
        self._screen.blit(
            right_surface, (self._right_button.x + 8, self._right_button.y + 8)
        )

    def draw_apple(self):
        """Draw the apple onto the screen."""
        pygame.draw.rect(
            self._screen,
            RED,
            pygame.Rect(
                150 + self._apple_coords[0] * 20,
                150 + self._apple_coords[1] * 20,
                20,
                20,
            ),
        )

    def draw_snake_parts(self):
        """Draws all the individual parts of the snake."""
        for coord in self._snake_part_coords:
            pygame.draw.rect(
                self._screen,
                WHITE,
                pygame.Rect(150 + coord[0] * 20, 150 + coord[1] * 20, 20, 20),
            )

    def draw_score(self):
        """Draws the scoreboard."""
        score_surface, rect = self._font.render(str(self._score), WHITE)
        self._screen.blit(score_surface, (600, 700))
