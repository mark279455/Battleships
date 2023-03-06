import random
import re

from screen_control import ScreenControl


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
        """
        Board constructor
        """
        # print(f"Board {name}")
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
        # print frame
        self.screencontrol.drawframe()

        self.screencontrol.printname(
            f"{ScreenControl.FG_CYAN + ScreenControl.BRIGHT}"
            + f"{ScreenControl.UNDERLINE_ON}"
            + f"{self.name + ScreenControl.UNDERLINE_OFF}"
        )
        # print 'Moves:'
        self.screencontrol.printmoves()

        # print 'Hits:'
        self.screencontrol.printhits()
        # print columnlabel
        self.screencontrol.printcolumnlabels(self.columns)

        # print rowlabel
        self.screencontrol.printrowlabels(self.rows)

        # print grid
        for x in self.columns:
            for y in self.rows:
                self.screencontrol.showongrid(
                    [x, y],
                    f"{ScreenControl.FG_YELLOW + ScreenControl.BRIGHT}"
                    + f"{ScreenControl.EMPTY}{ScreenControl.RESET_ALL}",
                )
        print(ScreenControl.RESET_ALL)

    def showships(self):
        """
        Shows this boards ships through ScreenControl on the screen.
        """
        for coord in self.ships:
            self.screencontrol.showongrid(coord, ScreenControl.SHIP)
        print(ScreenControl.RESET_ALL)

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
            otherboard.screencontrol.showongrid(guess, ScreenControl.SHELL_HIT)
        else:
            self.screencontrol.printplayermessage(
                f"{self.name} missed at {guess}"
            )
            otherboard.screencontrol.showongrid(guess, ScreenControl.SHELL_MIS)
        self.screencontrol.updatemoves(len(self.moves))
        self.screencontrol.updatehits(self.hits)
        if self.hits == len(otherboard.ships):
            ScreenControl.clearline(24)
            msg = "lose." if self.name.lower() == "computer" else "win."
            ScreenControl.printendgamemessage(
                f"{self.name} has sunk all of {otherboard.name}'s "
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
                    "Input is 2 digits, a letter and a " +
                    f"number - you gave '{playerinput}'"
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
                    "input out of range, " +
                    f"'{playerinput}' is not on the board"
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
    ScreenControl.setupdisplay()
    playerboard = Board(playername, 0)
    compboard = Board("Computer", 40)
    playerboard.setupboard()
    compboard.setupboard()
    playerboard.setupboard()
    playerboard.showships()
    compboard.setupboard()

    while True:
        validcoord = playerboard.makeaguess()
        playerboard.processguess(validcoord, compboard)
        validcoord = compboard.makeaguess()
        compboard.processguess(validcoord, playerboard)


def getplayername():
    """
    ask for player name
    verify its length is > 0
    and less than 15
    """
    maxlength = 15
    ScreenControl.clearscreen()
    while True:
        ScreenControl.pos(2, 2, "Welcome To Battleships")
        ScreenControl.clearline(5)
        ScreenControl.pos(2, 5, "", True)
        name = input("Please enter your name ")
        if len(name) > 0 and len(name) < maxlength:
            break
        else:
            ScreenControl.pos(2, 8, f"You entered an invalid name '{name}'")
            ScreenControl.pos(
                2,
                10,
                "We dont mind which name you use but "
                + "we are short of screenspace, so",
            )
            ScreenControl.pos(
                2,
                12,
                "please use a name less than " + f"{maxlength} characters.",
            )
    return name


def main():
    """
    main method
    catches player name and starts game
    """
    playername = getplayername()
    # playername = "Mark"
    ScreenControl.clearscreen()
    startgame(playername)
    ScreenControl.pos(1, 24, "End")


main()
