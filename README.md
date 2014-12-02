chess
=====

Play chess in the terminal with Python 2!

This has wonderul color control - YOU can pick ANY color for your pieces and
play chess RIGHT IN THE TERMINAL. And you don't even have to press [Enter] EVERY
time - because that's just annoying. You can move the cursor around and select
your piece and then the square that it moves to. No "e2 e4" or [command][Enter]
slop can be found here.

Seriously! Try it out for yourself if you are on Unix. Unfortunately Windows is
not very good about displaying color in the terminal.

Funtionalities (keys) currently implemented:
  * "?": help menu
    - beautiful and condensed.
    - prints to the right of the board if screen is large enough
    - if screen is too small, it occupies the whole screen and waits for any key
 
  * arrows: move cursor around screen with arrow keys
  * "hjkl": move cursor around screen with vim-style keys
  
  * [Enter]: (1) select piece (2) deslect same piece (if same square) or try to
    move to new square
  * [space]: (1) select piece (2) deslect same piece (if same square) or try to
    move to new square
  
  * "ctrl+z": undo as many moves as you want (this will change when playing
    other people... future, though)
  * "ctrl+y": redo as many moves as you want (this will change when playing
    other people... future, though)
  
  * "ctrl+r": repaint the screen 
   - if you press ctrl+shft++ or ctrl+-, you can
     mess up the screen by changing the font size;
     to counteract this, every time [Enter] is
     pressed (the second time) and it is a valid
     move or undo/redo controls are used, the
     screen is repainted,
     
   - NOTE: the screen is NOT repainted every arrow
           key pressed because this makes the
           screen flicker if an arrow key is held down.
   
   - this can also be used to clear the help menu

TODO:
* allow for game log scrolling (shift + up/down)
* check for and handle promotion (in progress)
* check if king is put in check and validate moves with that
    - all other move validation is working (en passant and castling)
* check for checkmate

If you want to join in please do! I have tried to keep the code as clean and
commented as possible. I am trying to get everything 80 characters wide with a
comment for everything no matter how simple. This should be helpful for me as
well as for anyone wanting to help or even just look at the code.
