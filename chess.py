#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__  = "Violet"

# IMPORTS
from os import popen, system as term
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
            elif keys[0] == 3: # 'ctrl+c''
                return 0
            elif keys[0] == 4: # 'ctrl+d'
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
            bg = self.selectColor("\x1b[0;0H\x1b[J\x1b[1mSelect a background color\x1b[m\n\tctrl+c to use default (RECOMMENDED)\n\tctrl+d to exit", "4", 0)
        except KeyboardInterrupt:
            bg = None
        try:
            c1 = self.selectColor("\x1b[1mSelet the color of p1's (\"white's\") pieces\x1b[m\n\tctrl+c to use default (RECOMMENDED)\n\tctrl+d to exit", "3", 3)
        except KeyboardInterrupt:
            c1 = None
        try:
            c2 = self.selectColor("\x1b[1mSelect the color of p2's (\"black's\") pieces\x1b[m\n\tctrl+c to use default (RECOMMENDED)\n\tctrl+d to exit", "3", 4)
        except KeyboardInterrupt:
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
        
        self.pieceMap = {0:" ",
                         1:"K", 7: "K",
                         2:"Q", 8: "Q",
                         3:"R", 9: "R",
                         4:"B", 10:"B",
                         5:"N", 11:"N",
                         6:"P", 12:"P",}
        
        
        self.validMoves = bytearray((1,0,0,0,0,0,0,2,0,0,0,0,0,0,1,
                                     0,1,0,0,0,0,0,2,0,0,0,0,0,1,0,
                                     0,0,1,0,0,0,0,2,0,0,0,0,1,0,0,
                                     0,0,0,1,0,0,0,2,0,0,0,1,0,0,0,
                                     0,0,0,0,1,0,0,2,0,0,1,0,0,0,0,
                                     0,0,0,0,0,1,3,2,3,1,0,0,0,0,0,
                                     0,0,0,0,0,3,4,5,4,3,0,0,0,0,0,
                                     2,2,2,2,2,2,6,0,6,2,2,2,2,2,2,
                                     0,0,0,0,0,3,7,6,7,3,0,0,0,0,0,
                                     0,0,0,0,0,1,3,2,3,1,0,0,0,0,0,
                                     0,0,0,0,1,0,0,2,0,0,1,0,0,0,0,
                                     0,0,0,1,0,0,0,2,0,0,0,1,0,0,0,
                                     0,0,1,0,0,0,0,2,0,0,0,0,1,0,0,
                                     0,1,0,0,0,0,0,2,0,0,0,0,0,1,0,
                                     1,0,0,0,0,0,0,2,0,0,0,0,0,0,1,))
        
        self.pieceGroups = {1:(4,5,6,7,),
                            2:(1,2,4,5,6,7,),
                            3:(2,5,6,),
                            4:(1,4,7,),
                            5:(3,),
                            0:(5,),
                            7:(4,)}
    
    
    def play(self, once=False, **kwargs):
        """
        
        """
        keys = bytearray([0, 0, 0, 0])
        self.curpos = 56 # 0-63
        self.moveNum = 0
        
        self.moveLog = []
        self.fullMoves = []
        
        self.selected = None # piece currently selected
        
        self.kingMoved = [False, False]
        self.rookMoved = [False, False, False, False]
        
        """
            0 = nothing
            1 = castle queen-side
            2 = castle king-side
            3 = en passant
            4 = pawn promotion
        """
        self.specialMove = 0
        
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
                stdout.write("\x1b[{};24H{}".format(i + 2, l))
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
                if self.selected is None: # first enter
                    if self.pieces[self.curpos] > 6:
                        if self.moveNum % 2 == 0:
                            continue
                    elif self.moveNum % 2 == 1:
                        continue
                    if self.pieces[self.curpos] != 0:
                        self.selected = self.curpos
                elif self.curpos == self.selected: # second enter but same piece
                    self.selected = None
                else: # second enter
                    if not self.valMove():
                        continue
                    if self.moveNum % 2 == 0: # white (new row)
                        self.moveLog.append(bytearray())
                        self.moveLog[-1].extend("{}.".format(self.moveNum / 2 + 1))
                    self.moveLog[-1].extend(" ")
                    
                    if self.pieces[self.selected] != 6 and self.pieces[self.selected] != 12:
                        self.moveLog[-1].extend(self.pieceMap[self.pieces[self.selected]])
                    if self.pieces[self.curpos] != 0:
                        if self.pieces[self.selected] == 6 or self.pieces[self.selected] == 12:
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
                    
                    self.fullMoves.append({"from":self.selected,
                                           "to":self.curpos,
                                           "captured":self.pieces[self.curpos],
                                           "victor":self.pieces[self.selected],
                                           "flag":self.specialMove})
                    
                    if len(self.fullMoves) > self.moveNum:
                        self.fullMoves = self.fullMoves[:self.moveNum + 1]
                    
                    self.pieces[self.curpos] = self.pieces[self.selected]   # replace the current position with previously self.selected location
                    self.pieces[self.selected] = "\x00"                     # replace the previously self.selected location with blank
                    self.selected = None                                    # reset self.selected to None because nothing is self.selected
                    
                    self.moveNum += 1
                    
                    if self.curpos == 60 or self.selected == 60:
                        self.kingMoved[0] = True
                    elif self.curpos == 4 or self.selected == 4:
                        self.kingMoved[1] = True
                    
                    if self.curpos == 56 or self.selected == 56:
                        self.rookMoved[0] = True
                    elif self.curpos == 56 or self.selected == 56:
                        self.rookMoved[1] = True
                    elif self.curpos == 0 or self.selected == 0:
                        self.rookMoved[2] = True
                    elif self.curpos == 0 or self.selected == 7:
                        self.rookMoved = True
                    
                    repaint = True
            elif keys[0] == 26: # 'ctrl+z' (undo)
                if self.moveNum == 0:
                    continue
                self.selected = None
                self.moveNum -= 1
                self.fullMove = self.fullMoves[self.moveNum]
                
                if self.moveNum % 2 == 0: # transitioning from black to (currently) white move # len(self.moveLog[-1].split(" ")) == 2: # only one move after number
                    self.moveLog = self.moveLog[:-1]
                else:
                    extra = self.moveLog[-1]
                    self.moveLog = self.moveLog[:-1]
                    self.moveLog.append(bytearray(" ".join(str(extra).split(" ")[:-1])))
                
                self.pieces[self.fullMove["from"]] = self.fullMove["victor"] # victor goes back whence he came
                self.pieces[self.fullMove["to"]] = self.fullMove["captured"] # the captured piece is restored
                
                # TODO properly implement all flags
                if self.fullMove["flag"] == 1:
                    if self.moveNum % 2 == 0:
                        self.pieces[56] = 3
                        self.pieces[59] = 0
                        #self.pieces[60] = 1
                    else:
                        self.pieces[0] = 9
                        self.pieces[3] = 0
                        #self.pieces[4] = 7
                elif self.fullMove["flag"] == 2:
                    if self.moveNum % 2 == 0:
                        self.pieces[63] = 3
                        self.pieces[61] = 0
                        #self.pieces[60] = 1
                    else:
                        self.pieces[7] = 9
                        self.pieces[5] = 0
                        #self.pieces[4] = 7
                
                
                #self.fullMoves = self.fullMoves[:self.moveNum]
                
                repaint = True
            elif keys[0] == 25: # 'ctrl+y' (redo)
                if self.moveNum == len(self.fullMoves):
                    continue
                
                tempCurpos = self.curpos
                
                self.fullMove = self.fullMoves[self.moveNum]
                self.selected = self.fullMove["from"]
                self.curpos = self.fullMove["to"]
                
                self.writeMoveLog()
                
                self.pieces[self.selected] = "\x00"
                self.pieces[self.curpos] = self.fullMove["victor"]
                
                self.pieces[self.fullMove["to"]] = self.fullMove["victor"] # victor reconquers
                self.pieces[self.fullMove["from"]] = "\x00"                # victor leaves old square empty
                
                self.moveNum += 1
                
                self.curpos = tempCurpos
                self.selected = None
                repaint = True
            elif keys[0] == 18: # 'ctrl+r' (refresh)
                stdout.write("\x1b[0;0H\x1b[J")
            elif keys[0] == 127 or keys[3] == 27 and keys[2] == 91 and keys[1] == 51 and keys[0] == 126: # '[Backspace]' or '[Del]'
                self.selected = None
            elif keys[0] == 3: # 'ctrl+c' (resign)  # "after pawn e4, black resigned!" :D
                if raw_input("\x1b[13;0Hresign? [Y/n]") in ("y", "Y", ""):
                    exit(0)
                repaint = True
            elif keys[0] == 4: # 'ctrl+d' (exit)
                stdout.write("\x1b[m\x1b[?25h")
                break
            elif keys[0] == 63:
                repaint = not self.help()
            else:
                pass
    
    
    def writeMoveLog(self):
        if self.moveNum % 2 == 0:
            self.moveLog.append(bytearray())
            self.moveLog[-1].extend("{}.".format(self.moveNum / 2 + 1))
        self.moveLog[-1].extend(" ")
        
        # check for special moves
        if self.specialMove == 1: # O-O
            self.moveLog[-1].write("O-O")
            self.specialMove = 0
            return
        elif self.specialMove == 2: # O-O-O
            self.moveLog[-1].write("O-O-O")
            self.specialMove = 0
            return
        elif self.specialMove == 4: # pawn promotion
            # TODO
            self.specialMove = 0
            return
        
        if self.fullMove["victor"] % 6 != 0:
            self.moveLog[-1].extend(self.pieceMap[self.fullMove["victor"]])
        if self.fullMove["captured"] != 0:
            if self.fullMove["victor"] % 6 == 0:
                self.moveLog[-1].extend(chr(self.fullMove["from"] % 8 + 97))
            self.moveLog[-1].extend("x")
        # TODO
        if 0: # TODO if similar piece can move to same square
            if 0: # TODO if pieces are on same rank (row)
                self.moveLog[-1].extend(chr(self.fullMove["from"] % 8 + 97))
            if 0: # TODO if pieces are on same file (col)
                self.moveLog[-1].extend(chr(56 - self.fullMove["from"] / 8))
        self.moveLog[-1].extend(chr(self.fullMove["to"] % 8 + 97))
        self.moveLog[-1].extend(chr(56 - self.fullMove["to"] / 8))
    
        if self.specialMove == 3: # en passant
            self.moveLog.write(" ep")
            self.specialMove = 0
            return
    
    def valMove(self):
        if self.pieces[self.selected] > 6:
            return (self.pieces[self.curpos] + 5) / 6 != 2 and self.sloppyVal()
        elif self.pieces[self.selected] > 0:
            return (self.pieces[self.curpos] + 5) / 6 != 1 and self.sloppyVal()
        else:
            pass
        return not self.kingAttacked()
    
    
    def sloppyVal(self):
        if self.pieces[self.selected] == 1:
            if not self.kingMoved[0]:
                if self.curpos - self.selected == -2 and map(sum, (self.pieces[57:60],))[0] == 0 and not self.rookMoved[0]: # TODO check if king attacked on way over
                    self.pieces[59] = 3
                    self.pieces[56] = 0
                    self.specialMove = 1
                    return True
                elif self.curpos - self.selected == 2 and self.pieces[61] + self.pieces[62] == 0 and not self.rookMoved[1]:
                    self.pieces[61] = 3
                    self.pieces[63] = 0
                    self.specialMove = 2
                    return True
        elif self.pieces[self.selected] == 7:
            if not self.kingMoved[1]:
                if self.curpos - self.selected == -2 and map(sum, (self.pieces[1:4],))[0] == 0 and not self.rookMoved[2]:
                    self.pieces[3] = 9
                    self.pieces[0] = 0
                    self.specialMove = 1
                    return True
                elif self.curpos - self.selected == 2 and self.pieces[5] + self.pieces[6] == 0 and not self.rookMoved[3]:
                    self.pieces[5] = 9
                    self.pieces[7] = 0
                    self.specialMove = 2
                    return True
            if not self.kingMoved[0] and (self.curpos - self.selected == -2 or self.curpos - self.selected == 2):
                return True
        elif self.pieces[self.selected] == 6:
            if self.curpos - self.selected == -16 and self.pieces[self.selected - 6] == 0 and self.pieces[self.curpos] == 0:
                return True
            elif self.curpos / 8 - self.selected / 8 == -1:
                if self.pieces[self.curpos] == 0:
                    if self.curpos - self.selected == -8:
                        return True
                    else:
                        return False
                elif self.curpos - self.selected == -9 or self.curpos - self.selected == -7:
                    return True
                else:
                    return False
        elif self.pieces[self.selected] == 12:
            if self.curpos - self.selected == 16 and self.pieces[self.selected + 6] == 0 and self.pieces[self.curpos] == 0:
                return True
            elif self.curpos / 8 - self.selected / 8 == 1:
                if self.pieces[self.curpos] == 0:
                    if self.curpos - self.selected == 8:
                        return True
                    else:
                        return False
                elif self.curpos - self.selected == 9 or self.curpos - self.selected == 7:
                    return True
                else:
                    return False
        return self.validMoves[112 + (self.curpos % 8 - self.selected % 8) + (self.curpos / 8 - self.selected / 8) * 15] in self.pieceGroups[self.pieces[self.selected] % 6]
        
    
    
    def kingAttacked(self): # TODO
        return False
    
    
    def help(self):
        rows, cols = popen('stty size', 'r').read().split()
        if int(rows) < 22 or int(cols) < 79:
            stdout.write("\x1b[0;0H\x1b[J")
            x = 0
        else:
            x = 38
        for y, line in enumerate(bytearray("""
\x1b[34;1mKEYS       \x1b[m|\x1b[35;1m DESCRIPTION                \x1b[3{0}m♚
\x1b[34;1m~~~~~~~~~~~\x1b[m+\x1b[35;1m~~~~~~~~~~~~~~~~~~~~~~~~~~~ \x1b[3{0}m♛
\x1b[34;1marrow keys \x1b[m|\x1b[35;1m move cursor (normal or vim \x1b[3{0}m♜
\x1b[34;1mvim arrows \x1b[m|\x1b[35;1m functionality)             \x1b[3{0}m♝
\x1b[34;1m           \x1b[m|\x1b[35;1m                            \x1b[3{0}m♞
\x1b[34;1menter      \x1b[m|\x1b[35;1m select (first press) or    \x1b[3{0}m♟
\x1b[34;1mspace      \x1b[m|\x1b[35;1m deselect (same square)     \x1b[3{1}m♚
\x1b[34;1m           \x1b[m|\x1b[35;1m                            \x1b[3{1}m♛
\x1b[34;1mctrl\x1b[37;2m+\x1b[34;1mz     \x1b[m|\x1b[35;1m undo (computer or self)    \x1b[3{1}m♜
\x1b[34;1mctrl\x1b[37;2m+\x1b[34;1my     \x1b[m|\x1b[35;1m redo if you undo           \x1b[3{1}m♝
\x1b[34;1m           \x1b[m|\x1b[35;1m                            \x1b[3{1}m♞
\x1b[34;1mctrl\x1b[37;2m+\x1b[34;1mr     \x1b[m|\x1b[35;1m repaint (clear this mssg)  \x1b[3{1}m♟
\x1b[34;1m           \x1b[m|\x1b[35;1m                            \x1b[3{0}m♚
\x1b[34;1mdelete     \x1b[m|\x1b[35;1m deselect regaurdless of    \x1b[3{0}m♛
\x1b[34;1mbackspace  \x1b[m|\x1b[35;1m cursor location            \x1b[3{0}m♜
\x1b[34;1m           \x1b[m|\x1b[35;1m                            \x1b[3{0}m♝
\x1b[34;1mctrl\x1b[37;2m+\x1b[34;1mc     \x1b[m|\x1b[35;1m resign                     \x1b[3{0}m♞
\x1b[34;1mctrl\x1b[37;2m+\x1b[34;1md     \x1b[m|\x1b[35;1m save and exit              \x1b[3{1}m♛
\x1b[34;1m           \x1b[m|\x1b[35;1m                            \x1b[3{1}m♜
\x1b[34;1mctrl\x1b[37;2m+\x1b[34;1mshft\x1b[37;2m+\x1b[34;1m+\x1b[m|\x1b[35;1m enlarge text               \x1b[3{1}m♟
\x1b[34;1mctrl\x1b[37;2m+\x1b[34;1m-     \x1b[m|\x1b[35;1m shrink text                \x1b[3{1}m♚\x1b[m\
""".format(self.c1, self.c2)).split("\n")):
            stdout.write("\x1b[{};{}H{}".format(y, x, line))
        if x == 0:
            # wait for user input
            setraw(self.fd)
            stdin.read(1)
            setat(self.fd, TCSADRAIN, self.old_settings)
            return False
        return True
    
    
    def getGraphicalChars(self):
        """
        
        """
        gr = bytearray("\x1b[0;0H\x1b[4{0}m\x1b[0;4H? = help\x1b[m\n   \x1b[4{0}m╔═════════════════╗".format(self.bg)) # graphical representation of pieces
        for i, piece in enumerate(unpack(">64B", self.pieces)):
            if i % 8 == 0: # x == 0
                gr.extend("\n{}{}\x1b[27m \x1b[m \x1b[4{}m║ ".format("\x1b[7m" if int(i / 8.0) == int(self.curpos / 8.0) else "", 8 - int(i / 8.0), self.bg))
            if piece > 6: # p2 (black in conv. chess)
                gr.extend("\x1b[21;22;3{}m".format(self.c2))
            elif piece > 0: # p1 (white in conv. chess)
                gr.extend("\x1b[21;22;3{}m".format(self.c1))
            if i == self.curpos:
                gr.extend("\x1b[7m")
            if i == self.selected:
                gr.extend("\x1b[4m")
            gr.extend("{}\x1b[0;4{}m{}".format(self.pieceMap[piece], self.bg, " ║" if i % 8 == 7 else "|"))
        gr.extend("\n\x1b[m   \x1b[4{0}m╚═════════════════╝\n\x1b[0m    \x1b[4{0}m|".format(self.bg))
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
        
