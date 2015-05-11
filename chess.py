#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Violet"

# John is with me!

# IMPORTS
from os import popen, system as term
from random import random
from sys import exit, stdin, stdout

try:
    from termios import tcgetattr as getat, tcsetattr as setat, TCSADRAIN
    from tty import setraw
except ImportError:
    print "This game only works on Unix operating systems"
    exit(1)


def main():
    g = game()
    g.newGame()


class game():
    def __init__(self):
        self.fd = stdin.fileno()
        self.old_settings = getat(self.fd)
        self.buffer = 4
    
    def selectColor(self, desc = "", typ = "3", cInd = 7):
        rec = (typ, cInd)
        colorMap = dict()
        darkColors = list()
        colors = list()
        lightColors = list()
        for i, color in enumerate(("black", "red",
                                   "green", "yellow",
                                   "blue",  "purple",
                                   "cyan",  "white")
        ):
            darkColors.append("dark {}".format(color))
            colors.append(color)
            lightColors.append("light {}".format(color))
            colorMap["dark {}".format(color)] = "{};2".format(i)
            colorMap[color] = "{}".format(i)
            colorMap["light {}".format(color)] = "{};1".format(i)
        
        self.keys = bytearray([0, 0, 0, 0])
        ch = None
        if typ == "4":
            shade = 2
        else:
            typ = "3"
            shade = 0
        print "\x1b[0;0H\x1b[J{}\n".format(desc)
        
        # wait for [Enter]
        while ch != 13:
            if shade == 0:
                print "\x1b[7;0H\x1b[2K\x1b[3{}m{}\x1b[m{}".format(
                       colorMap[lightColors[cInd]], lightColors[cInd],
                       " (recommended)" if (rec[0] == "3"
                                            and rec[1] == cInd)
                                        else ""
                      )
            elif shade == 1:
                print "\x1b[7;0H\x1b[2K\x1b[3{}m{}\x1b[m".format(
                       colorMap[colors[cInd]],
                       colors[cInd]
                      )
            else:
                print "\x1b[7;0H\x1b[2K\x1b[3{}m{}\x1b[m{}".format(
                       colorMap[darkColors[cInd]],
                       darkColors[cInd],
                       " (recommended)" if (rec[0] == "4"
                                            and rec[1] == cInd)
                                        else ""
                      )
            
            # wait for user input
            setraw(self.fd)
            self.keys.insert(0,stdin.read(1))
            setat(self.fd, TCSADRAIN, self.old_settings)
            self.keys = self.keys[:self.buffer]
            
            # use input
            
            # 'h' or '[left]'
            if ( self.keys[0] == 104
                 or self.keys[2] == 27
                 and self.keys[1] == 91
                 and self.keys[0] == 68
            ):
                if shade > 0:
                    shade -= 1
                else:
                    shade = 2
            
            # 'j' or '[down]'
            elif ( self.keys[0] == 106
                   or self.keys[2] == 27
                   and self.keys[1] == 91
                   and self.keys[0] == 66
            ):
                if cInd == 7:
                    cInd = 0
                else:
                    cInd += 1
            
            # 'k' or '[up]'
            elif ( self.keys[0] == 107
                   or self.keys[2] == 27
                   and self.keys[1] == 91
                   and self.keys[0] == 65
            ):
                if cInd == 0:
                    cInd = 7
                else:
                    cInd -= 1
            
            # 'l' or '[right]'
            elif ( self.keys[0] == 108
                   or self.keys[2] == 27
                   and self.keys[1] == 91
                   and self.keys[0] == 67
            ):
                if shade < 2:
                    shade += 1
                else:
                    shade = 0
            
            # '[Enter]' or '[space]'
            elif self.keys[0] == 13 or self.keys[0] == 32:
                c = "{}{}".format(
                     cInd,
                     ";1" if shade == 0 
                          else ";2" if shade == 2
                                    else ""
                    )
                
                if shade == 0:
                    return "{};1".format(cInd)
                
                elif shade == 2:
                    return "{};2".format(cInd)
                
                else:
                    return str(cInd)
                
            elif self.keys[0] == 3: # 'ctrl+c''
                return 0
            elif self.keys[0] == 4: # 'ctrl+d'
                exit(0)
    
    
    def menu(self):
        stdout.write("\x1bc")
        self.keys = bytearray([0, 0, 0, 0])
        line = 0
        while self.keys[0] != 13:
            print "\x1b[0;0H{}\n".format(msg)
            for i in xrange(len(options)):
                print "\x1b[34;1m{}. {}{}\x1b[m".format(
                       i + 1,
                       "\x1b[7m" if i == line
                                 else "",
                       options[i]
                      )
            
            # wait for user input
            setraw(self.fd)
            self.keys.insert(0,stdin.read(1))
            setat(self.fd, TCSADRAIN, self.old_settings)
            self.keys = self.keys[:self.buffer]
            
            # use input
            
            # 'j' or '[down]'
            if ( self.keys[0] == 106
                 or self.keys[2] == 27
                 and self.keys[1] == 91
                 and self.keys[0] == 66
            ):
                if line == len(options) - 1:
                    line = 0
                else:
                    line += 1
            
            # 'k' or '[up]'
            elif ( self.keys[0] == 107
                   or self.keys[2] == 27
                   and self.keys[1] == 91
                   and self.keys[0] == 65
            ):
                if line == 0:
                    line = len(options) - 1
                else:
                    line -= 1
            
            elif ( self.keys[0] == 3
                   or self.keys[0] == 4
            ): # 'ctrl+c' or 'ctrl+d'
                print "\x1bc"
                exit(0)
            else:
                pass
        return line
    
    def newGame(self):
        try:
            bg = self.selectColor(
"\x1bcSelect a background color\x1b[m\n\tctrl+c to use \
default (RECOMMENDED)\n\tctrl+d to exit", "4",
0
                 )
        except KeyboardInterrupt:
            bg = None
        try:
            c1 = self.selectColor(
"\x1b[1mSelet the color of p1's (\"white's\") pieces\x1b[m\n\tctrl+c to use \
default (RECOMMENDED)\n\tctrl+d to exit", "3",
3
                 )
        except KeyboardInterrupt:
            c1 = None
        try:
            c2 = self.selectColor(
"\x1b[1mSelect the color of p2's (\"black's\") pieces\x1b[m\n\tctrl+c to use \
default (RECOMMENDED)\n\tctrl+d to exit", "3",
4
                 )
        except KeyboardInterrupt:
            c2 = None
        
        b = board()
        stdout.write("\x1bc")
        if random() >= .5:
            try: raw_input(
"You are playing as player one (\"white\" pieces in conventional chess) [Enter]"
                 )
            except (KeyboardInterrupt, SystemExit): pass
            b.play(True, bg=bg, c1=c1, c2=c2)
        else:
            try: raw_input(
"You are playing as player two (\"black\" pieces in conventional chess) [Enter]"
                 )
            except (KeyboardInterrupt, SystemExit): pass
            b.play(True, bg=bg, c1=c1, c2=c2)
    

