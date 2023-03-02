from colorama import just_fix_windows_console

just_fix_windows_console()

class ScreenControl:
    """
    Controls all display elements
    -   where to put data on display
    -   what color
    """
    # foreground:
    fgblack = "\x1b[30m"
    fgred = "\x1b[31m"
    fggreen = "\x1b[32m"
    fgyellow = "\x1b[33m"
    fgblue = "\x1b[34m"
    fgmagenta = "\x1b[35m"
    fgcyan = "\x1b[36m"
    fgwhite = "\x1b[37m"
    fgreset = "\x1b[39m"

    # background
    bgblack = "\x1b[40m"
    bgred = "\x1b[41m"
    bggreen = "\x1b[42m"
    bgyellow = "\x1b[43m"
    bgblue = "\x1b[44m"
    bgmagenta = "\x1b[45m"
    bgcyan = "\x1b[46m"
    bgwhite = "\x1b[47m"
    bgreset = "\x1b[49m"

    underline_on = "\033[4m"
    underline_off = "\033[0m"

    resetall = "\x1b[0m"  # reset all (colors and brightness)
    bright = "\x1b[1m"  # bright
    dim = "\x1b[2m"  # dim (looks same as normal brightness)
    normal = "\x1b[22m"  # normal brightness

    gridgap_x = 2
    gridgap_y = 3

    screenwidth = 80

    start_x = 1
    labelstart_x = 4
    labeldata_x = 11
    columnlabel_x = 18
    gridstart_x = 16
    rowlabel_x = 16
    playermessagestart_x = 2

    boardblocktop_y = 4
    boardblockbottom_y = 20
    move_y = 4
    hit_y = 6
    columnlabel_y = 1
    guess_y = 21
    gridstart_y = 2
    infomessage_y = 23
    gamemessage_y = 22
    playermessage_y = 17

    framecol = bgblue
    ship = bgmagenta + bright + " " + resetall
    shellhit = bgred + bright + " " + resetall
    shellmiss = bgyellow + " " + resetall
    empty = bgwhite + bright + " " + resetall

    def __init__(self, start_y, start_x):
        """
        Constructor
        -   defines start position of the players area
        """
        self.start_y = start_y
        self.start_x = start_x

    gridstart_x = 16
    gridstart_y = 2

    def showongrid(self, coord, text):
        """
        position and print data within the players map grid
        """
        ScreenControl.log.debug(f"coord {coord}")
        x = (
            (self.start_x + ScreenControl.gridstart_x)
            + (int(coord[0]) * ScreenControl.gridgap_y)
            - 1
        )
        y = (
            self.start_y
            + ScreenControl.gridstart_y
            + (int(ScreenControl.let2num(coord[1])) * ScreenControl.gridgap_x)
        )

        ScreenControl.pos(x, y, text)
        ScreenControl.pos(x + 1, y, text)
        ScreenControl.pos(x + 2, y, text)
        ScreenControl.pos(x, y + 1, text)
        ScreenControl.pos(x + 1, y + 1, text)
        ScreenControl.pos(x + 2, y + 1, text)
        print(ScreenControl.resetall)

    columnlabel_x = 18
    columnlabel_y = 1

    def printcolumnlabels(self, columnlist):
        """
        position and print the labels for the columns in the players map grid
        """
        columnlabel = " ".join([str(i) + " " for i in columnlist])
        ScreenControl.pos(
            self.start_x + ScreenControl.columnlabel_x,
            self.start_y + ScreenControl.columnlabel_y,
            f"{ScreenControl.fgcyan + ScreenControl.bright}{columnlabel}",
        )

    rowlabel_x = 16

    def printrowlabels(self, rowlist):
        """
        position and print the labels for the rows in the players map grid
        """
        for i in range(len(rowlist)):
            ScreenControl.pos(
                self.start_x + ScreenControl.rowlabel_x,
                self.start_y + ScreenControl.gridgap_x + (i * 2),
                rowlist[i],
            )

    @staticmethod
    def clearline(y):
        """
        clear the line on the screen denoted by y
        """
        ScreenControl.pos(1, y, " " * 80)

    def printname(self, text):
        """
        print the players name in the correct position on the screen 
        """
        ScreenControl.pos(
            self.start_x + ScreenControl.labelstart_x,
            self.start_y,
            f"{ScreenControl.fgcyan + ScreenControl.bright}"
            + f"{ScreenControl.underline_on}"
            + f"{text + ScreenControl.underline_off}",
        )
        ScreenControl.pos(
            self.start_x + ScreenControl.labelstart_x,
            self.start_y + ScreenControl.move_y,
            "Moves:",
        )
        ScreenControl.pos(
            self.start_x + ScreenControl.labelstart_x,
            self.start_y + ScreenControl.hit_y,
            "Hits:",
        )


    labeldata_x = 11

    def updatemoves(self, text):
        """
        update the number of moves on the screen 
        """
        ScreenControl.pos(
            self.start_x + ScreenControl.labeldata_x,
            self.start_y + ScreenControl.move_y,
            text,
        )


    def updatehits(self, text):
        """
        update the number of hits on the screen 
        """
        ScreenControl.pos(
            self.start_x + ScreenControl.labeldata_x,
            self.start_y + ScreenControl.hit_y,
            text,
        )



    @staticmethod
    def printinfomessage(text):
        """
        show error messages from invalid guesses
        """
        ScreenControl.clearinfomessage()
        ScreenControl.pos(
            ScreenControl.start_x, ScreenControl.infomessage_y, text
        )

    infomessage_y = 23

    @staticmethod
    def clearinfomessage():
        """
        remove the error message from the screen
        """
        ScreenControl.pos(
            ScreenControl.start_x,
            ScreenControl.infomessage_y,
            " " * ScreenControl.screenwidth,
        )


    gamemessage_y = 22

    @staticmethod
    def printendgamemessage(text, *nolinefeed):
        """
        print the end of game message
        """
        ScreenControl.pos(
            ScreenControl.start_x,
            ScreenControl.gamemessage_y,
            " " * ScreenControl.screenwidth,
        )
        if nolinefeed:
            ScreenControl.pos(
                ScreenControl.start_x, ScreenControl.gamemessage_y, text, True
            )
        else:
            ScreenControl.pos(
                ScreenControl.start_x, ScreenControl.gamemessage_y, text
            )

    playermessage_y = 17

    def printplayermessage(self, text):
        """
        show hit / miss information for the last guess
        """
        ScreenControl.pos(
            self.start_x + ScreenControl.playermessagestart_x,
            self.start_y + ScreenControl.playermessage_y,
            text,
            True,
        )


    def clearplayermessage(self):
        """
        clear hit / miss information
        """
        print("clearplayermessage 225")

    guess_y = 21

    @staticmethod
    def makeaguess():
        """
        position cursor and get guess for player
        """
        ScreenControl.pos(
            ScreenControl.start_x, ScreenControl.guess_y, "Make a guess: ", True
        )

    @staticmethod
    def setupdisplay():
        """
        setup the commom display areas
        -   heading
        -   instructions
        -   error messages
        -   frame
        """
        ScreenControl.clearscreen()
        ScreenControl.pos(
            ScreenControl.start_x,
            ScreenControl.boardblocktop_y,
            f"{ScreenControl.framecol + ScreenControl.bright}"
            + " " * ScreenControl.screenwidth
            + ScreenControl.resetall,
        )
        ScreenControl.pos(
            ScreenControl.start_x,
            ScreenControl.boardblockbottom_y,
            f"{ScreenControl.framecol + ScreenControl.bright}"
            + " " * ScreenControl.screenwidth
            + ScreenControl.resetall,
        )
        for x in range(
            ScreenControl.boardblocktop_y + 1, ScreenControl.boardblockbottom_y
        ):
            ScreenControl.pos(
                int(ScreenControl.screenwidth / 2),
                x,
                f"{ScreenControl.framecol + ScreenControl.bright}"
                + f" {ScreenControl.resetall}",
            )
            ScreenControl.pos(
                ScreenControl.start_x,
                x,
                f"{ScreenControl.framecol + ScreenControl.bright}"
                + f" {ScreenControl.resetall}",
            )
            ScreenControl.pos(
                ScreenControl.screenwidth,
                x,
                f"{ScreenControl.framecol + ScreenControl.bright}"
                + f" {ScreenControl.resetall}",
            )

        ScreenControl.center(
            1,
            f"{ScreenControl.fgwhite + ScreenControl.bright}"
            + f"{ScreenControl.underline_on + 'Welcome to Battleships'}"
            + f"{ScreenControl.underline_off}",
        )
        ScreenControl.center(
            2,
            "You have 5 ships, as does the computer, "
            + "Columns are 1 to 6, rows are a to f.",
        )
        ScreenControl.center(
            3, "You can pick a square " + "in either order - eg 'a5' or '3c'"
        )
        ScreenControl.pos(1, 24, f"ship: {ScreenControl.ship}", True)
        ScreenControl.pos(21, 24, f"hit:  {ScreenControl.shellhit}", True)
        ScreenControl.pos(41, 24, f"miss: {ScreenControl.shellmiss}", True)
        ScreenControl.pos(61, 24, f"????: {ScreenControl.empty}", True)


    @staticmethod
    def pos(x, y, text, *nolinefeed):
        """
        Postions text on the display
        x - horizontal co-ord starts at 1 in top left corner
        y - vertical co-ord starts at 1 in top left corner

        move to x,y and print text
        set nolinefeed to true for subsequest input statement
        """
        if nolinefeed:
            print(f"\x1b[{y};{x}H{text}", end="")
        else:
            print(f"\x1b[{y};{x}H{text}")


    @staticmethod
    def clearscreen():
        """
        Clears the screen
        """
        print("\x1b[2J")


    @staticmethod
    def center(row, text):
        """
        position text so that its central in window (80 cols)
        """
        xpos = int((80 - len(text)) / 2)
        ScreenControl.pos(xpos, row, text)

    @staticmethod
    def let2num(let):
        """
        Converts letters to numbers
        -   ascii code of str(number) - 49
        -   'b' is ascii '98' will be converted to '1' ascii '49'
        """
        return chr(ord(str(let)) - 49)


