import logging
import random
import re

from ScreenControl import ScreenControl


def setup_logger(name, log_file, level=logging.DEBUG):
    # To setup as many loggers as you want
    handler = logging.FileHandler(log_file, "w", "utf-8")
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


class Board:
    startrow = 5
    log = setup_logger("log", "bg.log", level=logging.DEBUG)
    size = 6
    num_ships = 5

    def __init__(self, name, start_x):
        self.screencontrol = ScreenControl(5, start_x)
        self.hits = 0
        self.ships = []
        self.moves = []
        self.columns = [str(i) for i in range(1, self.size + 1)]
        self.rows = [ScreenControl.num2let(i) for i in range(Board.size)]

        while len(self.ships) < Board.num_ships:
            a = random.choice(self.columns)
            b = random.choice(self.rows)
            if [a, b] not in self.ships:
                self.ships.append([a, b])
        self.name = name


def startgame(playername):
    playerboard = Board(playername, 0)
    compboard = Board("Computer", 40)
    ScreenControl.setupdisplay()


def main():
    # playername = input("Please enter your name\n")
    playername = "Mark"
    startgame(playername)


main()
quit()

