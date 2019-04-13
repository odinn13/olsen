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
            self.value = rank 
            suit_name ="♥"
        elif suit == "D":
            self.value = rank + 13 
            suit_name = "♦"
        elif suit == "C":
            self.value = rank + 13 * 2
            suit_name ="♣"
        elif suit == "S":
            self.value = rank + 13 * 3
            suit_name = "♠"
        self.card_name1 = "|{:<3}|".format(rank_name)
        self.card_name2 = "| {} |".format(suit_name)
        self.card_name3 = "|{:>3}|".format(rank_name)
        self.rank_name = rank_name
        self.suit_value = suit
        

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
        random.shuffle(self.deck_list)

    def deal(self, remainder = None):
        if len(self.deck_list) == 0:
            self.reshuffle(remainder)
            if len(self.deck_list) == 0:
                return None
        card = self.deck_list[0]
        del self.deck_list[0]
        return card
    
    def reshuffle(self, remainder):
        top_card = remainder.get_card()
        self.deck_list = remainder.cards[:-1]
        self.shuffle()
        if top_card.rank == 8:
            top_card = Card(8, top_card.suit)
        remainder.cards = [top_card]

    def __len__(self):
        return len(self.deck_list)

class Player():
    NUMBER_CARDS = 30

    def __init__ (self, name):
        self.player = name
        self.hand = []
       
    def is_allowed(self, inp_card, top_card):
        return inp_card.suit==top_card.suit_value or inp_card.rank==top_card.rank

    def add_card(self, denoting_card):
        if denoting_card is not None:
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
    
    def change_value_of_8(self, card, choice):
        if choice == "1":
            new_suit = "♠"
            card.suit_value = "S"
        elif choice == "2":
            new_suit = "♣"
            card.suit_value = "C"
        elif choice == "3":
            new_suit = "♥"
            card.suit_value = "H"
        else:
            new_suit = "♦"
            card.suit_value = "D"
        card.card_name1 = "|   |"
        card.card_name2 = "| {} |".format(new_suit)
        card.card_name3 = "|   |"


class PlayableCharecter(Player):
    def __init__(self, player):
        Player.__init__(self, player)
    
    def merge_sort(self, arr):
        if len(arr) == 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        
        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            if left[i].value < right[j].value:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
        return arr

    def player_turn(self, remainder, deck):
        self.print_status(remainder)
        card_list = self.get_inp(remainder.get_card(), deck, remainder)
        for card in card_list:
            remainder.add_card(card)

    def get_inp(self, top_card, deck, remainder):
        again = False
        draw_count = 0
        while again is False:
            inp = input("choose a card: ")
            if inp.upper() == "D":
                if draw_count < 3:
                    prev_size = len(self.hand)
                    self.add_card(deck.deal(remainder))
                    if prev_size == len(self.hand):
                        print("No available cards in the deck nor in the remainder")
                        draw_count = 3
                    else:
                        draw_count += 1
                        self.print_status(remainder)
                else:
                    print("Can't draw any more cards")
            elif inp.upper() == "P":
                if draw_count == 3:
                    inp_card = []
                    again = True
                else:
                    print("You need to draw {} more cards to be able to pass".format(3-draw_count))
            elif inp.upper() == "S":
                self.hand = self.merge_sort(self.hand)
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
                    self.change_value_of_8(card, choice)    
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
        print("Too use more then 2 card use ' ' between the card")
        print("Your hand:")
        print(self)
        print("'D' to draw card,     'P' to pass,      'S' to sort cards")

class NPC(Player):
    def __init__(self, player):
        Player.__init__(self, player)
        self.available_card = []

    def print_status(self, remainder):
        print(self.player +" now has "+ str(len(self.hand)) + " cards left")

    def get_available_cards(self, top_card):
        available_card_list = []
        for card in self.hand:
            if self.is_allowed(card, top_card) or card.rank == 8:
                available_card_list.append(card)
        return available_card_list
    
    def draw_cards_if_needed(self, remainder, deck):
        self.available_card = self.get_available_cards(remainder.get_card())
        draw_counter = 0
        while len(self.available_card) == 0 and draw_counter < 3:   
            prev_size = len(self.hand)
            self.add_card(deck.deal(remainder)) 
            draw_counter +=1
            if prev_size == len(self.hand):  
                draw_counter = 3  
            card = self.hand[-1]
            if self.is_allowed(card, remainder.get_card()) or card.rank == 8:
                self.available_card.append(card)
        if draw_counter == 3:
            print(self.player, "passed")

class Easy(NPC):
    def __init__(self, player):
        Player.__init__(self, player)
        
    def player_turn(self, remainder, deck):
        self.draw_cards_if_needed(remainder, deck)
        if len(self.available_card) > 0:
            card = self.available_card[0]
            self.remove_card(card)
            if card.rank == 8:
                choice = random.choice(["S","C","H","D"])
                self.change_value_of_8(card, choice)
            
            remainder.add_card(card)
        self.print_status(remainder)
    
class Hard(NPC):
    def __init__(self, player):
        Player.__init__(self, player)
        
    def player_turn(self, remainder, deck):
        self.draw_cards_if_needed(remainder, deck)
        if len(self.available_card) > 0:
            card = self.available_card[0]
            self.remove_card(card)
            if card.rank == 8:
                choice = random.choice(["S","C","H","D"])
                self.change_value_of_8(card, choice)
            
            remainder.add_card(card)
        self.print_status(remainder)

def bua_til_leik():
    deck = Deck()
    deck.shuffle()
    players = []
    
    is_preset = input("Do you want preset game (Y/N): ").upper()
    if is_preset == "Y":
        player1 = PlayableCharecter("Player1")
        players.append(player1)
        npc1 = Easy("NPC1")
        players.append(npc1)
        nr_cards = 5
    else:

        while True:
            p_inp = input("How many playable charecters: ")
            if p_inp.isdigit()  and  0 <= int(p_inp) < 21:
                break
            else:
                print("Invalid input")
        p_inp = int(p_inp)
        for i in range(p_inp):
            players.append(PlayableCharecter("Player"+str(i+1)))

        while True:
            n_inp = input("How many NPC: ")
            if n_inp.isdigit() and 0 < (int(n_inp)+p_inp) < 21:
                break
            else:
                print("Invalid input")
        n_inp = int(n_inp)
        for i in range(n_inp):
            players.append(Hard("NPC"+str(i+1)))

        nr_cards = ""

        max_nr_cards = 52//(n_inp+p_inp)
        while True:
            nr_cards = input("How many card on hand? (MAX {}): ".format(max_nr_cards))
            if nr_cards.isdigit() and int(nr_cards) <= max_nr_cards:
                break
            else:
                print("Invalid input")
    for _ in range(int(nr_cards)):
        for player in players:
            player.add_card(deck.deal())
    remainder = Remainder(deck.deal())
    return deck, remainder, players

def main():
    deck, remainder, players = bua_til_leik()
    again = True
    while again == True:
        for player in players:              
            player.player_turn(remainder, deck)
            if len(player.hand) == 0:
                print("PLAYER", player.player, "WON!!!!!!!")
                again = False
                break
            print("_"*80)


main()
