"""
control the display
"""
# import logging


from colorama import just_fix_windows_console

just_fix_windows_console()


# def setup_logger(name, log_file, level=logging.DEBUG):
#     # To setup as many loggers as you want
#     handler = logging.FileHandler(log_file, "w", "utf-8")
#     logger = logging.getLogger(name)
#     logger.setLevel(level)
#     logger.addHandler(handler)
#     return logger


class ScreenControl:
    """
    Controls all display elements
    -   where to put data on display
    -   what color
    """

    # log = setup_logger("log", "bg.log")
    # foreground colors:
    FG_YELLOW = "\x1b[33m"
    FG_CYAN = "\x1b[36m"
    FG_WHITE = "\x1b[37m"

    # background colors
    BG_RED = "\x1b[41m"
    BG_YELLOW = "\x1b[43m"
    BG_BLUE = "\x1b[44m"
    BG_MAGENTA = "\x1b[45m"
    BG_WHITE = "\x1b[47m"

    UNDERLINE_ON = "\033[4m"
    UNDERLINE_OFF = "\033[0m"

    RESET_ALL = "\x1b[0m"  # reset all (colors and brightness)
    BRIGHT = "\x1b[1m"  # bright

    SCREEN_WIDTH = 80

    GRID_START_X = 16
    GRID_START_Y = 2
    GRID_GAP_X = 2
    GRID_GAP_Y = 3

    HIT_Y = 6

    INFO_MESSAGE_Y = 23
    LABEL_DATA_X = 11
    LABEL_START_X = 4
    MOVE_Y = 4
    START_X = 1

    FRAME_COLOUR = BG_BLUE
    SHIP = BG_MAGENTA + BRIGHT + " " + RESET_ALL
    SHELL_HIT = BG_RED + BRIGHT + " " + RESET_ALL
    SHELL_MIS = BG_YELLOW + " " + RESET_ALL
    EMPTY = BG_WHITE + BRIGHT + " " + RESET_ALL

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
        coord is a list e.g. ['3', 'd'] or ['5', 'f']
        first digit needs to be reduced by 1 - index is 0
        second digit is a letter which needs conversion to a number
        let2num converts a to 0, b to 1 etc

        gets a square of 4 squares - as defined by xmoves and ymoves and colors 
        them all
        """
        xval = (
            (self.start_x + ScreenControl.GRID_START_X)
            + (int(coord[0]) * ScreenControl.GRID_GAP_Y)
            - 1
        )
        yval = (
            self.start_y
            + ScreenControl.GRID_START_Y
            + (int(ScreenControl.let2num(coord[1])) * ScreenControl.GRID_GAP_X)
        )
        # create square from coord
        xmoves = [0, 1, 2, 0, 1, 2]
        ymoves = [0, 0, 0, 1, 1, 1]
        for xadd, yadd in zip(xmoves, ymoves):
            ScreenControl.pos(xval + xadd, yval + yadd, text)
        print(ScreenControl.RESET_ALL)

    def printcolumnlabels(self, columnlist):
        """
        position and print the labels for the columns in the players map grid
        """
        column_label_x = 18
        column_label_y = 1

        columnlabel = " ".join([str(i) + " " for i in columnlist])
        ScreenControl.pos(
            self.start_x + column_label_x,
            self.start_y + column_label_y,
            f"{ScreenControl.FG_CYAN + ScreenControl.BRIGHT}{columnlabel}",
        )

    def drawframe(self):
        """
        draw the frame around each player's map
        """
        board_block_bottom_y = 20
        board_block_top_y = 4

        ScreenControl.pos(
            ScreenControl.START_X + self.start_x,
            board_block_top_y,
            f"{ScreenControl.FRAME_COLOUR + ScreenControl.BRIGHT}"
            + " " * int(ScreenControl.SCREEN_WIDTH / 2)
            + ScreenControl.RESET_ALL,
        )
        ScreenControl.pos(
            ScreenControl.START_X + self.start_x,
            board_block_bottom_y,
            f"{ScreenControl.FRAME_COLOUR + ScreenControl.BRIGHT}"
            + " " * int(ScreenControl.SCREEN_WIDTH / 2)
            + ScreenControl.RESET_ALL,
        )
        for xval in range(
            board_block_top_y + 1,
            board_block_bottom_y,
        ):
            ScreenControl.pos(
                ScreenControl.START_X + self.start_x,
                xval,
                f"{ScreenControl.FRAME_COLOUR + ScreenControl.BRIGHT}"
                + f" {ScreenControl.RESET_ALL}",
            )
            ScreenControl.pos(
                ScreenControl.START_X
                + self.start_x
                + int(ScreenControl.SCREEN_WIDTH / 2)
                - 1,
                xval,
                f"{ScreenControl.FRAME_COLOUR + ScreenControl.BRIGHT}"
                + f" {ScreenControl.RESET_ALL}",
            )

    def printrowlabels(self, rowlist):
        """
        position and print the labels for the rows in the players map grid
        """
        row_label_x = 16
        for i in range(len(rowlist)):
            ScreenControl.pos(
                self.start_x + row_label_x,
                self.start_y + ScreenControl.GRID_GAP_X + (i * 2),
                rowlist[i],
            )

    @staticmethod
    def pause(text):
        """
        pause
        """
        ScreenControl.pos(1, 23, text, True)
        input("")

    @staticmethod
    def clearline(yval):
        """
        clear the line on the screen denoted by y
        """
        ScreenControl.pos(1, yval, " " * 80)

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

    def printmoves(self):
        """
        print the moves label under the players name in the correct position
        on the screen
        """
        ScreenControl.pos(
            self.start_x + ScreenControl.LABEL_START_X,
            self.start_y + ScreenControl.MOVE_Y,
            "Moves:",
        )

    def printhits(self):
        """
        print the hits label under the players name in the correct position
        on the screen
        """
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
        game_message_y = 22

        ScreenControl.pos(
            ScreenControl.START_X,
            game_message_y,
            " " * ScreenControl.SCREEN_WIDTH,
        )
        if nolinefeed:
            ScreenControl.pos(
                ScreenControl.START_X,
                game_message_y,
                text,
                True)
        else:
            ScreenControl.pos(ScreenControl.START_X, game_message_y, text)

    def printplayermessage(self, text):
        """
        show hit / miss information for the last guess
        """
        player_message_start_x = 2
        player_message_start_y = 17

        ScreenControl.pos(
            self.start_x + player_message_start_x,
            self.start_y + player_message_start_y,
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
        guess_y = 21
        ScreenControl.pos(
            ScreenControl.START_X, guess_y, "Make a guess: ", True
        )

    @staticmethod
    def setupdisplay():
        """
        setup the common display areas
        -   heading
        -   instructions
        -   the key - explains colors of squares
        """
        ScreenControl.clearscreen()
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
        ScreenControl.printkey()

    @staticmethod
    def printkey():
        """
        prints the key on line 24
        """
        ScreenControl.pos(9, 24, f"ship: {ScreenControl.SHIP}", True)
        ScreenControl.pos(26, 24, f"hit:  {ScreenControl.SHELL_HIT}", True)
        ScreenControl.pos(43, 24, f"miss: {ScreenControl.SHELL_MIS}", True)
        ScreenControl.pos(60, 24, f"????: {ScreenControl.EMPTY}", True)

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
        position text so that its horizontally central in window (80 cols)
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
