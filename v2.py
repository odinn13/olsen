import random

class Card():
    def __init__(self, rank = 0, suit = ""):
    
        rank_list = ["1","2","3","4","5","6","7","8","9","10","11","12","13","A","J","Q","K"]
        suit_list = ["S","C","D","H","s","c","d","h"]
        if rank in rank_list and suit in suit_list:
            if rank.isdigit():
                rank = int(rank)
            self.blank = False
        else:
            self.blank = True
        
        if self.blank == False:
            if type(rank) == str:
                if rank.upper() == "A":
                    rank = 1
                elif rank.upper() == "J":
                    rank = 11
                elif rank.upper() == "Q":
                    rank = 12
                elif rank.upper() == "K":
                    rank = 13
            self.rank = rank
            self.suit = suit.upper()
            self.card = str(rank) + suit.upper()
        else:
            self.card = "blk"
        
    def is_blank(self):
        return self.blank

    def __str__(self):
        if self.card == "blk":
            return ""
        else:
            rank_str = self.rank
            return "{}" .format(str(rank_str)+self.suit)

class Remainder():
    def __init__(self, top_card):
        self.all_card = [top_card]

    def add_card(self, card):
        self.all_card.append(card)

    def see_remainder(self):
        deck_str = ""
        for index, card in enumerate(self.all_card):           
            deck_str += "{:>3s} " .format(card)
            if (index+1) % 13 == 0 and index !=51:
                deck_str += "\n"
        return deck_str

    def __str__(self):
        card = self.all_card[-1]
        if "11" in card:
            card = "J" + card[2:]
        elif "12" in card:
            card = "Q" + card[2:]
        elif "13" in card:
            card = "K" + card[2:]
        elif "1" in card and card[1] in "SCDH":
            card = "A" + card[1:]
        if card[-1] == "H":
            card = card[:-1]+"♥"
        elif card[-1] == "D":
            card = card[:-1]+"♦"
        elif card[-1] == "C":
            card = card[:-1]+"♣"
        elif card[-1] == "S":
            card = card[:-1]+"♠"
        return "|{:<3}|\n| {} |\n|{:>3}|\n" .format(card[:-1], card[-1], card[:-1]) 

class Deck():
    def __init__(self):
        self.deck_list = [str(rank) + suit for rank in range(1,14) for suit in "SHDC"]

    def shuffle(self):
        return random.shuffle(self.deck_list)

    def deal(self):
        for i, card in enumerate(self.deck_list):
            del self.deck_list[i]
            return card

    def __str__(self):
        deck_str = ""
        for index, card in enumerate(self.deck_list):
            if "11" in card:
                card = "J" + card[2:]
            elif "12" in card:
                card = "Q" + card[2:]
            elif "13" in card:
                card = "K" + card[2:]
            elif "1" in card and card[1] in "SCDH":
                card = "A" + card[1:]
            
            if card[-1] == "H":
                card = card[:-1]+"♥"
            elif card[-1] == "D":
                card = card[:-1]+"♦"
            elif card[-1] == "C":
                card = card[:-1]+"♣"
            elif card[-1] == "S":
                card = card[:-1]+"♠"
            
                
            deck_str += "|{:<3}|\n| {} |\n|{:>3}|\n" .format(card[:-1], card[-1], card[:-1])
            if (index+1) % 13 == 0 and index !=51:
                deck_str += "\n"

        return deck_str

