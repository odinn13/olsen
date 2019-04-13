import random

class Card():
    def __init__(self, rank = 0, suit = "", priority = None):
        self.rank = rank
        self.suit = suit
        self.priority = priority
        rank_name = str(rank)
        suit_name = ""
        if rank == 1:
            rank_name = "A"
        if rank >= 11:
            if rank == 11:
                rank_name = "J"
            elif rank == 12:
                rank_name = "Q"
            elif rank == 13:
                rank_name = "K"
        if suit == "H":
            suit_name ="♥"
        elif suit == "D":
            suit_name = "♦"
        elif suit == "C":
            suit_name ="♣"
        elif suit == "S":
            suit_name = "♠"
        self.card_name1 = "|{:<3}|".format(rank_name)
        self.card_name2 = "| {} |".format(suit_name)
        self.card_name3 = "|{:>3}|".format(rank_name)
        self.rank_name = rank_name

    def __str__(self):
            return "{}\n{}\n{}" .format(self.card_name1, self.card_name2, self.card_name3)

class Remainder():
    def __init__(self, card, next = None):
        self.cards = [card]

    def add_card(self, card):
        self.cards.append(card)

    def see_remainder(self):
        deck_str = ""
        for index, card in enumerate(self.cards):           
            deck_str += "{:>3s} " .format(card)
            if (index+1) % 13 == 0 and index !=51:
                deck_str += "\n"
        return deck_str
    
    def get_card(self):
        return self.cards[-1]

    def __str__(self):
        return str(self.cards[len(self.cards)-1])

class Deck():
    def __init__(self):
        self.deck_list = [Card(rank, suit) for rank in range(1,14) for suit in "SHDC"]

    def shuffle(self):
        return random.shuffle(self.deck_list)

    def deal(self):
        card = self.deck_list[0]
        del self.deck_list[0]
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
        self.hand = []
       
    def add_card(self, denoting_card):
        self.hand.append(denoting_card)

    def remove_card(self, denoting_card):
        self.hand.remove(denoting_card)

    def __str__(self):
        hand_str = ""
        hand_str_list1 = []
        hand_str_list2 = []
        hand_str_list3 = []
        for card in self.hand:
            hand_str_list1.append(card.card_name1)
            hand_str_list2.append(card.card_name2)
            hand_str_list3.append(card.card_name3)
        
        h_s_l = [hand_str_list1, hand_str_list2, hand_str_list3]
        for a_list in h_s_l:
            for item in a_list:
                hand_str += item
            hand_str += "\n"
        return hand_str



class PlayableCharecter(Player):
    def __init__(self, player):
        Player.__init__(self, player)

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
        card_list = self.get_inp(remainder.get_card(), deck, remainder)
        for card in card_list:
            remainder.add_card(card)

    def get_inp(self, top_card, deck, remainder):
        again = False
        draw_count = 0
        while again is False:
            inp = input("choose a card: ")
            if inp.upper() == "D" and draw_count < 3:
                self.add_card(deck.deal())
                draw_count += 1
                self.print_status(remainder)
            elif inp.upper() == "P" and draw_count == 3:
                inp_card = []
            elif inp.upper() == "S":
                self.sort_hand()
                self.print_status(remainder)
            else:
                inp_card = self.test_card_inp(inp, top_card)
                if inp_card is False:
                    print("Invalid input")
                else:
                    again = True
        return inp_card

    def is_valid(self, card):
        suit = card[-1].upper()
        rank = card[:-1].upper()
        if suit in ["H","D","S","C"]:
            if rank in ["A","J","Q","K"] or (rank.isdigit() and 1 <= int(rank) <= 13):
                for card in self.hand:
                    if suit == card.suit and rank == card.rank_name:
                        return card
        return False

    def test_card_inp(self, inp, top_card):
        """if True it returns card else False"""
        inp = inp.strip()
        card_list = []
        if " " in inp:
            inp_card_list = inp.split(" ")
        else:
            inp_card_list = [inp]

        for card in inp_card_list:
            card = card.strip()
            card = self.is_valid(card)
            if card is False:
                return False
            elif card.rank == 8:
                if len(inp_card_list) == 1:
                    choice = self.print_choice()
                    if choice == "1":
                        card_list = [Card(0, "S")]
                    elif choice == "2":
                        card_list = [Card(0, "C")]
                    elif choice == "3":
                        card_list = [Card(0, "H")]
                    elif choice == "4":
                        card_list = [Card(0, "D")]
                else:
                    return False
            elif self.is_allowed(card, top_card) is False:
                return False
            card_list.append(card)
            top_card = Card(card.rank)

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
        print(self)
        print("'D' to draw card,     'P' to pass,      'S' to sort cards")

    def is_allowed(self, inp_card, top_card):
        return inp_card.suit==top_card.suit or inp_card.rank==top_card.rank

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
    
    player1 = PlayableCharecter("P1")
    players.append(player1)

    # inp = ""
    # while inp.isdigit() != True:
        # inp = input("how many playable charecters? (max 5) ")
    # inp = int(inp)
    # for i in range(inp):
    #     print("player nr." + str(i+1) , "name?")
    #     name = input()
    #     namelist.append(name)

    # if inp >= 1:
    #     player1 = PlayableCharecter(namelist[0])
    #     players.append(player1)
    # if inp >= 2:
    #     player2 = PlayableCharecter(namelist[1])
    #     players.append(player2)
    # if inp >= 3:
    #     player3 = PlayableCharecter(namelist[2])
    #     players.append(player3)
    # if inp >= 4:
    #     player4 = PlayableCharecter(namelist[3])
    #     players.append(player4)
    # if inp >= 5:
    #     player5 = PlayableCharecter(namelist[4])
    #     players.append(player5)

    namelist = []
    npc1 = Easy("NPC1")
    players.append(npc1)
    # inp = ""
    # while inp.isdigit() != True:
    #     inp = input("how many NPC? (max 5) ")
    # for i in range(int(inp)):
    #     print("NPC nr." + str(i+1) , "name?")
    #     name = input()
    #     namelist.append(name)
    # inp = int(inp)
    # if inp >= 1:
    #     npc1 = Easy(namelist[0])
    #     players.append(npc1)
    # if inp >= 2:
    #     npc2 = Easy(namelist[1])
    #     players.append(npc2)
    # if inp >= 3:
    #     npc3 = Easy(namelist[2])
    #     players.append(npc3)
    # if inp >= 4:
    #     npc4 = Easy(namelist[3])
    #     players.append(npc4)
    # if inp >= 5:
    #     npc5 = Easy(namelist[4])
    #     players.append(npc5)

    # inp = ""
    # while inp.isdigit() == False:
    #     inp = input("how many card on hand? ")

    inp = 10
    for _ in range(int(inp) ):
        for player in players:
            player.add_card(deck.deal())
    remainder = Remainder(deck.deal())
    return deck, remainder, players

def main():
    deck, remainder, players = bua_til_leik()
    again = True
    while again == True:
        for player in players:
            player.print_status(remainder)  # bæta við npc
            player.player_turn(remainder, deck)
            if len(player.hand) == 0:
                print("PLAYER", player.player, "WON!!!!!!!")
                again = False
                break


main()