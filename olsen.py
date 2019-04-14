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
        self.nr_of_card_types = {"H": 0, "S": 0, "D": 0, "C": 0, "8": 0}

    def add_card(self, card):
        self.cards.append(card)
        if card.rank == 8:
            self.nr_of_card_types["8"] += 1
        else:
            if card.suit == "H":
                self.nr_of_card_types["H"] += 1
            elif card.suit == "S":
                self.nr_of_card_types["S"] += 1
            elif card.suit == "C":
                self.nr_of_card_types["C"] += 1
            else:
                self.nr_of_card_types["D"] += 1  

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
        remainder.cards = []
        remainder.add_card(top_card)
        remainder.nr_of_card_types = {"H": 0, "S": 0, "D": 0, "C": 0, "8": 0}

    def __len__(self):
        return len(self.deck_list)

class Player():
    def __init__ (self, name):
        self.player = name
        self.hand = []
        self.nr_of_card_types = {"H": 0, "S": 0, "D": 0, "C": 0, "8": 0, "2":0, "3":0, "4":0}
       
    def is_allowed(self, inp_card, top_card):
        return inp_card.suit==top_card.suit_value or inp_card.rank==top_card.rank

    def add_card(self, denoting_card, remainder = None):
        if denoting_card is not None:
            if denoting_card.rank == 8:
                if self.nr_of_card_types["8"] > 0:
                    denoting_card.priority = 570
                else:
                    denoting_card.priority = 700
                self.nr_of_card_types["8"] += 1
            else:
                denoting_card.priority = 200
                if denoting_card.suit == "H":
                    self.nr_of_card_types["H"] += 1
                elif denoting_card.suit == "S":
                    self.nr_of_card_types["S"] += 1
                elif denoting_card.suit == "C":
                    self.nr_of_card_types["C"] += 1
                else:
                    self.nr_of_card_types["D"] += 1    

                same_rank_count = 0
                
                for card in self.hand:
                    if card.rank == denoting_card.rank:
                        card.priority += 200
                        same_rank_count += 1
                    elif card.suit == denoting_card.suit:
                        card.priority -= 1
                if remainder is not None:
                    for card in remainder.cards:
                        if card.rank == denoting_card.rank:
                            denoting_card.priority += 1
                if same_rank_count == 1:
                    self.nr_of_card_types["2"] += 1
                elif same_rank_count == 2:
                    self.nr_of_card_types["2"] -= 1
                    self.nr_of_card_types["3"] += 1
                    if self.nr_of_card_types["3"] > 1:
                        denoting_card.priority = 500
                        same_rank_count = 0
                elif same_rank_count == 3:
                    self.nr_of_card_types["3"] -= 1
                    self.nr_of_card_types["4"] += 1
                    if self.nr_of_card_types["4"] > 1:
                        denoting_card.priority = 550
                        same_rank_count = 0                    
                
                denoting_card.priority += 200 * same_rank_count
                denoting_card.priority -= self.nr_of_card_types[denoting_card.suit]
            self.hand.append(denoting_card)


    def remove_card(self, denoting_card):
        if denoting_card.rank == 8:
            self.nr_of_card_types["8"] -= 1
        elif denoting_card.suit == "H":
            self.nr_of_card_types["H"] -= 1
        elif denoting_card.suit == "S":
            self.nr_of_card_types["S"] -= 1
        elif denoting_card.suit == "C":
            self.nr_of_card_types["C"] -= 1
        else:
            self.nr_of_card_types["D"] -= 1    
        for card in self.hand:
            if card.suit == denoting_card.suit:
                card.priority += 1

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
        self.av_card_to_spare = []

    def print_status(self, remainder):
        print(self.player +" now has "+ str(len(self.hand)) + " cards left")

    def get_available_cards(self, top_card, skip = False):
        available_card_list = []
        self.av_card_to_spare = []
        for card in self.hand:
            if self.is_allowed(card, top_card) or card.rank == 8:
                if skip is True and card.priority > 600:
                    self.av_card_to_spare.append(card)
                else:
                    available_card_list.append(card)
        return available_card_list
    
    def draw_cards_if_needed(self, remainder, deck, skip = False):
        self.available_card = self.get_available_cards(remainder.get_card(), skip)
        draw_counter = 0
        if self.can_win() is False:
            while len(self.available_card) == 0 and draw_counter < 3:   
                prev_size = len(self.hand)
                self.add_card(deck.deal(remainder), remainder) 
                draw_counter += 1
                if prev_size == len(self.hand):  
                    draw_counter = 3  
                card = self.hand[-1]
                if self.is_allowed(card, remainder.get_card()) or (card.rank == 8 and self.nr_of_card_types["8"] > 1):
                    self.available_card.append(card)
            if draw_counter == 3:
                print(self.player, "passed")
    
    def can_win(self):
        if len(self.hand) < 5 and len(self.av_card_to_spare) > 0:
            if len(self.hand) == 1 and self.hand[0].rank == 8:
                self.available_card = self.av_card_to_spare
                return True

            for i in range(2,5): # skoður hvort hægt se að enda leikinn
                if len(self.hand) == i and self.nr_of_card_types[str(i)] > 0 and len(self.av_card_to_spare) > 0:
                    self.available_card = self.av_card_to_spare
                    return True
        return False

