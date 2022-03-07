#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 13:05:15 2022

@author: Toby



Welcome to the Solitaire Test Module.

"""

import unittest
from Solitaire_1_4 import * #import all from module


class test_solitaire_class(unittest.TestCase): #class inherits from unittest.TestCase - gives lots of testing capabilities

    def setUp(self):

        self.location_list=set_up_locations()
    
        self.deck=create_deck()
        
        self.deck_2=create_deck() #deck 2 is all face-up
        for card in self.deck_2:
            card.set_side('face-up')
        
        self.shuffled_deck_1=shuffle_deck()
        self.shuffled_deck_2=shuffle_deck()
    
        self.location_1=location("test", [])
        
        
    '''
    Card class test cases
    '''
    def test_card_get_colour(self):
        self.assertEqual(self.deck[0].get_colour(), "red")
        self.assertEqual(self.deck[14].get_colour(), "black")

    def test_card_get_value(self):
        self.assertEqual(self.deck[5].get_value(), 6)
        self.assertEqual(self.deck[0].get_value(), 1)
        self.assertEqual(self.deck[25].get_value(), 13)


    def test_card_get_suit(self):
        self.assertEqual(self.deck[26].get_suit(), "Clubs")
        self.assertEqual(self.deck[13].get_suit(), "Spades")
        self.assertEqual(self.deck[0].get_suit(), "Hearts")
        self.assertEqual(self.deck[39].get_suit(), "Diamonds")

    def test_card_get_set_side(self):
        self.assertEqual(self.deck[0].get_side(), "face-down")
        self.deck[0].set_side("face_up")
        self.assertEqual(self.deck[0].get_side(), "face_up")

    def test_card_get_suit_and_value(self):
        self.assertEqual(self.deck[31].get_suit_and_value(), "6 of Clubs")
        self.assertEqual(self.deck[13].get_suit_and_value(), "Ace of Spades")
        self.assertEqual(self.deck[12].get_suit_and_value(), "King of Hearts")
        self.assertEqual(self.deck[50].get_suit_and_value(), "Queen of Diamonds")
        self.assertEqual(self.deck[49].get_suit_and_value(), "Jack of Diamonds")


    '''
    Create_deck function test cases
    '''
    def test_deck_length(self):
        self.assertEqual(len(self.deck), 52) #52 cards
       
    def test_deck_no_duplicates(self):
        no_dups_list=[]
        for card in self.deck:
            if card not in no_dups_list:
                no_dups_list.append(card)
        self.assertEqual(len(no_dups_list), 52)

        
    '''
    shuffle_deck function test cases
    '''
    def test_shuffle_deck_length(self):
        self.assertEqual(len(self.shuffled_deck_1), 52) #52 cards
    
    def test_shuffle_deck_diff_deck(self):#test that shuffled deck is different from standard deck
        self.assertNotEqual(self.shuffled_deck_1, self.deck)
    
    def test_shuffle_deck_diff(self): #test that 2 shuffled decks are different from each other
        self.assertNotEqual(self.shuffled_deck_1, self.shuffled_deck_2)
        
    
    '''
    location class test cases
    '''
    def test_get_location_id(self):
        location_1=location("test", [])
        self.assertEqual(location_1.get_location_id(), "test")
    
    
    def test_add_card(self):
        test_card_list_1=[self.deck[0],self.deck[16], self.deck[32]]
        test_card_list_2=[self.deck[11], self.deck[36]]
        location_1=location("test", test_card_list_1)

        
        location_1.add_cards(test_card_list_2)
        self.assertEqual(len(location_1.card_list), 5) # new list is 5 card objects in length
        self.assertEqual(location_1.card_list[-1], self.deck[36]) #last card of locaton_1 is now deck[35]
        
    def test_remove_card(self):
        test_card_list_1=[self.deck[0],self.deck[16], self.deck[32], self.deck[11], self.deck[36]]
        location_1=location("test", test_card_list_1)
        
        location_1.remove_cards(self.deck[32])
        self.assertEqual(len(location_1.card_list), 2) #new length is 2
        self.assertEqual(location_1.card_list[-1], self.deck[16]) #last card is now Card2

        
    def test_can_move_cards(self):   #True if opposite colours, card 1 == card 2-1.
        self.assertTrue(self.location_1.can_move_cards(self.deck[1], self.deck[15])) #Valid colours, Valid number (2 onto 3)
        self.assertFalse(self.location_1.can_move_cards(self.deck[1], self.deck[40]))  #Invalid colour, Invalid number (2 onto 2)        
        self.assertFalse(self.location_1.can_move_cards(self.deck[1], self.deck[2]))  #Invalid colour, Valid number (2 onto 3)     
        self.assertFalse(self.location_1.can_move_cards(self.deck[1], self.deck[18]))  #Valid colour, Invalid number (2 onto 6)     
        self.assertFalse(self.location_1.can_move_cards(self.deck[15], self.deck[1]))  #Valid colour, Invalid (3 onto 2) number       
        self.assertFalse(self.location_1.can_move_cards(self.deck[18], self.deck[1]))  #Valid colour, Invalid number (6 onto 2)     

    def test_can_move_home(self):   #True if same suit, card 1==card 2+1  
        self.assertTrue(self.location_1.can_move_home(self.deck[2], self.deck[1])) #Valid suit (hearts), Valid number (3 onto 2)
        self.assertFalse(self.location_1.can_move_home(self.deck[15], self.deck[13]))  #Invalid suit, Valid number (3 onto 2)       
        self.assertFalse(self.location_1.can_move_home(self.deck[18], self.deck[15]))  #Valid suit, Invalid number (6 onto 3)     
        self.assertFalse(self.location_1.can_move_home(self.deck[1], self.deck[2]))  #Valid suit, Invalid number (2 onto 6)     

    def test_move_to_home(self):#Move top card from location to home location
        test_card_list_1=[self.deck[4], self.deck[6], self.deck[11], self.deck[21], self.deck[0]] #Ends with Ace of Hearts
        test_card_list_2=[self.deck[4], self.deck[6], self.deck[11], self.deck[0], self.deck[21]] #Ends with 9 value
        location_1=location("test", test_card_list_1)
        location_2=location("test", test_card_list_2)

        self.assertEqual(len(location_1.card_list), 5) #location_1 cards list is 5 long
        location_1.move_to_home(self.location_list) #carry out move
        self.assertEqual(len(location_1.card_list), 4) #location_1 cards list is 4 long
        self.assertEqual(self.location_list[9].card_list[-1].get_suit_and_value(),"Ace of Hearts") #Ace of Hearts is now in appropriate locaiton in Home list
        
        self.assertEqual(len(location_2.card_list), 5) #location_2 cards list is 5 long
        location_1.move_to_home(self.location_list) #carry out move
        self.assertEqual(len(location_2.card_list), 5) #location_2 cards list is still 5 long

    '''
    column subclass test cases
    '''
    def test_reveal_card(self):
        column_1=column("test", self.deck)
        
        self.assertEqual(column_1.card_list[-1].get_side(), "face-down") #face-down as default
        column_1.reveal_card()
        self.assertEqual(column_1.card_list[-1].get_side(), "face-up") #face-up when revealed default
        self.assertEqual(column_1.card_list[0].get_side(), "face-down") #1st card in list not affected


    def test_move_cards(self):
        test_card_list_1=[self.deck[4], self.deck[6], self.deck_2[16], self.deck_2[41], self.deck_2[27]] #Cards: 5HeartsFace-down, 7HeartsFaceDown, 4SpadesFace-Up, 3DiamondsFace-up, 2ClubsFace-Up
        test_card_list_2=[self.deck[7], self.deck_2[4]] #Ends with 5HeartsFace-Up
        test_card_list_3=[self.deck[7], self.deck_2[12]] #Ends with KingHeartsFace-up
        test_card_list_4=[self.deck[7], self.deck_2[15]] #Ends with 5SpadeFace-Up

        column_1=column("test", test_card_list_1)
        column_2=column("test", test_card_list_2)
        column_3=column("test", [])
        column_4=column("test", test_card_list_3)
        column_5=column("test", test_card_list_4)

        column_1.move_cards(self.location_list, column_2) #valid move
        self.assertEqual(len(column_1.card_list), 2) #after move, 2 cards in column_1
        self.assertEqual(len(column_2.card_list), 5) #after move, 5 cards in column_2
        
        # self.assertEqual(column_1.move_cards(self.location_list, column_3), False) #test moveig a non-king to blank column doesn't run
        
        column_4.move_cards(self.location_list, column_3) #valid move - King to blank
        self.assertEqual(len(column_4.card_list), 1)
    
        # self.assertFalse(column_1.move_cards(self.location_list, column_5)) #test consecutive numbers but same suit

        
    '''
    home subclass test cases
    
    ''' 
    def test_check_complete (self):
        self.location_list[7].add_cards(self.deck[:13])
        self.location_list[8].add_cards(self.deck[13:25])


        self.assertTrue(self.location_list[7].check_complete()) #True if len(card_list)==14 (Home location already has a zero card in)
        self.assertFalse(self.location_list[8].check_complete()) #False as len(card_list)==12
        self.assertFalse(self.location_list[9].check_complete()) #False as len(card_list)==0

        
    '''
    spare subclass test cases
    
    '''
    def test_advance(self):
        test_card_list_1=[self.deck[4], self.deck[6], self.deck[16], self.deck[41], self.deck[27]] #5 cards
        test_card_list_2=[self.deck[7], self.deck[4]] #2 cards
        self.location_list[11]=spare_cards("Spare cards", test_card_list_1)
        self.location_list[13]=spare_cards("Visible pile", [])
        
        x=len(self.location_list[11].card_list) #x=5
        self.location_list[11].advance(self.location_list) #advance 3 cards from [11] to [13]
        self.assertEqual(len(self.location_list[11].card_list), x-3) #new length of [11] == old length -3
        self.assertEqual(len(self.location_list[13].card_list), 3) #new length of [13] == 3

        self.location_list[11]=spare_cards("Spare cards", test_card_list_2)
        self.location_list[13]=spare_cards("Visible pile", [])

        x=len(self.location_list[11].card_list) #x=2
        self.location_list[11].advance(self.location_list) #try to advance 3 cards from [11] to [13] (only 2 available)
        self.assertEqual(len(self.location_list[11].card_list), 0) #new length of [11] == 0
        self.assertEqual(len(self.location_list[13].card_list), 2) #new length of [13] == 2

        self.location_list[11]=spare_cards("Spare cards", [])
        self.location_list[12]=spare_cards("Discard pile", test_card_list_1) # 5 cards
        self.location_list[13]=spare_cards("Visible pile", [])

        self.location_list[11].advance(self.location_list) #try to advance 3 cards from [11] to [13] None available
        self.assertEqual(len(self.location_list[11].card_list), 2) #moves 5 cards from discard to spare before moving 3 to visible
        self.assertEqual(len(self.location_list[13].card_list), 3) #new length of [13] == 3
        self.assertEqual(len(self.location_list[12].card_list), 0) #new length of [12] == 0

    def test_move_to_column(self):
        test_card_list_1=[self.deck[4], self.deck[6], self.deck_2[16]] #Top card = 4SpadesFace-Up

        self.location_list[13]=spare_cards("Visible pile", test_card_list_1)
        self.location_list[0]=column(1, []) #no cards in column
        self.location_list[1]=column(2, [self.deck_2[4]]) #for possible move
        self.location_list[2]=column(3, [self.deck[17]]) #for impossible move
        
        # self.assertFalse(self.location_list[13].move_to_column(self.location_list, self.location_list[0])) #Move of 4Spades to empty column returns False
        # self.assertFalse(self.location_list[13].move_to_column(self.location_list, self.location_list[2])) #Move of 4Spades to 5 Spades returns False
        self.location_list[13].move_to_column(self.location_list, self.location_list[1]) #valid move
        self.assertEqual(len(self.location_list[13].card_list), 2) #2 cards left in location_list[13] after move
        self.assertEqual(self.location_list[1].card_list[-1].get_suit_and_value(), "4 of Spades") #4Spades is now in location_list[1]
        
        self.location_list[13]=spare_cards("Visible pile", []) #0 cards in location_list[13]
        # self.assertFalse(self.location_list[13].move_to_column(self.location_list, self.location_list[0]))

    
    '''
    Deal New Hand Test
    '''
    def test_deal_new_hand(self):
        location_list=deal_new_hand()
        for list in location_list[0:7]:
            self.assertEqual(list.card_list[-1].get_side(), "face-up") #end card is always face-up
        for list in location_list[1:7]:
            self.assertEqual(list.card_list[-2].get_side(), "face-down") #penultimate card always face-down

        for i in range(0, 7):
            self.assertEqual(len(location_list[i].card_list), i+1) #correct number of cards in each column
        for i in range(7, 11):
            self.assertEqual(len(location_list[i].card_list), 1) #Single card in home piles
        self.assertEqual(len(location_list[11].card_list), 24) #24 cards left over in spares pile
        self.assertEqual(len(location_list[12].card_list), 0) #0 cards in visible pile
        self.assertEqual(len(location_list[13].card_list), 0) #0 cards in discard pile

        for card in location_list[11].card_list:
            self.assertEqual(card.get_side(), "face-down") #all cards in spares pile are face-down

    '''
    Have won function test cases
    
    '''
    def test_have_won(self):
        test_card_list_1=self.deck_2[0:13] #Complete set of Hearts
        test_card_list_1.append(card("Hearts", 0))
        test_card_list_2=self.deck_2[13:26] #Complete set of Spades
        test_card_list_2.append(card("Spades", 0))
        test_card_list_3=self.deck_2[26:39] #Complete set of Clubs
        test_card_list_3.append(card("Clubs", 0))
        test_card_list_4=self.deck_2[39:] #Complete set of Diamonds
        test_card_list_4.append(card("Diamonds", 0))
        
        self.location_list[7]=home("Clubs home pile", test_card_list_1)
        self.location_list[8]=home("Clubs home pile", test_card_list_2)
        self.location_list[9]=home("Clubs home pile", test_card_list_3)
        self.location_list[10]=home("Clubs home pile", test_card_list_4)
        
        self.assertTrue(have_won(self.location_list)) #Returns True with corrent number of cards in each home list


        test_card_list_1=self.deck_2[0:12] #Complete set of Hearts
        test_card_list_1.append(card("Hearts", 0))
        test_card_list_2=self.deck_2[13:25] #Complete set of Spades
        test_card_list_2.append(card("Spades", 0))
        test_card_list_3=self.deck_2[26:38] #Complete set of Clubs
        test_card_list_3.append(card("Clubs", 0))
        test_card_list_4=self.deck_2[39:52] #Complete set of Diamonds
        test_card_list_4.append(card("Diamonds", 0))

        self.location_list[7]=home("Clubs home pile", test_card_list_1)
        self.location_list[8]=home("Clubs home pile", test_card_list_2)
        self.location_list[9]=home("Clubs home pile", test_card_list_3)
        self.location_list[10]=home("Clubs home pile", test_card_list_4)
        
        self.assertFalse(have_won(self.location_list)) #Returns False with 13 cards in each home list
        
        
        self.location_list[7]=home("Clubs home pile", [])
        self.location_list[8]=home("Clubs home pile", [])
        self.location_list[9]=home("Clubs home pile", [])
        self.location_list[10]=home("Clubs home pile", [])
        
        self.assertFalse(have_won(self.location_list)) #Returns False with 0 cards in each home list

    # '''
    # input function test cases
    
    # '''
    # def test_decide_move(self):
        
    
    
if __name__=='__main__':
    unittest.main()
    
        