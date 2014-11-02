#! /usr/bin/env python

from threading import Thread
from time import sleep
import select
from sys import stdin, stdout

try:
    from termios import tcgetattr as getat, tcsetattr as setat, TCSADRAIN
    from tty import setraw
except ImportError:
    print "psh! Get a unix machine"
    from sys import exit
    exit(1)

global keys

if __name__ == "__main__":
    keys = bytearray()
    fd = stdin.fileno()
    old_settings = getat(fd)
    t = None
    
    
    def readCh():
        setraw(fd)
        try:
            keys.insert(0,stdin.read(1))
            return
        except ValueError:
            pass
        finally:
            setat(fd, TCSADRAIN, old_settings)
    
    
    while True:
        keys = bytearray()
        
        if t is None or not t.is_alive():
            readCh()
        else:
            t.join(.005)
        if len(keys) == 0:
            continue
        elif keys[0] == 27:
            t = Thread(target=readCh)
            t.start()
            t.join(.005)
            if keys[0] == 91:
                readCh()
        
        if len(keys) == 1:
            if keys[0] == 27:
                print "[Esc] only"
            elif keys[0] == 13:
                print "[Enter]"
            elif keys[0] == 32:
                print "[space]"
            elif keys[0] == 26:
                print "ctrl+z"
            elif keys[0] == 3:
                print "ctrl+c"
            elif keys[0] == 4:
                print "ctrl+d"
                from sys import exit
                exit(0)
            else:
                print "\x1b[36;1munimplemented...\x1b[m keys: {}".format(
                       list(reversed(keys))
                                                                   )
        elif len(keys) == 2:
            continue
        elif len(keys) == 3:
            if keys[2] == 27 and keys[1] == 91 and keys[0] == 68:
                print "left"
            elif keys[2] == 27 and keys[1] == 91 and keys[0] == 66:
                print "down"
            elif keys[2] == 27 and keys[1] == 91 and keys[0] == 65:
                print "up"
            elif keys[2] == 27 and keys[1] == 91 and keys[0] == 67:
                print "right"
        else:
            pass
