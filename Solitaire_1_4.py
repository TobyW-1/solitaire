#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 09:56:30 2022

@author: Toby

- - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Welcome to Solitaire!
- - - - - - - - - - - - - - - - - - - - - - - - - - - - 


Fully playable in the console.

I created this primarily to practice classes and inheritance.
I followed no brief, and all the code came out of my head (with the usual research to solve problems).
I just had the standard rules of the game in mind.

I have learnt a lot from working on this, and there are certainly things I would approach differently if re-doing the project.

Once one is used to moving the cards around, it is relatively playable for a text based version of a card game.

There are a few tweaks that I would like to make:
    - Add in handlers for exceptions to cope with bad user input (a bit more elegant than my if/else statements)
    - Work on simpler user input
    - Add functionality to restart the current game
    - Add an "Undo" button
    - Allow the user to advance the spares pile by 2 or 1 card, as this makes a win much more likely.
    - The user interface can be worked on - the lists of cards in the 7 main columns can get messy later on in the game as they get longer.

"""




class card(object):
    '''
    Attributes:
        suit (string)
        value (int, 1-13)
        side (string, default = "face-down")
    Methods:
        set side - change side from face-down to face-up. Input should be string.
        __str__ - returns value and suit only if card is not face-down (otherwise retruns "x")

    '''
    def __init__ (self, suit, value, side="face-down"): #card defaults to face-down
        self.suit=suit
        self.value=value
        self.side=side
        
        black_suits=["Spades", "Clubs"]
        if suit in black_suits:
            self.colour="black"
        else: self.colour="red"
        
    def set_side(self, new_side):
        self.side=new_side
    
    def get_suit (self):
        return self.suit
    def get_value(self):
        return self.value
    def get_side(self):
        return self.side
    def get_colour(self):
        return self.colour
    
    def get_suit_and_value(self):
        i=self.value
        if i==1:
            i="Ace"
        if i==11:
            i='Jack'
        if i==12:
            i='Queen'
        if i==13:
            i='King'
        return f"{i} of {self.suit}"
    
    def __str__ (self): #only return card value if it can be seen.
        if self.side=="face-down":
            return "X"
        else:
            i=self.value
            if i==1:
                i="Ace"
            if i==11:
                i='Jack'
            if i==12:
                i='Queen'
            if i==13:
                i='King'
            return f"{i} of {self.suit}"
  

def create_deck():
    '''
    Creates a standard deck of cards.
    Returns the list 'deck' of card objects (unshuffled)
    Card objects are numbered 1-13. When card values need to be printed, the special values (AJQK) are substituted for number 1, 11, 12 & 13.
    '''
    
    suits=["Hearts", "Spades", "Clubs", "Diamonds"]
    deck=[]
    
    for i in range (1, 53):
        if i < 14:
            i=card(suits[0], i)
            deck.append(i)
        elif i <27:
            i-=13
            i=card(suits[1], i)
            deck.append(i)
        elif i <40:
            i-=26
            i=card(suits[2], i)
            deck.append(i)
        else:
            i-=39
            i=card(suits[3], i)
            deck.append(i)
    return deck


def shuffle_deck():
    '''
    Uses the function create_deck to create a deck. Then randomises the list.
    Returns a list of card objects in a random order.
    '''
    import random

    unshuffled_deck= create_deck()
    
    shuffled_deck=[]
    
    for i in range(0, 52):
        x=random.choice(unshuffled_deck)
        shuffled_deck.append(x)
        unshuffled_deck.remove(x)

    return shuffled_deck


def set_up_locations():
    '''
    Returns a list of all the location classes that the game needs:
        column_1 -> column_7
        home_clubs, home_diamonds, home_hearts, home_spades
        spare_pile_face_down - unused remains of deck.
        spare_pile_visible - 3 cards get drawn into this list from spare_pile_face_down, and displayed
        spare_pile_discard - when a new set of 3 cards are drawn, any remaining in the spare_visible move here.
    
    The home card_lists have a non-existant card object in that can't be used in the game.
    This allows them to check for valid moves later in the game.

    The other locations are empty.
    '''
    
    column_1=column(1, [])
    column_2=column(2, [])
    column_3=column(3, [])
    column_4=column(4, [])
    column_5=column(5, [])
    column_6=column(6, [])
    column_7=column(7, [])
    
    suit_list=["Clubs", "Diamonds", "Hearts", "Spades"]
    zero_card_list=[]
    for suit in suit_list: #create a zero card for each suit
        zero_card=card(suit, 0)
        zero_card_list.append(zero_card)
    
    home_clubs=home("Clubs home pile", [zero_card_list[0]])
    home_diamonds=home("Diamonds home pile", [zero_card_list[1]])
    home_hearts=home("Hearts home pile", [zero_card_list[2]])
    home_spades=home("Spades home pile", [zero_card_list[3]])

    spare_pile_face_down=spare_cards("Spare cards", [])
    spare_pile_discard=spare_cards("Discard pile", [])
    spare_pile_visible=spare_cards("Visible pile", [])
    
    
    location_list=[column_1, column_2, column_3, column_4, column_5, column_6, column_7, home_clubs, home_diamonds, home_hearts, home_spades, spare_pile_face_down, spare_pile_discard, spare_pile_visible]

    return location_list


def deal_new_hand():
    
    '''    
    Creates a deck, shuffels deck
    creates the location_list using function "set_up_locations"
    Deals cards into the 7 columns of increasing number, revealing top card of each
    Rest of deck goes into "spare_pile_face_down"
    
    Returns the location_list, now holding the locations of the card objects
    
    '''   
    
    #1.0 create and shuffle deck
    deck=shuffle_deck() 
        
    #2.0 deal the cards into the columns
    location_list=set_up_locations()
    
    x=1
    for i in range (0, 7):
        new_cards=deck[:x]#create a list of the cards to be added
        location_list[x-1].add_cards(new_cards) #adds the new_cards list to the column
        deck=deck[x:] #remove the used cards from the deck
        new_cards=[] 
        x+=1
    
    #3.0 reveal the top card of each column
    for x in range (0, 7): #change to iterate through values, not dict.
        location_list[x].reveal_card()

    #4.add the remaining deck cards into spare_pile_face_down
    location_list[11].add_cards(deck)    

    return location_list

class location(object):
    '''
    Locations are lists designed to hold card objects
    
    Attributes:
        location_id - name of location (string or int)
        card_list - a list of card objects
    
    Methods:
        get_card_list - returns a list of all the cards objects in the location
        get_locattion_id - returns location_id
        add_cards - takes a list of cards (new_cards) and appends them to the existing card_list
        remove_cards - removes all cards after and including the given card from card_list
        display_cards - prints the location ID followed by a list of all the cards in the location
        can_move_cards - see info below
        can_move_home - see info below
        move_to_home - Move last/top card in column_1 to it's appropriate home pile. Returns updated location_list if the move is possible.

    '''
    def __init__(self, location_id, card_list):
        self.location_id = location_id
        self.card_list = card_list
        
    def get_location_id(self):
        return self.location_id

    def get_card_list(self):
        l=[]
        for card in self.card_list:
            l.append(card)
        return l
        
    def add_cards (self, new_cards):
        for card in new_cards:
            self.card_list.append(card)
    
    def remove_cards (self, card):
        temp_list=[]
        for i in self.card_list:
            if i!=card: #adds all cards to temp_list until it reaches the given card
                temp_list.append(i)
            elif i==card: #breaks when it reaches the given card
                break
        self.card_list=temp_list #updates card_list
    
    def display_cards (self):
        c_list=[]
        x=1
        for card in self.card_list:
            if card.side=="face-down":
                # print(f"Card {x}: unknown card (face-down)")
                c_list.append("x")
            else:
                # print(f"Card {x}: {card}")  
                c_list.append(card.get_suit_and_value())
            x+=1
        if len(c_list)>0:
            print(f"{self.location_id}: {c_list}")
        else: print(f"{self.location_id}: No cards")

    def can_move_cards(self, card_1, card_2): 
        '''
        Checks to see if a move of one card to another is possible
        Move is of card_1 onto card_2
        
        Possible - opposite colours, card_1 value == card_2 value-1
        
        Returns True if possible
        else False
        '''
        #get necissary data:
        card_1_colour=card_1.get_colour()
        card_2_colour=card_2.get_colour()
        card_1_value=card_1.get_value()
        card_2_value=card_2.get_value()

        if card_2_value==1:
            return False
        elif card_1_colour != card_2_colour and card_1_value==card_2_value-1:
            return True
        else:
            return False

    def can_move_home(self, card_1, card_2):
        '''
        Checks to see if a card can be moved onto it's home pile.
        card_1 = card to be moved
        card_2= top (last) card of home pile
        
        Possible - same suit, card_1 value == card_2 value+1
        
        Returns True if possible
        else False
        
        '''
        #get necissary data:
        card_1_suit=card_1.get_suit()
        card_2_suit=card_2.get_suit()
        card_1_value=card_1.get_value()
        card_2_value=card_2.get_value()


        if card_1_suit == card_2_suit and card_1_value==card_2_value+1:
            return True
        else:
            return False



    def move_to_home (self, location_list):
        if len(self.card_list)==0:
            print("Invalid move")
            return None
        card_1=self.card_list[-1]
        for i in range (7,11): #To select each of the home piles in turn        
            possible_home_pile=location_list[i]
            card_2=possible_home_pile.get_card_list()[-1]
        
            if self.can_move_home(card_1, card_2) == False:
                pass
            else:
                temp_list=[card_1] #card needs to be in a list for add_cards to work
                location_list[i].add_cards(temp_list)
                self.remove_cards(card_1)
                return location_list
        

class column(location):
    '''
    Subclass of location for the 7 main card columns.
    
    Methods:
        len - returns the length of the card_list
        show_column - prints all the cards in the column (face-down is displayed as 'X'). Displays on new lines        
        reveal_card - sets the side of the top card to face-up
        move_cards - See details below
    '''
    
    def len(self):
        return len(self.card_list)
    
    def show_column (self): 
        print(f"\nColumn Number: {self.column_number}")
        for card in self.card_list:
            print(card)
   
    def reveal_card(self):
        self.card_list[-1].set_side("face-up")  
    
    
    def move_cards (self, location_list, column_2): #move from self to other
        '''
        Moves a card from the column to another location.
        If card is part-way through stack, then the rest stack is also moved.
                
        Move from self to column_2
        (move is the largest possible stack of cards)
        
        Checks whether a move is possible, if not an error message is printed and returns False
        
        If move possible: carries out move and returns updated location_list
        '''
        
        column_2_card_list=column_2.get_card_list()    
        
        if column_2.len()==0: #if moving to an empty column, doesn't need to know second column card
            pass
        else:
            card_2=column_2_card_list[-1] #last card in column 2
        
        column_1_card_list=self.get_card_list() #card_list for column 1
        
        
        x=0 #counter needed to know where in stack to move the cards
        for card_1 in column_1_card_list:
         
            if card_1.get_side()=="face-down":
                x+=1
            else:
                if card_1.get_value()==13 and column_2.len()==0: #king moving to empty column
                    column_2.add_cards(column_1_card_list[x:])#move the cards to column_2
                    self.remove_cards(card_1) #remove cards from column_1
                    if self.len()>0:
                        self.reveal_card() #reveals the next card in the column (turns face-up)
                    return location_list
                
                elif column_2.len()>0 and self.can_move_cards(card_1, card_2) == True: #cards moving to another card
                    column_2.add_cards(column_1_card_list[x:])#move the cards to column_2
                    self.remove_cards(card_1) #remove cards from column_1
                    if self.len()>0:
                        self.reveal_card() #reveals the next card in the column (turns face-up)
    
                    return location_list
                else: x+=1 #if the move can't be made
        print("Hmm, That move isn't allowed")
        input("Hit Enter to continue...")       
        return False

    
class home(location):
    '''
    Location objects for the 4 home piles
    
    Methods:
        check_complete - returns True if card list contains 14 cards #including the existing 0 value card!
        __len__ - returns the length of the card_list
    
    '''
    def check_complete (self):
        list=self.get_card_list()
        if len(list)==14:
            return True
        else: return False

    def __len__ (self):
        return len(self.card_list)
    
    
class spare_cards (location):
    '''
    A location the contains the remaining cards not on the table after the deal.
        
    Methods:
        len - returns length of card_list
        advance - moves the 1st 3 cards into the card_list of spare_pile_visible. Returns updated location_list
        move_to_column - See information below
    
    turn_3 - moves 3 cards (or whatever is remaining) to spare_cards_visible. If 0 cards in pile, 
    use_card - moves card at end of list to target column
    
    '''
    
    def len(self):
        return len(self.card_list)
    
    def advance (self, location_list):
        #1.0 reset visible pile: move cards from visible pile to discard pile
        cards_to_move=[]

        for card in location_list[13].card_list:
            card.set_side("face-down")
            cards_to_move.append(card)
        location_list[12].add_cards(cards_to_move)
        
        #2.0 removes the cards from the visible pile
        location_list[13].card_list=[] #updates card_list
        
        #3.0 If spares pile has no more cards, move from discard
        if len(location_list[11].card_list)==0:
            location_list[11].add_cards(location_list[12].get_card_list())
        
            #3.1 Clean out discard pile:
            location_list[12].card_list=[]
        
        #4.0 add 3 new cards to visible pile
        cards_to_move=[]
        if len(self.card_list)<3:
            for card in self.card_list:
                card.set_side("face-up")
                cards_to_move.append(card)
            location_list[13].add_cards(cards_to_move)
        else:
            for card in self.card_list[0:3]:
                card.set_side("face-up")
                cards_to_move.append(card)
            location_list[13].add_cards(cards_to_move)
        
        #5.0 removes the cards from the original spare pile
        temp_list=[]
        for i in self.card_list:
            if i not in cards_to_move: #adds all cards to temp_list that aren't being moved
                temp_list.append(i)
        self.card_list=temp_list #updates card_list
          
        return location_list
    
    
    def move_to_column (self, location_list, column):
        '''
        Moves the top card from spare_visible location to a given column.
        input column is target to move to
        
        Returns updated location_list if possible
        Prints error message if not possible + returns False
        '''
        visible_card_list=self.get_card_list() #card_list for visible_pile
        if len(visible_card_list)==0: #if no cards in visible pile to move
            print("Hmm, there are no cards to move yet - hit \"S\" to get going")
            input("Hit Enter to continue...")            
            return False
        
        card_1=visible_card_list[-1] #card to move is the last in the list
    
        if column.len() ==0 and card_1.get_value() != 13: #can only move a king onto a blank column
            print("Hmm, That move isn't allowed")
            input("Hit Enter to continue...")            
            return False
    
        elif column.len() ==0 and card_1.get_value() ==13: #moving a king to blank space
            temp_list=[card_1]
            column.add_cards(temp_list)#move the cards to recieving column
            self.remove_cards(card_1) #remove cards from visible pile
            return location_list
        
        
        column_card_list=column.get_card_list()#list of cards in the revieving column 
        card_2=column_card_list[-1] #last card in recieving column
        
        if self.can_move_cards(card_1, card_2) == True:
            temp_list=[card_1]
            column.add_cards(temp_list)#move the cards to recieving column
            self.remove_cards(card_1) #remove cards from visible pile
        
            return location_list
    
        print("Hmm, That move isn't allowed")
        input("Hit Enter to continue...")
        return False



def have_won(location_list):
    '''
    Returns True if all 4 home locations have 13 cards in.
    Else, returns False    
    '''
    # len 14 rather than 13 as it already has a zero card in list at start of game
    if len(location_list[7])==14 and len(location_list[8])==14 and len(location_list[9])==14 and len(location_list[10])==14:
        return True
    else: return False
 
def decide_move(location_list):
    '''
    As the user what move they would like to make
    If input isn't a valid move, the function loops until the user enters a valid move
    '''
    is_move_valid =False
    while is_move_valid ==False:
    
        print("\nWhat move would you like to make?\n\nTo move bewtween columns, type \"M\" followed by the two column numbers (i.e. \"M35\")\nIf you would like to move from a column to a home pile, just enter a single column number.\nIf you would like to advance the spares pile, press \"S\".\nIf you would like to move the top card of the spares to a column, press \"S\" followed by the column number (i.e. \"S4\").\nTo move from the spares to the end pile, type \"SE\"\nGive up? Type \"New\" to start a new game.")
        move=input("->")
        uppercase_move=move.upper()
        
        
        valid_move_list=["S", 'SE', "NEW"]
        for x in range (1,8):
            valid_move_list.append(str(x))
            valid_move_list.append(f"S{x}")
            for y in range(1,8):
                if y==x:
                    pass
                else: 
                    valid_move_list.append(f"M{x}{y}")
        
        if uppercase_move in valid_move_list:
            is_move_valid=True
        else:
            print("\nOops, I don't understand that command - please try again!")
            input("Hit Enter to continue...")
            update_display(location_list)
    return uppercase_move

def execute_move(location_list, uppercase_move):
    '''
    Input - the users valid move and the location_list
    (move was made uppercase in "decide_move" function)
    
    Executes the move
    Returns location_list
    '''

    #The below section of code compenssates for the fact that the columns are 1-7, not 0-6 as Python sees it
    move_list=list(uppercase_move)
    x=0
    for char in move_list:
        if char in ["1", "2", "3", "4", "5", "6", "7"]:
            char=int(char)
            char-=1
            move_list[x]=(str(char))
            x+=1
        else: x+=1
    uppercase_move=''.join(move_list)
            
    
    if uppercase_move[0]=="M":
        col_1=int(uppercase_move[1])
        col_2=int(uppercase_move[2])
        location_list[col_1].move_cards(location_list, location_list[col_2])
        
        
    elif uppercase_move in ["0", "1", "2", "3", "4", "5", "6", "7"]:
        num=int(uppercase_move)
        location_list[num].move_to_home(location_list)
        l=location_list[num]
        if len(l.card_list)>0:
            location_list[num].reveal_card()
        
    elif uppercase_move=="S": #advance spare pile
        location_list[11].advance(location_list)

    elif uppercase_move=="SE":
        location_list[13].move_to_home(location_list)
    
    
    elif uppercase_move[0]=="S":
        col=int(uppercase_move[1])
        location_list[13].move_to_column(location_list, location_list[col])
    
def update_display(location_list):
    '''
    provides the latest visual representation of the location_list
    input: location_list
    
    prints the visuals
    
    output: None
    '''
    print("\n" + "- "*50 + "\n")
    
    for x in range (0, 14): #change to iterate through values, not dict.
        if x==6:
            location_list[x].display_cards() 
            print("\n")
        elif x==7 or x==8 or x==9 or x==10:
            # print("\n")
            c=location_list[x].get_card_list()
            if len(c)>1:
                print(f"{location_list[x].get_card_list()[0].get_suit()} home - {c[-1].get_suit_and_value()}")
            else:
                print(f"{location_list[x].get_card_list()[0].get_suit()} home - ...Empty")
        elif x==11:
            print(f"\nSpares pile: {location_list[x].len()} cards")
        elif x==12:
            print(f"Spares discard pile: {location_list[x].len()} cards")
        else:
            location_list[x].display_cards() 
    print("\n")

def play_game(location_list):
    '''
    Run this function to begin a game.
    '''    
    
    location_list=deal_new_hand()

    while have_won(location_list) == False: #Loops until a game is won
        update_display(location_list)
        uppercase_move=decide_move(location_list)
        if uppercase_move=="NEW":
            print("\nGiving up?")
            input("Hit enter to re-shuffle the deck and start again.")
            play_game(location_list)
            break
        execute_move(location_list, uppercase_move)
        
    print ("\n" + "- "*50 + "\nCongratulations, you have won!")
    
     
    

'''
The below code initiates a game:
'''

if __name__=='__main__': #i.e. The code won't automatically run if opened from another module
    location_list=set_up_locations()
    play_game(location_list)