class Player():
    NUMBER_CARDS = 30

    def __init__ (self, name):
        self.player = name
        self.hand = ["blk" for i in range(self.NUMBER_CARDS)]
       

    def add_card(self, denoting_card):
        for i, card in enumerate(self.hand):
            if card == "blk":
                self.hand[i] = denoting_card
                return self

    def remove_card(self, denoting_card):
        self.hand.remove(denoting_card)

    def lenght(self):
        for i, card in enumerate(self.hand):
            if card == "blk":
                return i

    def __str__(self):
        hand__str = ""
        hand_str_list1 = []
        hand_str_list2 = []
        hand_str_list3 = []
        for card in self.hand:
            if card != "blk":
                if "11" in card:
                    card = "J" + card[2:]
                elif "12" in card:
                    card = "Q" + card[2:]
                elif "13" in card:
                    card = "K" + card[2:]
                elif "1" in card and card[1] in "SCDH":
                    card = "A" + card[1:]
                if card[-1] == "H":
                    card = card[:-1]+"♥"
                elif card[-1] == "D":
                    card = card[:-1]+"♦"
                elif card[-1] == "C":
                    card = card[:-1]+"♣"
                elif card[-1] == "S":
                    card = card[:-1]+"♠"

                hand_str_list1.append("|{:<3}|  ".format(card[:-1]) )
                hand_str_list2.append("| {} |  " .format(card[-1]) )
                hand_str_list3.append("|{:>3}|  ".format(card[:-1]) )

            else:
                h_s_l = [hand_str_list1, hand_str_list2, hand_str_list3]
                for a_list in h_s_l:
                    for squre in a_list:
                        hand__str += squre
                    hand__str += "\n"
                return hand__str
        print("you have reach the card limit")
        return hand__str

class PlayableCharecter(Player):
    def __init__(self, player):
        Player.__init__(self, player)
        self.card_list = []

    def sort_hand(self):
        s=[]
        c=[]
        h=[]
        d=[]
        blk=[]
        for card in self.hand:
            suit = card[-1]
            if suit == "S":
                s.append(card)
            elif suit == "C":
                c.append(card)
            elif suit == "H":
                h.append(card)
            elif suit == "D":
                d.append(card)
            else:
                blk.append(card)
        s.sort(key=len)
        c.sort(key=len)
        h.sort(key=len)
        d.sort(key=len)
        d.sort(key=len)
        total = [s, c, h, d, blk]
        self.hand = [card for a_list in total for card in a_list]

    def player_turn(self, remainder, deck):
        card_list = self.get_inp(remainder.all_card[-1], deck, remainder)
        for card in card_list:
            if card != "blk":
                remainder.add_card(card)

    def get_inp(self, top_card, deck, remainder):
        inp_card = False
        draw_count = 0
        while inp_card == False:
            inp = input("choose a card: ")
            if inp.upper() == "D" and draw_count < 3:
                self.add_card(deck.deal())
                draw_count += 1
                self.print_status(remainder)
            elif inp.upper() == "P" and draw_count == 3:
                inp_card = ["blk"]
            elif inp.upper() == "S":
                self.sort_hand()
                inp_card = False
                self.print_status(remainder)
            elif 1<len(inp)<18:
                inp_card = self.test_card_inp(inp, top_card)
            else:
                inp_card = False
        return inp_card

    def test_card_inp(self, inp, top_card):
        card_list = []
        if " " in inp:
            inp_card_list = inp.split(" ")
        else:
            inp_card_list = [inp]
        for inp_card in inp_card_list:
            if len(inp_card) == 3:
                card = Card(inp_card[0:2], inp_card[2])
                card_list.append( card.__str__() )
            elif len(inp_card) == 2:
                card = Card(inp_card[0], inp_card[1])
                card_list.append( card.__str__() )
            else:
                card_list = [""]
        if  "8" in card_list[0]:
            if len(card_list) == 1 and card_list[0] in self.hand:
                choice = self.print_choice()
                self.remove_card(card_list[0])
                if choice == "1":
                    card_list = ["S"]
                elif choice == "2":
                    card_list = ["C"]
                elif choice == "3":
                    card_list = ["H"]
                elif choice == "4":
                    card_list = ["D"]

            else:
                card_list = False

        else:
            allowed = None
            for card in card_list:
                if card in self.hand and self.is_allowed(card, top_card) and allowed != False:
                    top_card = card[:-1]+"x"
                    allowed = True
                else:
                    allowed = False
                    card_list = False
            if allowed == True:
                for card in card_list:
                    self.remove_card(card)
        return card_list

    def print_choice(self):
        inp = ""
        print("What suit do you want to change too?")
        print("Type '1' for Spade\nType '2' for Club\nType '3' for Heart\nType '4' for Diamond")
        while len(inp) != 1 and "1234" not in inp:
            inp = input(": ")
        return inp

    def print_status(self, remainder):
        print(self.player, "Turn\n")
        print(remainder)
        print("Too put more then 2 card use ' ' between the card")
        print("Your hand:")
        print(self.__str__())
        print("'D' to draw card,     'P' to pass,      'S' to sort cards")

    def is_allowed(self, inp_card, top_card):
        return inp_card[-1]==top_card[-1] or inp_card[:-1]==top_card[:-1]