class Medium(NPC):
    def __init__(self, player):
        Player.__init__(self, player)
        
    def player_turn(self, remainder, deck):
        self.draw_cards_if_needed(remainder, deck)
        if len(self.available_card) > 0:
            min_card = self.available_card[0]
            if min_card.rank == 8:
                choice = random.choice(["1","2","3","4"])
                self.change_value_of_8(min_card, choice)
            card_list = [min_card]
            for card in self.hand:
                if min_card.rank == card.rank and min_card is not card:
                    card_list.append(card)
            for card in card_list:
                self.remove_card(card)
                remainder.add_card(card)
        self.print_status(remainder)
        if self.can_win() or len(self.hand) == 1:
            print("Óslen")

class Easy(NPC):
    def __init__(self, player):
        Player.__init__(self, player)
        
    def player_turn(self, remainder, deck):
        self.draw_cards_if_needed(remainder, deck)
        if len(self.available_card) > 0:
            card = self.available_card[0]
            self.remove_card(card)
            if card.rank == 8:
                choice = random.choice(["1","2","3","4"])
                self.change_value_of_8(card, choice)
            remainder.add_card(card)
        self.print_status(remainder)
        if self.can_win() or len(self.hand) == 1:
            print("Óslen")
        
class Hard(NPC):
    def __init__(self, player):
        Player.__init__(self, player)
        
    def best_choice_list(self):
        s = self.nr_of_card_types["S"]
        c = self.nr_of_card_types["C"]
        d = self.nr_of_card_types["D"]
        h = self.nr_of_card_types["H"]
        lis = [s,c,d,h]
        lis2 = []
        lis.sort()
        
        for i in range(4):
            if s == lis[i] and "S" not in lis2:
                lis2.append("S")
            elif c == lis[i] and "C" not in lis2:
                lis2.append("C")
            elif d == lis[i] and "D" not in lis2:
                lis2.append("D")
            else:
                lis2.append("H")
        return lis2

    def player_turn(self, remainder, deck):
        self.draw_cards_if_needed(remainder, deck, True)
        if len(self.available_card) > 0:
            choice_list = self.best_choice_list()
            min_card = self.available_card[0]
            for card in self.available_card:
                if card.priority < min_card.priority:
                    min_card = card
            card_list = [min_card]
            if min_card.rank == 8:
                choice = choice_list[0]
                self.change_value_of_8(min_card, choice)
                self.remove_card(min_card)
                remainder.add_card(min_card)

            else:
                for card in self.hand:
                    if min_card.rank == card.rank and min_card is not card:
                        card_list.append(card)
                if len(card_list) > 1:
                    self.nr_of_card_types[str(len(card_list))] -= 1
                    if len(card_list) > 2:
                        for i in range(1, len(card_list)):
                            for j in range(3):
                                if card_list[i].suit == choice_list[j]:
                                    top_card = card_list[i]
                                    card_list.remove(top_card)
                                    card_list.append(top_card)
                for card in card_list:
                    self.remove_card(card)
                    remainder.add_card(card)

        self.print_status(remainder)
        if self.can_win() or len(self.hand) == 1:
            print("Óslen")

def bua_til_leik():
    deck = Deck()
    deck.shuffle()
    players = []
    
    #is_preset = input("Do you want preset game (Y/N): ").upper()
    is_preset = "Y"
    if is_preset == "Y":
        #player1 = PlayableCharecter("Player1")
        #players.append(player1)
        npc1 = Hard("NPC1")
        players.append(npc1)
        npc3 = Medium("NPC medium")
        players.append(npc3)
        npc2 = Easy("NPC easy")
        players.append(npc2)
        nr_cards = 10
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
    easy_wins = 0
    hard_wins = 0
    medium_wins = 0
    for _ in range(1000):
        deck, remainder, players = bua_til_leik()
        again = True
        while again == True:
            for player in players:              
                player.player_turn(remainder, deck)
                if len(player.hand) == 0:
                    print("PLAYER", player.player, "WON!!!!!!!")
                    if player.player == "NPC1":
                        hard_wins += 1
                    elif player.player == "NPC medium":
                        medium_wins += 1
                    else:
                        easy_wins += 1
                    again = False
                    break

                print("_"*80)
    print("easy", easy_wins)
    print("medium", medium_wins)
    print("hard", hard_wins)


main()
