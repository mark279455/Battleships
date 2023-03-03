from colorama import just_fix_windows_console

just_fix_windows_console()


class ScreenControl:
    """
    Controls all display elements
    -   where to put data on display
    -   what color
    """
    # foreground:
    BG_BLACK = "\x1b[30m"
    FG_RED = "\x1b[31m"
    FG_GREEN = "\x1b[32m"
    FG_YELLOW = "\x1b[33m"
    FG_BLUE = "\x1b[34m"
    FG_MAGENTA = "\x1b[35m"
    FG_CYAN = "\x1b[36m"
    FG_WHITE = "\x1b[37m"
    FG_RESET = "\x1b[39m"

    # background
    BG_BLACK = "\x1b[40m"
    BG_RED = "\x1b[41m"
    BG_GREEN = "\x1b[42m"
    BG_YELLOW = "\x1b[43m"
    BG_BLUE = "\x1b[44m"
    BG_MAGENTA = "\x1b[45m"
    BG_CYAN = "\x1b[46m"
    BG_WHITE = "\x1b[47m"
    BG_RESET = "\x1b[49m"

    UNDERLINE_ON = "\033[4m"
    UNDERLINE_OFF = "\033[0m"

    RESET_ALL = "\x1b[0m"  # reset all (colors and brightness)
    BRIGHT = "\x1b[1m"  # bright
    DIM = "\x1b[2m"  # dim (looks same as normal brightness)
    NORMAL = "\x1b[22m"  # normal brightness

    BOARD_BLOCK_BOTTOM_Y = 20
    BOARD_BLOCK_TOP_Y = 4

    COLUMN_LABEL_X = 18
    COLUMN_LABEL_Y = 1

    GAME_MESSAGE_Y = 22

    GRID_GAP_X = 2
    GRID_GAP_Y = 3

    GRID_START_X = 16
    GRID_START_Y = 2

    GUESS_Y = 21
    HIT_Y = 6
    INFO_MESSAGE_Y = 23
    LABEL_DATA_X = 11
    LABEL_START_X = 4
    MOVE_Y = 4
    PLAYER_MESSAGE_START_X = 2
    PLAYER_MESSAGE_Y = 17
    ROW_LABEL_X = 16
    SCREEN_WIDTH = 80
    START_X = 1


    framecol = BG_BLUE
    ship = BG_MAGENTA + BRIGHT + " " + RESET_ALL
    shellhit = BG_RED + BRIGHT + " " + RESET_ALL
    shellmiss = BG_YELLOW + " " + RESET_ALL
    empty = BG_WHITE + BRIGHT + " " + RESET_ALL

    def __init__(self, start_y, start_x):
        """
        Constructor
        -   defines start position of the players area
        """
        self.start_y = start_y
        self.start_x = start_x

    def showongrid(self, coord, text):
        """
        position and print data within the players map grid
        """
        x = (
            (self.start_x + ScreenControl.GRID_START_X)
            + (int(coord[0]) * ScreenControl.GRID_GAP_Y)
            - 1
        )
        y = (
            self.start_y
            + ScreenControl.GRID_START_Y
            + (int(ScreenControl.let2num(coord[1])) * ScreenControl.GRID_GAP_X)
        )

        ScreenControl.pos(x, y, text)
        ScreenControl.pos(x + 1, y, text)
        ScreenControl.pos(x + 2, y, text)
        ScreenControl.pos(x, y + 1, text)
        ScreenControl.pos(x + 1, y + 1, text)
        ScreenControl.pos(x + 2, y + 1, text)
        print(ScreenControl.RESET_ALL)

    def printcolumnlabels(self, columnlist):
        """
        position and print the labels for the columns in the players map grid
        """
        columnlabel = " ".join([str(i) + " " for i in columnlist])
        ScreenControl.pos(
            self.start_x + ScreenControl.COLUMN_LABEL_X,
            self.start_y + ScreenControl.COLUMN_LABEL_Y,
            f"{ScreenControl.FG_CYAN + ScreenControl.BRIGHT}{columnlabel}",
        )

    def printrowlabels(self, rowlist):
        """
        position and print the labels for the rows in the players map grid
        """
        for i in range(len(rowlist)):
            ScreenControl.pos(
                self.start_x + ScreenControl.ROW_LABEL_X,
                self.start_y + ScreenControl.GRID_GAP_X + (i * 2),
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
            self.start_x + ScreenControl.LABEL_START_X,
            self.start_y,
            f"{ScreenControl.FG_CYAN + ScreenControl.BRIGHT}"
            + f"{ScreenControl.UNDERLINE_ON}"
            + f"{text + ScreenControl.UNDERLINE_OFF}",
        )
        ScreenControl.pos(
            self.start_x + ScreenControl.LABEL_START_X,
            self.start_y + ScreenControl.MOVE_Y,
            "Moves:",
        )
        ScreenControl.pos(
            self.start_x + ScreenControl.LABEL_START_X,
            self.start_y + ScreenControl.HIT_Y,
            "Hits:",
        )

    def updatemoves(self, text):
        """
        update the number of moves on the screen
        """
        ScreenControl.pos(
            self.start_x + ScreenControl.LABEL_DATA_X,
            self.start_y + ScreenControl.MOVE_Y,
            text,
        )

    def updatehits(self, text):
        """
        update the number of hits on the screen
        """
        ScreenControl.pos(
            self.start_x + ScreenControl.LABEL_DATA_X,
            self.start_y + ScreenControl.HIT_Y,
            text,
        )

    @staticmethod
    def printinfomessage(text):
        """
        show error messages from invalid guesses
        """
        ScreenControl.clearinfomessage()
        ScreenControl.pos(
            ScreenControl.START_X, ScreenControl.INFO_MESSAGE_Y, text
        )

    @staticmethod
    def clearinfomessage():
        """
        remove the error message from the screen
        """
        ScreenControl.pos(
            ScreenControl.START_X,
            ScreenControl.INFO_MESSAGE_Y,
            " " * ScreenControl.SCREEN_WIDTH,
        )

    @staticmethod
    def printendgamemessage(text, *nolinefeed):
        """
        print the end of game message
        """
        ScreenControl.pos(
            ScreenControl.START_X,
            ScreenControl.GAME_MESSAGE_Y,
            " " * ScreenControl.SCREEN_WIDTH,
        )
        if nolinefeed:
            ScreenControl.pos(
                ScreenControl.START_X, ScreenControl.GAME_MESSAGE_Y, text, True
            )
        else:
            ScreenControl.pos(
                ScreenControl.START_X, ScreenControl.GAME_MESSAGE_Y, text
            )

    def printplayermessage(self, text):
        """
        show hit / miss information for the last guess
        """
        ScreenControl.pos(
            self.start_x + ScreenControl.PLAYER_MESSAGE_START_X,
            self.start_y + ScreenControl.PLAYER_MESSAGE_Y,
            text,
            True,
        )

    def clearplayermessage(self):
        """
        clear hit / miss information
        """
        print("clearplayermessage 225")

    @staticmethod
    def makeaguess():
        """
        position cursor and get guess for player
        """
        ScreenControl.pos(
            ScreenControl.START_X, ScreenControl.GUESS_Y,
            "Make a guess: ", True
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
            ScreenControl.START_X,
            ScreenControl.BOARD_BLOCK_TOP_Y,
            f"{ScreenControl.framecol + ScreenControl.BRIGHT}"
            + " " * ScreenControl.SCREEN_WIDTH
            + ScreenControl.RESET_ALL,
        )
        ScreenControl.pos(
            ScreenControl.START_X,
            ScreenControl.BOARD_BLOCK_BOTTOM_Y,
            f"{ScreenControl.framecol + ScreenControl.BRIGHT}"
            + " " * ScreenControl.SCREEN_WIDTH
            + ScreenControl.RESET_ALL,
        )
        for x in range(
            ScreenControl.BOARD_BLOCK_TOP_Y + 1, ScreenControl.BOARD_BLOCK_BOTTOM_Y
        ):
            ScreenControl.pos(
                int(ScreenControl.SCREEN_WIDTH / 2),
                x,
                f"{ScreenControl.framecol + ScreenControl.BRIGHT}"
                + f" {ScreenControl.RESET_ALL}",
            )
            ScreenControl.pos(
                ScreenControl.START_X,
                x,
                f"{ScreenControl.framecol + ScreenControl.BRIGHT}"
                + f" {ScreenControl.RESET_ALL}",
            )
            ScreenControl.pos(
                ScreenControl.SCREEN_WIDTH,
                x,
                f"{ScreenControl.framecol + ScreenControl.BRIGHT}"
                + f" {ScreenControl.RESET_ALL}",
            )

        ScreenControl.center(
            1,
            f"{ScreenControl.FG_WHITE + ScreenControl.BRIGHT}"
            + f"{ScreenControl.UNDERLINE_ON + 'Welcome to Battleships'}"
            + f"{ScreenControl.UNDERLINE_OFF}",
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
    def pos(x_coord, y_coord, text, *nolinefeed):
        """
        Postions text on the display
        x - horizontal co-ord starts at 1 in top left corner
        y - vertical co-ord starts at 1 in top left corner

        move to x,y and print text
        set nolinefeed to true for subsequest input statement
        """
        if nolinefeed:
            print(f"\x1b[{y_coord};{x_coord}H{text}", end="")
        else:
            print(f"\x1b[{y_coord};{x_coord}H{text}")

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
