#!/usr/bin/env python3

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

"""This is the main snake file."""

from snake_game import SnakeGame


def main():
    """The entrypoint of the program."""
    print('hello world.')

    return SnakeGame().run()


if __name__ == '__main__':
    main()