class board():
    def __init__(self):
        self.fd = stdin.fileno()
        self.old_settings = getat(self.fd)
        self.buffer = 4
        
        # all of the pieces 0: blank, 1-6: white, 7-12: black
        # (white: K=1 Q=2 R=3 B=4  N=5  P=6)
        # (black: k=7 Q=8 R=9 B=10 N=11 P=12)
        self.pieces = bytearray([ 9,11,10, 8, 7,10,11, 9,
                                 12,12,12,12,12,12,12,12,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  6, 6, 6, 6, 6, 6, 6, 6,
                                  3, 5, 4, 2, 1, 4, 5, 3,])
        
        # maps number to character
        # you can't just use char because you have to distinguish between colors
        self.pieceMap = {0:" ",
                         1:"K", 7: "K",
                         2:"Q", 8: "Q",
                         3:"R", 9: "R",
                         4:"B", 10:"B",
                         5:"N", 11:"N",
                         6:"P", 12:"P",}
        
        # all of the normal valid moves for all pieces
        # (excludes pawn capture, castling, en passant)
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
        
        # shows pieces that can move to indicies in the validMoves array above
        self.pieceGroups = {1:(4,5,6,7,),
                            2:(1,2,4,5,6,7,),
                            3:(2,5,6,),
                            4:(1,4,7,),
                            5:(3,),
                            0:(5,),
                            7:(4,)}
        
    def play(self, once=False, **kwargs):
        self.keys = bytearray(4)
        
        self.curpos = 56        # cursor position 0-63 (64 places)
        self.selected = None    # cursor's selected location (1st enter)
        
        self.fullMoves = []     # full moves and flags
        self.moveNum = 0        # keeps track of place in fullMoves
        
        self.moveLog = []       # the printable move log
        
        # bytearray of pieces moved (Ke1, Ke8, Ra1, Rh1, Ra8, Rh8)
        self.moveFlags = bytearray(6) # all initially 0
        
        self.epFlag = 0
        
        # get correct colors for bg and both players
        self.bg = kwargs.get("bg", None)
        self.c1 = kwargs.get("c1", None)
        self.c2 = kwargs.get("c2", None)
        if self.bg is None:
            self.bg = "0;2"
        if self.c1 is None:
            self.c1 = "3;1"
        if self.c2 is None:
            self.c2 = "4;1"
        
        # self.repaint (on the first run through repaint screen)
        self.repaint = True
        
        # turn the cursor off and change the title to CHESS
        stdout.write("\x1b[?25l\x1b]0;CHESS\x07")
        
        while True:
            if self.repaint:
                stdout.write("\x1b[0;0H\x1b[J") # clear screen
                self.repaint = False
            
            stdout.write(str(self.getGraphicalChars()))     # print board only
            
            for i,l in enumerate(self.moveLog[-10:]):
                stdout.write("\x1b[{};24H{}".format(i + 2, l))
            
            if self.checkmate():
                print "\x1bcCHECKMATE"
                exit(0)
            
            # wait for user input
            setraw(self.fd)
            self.keys.insert(0,stdin.read(1))
            setat(self.fd, TCSADRAIN, self.old_settings)
            self.keys = self.keys[:self.buffer]
            
            self.interpretKeys()
    
    
    def interpretKeys(self):
        # 'h' or '[left]'
        # move cursor left
        if (self.keys[0] == 104 or
           self.keys[2] == 27 and self.keys[1] == 91 and self.keys[0] == 68):
            # cursor in first column
            if self.curpos % 8 == 0:
                self.curpos += 7
            # cursor not in first column
            else:
                self.curpos -= 1
        
        # 'j' or '[down]'
        # move cursor down
        elif self.keys[0] == 106 or self.keys[2] == 27 and self.keys[1] == 91 and self.keys[0] == 66:
            if int(self.curpos / 8.0) == 7: # cursor in last row
                self.curpos -= 56
            else:
                self.curpos += 8
        
        # 'k' or '[up]'
        # move cursor up
        elif (self.keys[0] == 107 or
             self.keys[2] == 27 and self.keys[1] == 91 and self.keys[0] == 65):
            if int(self.curpos / 8.0) == 0: # cursor in first row
                self.curpos += 56
            else:
                self.curpos -= 8
        
        # 'l' or '[right]'
        # move cursor right
        elif (self.keys[0] == 108 or
             self.keys[2] == 27 and self.keys[1] == 91 and self.keys[0] == 67):
            if self.curpos % 8 == 7: # cursor in last column
                self.curpos -= 7
            else:
                self.curpos += 1
        
        # '[Enter]' or '[space]'
        # (1) select piece to move
        # (2) select square to move selected piece
        #     OR
        # (2) deselect square if already selected
        elif self.keys[0] == 13 or self.keys[0] == 32:
            # first enter
            if self.selected is None:
                if self.pieces[self.curpos] > 6:
                    if self.moveNum % 2 == 0:
                        return
                elif self.moveNum % 2 == 1:
                    return
                if self.pieces[self.curpos] != 0:
                    self.selected = self.curpos
            
            # second enter but same piece
            elif self.curpos == self.selected:
                self.selected = None
                return
            
            # second enter
            else:
                if not self.valMove():
                    return
                
                # self.fullMove["flag"] populated in valMove()
                self.fullMove["from"] = self.selected
                self.fullMove["to"] = self.curpos
                self.fullMove["captured"] = self.pieces[self.curpos]
                self.fullMove["victor"] = self.pieces[self.selected]
                
                # TODO properly implement all flags
                if self.fullMove["flag"] == 1:
                    if self.moveNum % 2 == 0: # O-O-O
                        self.pieces[56] = 0
                        self.pieces[59] = 3
                    else:
                        self.pieces[0] = 0
                        self.pieces[3] = 9
                elif self.fullMove["flag"] == 2: # O-O
                    if self.moveNum % 2 == 0:
                        self.pieces[63] = 0
                        self.pieces[61] = 3
                    else:
                        self.pieces[7] = 0
                        self.pieces[5] = 9
                elif self.fullMove["flag"] == 3: # en passant
                    pass
                elif self.fullMove["flag"] == 4: # promotion
                    pass
                
                # limit fullMoves (in case of previous undos)
                if len(self.fullMoves) > self.moveNum:
                    self.fullMoves = self.fullMoves[:self.moveNum]
                
                # add fullMove to fullMoves for undo/redo
                self.fullMoves.append(self.fullMove)
                
                # add move to move log
                self.writeMoveLog()
                
                # replace the current position with previously self.selected location
                self.pieces[self.curpos] = self.pieces[self.selected]
                # replace the previously self.selected location with blank
                self.pieces[self.selected] = "\x00"
                
                # TODO properly implement all flags
                if self.fullMove["flag"] == 1:
                    if self.moveNum % 2 == 0: # O-O-O
                        self.pieces[56] = 0
                        self.pieces[59] = 3
                    else:
                        self.pieces[0] = 0
                        self.pieces[3] = 9
                elif self.fullMove["flag"] == 2: # O-O
                    if self.moveNum % 2 == 0:
                        self.pieces[63] = 0
                        self.pieces[61] = 3
                    else:
                        self.pieces[7] = 0
                        self.pieces[5] = 9
                elif self.fullMove["flag"] == 3:
                    self.fullMove["captured"] = self.pieces[self.epFlag]
                    self.pieces[self.epFlag] = 0
                elif self.fullMove["flag"] == 4:
                    self.pieces[self.curpos] = self.promotion()
                
                # check move flags
                if ((self.curpos == 60
                     or self.selected == 60)
                    and not self.moveFlags[0]
                ):
                    self.moveFlags[0] = True
                elif (
                      (self.curpos == 4
                       or self.selected == 4)
                      and not self.moveFlags[1]
                ):
                    self.moveFlags[1] = True
                
                if ( # rook a1 moved or taken
                    (self.curpos == 56
                     or self.selected == 56)
                    and not self.moveFlags[2]
                ):
                    self.moveFlags[2] = True
                
                elif ( # rook h1 moved or taken
                      (self.curpos == 56
                       or self.selected == 56)
                      and not self.moveFlags[3]
                ):
                    self.moveFlags[3] = True
                
                elif ( # rook a8 moved or taken
                      (self.curpos == 0
                       or self.selected == 0)
                      and not self.moveFlags[4]
                ):
                    self.moveFlags[4] = True
                
                elif ( # rook h8 moved or taken
                      (self.curpos == 0
                       or self.selected == 7)
                      and not self.moveFlags[5]
                ):
                    self.moveFlags[5] = True
                
                # NOTE: must occur before en passant possibility check
                if self.epFlag != 0:
                    self.epFlag = 0
                
                # en passant possibility check for next move
                if ( self.fullMove["victor"] == 6
                     and self.curpos - self.selected == -16
                ):
                    self.epFlag = self.curpos
                elif ( self.fullMove["victor"] == 12
                       and self.curpos - self.selected == 16
                ):
                    self.epFlag = self.curpos
                
                self.moveNum += 1
                
                self.selected = None
                self.repaint = True
        
        # 'ctrl+z'
        # undo
        elif self.keys[0] == 26:
            if self.moveNum == 0:
                return
            
            self.moveNum -= 1       # move pointer back one
            self.selected = None    # deselect piece if one is selected
            
            # since writeMoveLog operates on fullMove, populate it
            self.fullMove = self.fullMoves[self.moveNum]
            
            # transitioning from black to white move (backwards)
            if self.moveNum % 2 == 0:
                # remove last thing written to log
                del self.moveLog[-1]
            else:
                # store last two things written
                extra = self.moveLog[-1]
                # remove index written to log
                del self.moveLog[-1]
                # split log by space, take first (two) index and append to
                # previous moves
                self.moveLog.append(
                    bytearray(" ".join(str(extra).split(" ")[:-1]))
                )
            
            # victor goes back whence he came
            self.pieces[self.fullMove["from"]] = self.fullMove["victor"]
            # the captured piece is restored
            self.pieces[self.fullMove["to"]] = self.fullMove["captured"]
            
            # TODO properly implement all flags
            # O-O-O
            if self.fullMove["flag"] == 1:
                # white move
                if self.moveNum % 2 == 0:
                    # move rook
                    self.pieces[56] = 3
                    self.pieces[59] = 0
                # black move
                else:
                    # move rook
                    self.pieces[0] = 9
                    self.pieces[3] = 0
            
            # O-O
            elif self.fullMove["flag"] == 2:
                # white move
                if self.moveNum % 2 == 0:
                    # move rook
                    self.pieces[63] = 3
                    self.pieces[61] = 0
                # black move
                else:
                    # move rook
                    self.pieces[7] = 9
                    self.pieces[5] = 0
            
            # en passant
            elif self.fullMove["flag"] == 3:
                # override initial piece
                # (curpos isn't the captured pawn; the position of the pawn is)
                # (position of the pawn is stored in self.epFlag
                self.fullMove[self.epFlag] = 0
                if ( self.fullMove["from"] - self.fullMove["to"] == -7
                     or self.fullMove["from"] - self.fullMove["to"] == 9
                ):
                    self.pieces[self.fullMove["from"] + 1] = self.fullMove["captured"]
                elif ( self.fullMove["from"] - self.fullMove["to"] == -9
                       or self.fullMove["from"] - self.fullMove["to"] == 7
                ):
                    self.pieces[self.fullMove["from"] - 1] 
            
            # promotion
            elif self.fullMove["flag"] == 4:
                pass
            
            self.repaint = True
        
        # 'ctrl+y'
        # redo
        elif self.keys[0] == 25:
            if self.moveNum == len(self.fullMoves):
                return
            
            self.fullMove = self.fullMoves[self.moveNum]
            
            self.writeMoveLog()
            
            self.pieces[self.fullMove["from"]] = "\x00"
            
            # victor reconquers
            self.pieces[self.fullMove["to"]] = self.fullMove["victor"]
            # victor leaves old square empty
            self.pieces[self.fullMove["from"]] = "\x00"
            
            # TODO properly implement all flags
            if self.fullMove["flag"] == 1:
                if self.moveNum % 2 == 0: # O-O-O
                    self.pieces[56] = 0
                    self.pieces[59] = 3
                else:
                    self.pieces[0] = 0
                    self.pieces[3] = 9
            elif self.fullMove["flag"] == 2: # O-O
                if self.moveNum % 2 == 0:
                    self.pieces[63] = 0
                    self.pieces[61] = 3
                else:
                    self.pieces[7] = 0
                    self.pieces[5] = 9
            elif self.fullMove["flag"] == 3: # en passant
                pass
            elif self.fullMove["flag"] == 4: # promotion
                pass
            
            self.moveNum += 1 # increment pointer to fullMove
            
            self.selected = None # remove selected
            
            self.repaint = True
            
        # 'ctrl+r'
        # refresh
        elif self.keys[0] == 18:
            self.repaint = True
        
        # '[Backspace]'
        # '[Del]'
        elif ( self.keys[0] == 127
             or (self.keys[3] == 27
                 and self.keys[2] == 91
                 and self.keys[1] == 51
                 and self.keys[0] == 126)
        ):
            self.selected = None
        
        # 'ctrl+c'
        # resign
        # "after pawn e4, black resigned!" :P
        elif self.keys[0] == 3:
            if raw_input("\x1b[13;0Hresign? [Y/n]") in ("y", "Y", ""):
                exit(0)
            stdout.write("\x1b[m\x1b[?25l")
            self.repaint = True
        
        # 'ctrl+d'
        # exit
        elif self.keys[0] == 4:
            raise SystemExit()
        
        # '?'
        # help
        elif self.keys[0] == 63:
            self.repaint = not self.help()
        
        else:
            pass #print list(self.keys)
    
    
    def valMove(self):
        # piece attacking is black
        if self.pieces[self.selected] > 6:
            return (
                    (self.pieces[self.curpos] + 5) / 6 != 2 # not black piece
                    and self.sloppyVal()                    # valid move
                    and not self.pieceBetween()             # no piece between
                    and not self.kingAttacked()             # king not attacked
                   )
        
        # piece attacking is white
        elif self.pieces[self.selected] > 0:
            return (
                    (self.pieces[self.curpos] + 5) / 6 != 1 # not white piece
                    and self.sloppyVal()                    # valid move
                    and not self.pieceBetween()             # no piece between
                    and not self.kingAttacked()             # king not attacked
                   )
        
    
    def sloppyVal(self):
        # create a NEW dict to avoid referencing old (same) dict
        self.fullMove = dict(flag = 0)
        
        if self.pieces[self.selected] == 1: # white king selected
            if ( # O-O-O
                self.curpos - self.selected == -2 # king moved two left
                and map( sum, (self.pieces[57:60],) )[0] == 0 # piece sum = 0
                and not self.moveFlags[0] # white king not moved
                and not self.moveFlags[2] # rook a1 not moved
            ):
                self.fullMove["flag"] = 1 # O-O-O
                return True
            
            elif ( # O-O
                   self.curpos - self.selected == 2 # king moved two right
                   and self.pieces[61] + self.pieces[62] == 0 # piece sum = 0
                   and not self.moveFlags[0] # white king not moved
                   and not self.moveFlags[1] # rook a8 not moved
            ):
                self.fullMove["flag"] = 2 # O-O
                return True
            
        elif self.pieces[self.selected] == 7: # black king selected
            if ( # O-O-O
                self.curpos - self.selected == -2 # king moved two left
                and map(sum, (self.pieces[1:4],))[0] == 0 # piece sum = 0
                and self.moveFlags[1] # black king not moved
                and not self.rookMoved[2] # rook a8 not moved
            ):
                self.fullMove["flag"] = 1 # O-O-O
                return True
                
            elif ( # O-O
                  self.curpos - self.selected == 2 # king moved two right
                  and self.pieces[5] + self.pieces[6] == 0 # piece sum = 0
                  and self.moveFlags[1] # black king not moved
                  and not self.rookMoved[3] # rook h8 not moved
            ):
                self.fullMove["flag"] = 2
                return True
            
            #if (
            #    not self.moveFlags[0] # 
            #    and (self.curpos - self.selected == -2
            #         or self.curpos - self.selected == 2)
            #):
            #    return True
        
        # white pawn selected
        elif self.pieces[self.selected] == 6:
            # moved two first move
            if ( self.curpos - self.selected == -16
                 and self.pieces[self.selected - 8] == 0
            ):
                return True
            
            # moved one row forward
            elif self.curpos / 8 - self.selected / 8 == -1:
                # piece moved straight (not diag)
                if self.curpos - self.selected == -8:
                    # space empty
                    if self.pieces[self.curpos] == 0:
                        return True
                    # space not empty
                    else:
                        return False
                # TODO TODO TODO fix en passant
                # en passant
                elif ( self.epFlag != 0
                       and ( (self.selected == self.epFlag - 1
                              and self.curpos == self.selected - 7)
                            or (self.selected == self.epFlag + 1
                                and self.curpos == self.selected - 9)
                       )
                ):
                    self.fullMove["flag"] = 3
                    return True
                
                # taking diag
                elif ( self.curpos - self.selected == -9
                       or self.curpos - self.selected == -7
                ):
                    return True
                
                else:
                    return False
        
        # black pawn selected
        elif self.pieces[self.selected] == 12:
            if self.curpos - self.selected == 16 and self.pieces[self.curpos] == 0:
                return True
            elif self.curpos / 8 - self.selected / 8 == 1:
                if self.curpos - self.selected == 8:
                    if self.pieces[self.curpos] == 0:
                        return True
                    else:
                        return False
                
                # en passant
                elif ( self.epFlag != 0
                       and ( (self.selected == self.epFlag - 1
                              and self.curpos == self.selected + 9)
                           or (self.selected == self.epFlag + 1
                               and self.curpos == self.selected + 7)
                       )
                ):
                    self.fullMove["flag"] = 3
                    return True
                
                # taking diag
                elif ( self.curpos - self.selected == 9
                       or self.curpos - self.selected == 7
                ):
                    return True
                else:
                    return False
        
        return self.validMoves[
                   112
                   + (self.curpos % 8 - self.selected % 8)
                   + (self.curpos / 8 - self.selected / 8)
                   * 15
               ] in self.pieceGroups[
                        self.pieces[self.selected] % 6
                    ]
    
    
    def kingAttacked(self, moveNum = None):
        # TODO
        # back diagonals
        kingPosx = kingPosy = None
        if (self.moveNum if moveNum is None else moveNum) % 2 == 0:
            for p in xrange(64):
                if self.pieces[p] == 1:
                    break
            kingPosx = p % 8
            kingPosy = p / 8
            
            
            # check back diagonal: like \
            # check top-left
            for x,y in zip(xrange(kingPosx-1,-1,-1),xrange(kingPosy-1,-1,-1)):
                p = self.pieces[y * 8 + x]
                # piece is white (same color) (barrier)
                if (p + 5) / 2 == 1:
                    break
                # piece black queen or bishop
                elif p == 8 or p == 10:
                    return True
            
            # check bottom-right
            for x,y in zip(xrange(kingPosx+1,8),xrange(kingPosy+1,8)):
                p = self.pieces[y * 8 + x]
                # piece is white (same color) (barrier)
                if (p + 5) / 2 == 1:
                    break
                # piece black queen or bishop
                elif p == 8 or p == 10:
                    return True
                
            # check forward diagonal: like /
            # check top-right
            for x,y in zip(xrange(kingPosx+1,8),xrange(kingPosy-1,-1,-1)):
                p = self.pieces[y * 8 + x]
                # piece is white (same color) (barrier)
                if (p + 5) / 2 == 1:
                    break
                # piece black queen or bishop
                elif p == 8 or p == 10:
                    return True
            
            # check bottom-left
            for x,y in zip(xrange(kingPosx-1,-1,-1),xrange(kingPosy+1,8)):
                p = self.pieces[y * 8 + x]
                # piece is white (same color) (barrier)
                if (p + 5) / 2 == 1:
                    break
                # piece black queen or bishop
                elif p == 8 or p == 10:
                    return True
            
            # check vertical: like |
            # check top
            for y in xrange(kingPosy-1,-1,-1):
                p = self.pieces[y * 8 + kingPosx]
                if (p + 5) / 2 == 1:
                    break
                # piece black queen or rook
                elif p == 8 or p == 9:
                    return True
            
            # check bottom
            for y in xrange(kingPosy+1,8):
                p = self.pieces[y * 8 + kingPosx]
                # piece is white (same color) (barrier)
                if (p + 5) / 2 == 1:
                    break
                # piece black queen or rook
                elif p == 8 or p == 9:
                    return True
            
            # check horizontal: like -
            # check left
            for x in xrange(kingPosx-1,-1,-1):
                p = self.pieces[kingPosy * 8 + x]
                # piece is white (same color) (barrier)
                if (p + 5) / 2 == 1:
                    break
                # piece black queen or rook
                elif p == 8 or p == 9:
                    return True
            
            # check right
            for x in xrange(kingPosx+1,8):
                p = self.pieces[kingPosy * 8 + x]
                # piece is white (same color) (barrier)
                if (p + 5) / 2 == 1:
                    break
                # piece black queen or rook
                elif p == 8 or p == 9:
                    return True
            
            # check knights
            for x,y in zip((-1,1,-2,2,-2,2,-1,1),(-2,-2,-1,-1,1,1,2,2)):
                if ( kingPosx + x < 0 or kingPosx + x > 7
                     or kingPosy + y < 0 or kingPosy + y > 7
                ):
                    continue
                p = self.pieces[(kingPosy + y) * 8 + kingPosx + x]
                # piece black knight 
                if p == 11:
                    return True
            
            # check pawns
            # king below rank 7
            if kingPosy > 1:
                # king right of file a
                if kingPosx > 0:
                    # pawn up-left attacking king
                    if self.pieces[(kingPosy - 1) * 8 + kingPosx - 1] == 7:
                        return True
                # king left of file h
                if kingPosx < 0:
                    # pawn up-right attacking king
                    if self.pieces[(kingPosy - 1) * 8 + kingPosx + 1] == 7:
                        return True
            
            return False
        else:
            return False
        
            
    def checkmate(self, moveNum = None):
        if not self.kingAttacked(moveNum):
            return False
        
        if (self.moveNum if moveNum is None else moveNum) % 2 == 0:
            for x in xrange(64):
                if self.pieces[x] == 1:
                    kingPos = x
            
            self.pieces[kingPos] = 0
            # imitate selecting a piece with cursor
            self.selected = kingPos
            
            for x in xrange(-1,2):
                for y in xrange(-1,2):
                    if x == 0 and y == 0:
                        continue
                    self.curpos = kingPos + y * 8 + x
                    if not self.valMove():
                        continue
                    self.pieces[self.curpos] = 1
                    if not self.kingAttacked():
                        self.pieces[self.curpos] = 0
                        self.pieces[self.selected] = 1
                        return False
            
            #self.pieces[self.curpos] = 0
            #self.pieces[self.selected] = 1
            return True
        else:
            for x in xrange(64):
                if self.pieces[x] == 7:
                    kingpPos = x
        
                
                
    
    
    def pieceBetween(self):
        dx = self.curpos % 8 - self.selected % 8 # delta x
        dy = self.curpos / 8 - self.selected / 8 # delta y
        
        if dx == 0 and dy == 0: # impossible for now (taken care of elsewhere)
            return True
        elif dy == 0:
            # dx represents +/- 1 for moveing piece right or left ==> conserves memory
            dx = 1 if self.curpos > self.selected else -1
            # dx represents position now ==> conserves memory
            for dx in xrange(self.selected + dx, self.curpos, dx):
                if self.pieces[dx] != 0:
                    return True
            return False
        
        elif dx == 0:
            # dy represents +/- 8 for moving piece down/up ==> conserves memory
            dy = 8 if self.curpos > self.selected else - 8
            # dy represents position now ==> conserves memory
            for dy in xrange(self.selected + dy, self.curpos, dy):
                if self.pieces[dy] != 0:
                    return True
            return False
        
        elif abs(dx) != abs(dy): # most likely a knight ==> otherwise, another filter should (and does) catch this
            return False
        
        elif abs(dx) == abs(dy):
            # dx represents +/- 7/9 for moving piece along diags ==> conserves memory (if piece wraps around to other side, another filter should - and does - catch this
            if dx < 0 and dy < 0:
                dx = -9
            elif dx > 0 and dy < 0:
                dx = -7
            elif dx < 0 and dy > 0:
                dx = 7
            else:
                dx = 9
            # dx represents x position now ==> conserves memory
            for dx in xrange(self.selected + dx, self.curpos, dx):
                if self.pieces[dx] != 0:
                    return True
            return False
        else:
            return False
    
    
    def writeMoveLog(self):
        if self.moveNum % 2 == 0:
            self.moveLog.append(bytearray())
            self.moveLog[-1].extend("{}.".format(self.moveNum / 2 + 1))
        self.moveLog[-1].extend(" ")
        
        # check for special moves
        if self.fullMove["flag"] == 1: # O-O
            self.moveLog[-1].extend("O-O-O")
            return
        elif self.fullMove["flag"] == 2: # O-O-O
            self.moveLog[-1].extend("O-O")
            return
        elif self.fullMove["flag"] == 4: # pawn promotion
            # TODO
            return
        
        if self.fullMove["victor"] % 6 != 0:
            self.moveLog[-1].extend(self.pieceMap[self.fullMove["victor"]])
        if self.fullMove["captured"] != 0 or self.fullMove["flag"] == 3: # piece captured or en passant
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
    
        if self.fullMove["flag"] == 3: # en passant
            self.moveLog[-1].extend("e.p.")
            return
    
    
    def promotion(self):
        if self.moveNum % 2 == 0:
            piece = 2
        else:
            piece = 8
        while True:
            # wait for user input
            setraw(self.fd)
            self.keys.insert(0,stdin.read(1))
            setat(self.fd, TCSADRAIN, self.old_settings)
            self.keys = self.keys[:self.buffer]
            
            if self.keys[0] == 13 or self.keys[0] == 32: # '[space]' or '[Enter]'
                pass
            else:
                self.interpretKeys()
    
    def help(self):
        rows, cols = popen('stty size', 'r').read().split()
        if int(rows) < 22 or int(cols) < 79:
            stdout.write("\x1bc")
            x = 0
        else:
            x = 38
        for y, line in enumerate(bytearray("""
\x1b[34;1mKEYS       \x1b[m|\x1b[35;1m DESCRIPTION                \x1b[3{0}m♚
\x1b[34;1m~~~~~~~~~~~\x1b[m+\x1b[35;1m~~~~~~~~~~~~~~~~~~~~~~~~~~~ \x1b[3{0}m♛
\x1b[34;1marrow keys \x1b[m|\x1b[35;1m move cursor (normal or vim \x1b[3{0}m♜
\x1b[34;1mvim arrows \x1b[m|\x1b[35;1m functionality)             \x1b[3{0}m♝
\x1b[34;1m           \x1b[m|\x1b[35;1m                            \x1b[3{0}m♞
\x1b[34;1menter      \x1b[m|\x1b[35;1m select (1st/2nd press) or  \x1b[3{0}m♟
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
        gr = bytearray("\x1b[0;0H\x1b[4{0}m\x1b[0;4H? = help\x1b[m\n   \x1b[4{0}m╔═════════════════╗".format(self.bg)) # graphical representation of pieces
        #gr = bytearray("\x1b[0;0H\x1b[4{0}m\x1b[0;4H? = help\x1b[m\n   \x1b[4{0}m╭─────────────────╮".format(self.bg)) # graphical representation of pieces
        #gr = bytearray("\x1b[0;0H\x1b[4{0}m\x1b[0;4H? = help\x1b[m\n   \x1b[4{0}m╒═════════════════╕".format(self.bg)) # graphical representation of pieces
        for i, piece in enumerate(self.pieces):
            if i % 8 == 0: # x == 0
                gr.extend("\n{}{}\x1b[27m \x1b[m \x1b[4{}m║ ".format("\x1b[7m" if int(i / 8.0) == int(self.curpos / 8.0) else "", 8 - int(i / 8.0), self.bg))
                #gr.extend("\n{}{}\x1b[27m \x1b[m \x1b[4{}m│ ".format("\x1b[7m" if int(i / 8.0) == int(self.curpos / 8.0) else "", 8 - int(i / 8.0), self.bg))
                #gr.extend("\n{}{}\x1b[27m \x1b[m \x1b[4{}m│ ".format("\x1b[7m" if int(i / 8.0) == int(self.curpos / 8.0) else "", 8 - int(i / 8.0), self.bg))
            if piece > 6: # p2 (black in conv. chess)
                gr.extend("\x1b[21;22;3{}m".format(self.c2))
            elif piece > 0: # p1 (white in conv. chess)
                gr.extend("\x1b[21;22;3{}m".format(self.c1))
            if i == self.curpos:
                gr.extend("\x1b[7m")
            if i == self.selected:
                gr.extend("\x1b[4m")
            gr.extend("{}\x1b[0;4{}m{}".format(self.pieceMap[piece], self.bg, " ║" if i % 8 == 7 else "|"))
            #gr.extend("{}\x1b[0;4{}m{}".format(self.pieceMap[piece], self.bg, " │" if i % 8 == 7 else "|"))
            #gr.extend("{}\x1b[0;4{}m{}".format(self.pieceMap[piece], self.bg, " │" if i % 8 == 7 else "|"))
        gr.extend("\n\x1b[m   \x1b[4{0}m╚═════════════════╝\n\x1b[0m    \x1b[4{0}m|".format(self.bg))
        #gr.extend("\n\x1b[m   \x1b[4{0}m╰─────────────────╯\n\x1b[0m    \x1b[4{0}m|".format(self.bg))
        #gr.extend("\n\x1b[m   \x1b[4{0}m╘═════════════════╛\n\x1b[0m    \x1b[4{0}m|".format(self.bg))
        for i in range(97, 105):
            gr.extend("{}{}\x1b[27m|".format("\x1b[7m" if int((i - 1) % 8.0) == int(self.curpos % 8.0) else "", chr(i)))
        gr.extend("\x1b[m")
        return gr


if __name__ == "__main__":
    try:
        main()
    finally:
        term("stty echo") # turn echo on if terminated in middle of password
        #stdout.write("\x1b[m\x1b[0;0H\x1b[J\x1b[?25h") # reset ansi, clear screen and turn cursor on
        stdout.write("\x1b[m\x1b[?25h")
