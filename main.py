from tkinter import *
from tkinter import messagebox
import logic
from PIL import Image,ImageTk
from random import randint

# window size
# the mapping is done exactly for 640x480
window_x = 640
window_y = 480

# mouse locations
mouse_x = 0 
mouse_y = 0
# how much one wants to bet
money_ammount = 20
# if there's a token ( if you decided on a bet )
token_val = -1
# the position of the token
token_pos = -1
# player 1 / 2
actual_player = 0

# only the straight bet is mapped, but all the others are implemented
is_inside_bet = -1
# all the outside bets are mapped
is_outside_bet = -1

# initialize the money
game = logic.Game ()
# get the money / stats for the given player
player = game.get_player ( actual_player )

# the positions of the rectangles : e.g. ( numbers_x[0], numbers_y[0] ), and ( numbers_x[1], numbers_y[1] ) are the top left and down right corners
# for straight bet 0
# from positions 37 * 2 to 48 * 2 there are the positions of the outside bets' betting zones

#              0             1         2        3        4          5        6         7          8         9         10        11        12
numbers_x = [ 36,67,      91,118,   90,117,   91,119,  135,158,  135,158,  135,159,  176,198,  175,199,  175,200,  217,240,  215,240,  218,241,
#              13          14        15         16       17        18       19         20        21        22        23         24
              260,282,  259,281,  259,281,  302,323,  301,323,  300,322,  341,363,  342,363,  343,363,  384,405,  385,404,  384,406,
#              25          26        27         28       29        30       31         32        33        34        35         36
              424,447,  425,446,  426,448,  467,489,  468,487,  467,488,  507,529,  507,529,  507,529,  548,571,  548,570,  548,572,
#            2-1 row1  2-1 row2   2-1 row3   1st 12     2nd 12    3rd 12   1to18     19to36   even      odd      red        black
              593,610,  593,611,  593,611,  143,193,  309,358,  477,524,  98,150,  512,563, 183,234,  436,480,  267,316,  351,400 ]

#              0             1         2        3        4          5        6         7          8         9         10        11        12
numbers_y = [ 300, 339,  352,383,  306,336,  259,291,  356,378,  309,332,  266,287,  356,378,  310,333,  264,288,  354,379,  310,335,  263,290,
#              13          14        15         16       17        18       19         20        21        22        23         24
              354,380,  309,332,  262,287,  355,379,  308,335,  263,288,  355,379,  308,335,  262,287,  355,380,  307,335,  263,288,
#              25          26        27         28       29        30       31         32        33        34        35         36
              355,381,  308,335,  260,289,  353,382,  306,336,  262,289,  354,382,  308,336,  261,290,  356,383,  308,335,  261,290,
#            2-1 row1  2-1 row2   2-1 row3   1st 12     2nd 12    3rd 12   1to18     19to36   even      odd      red        black
              260,291,  308,336,  357,382,  401,417,  404,417,  403,414,  443,457,  439,458,  441,458,  443,458,  437,460,  437,460 ]

# what numbers you bet for each outside bet
outside_bets = [ [ 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36 ],
                 [ 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35 ],
                 [ 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34 ],
                 [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ],
                 [ 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24 ],
                 [ 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36 ],
                 [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18 ],
                 [ 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36 ],
                 [ 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36 ],
                 [ 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35 ],
                 [ 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36 ],
                 [ 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35 ] ]

# the names for each outside bet
outside_bets_names = [ "2 to 1 1st row", "2 to 1 2nd row", "2 to 1 3rd row", "First 12", "Second 12", "Last 12", "1 to 18", "19 to 36", "Even", "Odd", "Red", "Black" ] 

