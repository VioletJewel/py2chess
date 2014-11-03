#! /usr/bin/env python
# -*- coding: latin-1 -*-

__author__ = "Violet"


# IMPORTS
from os import system as term
from os.path import expanduser as expu, isdir, isfile
from random import random
from struct import pack, unpack
from sys import argv, exit, stdin, stdout
from time import sleep

try:
    from termios import tcgetattr as getat, tcsetattr as setat, TCSADRAIN
    from tty import setraw
except ImportError:
    print "This game only works on Unix operating systems"
    exit(1)


def main():
    g = game()
    g.newGame()


# GAME CLASS
class game:
    
    def __init__(self):
        """
        
        """
        self.fd = stdin.fileno()
        self.old_settings = getat(self.fd)
        self.buffer = 4
    
    
    def selectColor(self, desc = "", typ = "3", cInd = 7):
        """
            Allows user to easily select a color.
            
            Arguments:
                typ| 3: foreground
                   | 4: background
        """
        rec = (typ, cInd)
        colorMap = dict()
        darkColors = list()
        colors = list()
        lightColors = list()
        for i, color in enumerate(("black", "red", "green", "yellow", "blue", "purple", "cyan", "white")):
            darkColors.append("dark {}".format(color))
            colors.append(color)
            lightColors.append("light {}".format(color))
            colorMap["dark {}".format(color)] = "{};2".format(i)
            colorMap[color] = "{}".format(i)
            colorMap["light {}".format(color)] = "{};1".format(i)
        
        keys = bytearray([0, 0, 0, 0])
        ch = None
        if typ == "4":
            shade = 2
        else:
            typ = "3"
            shade = 0
        print "\x1b[0;0H\x1b[J{}\n".format(desc)
        while ch != 13:
            if shade == 0:
                print "\x1b[7;0H\x1b[2K\x1b[3{}m{}\x1b[m{}".format(colorMap[lightColors[cInd]], lightColors[cInd], " (recommended)" if (rec[0] == "3" and rec[1] == cInd) else "")
            elif shade == 1:
                print "\x1b[7;0H\x1b[2K\x1b[3{}m{}\x1b[m".format(colorMap[colors[cInd]], colors[cInd])
            else:
                print "\x1b[7;0H\x1b[2K\x1b[3{}m{}\x1b[m{}".format(colorMap[darkColors[cInd]], darkColors[cInd], " (recommended)" if (rec[0] == "4" and rec[1] == cInd) else "")
            
            # wait for user input
            setraw(self.fd)
            keys.insert(0,stdin.read(1))
            setat(self.fd, TCSADRAIN, self.old_settings)
            keys = keys[:self.buffer]
            
            # use input
            if keys[0] == 104 or keys[2] == 27 and keys[1] == 91 and keys[0] == 68: # 'h' or '[left]'
                if shade > 0:
                    shade -= 1
                else:
                    shade = 2
            elif keys[0] == 106 or keys[2] == 27 and keys[1] == 91 and keys[0] == 66: # 'j' or '[down]'
                if cInd == 7:
                    cInd = 0
                else:
                    cInd += 1
            elif keys[0] == 107 or keys[2] == 27 and keys[1] == 91 and keys[0] == 65: # 'k' or '[up]'
                if cInd == 0:
                    cInd = 7
                else:
                    cInd -= 1
            elif keys[0] == 108 or keys[2] == 27 and keys[1] == 91 and keys[0] == 67: # 'l' or '[right]'
                if shade < 2:
                    shade += 1
                else:
                    shade = 0
            elif keys[0] == 13: # '[Enter]'
                c = "{}{}".format(cInd, ";1" if shade == 0 else ";2" if shade == 2 else "")
                #try: raw_input("\nYou have self.selected \x1b[3{}m{}\x1b[m OK! ([Enter] to continue)".format(c, colors[cInd]))
                #except (KeyboardInterrupt, SystemExit): pass
                if shade == 0:
                    return "{};1".format(cInd)
                elif shade == 2:
                    return "{};2".format(cInd)
                else:
                    return str(cInd)
            elif keys[0] == 3 or keys[0] == 4: # 'ctrl+c' or 'ctrl+d'
                exit(0)
    
    
    def menu(self, options, msg = "What would you like to do?"):
        """
        
        """
        stdout.write("\x1b[0;0H\x1b[J")
        keys = bytearray([0, 0, 0, 0])
        line = 0
        while keys[0] != 13:
            print "\x1b[0;0H{}\n".format(msg)
            for i in range(len(options)):
                print "\x1b[34;1m{}. {}{}\x1b[m".format(i + 1, "\x1b[7m" if i == line else "", options[i])
            
            # wait for user input
            setraw(self.fd)
            keys.insert(0,stdin.read(1))
            setat(self.fd, TCSADRAIN, self.old_settings)
            keys = keys[:self.buffer]
            
            # use input
            if keys[0] == 106 or keys[2] == 27 and keys[1] == 91 and keys[0] == 66: # 'j' or '[down]'
                if line == len(options) - 1:
                    line = 0
                else:
                    line += 1
            elif keys[0] == 107 or keys[2] == 27 and keys[1] == 91 and keys[0] == 65: # 'k' or '[up]'
                if line == 0:
                    line = len(options) - 1
                else:
                    line -= 1
            elif keys[0] == 3 or keys[0] == 4: # 'ctrl+c' or 'ctrl+d'
                print "\x1b[0;0H\x1b[J"
                exit(0)
            else:
                pass
        return line
    
    
    def newGame(self):
        """
        
        """
        try:
            bg = self.selectColor("\x1b[0;0H\x1b[J\x1b[1mSelect a background color\n\tuse arrow keys (vim or normal) to navigate\n\tup/down to change color\n\tleft/right to lighten/darken\n\tctrl+c to use default (RECOMMENDED)", "4", 0)
        except (KeyboardInterrupt, SystemExit):
            bg = None
        try:
            c1 = self.selectColor("\x1b[1mSelet the color of p1's (\"white's\") pieces\x1b[m\n\tuse arrow keys (vim or normal) to navigate\n\tup/down to change color\n\tleft/right to lighten/darken\n\tctrl+c to use default (RECOMMENDED)", "3", 3)
        except (KeyboardInterrupt, SystemExit):
            c1 = None
        try:
            c2 = self.selectColor("\x1b[1mSelect the color of p2's (\"black's\") pieces\x1b[m\n\tuse arrow keys (vim or normal) to navigate\n\tup/down to change color\n\tleft/right to lighten/darken\n\tctrl+c to use default (RECOMMENDED)", "3", 4)
        except (KeyboardInterrupt, SystemExit):
            c2 = None
        
        b = board()
        stdout.write("\x1b[0;0H\x1b[J")
        if random() >= .5:
            try: raw_input("You are playing as player one (\"white\" pieces in conventional chess) [Enter]")
            except (KeyboardInterrupt, SystemExit): pass
            b.play(True, bg=bg, c1=c1, c2=c2)
        else:
            try: raw_input("You are playing as player two (\"black\" pieces in conventional chess) [Enter]")
            except (KeyboardInterrupt, SystemExit): pass
            b.play(True, bg=bg, c1=c1, c2=c2)
    
    
    def practice(self):
        """
        
        """
        try:
            bg = self.selectColor("\x1b[0;0H\x1b[J\x1b[1mBACKGROUND COLOR\n\tuse arrow keys (vim or normal) to navigate\n\tup/down to change color\n\tleft/right to lighten/darken\n\tctrl+c to use default (RECOMMENDED)", "4", 0)
        except (KeyboardInterrupt, SystemExit):
            bg = None
        try:
            c1 = self.selectColor("\x1b[1mP1's (\"white's\") COLOR\x1b[muse arrow keys (vim or normal) to navigate\n\tup/down to change color\n\tleft/right to lighten/darken\n\tctrl+c to use default (RECOMMENDED)", "3", 3)
        except (KeyboardInterrupt, SystemExit):
            c1 = None
        try:
            c2 = self.selectColor("\x1b[1mP2's (\"black's\") COLOR\x1b[muse arrow keys (vim or normal) to navigate\n\tup/down to change color\n\tleft/right to lighten/darken\n\tctrl+c to use default (RECOMMENDED)", "3", 4)
        except (KeyboardInterrupt, SystemExit):
            c2 = None
        
        b = board()
        b.play(bg=bg, c1=c1, c2=c2)


