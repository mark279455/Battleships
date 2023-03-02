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


    """
        Shows board details for this board through ScreenControl on the screen 
    """
    def setupboard(self):
        self.screencontrol.printname(
            f"{ScreenControl.fgcyan + ScreenControl.bright}"
            + f"{ScreenControl.underline_on}"
            + f"{self.name + ScreenControl.underline_off}"
        )

        # print columnlabel
        self.screencontrol.printcolumnlabels(self.columns)

        # print rowlabel
        self.screencontrol.printrowlabels(self.rows)

        # print grid
        for x in self.columns:
            for y in self.rows:
                self.screencontrol.showongrid(
                    [x, y],
                    f"{ScreenControl.fgyellow + ScreenControl.bright}"
                    + f"{ScreenControl.empty}{ScreenControl.resetall}",
                )
        print(ScreenControl.resetall)


    def showships(self):
        """
        Shows this boards ships through ScreenControl on the screen 
        """
        pass

    def makeaguess(self):
        """
        Takes the players guess ScreenControl on the screen 
        """
        pass


    def processguess(self):
        """
        Processes the players validated guess
        - updates both players displays and checks game over
        """
        pass

    def makerandomguess(self):
        """
        Generates a random guess for the computer
        """
        pass

    def validateinput(self):
        """
        Validates the players guess.
        -   2 chars long
        -   1 letter and 1 number
        -   letter is between a and f
        -   number between 1 and 6
        -   player hasnt targetted this square before        
        """
        pass

    @staticmethod
    def num2let(num):
        """
        Converts numbers to letters
        -   ascii code of str(number) + 49
        -   e.g. 
        -   '0' is ascii '48' will be converted to 'a' ascii '97'
        """
        return chr(ord(str(num)) + 49)

    @staticmethod
    def let2num(let):
        """
        Converts letters to numbers
        -   ascii code of str(number) - 49
        -   e.g. 
        -   'b' is ascii '98' will be converted to '1' ascii '49'
        """
        pass




























def startgame(playername):
    playerboard = Board(playername, 0)
    compboard = Board("Computer", 40)
    ScreenControl.setupdisplay()
    playerboard.setupboard()

def main():
    # playername = input("Please enter your name\n")
    playername = "Mark"
    startgame(playername)




print(f"1 = {Board.num2let('0')}")
# main()
# quit()