class NPC(Player):
    def __init__(self, player):
        Player.__init__(self, player)

    def print_status(self, remainder):
        lenght = 0
        for i in range( len(self.hand)):    
            if self.hand[i] != "blk":
                lenght = i+1
        print(self.player + "(NPC)" + " has "+ str(lenght) + " cards left")
        

    def available_cards(self, top_card):
        available_card_list = []
        if len(top_card) == 1:
            suit_available = top_card
            rank_available = ""
        else:
            suit_available = top_card[-1]
            rank_available = top_card[:-1]
        for card in self.hand:
            if card[-1] == suit_available or card[:-1] == rank_available or card[:-1] == "8":
                available_card_list.append(card)
        return available_card_list

class Easy(NPC):
    def __init__(self, player):
        Player.__init__(self, player)

    def player_turn(self, remainder, deck):
        self.available_card = self.available_cards(remainder.all_card[-1])
        draw_counter = 0
        while draw_counter < 3:        
            if len(self.available_card) == 0:
                    self.add_card(deck.deal())
                    draw_counter +=1
                    self.available_card = self.available_cards(remainder.all_card[-1])
            else:
                draw_counter = 5
        if draw_counter == 3:
            print("pass")
            choice = "blk"
        else:
            choice = self.pick_a_card(deck)
            remainder.add_card(choice)
        self.print_status(remainder)

    def pick_a_card(self, deck):
        choice = random.choice(self.available_card)
        self.remove_card(choice)
        if choice[:-1] == "8":
            choice = random.choice(["S","C","H","D"])
        return choice
        
def bua_til_leik():
    #random.seed(10)
    namelist = []
    deck = Deck()
    deck.shuffle()
    players = []
    inp = ""
    while inp.isdigit() != True:
        inp = input("how many playable charecters? (max 5) ")
    inp = int(inp)
    for i in range(inp):
        print("player nr." + str(i+1) , "name?")
        name = input()
        namelist.append(name)

    if inp >= 1:
        player1 = PlayableCharecter(namelist[0])
        players.append(player1)
    if inp >= 2:
        player2 = PlayableCharecter(namelist[1])
        players.append(player2)
    if inp >= 3:
        player3 = PlayableCharecter(namelist[2])
        players.append(player3)
    if inp >= 4:
        player4 = PlayableCharecter(namelist[3])
        players.append(player4)
    if inp >= 5:
        player5 = PlayableCharecter(namelist[4])
        players.append(player5)

    namelist = []
    inp = ""
    while inp.isdigit() != True:
        inp = input("how many NPC? (max 5) ")
    for i in range(int(inp)):
        print("NPC nr." + str(i+1) , "name?")
        name = input()
        namelist.append(name)
    inp = int(inp)
    if inp >= 1:
        npc1 = Easy(namelist[0])
        players.append(npc1)
    if inp >= 2:
        npc2 = Easy(namelist[1])
        players.append(npc2)
    if inp >= 3:
        npc3 = Easy(namelist[2])
        players.append(npc3)
    if inp >= 4:
        npc4 = Easy(namelist[3])
        players.append(npc4)
    if inp >= 5:
        npc5 = Easy(namelist[4])
        players.append(npc5)

    inp = ""
    while inp.isdigit() == False:
        inp = input("how many card on hand? ")
    for i in range(int(inp) ):
        for player in players:
            player.add_card(deck.deal())
    remainder = Remainder(deck.deal())
    return deck, remainder, players

def main():
    deck, remainder, players = bua_til_leik()
    again = True
    while again == True:
        if len(deck.deck_list)>4:
            deck = Deck()
            deck.shuffle()
        for player in players:
            player.print_status(remainder)
            player.player_turn(remainder, deck)
            if player.lenght() == 0:
                print("PLAYER", player.player, "WON!!!!!!!")
                again = False
                break


main()
