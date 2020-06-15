import random


def ask_numbers(question, low, high):
    # Checks if the answer is in given range
    check = None
    while check not in range(low, high):
        try:
            check = int(input(question))
        except ValueError:
            print("Podaj poprawną liczbe")
    return check


class Cards(object):
    # creates cards
    TYPES = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "D", "K", "A")
    COLORS = ("CZ", "DZ", "ŻY", "PI")

    def __init__(self, types, color):
        self.types = types
        self.color = color

    def __str__(self):
        info = self.types + " " + self.color
        return info


class Hand(object):
    # creates hand for each player

    def __init__(self):
        self.cards = []

    def __str__(self):
        # show information about card
        info = ""
        if self.cards:
            for card in self.cards:
                info += str(card) + "\t"
        else:
            info = "Empty hand"
        return info

    def add_card(self, card):
        # adds card
        self.cards.append(card)


class Deck(Hand):
    # creates deck to play

    def population(self):
        # Creates 52 unique cards
        for typ in Cards.TYPES:
            for color in Cards.COLORS:
                card = Cards(typ, color)
                self.cards.append(card)

    def give_cards(self, players_hands, per_toss=5):
        # deals a certain number of cards

        try:
            for i in range(per_toss):
                for player_hand in players_hands:
                    player_hand.add_card(self.cards[0])
                    self.cards.remove(self.cards[0])
        except:
            print("There are only 52 cards"
                  "\nAll of them will be deal")
            input("Press anything to continue")

    def shuffle(self):
        # shuffle deck/hand
        random.shuffle(self.cards)


class PlayerDeck(Hand):
    # Manage player hand

    def __init__(self, name, cemetery):
        # Add cemetery to hand
        super(PlayerDeck, self).__init__()
        self.name = name
        self.cemetery = cemetery

    def start_vs(self):
        # Take one card to single duel
        self.cards.pop(0)

    def add_to_cemetery(self, cards):
        # adds cards from duel to cemetery
        self.cemetery += cards

    def add_cemetery_to_hand(self):
        # Adds cards from cemetery to hand
        self.cards += self.cemetery
        random.shuffle(self.cards)
        self.cemetery.clear()


def fight(cards):
    # Creates a duel

    i = 0
    for card in cards:
        print(f"{card} - Player:{hands[i].name}")
        i += 1

    # defines values of the cards
    list_types = []
    for card in cards:
        x = Cards.TYPES.index(card.types)
        list_types.append(x)

    # defines value of the figure
    tuple(list_types)
    max_value = max(list_types)
    max_index = list_types.index(max_value)

    # Checks if there are the same figures in the duel
    remis_from_types = list_types.count(max_value)

    # If there are different figures card value wins
    while remis_from_types == 1:
        x = max_index
        print("Winning card: ", cards[x], "\nWinner of the round: ", end="")
        return x

    else:
        # If there is the same figure
        for card in cards:
            if str(cards[max_index].types) == str(card.types):
                if card.color == "CZ":
                    x = cards.index(card)
                    print("Winning card: ", card, "\nWinner of the round: ", end="")
                    return x

        for card in cards:
            if str(cards[max_index].types) == str(card.types):
                if card.color == "DZ":
                    x = cards.index(card)
                    print("Winning card: ", card, "\nWinner of the round: ", end="")
                    return x

        for card in cards:
            if str(cards[max_index].types) == str(card.types):
                if card.color == "ŻY":
                    x = cards.index(card)
                    print("Winning card: ", card, "\nWinner of the round: ", end="")
                    return x


class DefeatPlayer:
    # Creates informations about players who lost

    def __init__(self, name, turn):
        self.name = name
        self.turn = turn

    def __str__(self):
        info = "Player - " + self.name + " lost in " + str(self.turn) + " round"
        return info


# Creates deck and shuffle it
Deck = Deck()
Deck.population()
Deck.shuffle()

# Decides how many players take part in game
print("Welcome to the improved war-game")
number_of_players = ask_numbers("How many players will take part in war(2-4)?", low=2, high=4 + 1)

# Creates players and their decks
hands = []
for i in range(number_of_players):
    nick = input("Write your nick")
    nickName = PlayerDeck(nick, cemetery=[])
    hands.append(nickName)

Deck.give_cards(hands, ask_numbers("How many cards to give out to playerse", low=0, high=100))

number_of_rounds = 0
answer = None
list_of_losers = []

while answer != "end":
    # Adds card to duel
    fighting_cards = []

    for hand in hands:
        fighting_cards.append(hand.cards[0])
        hand.start_vs()

    print("=================War... War never changes====================")
    winner = fight(fighting_cards)
    print(hands[winner].name)
    number_of_rounds += 1

    # Adds cards to winner cemetery
    hands[winner].add_to_cemetery(fighting_cards)

    # adds cards from cemetery to players that have empty hand
    for hand in hands:
        if len(hand.cards) == 0:
            hand.add_cemetery_to_hand()

    # Creates list of losers and when they lost
    losers = []

    for hand in hands:
        if len(hand.cards) == 0:
            print("\nThis player lost: ", hand.name)
            loser = DefeatPlayer(hand.name, number_of_rounds)
            list_of_losers.append(loser)
            losers.append(hand)
            input("Press anything to continue")

    # Remove players who lost from the game
    for loos in losers:
        if loos in hands:
            hands.remove(loos)

    # Ends game if there is only oe player left
    if len(hands) == 1:
        answer = "end"

print("==================================================\nWINNER: ", hands[0].name)
list_of_losers.reverse()
for loser in list_of_losers:
    print(loser)
