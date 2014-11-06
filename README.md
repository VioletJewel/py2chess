chess
=====

Play chess in the terminal with Python 2!

This has wonderul color control - YOU can pick ANY color for your pieces and play chess RIGHT IN THE TERMINAL. And you don't even have to press [Enter] EVERY time - because that's just annoying. You can move the cursor around and select your piece and then the square that it moves to. No "e2 e4" or [command][Enter] slop can be found here.

Seriously! Try it out for yourself if you are on Unix. Unfortunately Windows is not very good about displaying color in the terminal.

Funtionalities (keys) currently implemented:
  * "?": help menu * beautiful and condensed.
                   * prints to the right of the board if screen is large enough
                   * if screen is too small, it occupies the whole screen and waits for any key
                 
  * arrows: move cursor around screen with arrow keys
  * "hjkl": move cursor around screen with vim-style keys
  
  * [Enter]: (1) select piece (2) deslect same piece (if same square) or try to move to new square
  * [space]: (1) select piece (2) deslect same piece (if same square) or try to move to new square
  
  * "ctrl+z": undo as many moves as you want (this will change when playing other people... future, though)
  * "ctrl+y": redo as many moves as you want (this will change when playing other people... future, though)
  
  * "ctrl+r": repaint the screen - if you press ctrl+shft++ or ctrl+-, you can mess up the screen by changing
                                 the font size; to counteract this, every time [Enter] is pressed (the second
                                 time) and it is a valid move or undo/redo controls are used, the screen is
                                 repainted,
                                - the screen is NOT repainted every arrow key pressed because this makes the
                                  screen flicker if an arrow key is held down.
                                - this can also be used to clear the help menu

Functionalities (programatically) currently implemented:
  * move validation: needs work for special moves and checking for pieces in between, but everything else works.
  * move log: stored into array and last ten moves printed just to the right of chess board; this uses proper
              chess (algebraic) notation.

Please note that this chess program - in its current state - is not functioning as it should: there are a few bugs and all of the functionality is not there. However, every day I am working on it in my spare time and it has started from absolutely nothing just a couple weeks ago. If you want to contribute or take a look at the code, please do so.

This is just 12 commits (not 13) in 7 days! That's prettay good in my book. Two people could viably play chess now - they wouldn't be able to (1) undo after a castle without a crash, (2) use en passant and white would be able to take his/her opponent's queen on the first move and then a rook on the second... but it works (mostly).
