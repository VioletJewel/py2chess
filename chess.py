#! /usr/bin/env python
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
                #print "down"
                if line == len(options) - 1:
                    line = 0
                else:
                    line += 1
            elif keys[0] == 107 or keys[2] == 27 and keys[1] == 91 and keys[0] == 65: # 'k' or '[up]'
                #print "up"
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
        self.moveLog = bytearray()
        self.pieces = bytearray([ 9,11,10, 8, 7,10,11, 9,
                                 12,12,12,12,12,12,12,12,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  6, 6, 6, 6, 6, 6, 6, 6,
                                  3, 5, 4, 2, 1, 4, 5, 3,])
        
        self.pieceMap = {  0:" ",
                            1:"K", 7:"K",
                            2:"Q", 8:"Q",
                            3:"R", 9:"R",
                            4:"B", 10:"B",
                            5:"N", 11:"N",
                            6:"P", 12:"P",}
    
    
    def play(self, once=False, **kwargs):
        """
        
        """
        keys = bytearray([0, 0, 0, 0])
        self.curpos = 0 # 0-63
        print "\x1b[0;0H\x1b[J\x1b[m"
        movesInd = -1
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
        
        stdout.write("\x1b[?25l")
        while True:
            print self.getGraphicalChars()
            
            #print "\x1b[2Kkeys:", list(keys)
            print "moves:"
            print self.moveLog
            #print "\x1b[2Kpieces removed:", removed
            
            # wait for user input
            setraw(self.fd)
            keys.insert(0,stdin.read(1))
            setat(self.fd, TCSADRAIN, self.old_settings)
            keys = keys[:self.buffer]
            
            # use input
            if keys[0] == 104 or keys[2] == 27 and keys[1] == 91 and keys[0] == 68: # 'h' or '[left]'
                #print "left"
                if self.curpos % 8 == 0: # cursor in first column
                    self.curpos += 7
                else:
                    self.curpos -= 1
            elif keys[0] == 106 or keys[2] == 27 and keys[1] == 91 and keys[0] == 66: # 'j' or '[down]'
                #print "down"
                if int(self.curpos / 8.0) == 7: # cursor in last row
                    self.curpos -= 56
                else:
                    self.curpos += 8
            elif keys[0] == 107 or keys[2] == 27 and keys[1] == 91 and keys[0] == 65: # 'k' or '[up]'
                #print "up"
                if int(self.curpos / 8.0) == 0: # cursor in first row
                    self.curpos += 56
                else:
                    self.curpos -= 8
            elif keys[0] == 108 or keys[2] == 27 and keys[1] == 91 and keys[0] == 67: # 'l' or '[right]'
                #print "right"
                if self.curpos % 8 == 7: # cursor in last column
                    self.curpos -= 7
                else:
                    self.curpos += 1
            elif keys[0] == 13 or keys[0] == 32: # '[Enter]' or '[space]'
                #print "[Enter]"
                if self.selected is None:
                    self.selected = self.curpos
                elif self.curpos == self.selected:
                    self.selected = None
                else:
                    self.moveLog.extend("  ")
                    if self.pieces[self.selected] != 0x06 and self.pieces[self.selected] != 0x0c:
                        self.moveLog.extend(self.pieceMap[self.pieces[self.selected]])
                    if self.pieces[self.curpos] != 0:
                        if self.pieces[self.selected] == 0x06 or self.pieces[self.selected] == 0x0c:
                            self.moveLog.extend(chr(self.selected % 8 + 97))
                        self.moveLog.extend("x")
                    # TODO
                    if 0: # TODO if similar piece can move to same square
                        if 0: # TODO if pieces are on same rank (row)
                            self.moveLog.extend(chr(self.selected % 8 + 97))
                        if 0: # TODO if pieces are on same file (col)
                            self.moveLog.extend(chr(56 - self.selected / 8))
                    self.moveLog.extend(chr(self.curpos % 8 + 97))
                    self.moveLog.extend(chr(56 - self.curpos / 8))
                    
                    self.pieces[self.curpos] = self.pieces[self.selected]   # replace the current position with previously self.selected location
                    self.pieces[self.selected] = "\x00"                     # replace the previously self.selected location with blank
                    self.selected = None                                    # reset self.selected to None because nothing is self.selected
            elif keys[0] == 26: # 'ctrl+z' (undo)
                if len(removed) > 0:
                    old = moves.pop()                               # the old pos (where piece came from)
                    self.pieces[moves.pop()] = self.pieces[old]     # restore old position before it is changed
                    self.pieces[old] = removed.pop()                # restore the last piece removed
            elif keys[0] == 25: # 'ctrl+y' (redo)
                pass
            elif keys[0] == 18: # 'ctrl+r' (refresh)
                stdout.write("\x1b[0;0H\x1b[J")
            elif keys[0] == 3: # 'ctrl+c' (unselect piece)
                self.selected = None
            elif keys[0] == 4: # 'ctrl+d' (exit)
                stdout.write("\x1b[m\x1b[?25h")
                break
            else:
                pass
    

    def getGraphicalChars(self):
        """
        
        """
        gr = bytearray("\x1b[0;0H\x1b[4{}m".format(self.bg)) # graphical representation of pieces
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
        
