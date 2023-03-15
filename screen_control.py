from colorama import just_fix_windows_console
just_fix_windows_console()


class ScreenControl:
    """
        Controls all display elements
    -   where to put data on display
    -   what color
    """

    # foreground colors:
    FG_YELLOW = "\x1b[33m"
    FG_CYAN = "\x1b[36m"
    FG_WHITE = "\x1b[37m"
    FG_RED = "\x1b[31m"
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
    GRID_GAP_X = 2
    GRID_GAP_Y = 3
    INFO_MESSAGE_Y = 23
    START_X = 1

    SHIP = BG_MAGENTA + BRIGHT + " " + RESET_ALL
    SHELL_HIT = BG_RED + BRIGHT + " " + RESET_ALL
    SHELL_MIS = BG_YELLOW + " " + RESET_ALL
    EMPTY = BG_WHITE + BRIGHT + " " + RESET_ALL

    def __init__(self, start_y, start_x, name):
        """
        Constructor
        -   defines start position of the players area

        :param start_y:
        start vertical position for the instances game
        :param start_x:
        start horizontal position for the instances game
         :param name:   name of player or "Computer"
        """
        self.name = name
        self.start_y = start_y
        self.start_x = start_x

    def showongrid(self, coord, text):
        """
        position and print data within the players map grid
        first digit needs to be reduced by 1 - index is 0
        second digit is a letter which needs conversion to a number
        let2num converts a to 0, b to 1 etc

        gets a square of 4 squares - as defined by xmoves and ymoves and colors
        them all
        """
        grid_start_x = 16
        grid_start_y = 2
        xval = (
            (self.start_x + grid_start_x)
            + (int(coord[0]) * ScreenControl.GRID_GAP_Y)
            - 1
        )
        yval = (
            self.start_y
            + grid_start_y
            + (int(ScreenControl.let2num(coord[1])) * ScreenControl.GRID_GAP_X)
        )

        xmoves = [0, 1, 2, 0, 1, 2]
        ymoves = [0, 0, 0, 1, 1, 1]
        for xadd, yadd in zip(xmoves, ymoves):
            ScreenControl.pos(xval + xadd, yval + yadd, text)
        print(ScreenControl.RESET_ALL)

    def printrowlabels(self, rowlist):
        """
        position and print the labels for the rows in the players map grid
        these are printed down the screen so multiple calls to pos() are
        required
        :param rowlist:     the Board objects list of row names
                ['a', 'b', 'c', 'd', 'e', 'f']
        :return:    nothing
        """
        row_label_x = 16
        for i in range(len(rowlist)):
            ScreenControl.pos(
                self.start_x + row_label_x,
                self.start_y + ScreenControl.GRID_GAP_X + (i * 2),
                rowlist[i],
            )

    def printcolumnlabels(self, columnlist):
        """
        position and print the labels for the columns in the players map grid
        :param columnlist:        the Board objects list of column names
                ['1', '2', '3', '4', '5', '6']
        :return:    nothing
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
        :return:        nothing
        """
        frame_color = ScreenControl.BG_BLUE
        frame_bottom_y = 20
        frame_top_y = 4

        ScreenControl.pos(
            ScreenControl.START_X + self.start_x,
            frame_top_y,
            f"{frame_color + ScreenControl.BRIGHT}"
            + " " * int(ScreenControl.SCREEN_WIDTH / 2)
            + ScreenControl.RESET_ALL,
        )
        ScreenControl.pos(
            ScreenControl.START_X + self.start_x,
            frame_bottom_y,
            f"{frame_color + ScreenControl.BRIGHT}"
            + " " * int(ScreenControl.SCREEN_WIDTH / 2)
            + ScreenControl.RESET_ALL,
        )
        for yval in range(
            frame_top_y + 1,
            frame_bottom_y,
        ):
            ScreenControl.pos(
                ScreenControl.START_X + self.start_x,
                yval,
                f"{frame_color + ScreenControl.BRIGHT}"
                + f" {ScreenControl.RESET_ALL}",
            )
            ScreenControl.pos(
                ScreenControl.START_X
                + self.start_x
                + int(ScreenControl.SCREEN_WIDTH / 2)
                - 1,
                yval,
                f"{frame_color + ScreenControl.BRIGHT}"
                + f" {ScreenControl.RESET_ALL}",
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
        :param yval:    the number of the line to be cleared
        :return:        nothing
        """
        ScreenControl.pos(1, yval, " " * 80)

    def printname(self, text):
        """
        print the players name in the correct position on the screen
        :param text:    the players / computers name amd
                        its color formatting codes
        :return:    nothing
        """
        name_start_x = 4
        ScreenControl.pos(
            self.start_x + name_start_x,
            self.start_y,
            f"{ScreenControl.FG_CYAN + ScreenControl.BRIGHT}"
            + f"{ScreenControl.UNDERLINE_ON}"
            + f"{text + ScreenControl.UNDERLINE_OFF}",
        )

    def printmoves(self):
        """
        print the moves label under the players name in the correct position
            on the screen
        :return:        nothing
        """
        moves_start_x = 4
        moves_start_y = 4
        ScreenControl.pos(
            self.start_x + moves_start_x,
            self.start_y + moves_start_y,
            "Moves:",
        )

    def printhits(self):
        """
        print the hits label under the players name in the correct position
        on the screen
        :return:        nothing
        """
        hits_start_x = 4
        hits_start_y = 6
        ScreenControl.pos(
            self.start_x + hits_start_x,
            self.start_y + hits_start_y,
            "Hits:",
        )

    def updatemoves(self, text):
        """
        update the number of moves on the screen
        :param text:        the number to update moves to
        :return:        nothing
        """
        move_data_x = 11
        move_data_y = 4
        ScreenControl.pos(
            self.start_x + move_data_x,
            self.start_y + move_data_y,
            text,
        )

    def updatehits(self, text):
        """
        update the number of hits on the screen
        :param text:        the number to update hits to
        :return:        nothing
        """
        hits_data_x = 11
        hits_data_y = 6
        ScreenControl.pos(
            self.start_x + hits_data_x,
            self.start_y + hits_data_y,
            text,
        )

    @staticmethod
    def printinfomessage(text):
        """
        show error messages from invalid guesses
        :param text:        the error message
        :return:        nothing
        """
        ScreenControl.clearinfomessage()
        ScreenControl.pos(
            ScreenControl.START_X, ScreenControl.INFO_MESSAGE_Y, text
        )

    @staticmethod
    def clearinfomessage():
        """
        remove the error message from the screen
        :return:        nothing
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
                True
                )
        else:
            ScreenControl.pos(ScreenControl.START_X, game_message_y, text)

    def printplayermessage(self, text):
        """
        show hit / miss information for the last guess
        :param text:        the information
        :return:        nothing
        """
        self.clearplayermessage()
        player_message_start_x = 2
        player_message_start_y = 17
        ScreenControl.pos(
            self.start_x + player_message_start_x,
            self.start_y + player_message_start_y,
            text,
        )

    def clearplayermessage(self):
        """
        clear the show hit / miss information for the last guess
        :param text:    nothing
        :return:        nothing
        """
        player_message_start_x = 2
        player_message_start_y = 17
        ScreenControl.pos(
            self.start_x + player_message_start_x,
            self.start_y + player_message_start_y,
            " " * 38,
        )

    @staticmethod
    def makeaguess():
        """
        position cursor and get guess for player
        :return:        nothing
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
        :return:        nothing
        """
        ScreenControl.clearscreen()
        ScreenControl.center(
            1,
            f"{ScreenControl.FG_WHITE + ScreenControl.BRIGHT}"
            + f"{ScreenControl.UNDERLINE_ON + 'Welcome to Battleships'}"
            + f"{ScreenControl.UNDERLINE_OFF}"
        )
        ScreenControl.center(
            2,
            "Forces: 3 subs - 2 sq: 1 cruiser - 3 sq: 1 battleship - 4 sq"
        )
        ScreenControl.center(
            3, "You can pick a square " + "in either order - eg 'a5' or '3c'"
        )
        ScreenControl.printkey()

    @staticmethod
    def printkey():
        """
        prints the key on line 24
        :return:        nothing
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

        :param x_coord:     horizontal coordinate
        :param y_coord:     vertical coordinate
        :param text:        text to be printed
        :param nolinefeed:  optional - for input statements
        :return:            nothing
        """
        if nolinefeed:
            print(f"\x1b[{y_coord};{x_coord}H{text}", end="")
        else:
            print(f"\x1b[{y_coord};{x_coord}H{text}")

    @staticmethod
    def clearscreen():
        """
        Clears the screen
        :return:        nothing
        """
        print("\x1b[2J")

    @staticmethod
    def center(row, text):
        """
        position text so that its horizontally central in window (80 cols)
        :param row:     line to center on
        :param text:    text to center
        :return:        nothing
        """
        xpos = int((80 - len(text)) / 2)
        ScreenControl.pos(xpos, row, text)

    @staticmethod
    def let2num(let):
        """
        Converts letters to numbers
        -   ascii code of str(number) - 49
        -   'b' is ascii '98' will be converted to '1' ascii '49'
        format:
            input - one of   ['a', 'b', 'c', 'd', 'e', 'f']
            output  - one of ['0', '1', '2', '3', '4', '5']

        :param let:     any letter (English alphabet) - only 1 char used here
        :return:        returns the corresponding number as string
        """
        return chr(ord(str(let)) - 49)
