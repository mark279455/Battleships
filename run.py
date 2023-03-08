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
        self.name = name
        self.screencontrol = ScreenControl(5, start_x, self.name)
        self.hits = 0
        self.ships = []
        self.moves = []
        self.columns = [str(i) for i in range(1, self.size + 1)]
        self.rows = [Board.num2let(i) for i in range(Board.size)]

        ScreenControl.log.debug(f"self.columns = {self.columns}")
        ScreenControl.log.debug(f"self.rows    = {self.rows}")

        while len(self.ships) < Board.num_ships:
            aval = random.choice(self.columns)
            bval = random.choice(self.rows)
            if [aval, bval] not in self.ships:
                self.ships.append([aval, bval])

    def setupboard(self):
        """
        Shows board details for this board through ScreenControl on the screen

        the blue frame
        the Board owners name
        the word 'Moves:'
        the word 'Hits:'
        column labels for the map grid (1 to 6)
        row labels for the map grid (a to f)
        """
        self.screencontrol.drawframe()

        # print name
        self.screencontrol.printname(
            f"{ScreenControl.FG_CYAN + ScreenControl.BRIGHT}"
            + f"{ScreenControl.UNDERLINE_ON}"
            + f"{self.name + ScreenControl.UNDERLINE_OFF}"
        )

        # print 'Moves:'
        self.screencontrol.printmoves()

        # print 'Hits:'
        self.screencontrol.printhits()

        # print columnlabel - 1 to 6 over map grid
        self.screencontrol.printcolumnlabels(self.columns)

        # print rowlabel - a to f beside map grid
        self.screencontrol.printrowlabels(self.rows)

        # print map grid
        for xval in self.columns:
            for yval in self.rows:
                self.screencontrol.showongrid(
                    [xval, yval],
                    f"{ScreenControl.FG_YELLOW + ScreenControl.BRIGHT}"
                    + f"{ScreenControl.EMPTY}{ScreenControl.RESET_ALL}",
                )
        print(ScreenControl.RESET_ALL)

    def showships(self):
        """
        Shows this boards ships (self) through ScreenControl on the screen.
        no return value
        """
        for coord in self.ships:
            self.screencontrol.showongrid(coord, ScreenControl.SHIP)
        print(ScreenControl.RESET_ALL)

    def makeaguess(self):
        """
        Takes the players guess through ScreenControl on the screen.
        :return:
        returns validated input from user in form of ['letter', 'number']
        """
        validcoord = []
        if self.name.lower().startswith("comp"):
            return self.makerandomguess()
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
        - updates both players displays
        - detects game over and returns False if it is

        :param guess:
            the target coordinate of the guess
        :param otherboard:
            the other board - to check its ships' locations
        :return:
            returns false if game is over - all otherboards ships sunk
            else true
        """
        self.moves.append(guess)
        ScreenControl.log.debug(f"self.moves = {self.moves}")
        if guess in otherboard.ships:
            self.hits += 1
            self.screencontrol.printplayermessage(
                f"{self.name} hit a ship at {guess}"
            )
            # ScreenControl.pos(1, 24, f"hit: {guess}")
            otherboard.screencontrol.showongrid(guess, ScreenControl.SHELL_HIT)
        else:
            self.screencontrol.printplayermessage(
                f"{self.name} missed at {guess}"
            )
            # ScreenControl.pos(1, 24, f"miss: {guess}")
            otherboard.screencontrol.showongrid(guess, ScreenControl.SHELL_MIS)
        self.screencontrol.updatemoves(len(self.moves))
        self.screencontrol.updatehits(self.hits)
        if self.hits == len(otherboard.ships):
            return False
        return True

    def makerandomguess(self):
        """
        Generates a random guess for the computer

        :return:
            returns guess if its not in self.moves - i.e. been already targeted
        """
        resultlist = []
        while True:
            xval = random.choice(self.columns)
            yval = random.choice(self.rows)
            resultlist = [xval, yval]
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

        :param playerinput:
            typed input from the player
        :return:
            returns a succesfully verified list e.g. ['4', 'd']
            or false if unverified
        """
        # resultlist = []
        playerinput = playerinput.strip().lower()
        try:
            if Board.validatelength2(playerinput):
                resultlist = self.validateinputasletnum(playerinput)
                if resultlist:
                    self.validateinputasalready(resultlist)
                    return resultlist
        except ValueError as error:
            # ScreenControl.printinfomessage(f"{error}, please try again")
            ScreenControl.printinfomessage(f"{error}, please try again")
        return False

    @staticmethod
    def validatelength2(inputdata):
        """
        called from validateinput with the players guess as a string
        :param inputdata:
            the players guess - could be anything at this point
        :return:
            returns true is length = 2
            otherwise throws valueerror
        """
        if len(inputdata) != 2:
            raise ValueError(
                "Input is 2 digits, a letter and a "
                + f"number - you gave '{inputdata}'"
            )
        else:
            return True

    def validateinputasletnum(self, inputdata):
        """
        called from validateinput with the players guess as a string
        uses regex to test if its within the map grid.
        :param inputdata:
        the players guess - is 2 chars at this point
        :return:
            returns the successfully validated result in the form ['4', 'd']
            or throws valueerror
        """
        searchletters = "".join([str(i) for i in self.columns])
        searchnumbers = "".join([str(i) for i in self.rows])
        letnum = re.search(
            "^[" + searchletters + "][" + searchnumbers + "]$",
            inputdata,
        )
        numlet = re.search(
            "^[" + searchnumbers + "][" + searchletters + "]$",
            inputdata,
        )
        if letnum is not None:
            resultlist = [inputdata[0], inputdata[1]]
        elif numlet is not None:
            resultlist = [inputdata[::-1][0], inputdata[::-1][1]]
        else:
            raise ValueError(
                "Input out of range, " + f"'{inputdata}' is not on the board"
            )
        return resultlist

    def validateinputasalready(self, inputdata):
        """
        validates if the inputdata list is an already targeted coordinate
        :param inputdata:
        the coordinate in question
        :return:
        returns inputdata if validated
        value error if previously targeted
        """
        if inputdata in self.moves:
            raise ValueError(
                "Coordinate "
                + f"{inputdata[0] + inputdata[1]} has already been targeted"
            )
        else:
            ScreenControl.clearinfomessage()
            return inputdata

    @staticmethod
    def num2let(num):
        """
        Converts numbers to letters
        -   ascii code of str(number) + 49
        -   '0' is ascii '48' will be converted to 'a' ascii '97'
        format:
            input - one of   ['0', '1', '2', '3', '4', '5']
            output  - one of ['a', 'b', 'c', 'd', 'e', 'f']
        :param num:
        any digit - only 1 digit used here
        :return:
        returns the corresponding letter
        """
        return chr(ord(str(num)) + 49)

    def gameover(self, otherboard):
        """
        End of game

        :param otherboard:
            to populate the string
        :return: nothing returned
        either quits
        or restarts game
        """
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