# loads 37 images from the numbers folder; used when showing random results, and the final one after selecting a bet
def LoadImages () :
    global im_bet_number
    global bet_number

    im_bet_number = [  ]
    bet_number = [ ]

    i = 0
    for i in range ( 0, 37 ) :
        im_bet_number.append ( 0 )
        bet_number.append ( 0 )
        im_bet_number[i] = Image.open ( "numbers/" + str ( i ) + ".png" )
        bet_number[i] = ImageTk.PhotoImage ( im_bet_number[i] )

# checks if the cursor was pressed in a mapped rectangle
def IsCursorInButton ( x1, x2, y1, y2 ) :
    global mouse_x
    global mouse_y
    
    return ( x1 <= mouse_x and mouse_x <= x2 and y1 <= mouse_y and mouse_y <= y2 )

# the mouse was pressed : finds out the rectangle, and moves the token there
def GetPush () :
    global token_val
    global token_name
    global token_pos

    global is_inside_bet
    global is_outside_bet
    
    i = 0
    while i < 49 and IsCursorInButton ( numbers_x[i*2], numbers_x[i*2+1], numbers_y[i*2], numbers_y[i*2+1] ) == 0 :
        i += 1

    if i < 49 :
        if token_val != -1 :
            canvas.delete ( token_name )
        
        token_name = canvas.create_image ( mouse_x, mouse_y, image = token )
        
        token_val = 0

        if i < 37 :
            token_pos = i
            is_inside_bet = 1
            is_outside_bet = 0
        else :
            token_pos = i - 37
            is_inside_bet = 0
            is_outside_bet = 1      

# mouse pressed
def PrintMousePos ( event ) :
    global mouse_x
    global mouse_y

    mouse_x = event.x
    mouse_y = event.y
    
    print ( event.x, event.y )

    GetPush ()

# shows 4 random numbers after betting, and the fifth one, which is correct
def ShowRandomNumbers ( actual_number ) :
    global random_number
    
    for i in range ( 0, 5 ) :
        canvas.create_image ( window_x / 4 * 3 - 150 + i * 40, 50, image = bet_number[ randint ( 0, 36 ) ] )

    canvas.create_image ( window_x / 4 * 3 - 150 + 5 * 40, 50, image = bet_number[ actual_number ]  )

# player selected a bet, and a sum, and wants to bet
def DoBet () :
    global game
    global player

    global is_inside_bet
    global is_outside_bet

    # shows what you bet on : nothing / inside ( token_pos ) / outside ( the string outside_bets_names [ token_pos ] )
    if ( token_pos == -1 ) :
        messagebox.showinfo ( "Wait !", "You didn't select a bet !" )
    elif is_inside_bet == 1 :
        messagebox.showinfo ( "Player " + str ( actual_player + 1 ) + " : " + "Confirmation", "You have bet on " + str ( token_pos ) )
    else :
        messagebox.showinfo ( "Player " + str ( actual_player + 1 ) + " : " + "Confirmation", "You have bet on " + outside_bets_names[token_pos] )

    if player.money - money_ammount >= 0 : # if you have enough money

        if is_inside_bet == 1 :
            st = game.bet ( actual_player, money_ammount, logic.TypeOfBet.SINGLE_NUMBER, [ token_pos ] )
        else : # outside bets
            if token_pos <= 2 : # 2 to 1
                st = game.bet ( actual_player, money_ammount, logic.TypeOfBet.LINE_BET, outside_bets[ token_pos ] )
            elif token_pos <= 5 : # dozens
                st = game.bet ( actual_player, money_ammount, logic.TypeOfBet.DOZENS, outside_bets[ token_pos ] )
            else : # 1 to 1 payout
                st = game.bet ( actual_player, money_ammount, logic.TypeOfBet.ODD_OR_EVEN, outside_bets[ token_pos ] )

        #refreshes player data
        player = game.get_player ( actual_player )

        #shows random numbers, and the correct one
        ShowRandomNumbers ( st.number )        

        # prints who won, and how much money you have
        if st.state == logic.States.WIN :
                messagebox.showinfo ( "Player " + str ( actual_player + 1 ) + " : " + str ( st.number ) + " was the winner", "You won, and now have " + str ( player.money ) + " $" )
        elif st.state == logic.States.LOSS :
                messagebox.showinfo ( "Player " + str ( actual_player + 1 ) + " : " + str ( st.number ) + " was the winner", "You lost, and now have " + str ( player.money ) + " $"  )
    else : # not enough money
        messagebox.showinfo ( "Player " + str ( actual_player + 1 ) + " : " + "Oops !", "Not enough money !" );

    print ( player.money )