# BOARD CLASS
class board:
    
    def __init__(self):
        """
        
        """
        self.fd = stdin.fileno()
        self.old_settings = getat(self.fd)
        self.buffer = 4
        self.pieces = bytearray([ 9,11,10, 8, 7,10,11, 9,
                                 12,12,12,12,12,12,12,12,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  6, 6, 6, 6, 6, 6, 6, 6,
                                  3, 5, 4, 2, 1, 4, 5, 3,])
        
        self.pieceMap = { 0:" ",
                          1:"K", 7:"K",
                          2:"Q", 8:"Q",
                          3:"R", 9:"R",
                          4:"B", 10:"B",
                          5:"N", 11:"N",
                          6:"P", 12:"P",}
        
        
        self.sloppyValMove = { 1:[-9, -8, -7, -1, 1, 7, 8, 9],
                                2:[-9, -8, -7, -1, 1, 7, 8, 9],
                                3:[-8, -1, 1, 9],
                                4:[-9, -7, 7, 9],
                                5:[-17, -15, -10, -6, 6, 10, 15, 17],}
        
        self.longMovers = [2, 3, 4]
    
    
    def play(self, once=False, **kwargs):
        """
        
        """
        keys = bytearray([0, 0, 0, 0])
        self.curpos = 56 # 0-63
        self.moveNum = 0
        self.moveLog = []
        self.fullMoves = []
        self.selected = None # piece currently selected
        self.bg = kwargs.get("bg", None)
        self.c1 = kwargs.get("c1", None)
        self.c2 = kwargs.get("c2", None)
        
        if self.bg is None:
            self.bg = "0;2"
        if self.c1 is None:
            self.c1 = "3;1"
        if self.c2 is None:
            self.c2 = "4;1"
        
        repaint = True
        
        stdout.write("\x1b[?25l")
        while True:
            if repaint:
                repaint = False
                stdout.write("\x1b[0;0H\x1b[J")
            print self.getGraphicalChars()
            
            #print "\x1b[2Kkeys:", list(keys)
            for i, l in enumerate(self.moveLog[-10:]):
                stdout.write("\x1b[{};22H{}    ".format(i + 2, l))
            #print "\x1b[2Kpieces removed:", removed
            
            # wait for user input
            setraw(self.fd)
            keys.insert(0,stdin.read(1))
            setat(self.fd, TCSADRAIN, self.old_settings)
            keys = keys[:self.buffer]
            
            # use input
            if keys[0] == 104 or keys[2] == 27 and keys[1] == 91 and keys[0] == 68: # 'h' or '[left]'
                if self.curpos % 8 == 0: # cursor in first column
                    self.curpos += 7
                else:
                    self.curpos -= 1
            elif keys[0] == 106 or keys[2] == 27 and keys[1] == 91 and keys[0] == 66: # 'j' or '[down]'
                if int(self.curpos / 8.0) == 7: # cursor in last row
                    self.curpos -= 56
                else:
                    self.curpos += 8
            elif keys[0] == 107 or keys[2] == 27 and keys[1] == 91 and keys[0] == 65: # 'k' or '[up]'
                if int(self.curpos / 8.0) == 0: # cursor in first row
                    self.curpos += 56
                else:
                    self.curpos -= 8
            elif keys[0] == 108 or keys[2] == 27 and keys[1] == 91 and keys[0] == 67: # 'l' or '[right]'
                if self.curpos % 8 == 7: # cursor in last column
                    self.curpos -= 7
                else:
                    self.curpos += 1
            elif keys[0] == 13 or keys[0] == 32: # '[Enter]' or '[space]'
                if self.selected is None:
                    if self.pieces[self.curpos] > 6:
                        if self.moveNum % 2 == 0:
                            continue
                    elif self.moveNum % 2 == 1:
                        continue
                    if self.pieces[self.curpos] != 0:
                        self.selected = self.curpos
                elif self.curpos == self.selected:
                    self.selected = None
                else:
                    #TODO make move validation better
                    if not self.valMove():
                        continue
                    if self.moveNum % 2 == 0:
                        self.moveLog.append(bytearray())
                        self.moveLog[-1].extend("{}.".format(self.moveNum / 2 + 1))
                    self.moveLog[-1].extend(" ")
                    if self.pieces[self.selected] != 0x06 and self.pieces[self.selected] != 0x0c:
                        self.moveLog[-1].extend(self.pieceMap[self.pieces[self.selected]])
                    if self.pieces[self.curpos] != 0:
                        if self.pieces[self.selected] == 0x06 or self.pieces[self.selected] == 0x0c:
                            self.moveLog[-1].extend(chr(self.selected % 8 + 97))
                        self.moveLog[-1].extend("x")
                    # TODO
                    if 0: # TODO if similar piece can move to same square
                        if 0: # TODO if pieces are on same rank (row)
                            self.moveLog[-1].extend(chr(self.selected % 8 + 97))
                        if 0: # TODO if pieces are on same file (col)
                            self.moveLog[-1].extend(chr(56 - self.selected / 8))
                    self.moveLog[-1].extend(chr(self.curpos % 8 + 97))
                    self.moveLog[-1].extend(chr(56 - self.curpos / 8))
                    
                    self.fullMoves.append({"from":self.selected, "to":self.curpos, "captured":self.pieces[self.curpos], "victor":self.pieces[self.selected]})
                    
                    self.pieces[self.curpos] = self.pieces[self.selected]   # replace the current position with previously self.selected location
                    self.pieces[self.selected] = "\x00"                     # replace the previously self.selected location with blank
                    self.selected = None                                    # reset self.selected to None because nothing is self.selected
                    
                    self.moveNum += 1
                    
                    repaint = True
            elif keys[0] == 26: # 'ctrl+z' (undo)
                if self.moveNum == 0:
                    continue
                self.moveNum -= 1
                fullMove = self.fullMoves[self.moveNum]
                
                if self.moveNum % 2 == 0: # transitioning from black to (currently) white move # len(self.moveLog[-1].split(" ")) == 2: # only one move after number
                    self.moveLog = self.moveLog[:-1]
                else:
                    extra = self.moveLog[-1]
                    self.moveLog = self.moveLog[:-1]
                    self.moveLog.append(" ".join(str(extra).split(" ")[:-1]))
                
                self.pieces[fullMove["from"]] = fullMove["victor"]
                self.pieces[fullMove["to"]] = fullMove["captured"]
                
                repaint = True
            elif keys[0] == 25: # 'ctrl+y' (redo)
                continue # TODO
                if self.moveNum == len(self.fullMoves) - 1:
                    continue
                self.moveNum += 1
                fullMove = self.fullMoves[self.moveNum]
                
                if self.moveNum % 2 == 0:
                    self.moveLog.append(bytearray())
                    self.moveLog[-1].extend("{}.".format(self.moveNum / 2 + 1))
                self.moveLog[-1].extend(" ")
                if self.pieces[self.selected] != 0x06 and self.pieces[self.selected] != 0x0c:
                    self.moveLog[-1].extend(self.pieceMap[self.pieces[self.selected]])
                if self.pieces[self.curpos] != 0:
                    if self.pieces[self.selected] == 0x06 or self.pieces[self.selected] == 0x0c:
                        self.moveLog[-1].extend(chr(self.selected % 8 + 97))
                    self.moveLog[-1].extend("x")
                # TODO
                if 0: # TODO if similar piece can move to same square
                    if 0: # TODO if pieces are on same rank (row)
                        self.moveLog[-1].extend(chr(self.selected % 8 + 97))
                    if 0: # TODO if pieces are on same file (col)
                        self.moveLog[-1].extend(chr(56 - self.selected / 8))
                self.moveLog[-1].extend(chr(self.curpos % 8 + 97))
                self.moveLog[-1].extend(chr(56 - self.curpos / 8))
                
                self.pieces[fullMove["to"]] = fullMove["victor"]
                self.pieces[fullMove["from"]] = "\x00"
                
                repaint = True
            elif keys[0] == 18: # 'ctrl+r' (refresh)
                stdout.write("\x1b[0;0H\x1b[J")
            elif keys[0] == 127 or keys[3] == 27 and keys[2] == 91 and keys[1] == 51 and keys[0] == 126: # '[Backspace]' or '[Del]'
                self.selected = None
            elif keys[0] == 3: # 'ctrl+c' (resign)  # "after pawn e4, black resigned!" :D
                if raw_input("\x1b[13;0Hresign? [Y/n]") in ("y", ""):
                    exit(0)
            elif keys[0] == 4: # 'ctrl+d' (exit)
                stdout.write("\x1b[m\x1b[?25h")
                break
            elif keys[0] == 63:
                self.help()
            else:
                pass
    
    
    def valMove(self):
        if self.pieces[self.selected] > 6:
            if self.pieces[self.curpos] > 6:
                return False
            if not self.sloppyVal():
                return False
        elif self.pieces[self.selected] > 0:
            if self.pieces[self.curpos] < 7 and self.pieces[self.curpos] != 0:
                return False
            if not self.sloppyVal():
                return False
        else:
            pass
        return True
    
    
    def sloppyVal(self):
        if self.pieces[self.selected] == 6 or self.pieces[self.selected] == 12:
            if self.moveNum % 2 == 0:
                if self.selected - self.curpos == 8 or self.selected - self.curpos == 16 and self.selected / 8 == 6:
                    return True
            else:
                if self.selected - self.curpos == -8 or self.selected - self.curpos == -16 and self.selected / 8 == 1:
                    return True
            return False
        return self.curpos - self.selected in self.sloppyValMove[self.pieces[self.selected] % 6]
    
    
    def kingAttcked(self):
        if self.moveNum % 2 == 0:
            return False
        else:
            return False
    
    
    def help(self):
        for i, line in enumerate(bytearray("""
\x1b[34;1mKEYS\x1b[m      | \x1b[35;1mDESCRIPTION\x1b[m| FUNCIONALITY                  \x1b[3{0}m♔\x1b[m
\x1b[34;1m~~~~~~~~~~\x1b[m+\x1b[35;1m~~~~~~~~~~~~\x1b[m+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \x1b[3{0}m♕\x1b[m
\x1b[34;1marrow keys\x1b[m| \x1b[35;1mmove cursor\x1b[m| left/h, down/j, up/k, right/l \x1b[3{0}m♖\x1b[m
\x1b[34;1mvim arrows\x1b[m|            | wraps around to beg/end       \x1b[3{0}m♗\x1b[m
          |            |                               \x1b[3{0}m♘\x1b[m
\x1b[34;1menter\x1b[m     | \x1b[35;1mselect or\x1b[m  | select piece under cursor; if \x1b[3{0}m♙\x1b[m
\x1b[34;1mspace\x1b[m     | \x1b[35;1mdeselect\x1b[m   | already selected, deselected  \x1b[3{1}m♚\x1b[m
          |            |                               \x1b[3{1}m♛\x1b[m
\x1b[34;1mctrl+z\x1b[m    | \x1b[35;1mundo\x1b[m       | undo against computer         \x1b[3{1}m♜\x1b[m
          |            |                               \x1b[3{1}m♝\x1b[m
\x1b[34;1mctrl+y\x1b[m    | \x1b[35;1mredo\x1b[m       | redo a move after you undo    \x1b[3{1}m♞\x1b[m
          |            |                               \x1b[3{1}m♟\x1b[m
\x1b[34;1mctrl+r\x1b[m    | \x1b[35;1mrepaint\x1b[m    | repaint screen*               \x1b[3{0}m♔\x1b[m
          |            |                               \x1b[3{0}m♕\x1b[m
\x1b[34;1mdelete\x1b[m    | \x1b[35;1mdeselect\x1b[m   | deselect a piece from         \x1b[3{0}m♖\x1b[m
\x1b[34;1mbackspace\x1b[m |            | anywhere                      \x1b[3{0}m♗\x1b[m
          |            |                               \x1b[3{0}m♘\x1b[m
\x1b[34;1mctrl+c\x1b[m    | \x1b[35;1mresign\x1b[m     | give up?                      \x1b[3{0}m♙\x1b[m
          |            |                               \x1b[3{1}m♚\x1b[m
\x1b[34;1mctrl+d\x1b[m    | \x1b[35;1mexit\x1b[m       | exit cleanly when your done   \x1b[3{1}m♛\x1b[m
\x1b[34;1m~~~~~~~~~~\x1b[m+\x1b[35;1m~~~~~~~~~~~~\x1b[m+~~~~~~~~~~~~~~~~~~~~~~~~~~~~   \x1b[3{1}m♜\x1b[m
*ctrl+shft+'+' (sometimes ctrl+'+') or ctrl+'-'        \x1b[3{1}m♝\x1b[m
 enlarges or shrinks (respectively) the screen. This   \x1b[3{1}m♞\x1b[m
 can mess up the screen, so repaint cleans it up.      \x1b[3{1}m♟\x1b[m
 repainting every time causes flickering, so it's up   \x1b[3{0}m♔\x1b[m
 to you! Screen also repainted with Enter, undo, redo. \x1b[3{0}m♕\x1b[m\
""".format(self.c1, self.c2)).split("\n")):
            stdout.write("\x1b[{};38H{}".format(i, line))
    
    
    def getGraphicalChars(self):
        """
        
        """
        gr = bytearray("\x1b[0;0H\x1b[4{}m\x1b[0;4H? = help\n".format(self.bg)) # graphical representation of pieces
        for i, piece in enumerate(unpack(">64B", self.pieces)):
            if i % 8 == 0: # x == 0
                gr.extend("\n{}{}\x1b[27m \x1b[m \x1b[4{}m|".format("\x1b[7m" if int(i / 8.0) == int(self.curpos / 8.0) else "", 8 - int(i / 8.0), self.bg))
            if piece > 6: # p2 (black in conv. chess)
                gr.extend("\x1b[21;22;3{}m".format(self.c2))
            elif piece > 0: # p1 (white in conv. chess)
                gr.extend("\x1b[21;22;3{}m".format(self.c1))
            if i == self.curpos:
                gr.extend("\x1b[7m")
            if i == self.selected:
                gr.extend("\x1b[4m")
            gr.extend("{}\x1b[0;4{}m|".format(self.pieceMap[piece], self.bg))
        gr.extend("\n\n\x1b[0m   \x1b[4{}m|".format(self.bg))
        for i in range(97, 105):
            gr.extend("{}{}\x1b[27m|".format("\x1b[7m" if int((i - 1) % 8.0) == int(self.curpos % 8.0) else "", chr(i)))
        gr.extend("\x1b[m")
        return gr


if __name__ == "__main__":
    try:
        main()
    finally:
        term("stty echo")
        stdout.write("\x1b[m\x1b[0;0H\x1b[J")
        
