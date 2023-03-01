from colorama import just_fix_windows_console

just_fix_windows_console()


class ScreenControl:
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
        self.start_y = start_y
        self.start_x = start_x