def ChangePlayer () :
    global actual_player
    actual_player = 1 - actual_player

def ShowMoney () :
    global game
    global player

    player = game.get_player ( actual_player )

    messagebox.showinfo ( "Player " + str ( actual_player + 1 ) + " : " + "Ammount of Money", str ( player.money ) + " $                                    " )

def PlusMoney10 () :
    global money_ammount

    money_ammount += 10

def PlusMoney1 () :
    global money_ammount

    money_ammount += 1

def LessMoney10 () :
    global money_ammount

    if ( money_ammount - 10 > 0 ) :
        money_ammount -= 10
    else :
        messagebox.showinfo ( "Player " + str ( actual_player + 1 ) + " : " + "Error", "You can't bet less than 1 $" )

def LessMoney1 () :
    global money_ammount

    if ( money_ammount - 1 > 0 ) :
        money_ammount -= 1
    else :
        messagebox.showinfo ( "Player " + str ( actual_player + 1 ) + " : " + "Error", "You can't bet less than 1 $" )

def ShowBetMoney ( ) :
    global money_ammount

    messagebox.showinfo ( "Player " + str ( actual_player + 1 ) + " : " + "Ammount of Money to bet", str ( money_ammount ) + " $                                    " )

root = Tk()

root.title("Tkinter Roulette")

canvas = Canvas()  
canvas.pack ( side='top', fill='both', expand='yes' )  

# used for finding the position of the mouse when pressed
root.bind ( "<Button-1>", PrintMousePos )

# loads the images
im_roulette_select = Image.open ( "roulette_fullscreen.png" )
roulette_select = ImageTk.PhotoImage ( im_roulette_select )

im_token = Image.open ( "token.png" )
token = ImageTk.PhotoImage ( im_token )

LoadImages ()

# makes the buttons on the left, and pairs them with a function to call after pressing
bet_button = Button ( root, text = "BET", command = DoBet )
bet_button.place ( x = 0, y = 0, anchor = "nw" )

change_player_button = Button ( root, text = "Change Player", command = ChangePlayer )
change_player_button.place ( x = 0, y = 25, anchor = "nw" )

show_money_button = Button ( root, text = "Show Money", command = ShowMoney )
show_money_button.place ( x = 0, y = 50, anchor = "nw" )

money_plus10_button = Button ( root, text = "Bet 10 more $", command = PlusMoney10 )
money_plus10_button.place ( x = 0, y = 75, anchor = "nw" )

money_plus1_button = Button ( root, text = "Bet 1 more $", command = PlusMoney1 )
money_plus1_button.place ( x = 0, y = 100, anchor = "nw" )

money_minus10_button = Button ( root, text = "Bet 10 less $", command = LessMoney10 )
money_minus10_button.place ( x = 0, y = 125, anchor = "nw" )

money_minus1_button = Button ( root, text = "Bet 1 less $", command = LessMoney1 )
money_minus1_button.place ( x = 0, y = 150, anchor = "nw" )

money_bet_button = Button ( root, text = "Show how much money you bet", command = ShowBetMoney )
money_bet_button.place ( x = 0, y = 175, anchor = "nw" )

# the backgrounds
canvas.create_image ( window_x / 2, window_y / 2, image = roulette_select )

# locks the window size
root.maxsize ( window_x, window_y )
root.minsize ( window_x, window_y )

# redraws the canvas' elements
root.mainloop()
