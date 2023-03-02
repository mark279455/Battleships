import random
import re

from ScreenControl import ScreenControl


class Board:
    """
    class for board
    controls locations of ships
    number of hits and misses
    previous moves
    """
    startrow = 5
    size = 6
    num_ships = 5

    def __init__(self, name, start_x):
        print(f"Board {name}")
        self.screencontrol = ScreenControl(5, start_x)
        self.hits = 0
        self.ships = []
        self.moves = []
        self.columns = [str(i) for i in range(1, self.size + 1)]
        self.rows = [Board.num2let(i) for i in range(Board.size)]

        while len(self.ships) < Board.num_ships:
            a = random.choice(self.columns)
            b = random.choice(self.rows)
            if [a, b] not in self.ships:
                self.ships.append([a, b])
        self.name = name

    def setupboard(self):
        """
            Shows board details for this board through ScreenControl on
            the screen 
        """
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
        Shows this boards ships through ScreenControl on the screen.
        """
        for coord in self.ships:
            self.screencontrol.showongrid(coord, ScreenControl.ship)
        print(ScreenControl.resetall)

    def makeaguess(self):
        """
        Takes the players guess through ScreenControl on the screen.
        """
        validcoord = []
        if self.name.lower().startswith("comp"):
            return self.makerandomguess()
        else:
            while True:
                ScreenControl.clearline(21)
                self.screencontrol.makeaguess()
                playerinput = input("")
                validcoord = self.validateinput(playerinput)
                if validcoord:
                    break
        return validcoord

    def processguess(self, guess, otherboard):
        """
        Processes the players validated guess
        - updates both players displays and checks game over
        """
        self.moves.append(guess)
        if guess in otherboard.ships:
            self.hits += 1
            self.screencontrol.printplayermessage(
                f"{self.name} hit a ship at {guess}"
            )
            otherboard.screencontrol.showongrid(guess, ScreenControl.shellhit)
        else:
            self.screencontrol.printplayermessage(
                f"{self.name} missed at {guess}"
            )
            otherboard.screencontrol.showongrid(guess, ScreenControl.shellmiss)
        self.screencontrol.updatemoves(len(self.moves))
        self.screencontrol.updatehits(self.hits)
        if self.hits == len(otherboard.ships):
            ScreenControl.clearline(24)
            msg = "lose." if self.name.lower() == "computer" else "win."
            ScreenControl.printendgamemessage(
                f"{self.name} has sunk all of {otherboard.name}'s"
                + f"ships. - you {msg}"
            )
            ScreenControl.printinfomessage("Play again?")
            ans = input("")
            if ans.lower().startswith("y"):
                main()
            else:
                quit()


    def makerandomguess(self):
        """
        Generates a random guess for the computer
        """
        resultlist = []
        while True:
            x = random.choice(self.columns)
            y = random.choice(self.rows)
            resultlist = [x, y]
            if resultlist not in self.moves:
                break
        return resultlist


    def validateinput(self, playerinput):
        """
        Validates the players guess.
        -   2 chars long
        -   1 letter and 1 number
        -   letter is between a and f
        -   number between 1 and 6
        -   player hasnt targetted this square before        
        """
        resultlist = []
        playerinput = playerinput.strip().lower()
        try:
            if len(playerinput) != 2:
                raise ValueError(
                    f"Input is 2 digits, a letter and a "
                    + f"number - you gave '{playerinput}'"
                )
            else:
                searchletters = "".join([str(i) for i in self.columns])
                searchnumbers = "".join([str(i) for i in self.rows])
                letnum = re.search(
                    "^[" + searchletters + "][" + searchnumbers + "]$",
                    playerinput,
                )
                numlet = re.search(
                    "^[" + searchnumbers + "][" + searchletters + "]$",
                    playerinput,
                )
            if letnum is not None:
                resultlist = [playerinput[0], playerinput[1]]
            elif numlet is not None:
                resultlist = [playerinput[::-1][0], playerinput[::-1][1]]
            else:
                raise ValueError(
                    f"input out of range, "
                    + f"'{playerinput}' is not on the board"
                )

            if resultlist in self.moves:
                raise ValueError(
                    f"Coordinate {playerinput} has already been targeted"
                )
            else:
                ScreenControl.clearinfomessage()
                return resultlist
        except ValueError as e:
            ScreenControl.printinfomessage(f"{e}, please try again")
        return False


    @staticmethod
    def num2let(num):
        """
        Converts numbers to letters
        -   ascii code of str(number) + 49
        -   '0' is ascii '48' will be converted to 'a' ascii '97'
        """
        return chr(ord(str(num)) + 49)


def startgame(playername):
    """
    creates boards for player and computer
    sets up display
    shows player and computers boards on display
    """
    print("129")
    playerboard = Board(playername, 0)
    compboard = Board("Computer", 40)
    ScreenControl.setupdisplay()
    playerboard.setupboard()
    playerboard.showships()
    compboard.setupboard()

    while True:
        validcoord = playerboard.makeaguess()
        playerboard.processguess(validcoord, compboard)
        validcoord = compboard.makeaguess()
        compboard.processguess(validcoord, playerboard)



def main():
    # playername = input("Please enter your name\n")
    playername = "Mark"
    startgame(playername)


main()