def startgame(playername):
    """
    creates boards for player and computer
    sets up display
    shows player and computers boards on display

    :param playername:
    so that the player name appears in the game
    the computer is always "Computer"
    :return:
    nothing returned - game will be restarted or quit
    """
    ScreenControl.setupdisplay()
    playerboard = Board(playername, 0)
    compboard = Board("Computer", 40)
    playerboard.setupboard()
    compboard.setupboard()
    playerboard.showships()
    compboard.showships()

    while True:
        validcoord = playerboard.makeaguess()
        if not playerboard.processguess(validcoord, compboard):
            playerboard.gameover(compboard)
        validcoord = compboard.makeaguess()
        if not compboard.processguess(validcoord, playerboard):
            compboard.gameover(playerboard)


def getplayername():
    """
    ask for player name
    verify its length is > 0
    and less than 15
    :return:
    the players inputted name
    """
    maxlength = 15
    ScreenControl.clearscreen()
    while True:
        ScreenControl.pos(2, 2, "Welcome To Battleships")
        ScreenControl.clearline(5)
        ScreenControl.pos(2, 5, "", True)
        name = input("Please enter your name ")
        if 0 < len(name) < maxlength:
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

    ScreenControl.clearscreen()
    startgame(playername)
    ScreenControl.pos(1, 24, "End")


main()
