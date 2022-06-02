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

"""This module controls the flow of the game."""

import pygame
import scene


def display_info():
    """Print out the information about the display driver and video information."""
    print(
        'The display is using "{}" driver.'.format(pygame.display.get_driver())
    )
    print('Video Info:')
    print(pygame.display.Info())


class SnakeGame:
    """The SnakeGame class."""

    def __init__(self):
        pass

    def run(self):
        """This is the entry point to the game. It is the main function!"""
        if not pygame.font:
            print('Warning: Fonts disabled.')
        if not pygame.mixer:
            print('Warning: Sound disabled.')
        pygame.init()
        display_info()
        window_size = (800, 800)
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(window_size)
        title = 'Snek'
        pygame.display.set_caption(title)

        scene_list = [
            scene.TitleScene(screen, (0, 0, 0)),
            scene.GameScene(screen, (0, 0, 0)),
        ]

        current_scene = scene_list[0]
        current_scene.start()
        while current_scene.game_is_valid():
            while current_scene.is_valid():
                clock.tick(current_scene.framerate())
                for event in pygame.event.get():
                    current_scene.process_event(event)
                    pygame.display.update()
                current_scene.update()
                current_scene.draw()
                pygame.display.update()

            current_scene.end()
            if current_scene.go_to_title_screen():
                current_scene = scene_list[0]
            elif current_scene.go_to_game_screen():
                current_scene = scene_list[1]
            else:
                pygame.quit()
                return 0
            current_scene.reset_flags()
            current_scene.start()
        print('Exiting')
        pygame.quit()

        return 0
