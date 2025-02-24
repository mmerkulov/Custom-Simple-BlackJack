import random
from abc import ABC

SUIT = ['Буби', 'Черви', 'Пики', 'Крести']
# Diamonds	Бубны
# Hearts	Червы/черви
# Spades	Пики
# Clubs	Трефы

CARDS_SET = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Туз', 'Король', 'Королева', 'Валет']
# Ace - Туз
# King - Крл
# Q - Королева
# Jack - Валет

denomination = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Король': 10, 'Королева': 10, 'Валет': 10, 'Туз': 11}


# Туз = 1 or 11

def generate_deck(suit: list, card_set: list) -> list:
    deck = [(s, c) for s in suit for c in card_set]
    random.shuffle(deck)
    return deck


def get_card(player: list):
    return player.append(start_deck.pop())


def get_sum(deck: list) -> int:
    sum = 0
    is_ace = False
    for el in deck:
        if el[1] in ('Туз', 'Ace'):
            is_ace = True
        sum += denomination[el[1]]
    if sum > 21 and is_ace:
        sum -= 10
    print(sum)
    return sum

def equal_result(sum_player: int, sum_dealer: int) -> str:
    if sum_player> sum_dealer:
        return 'Player win!'
    elif sum_player == sum_dealer:
        return 'Draw!'
    else:
        return 'Dealer win!'

def play():
    x = 0
    great = input('Приветствие: ')
    while True:
        if x > 50:
            break


# max 52
start_deck = generate_deck(suit=SUIT, card_set=CARDS_SET)

my_hand = []
dealer_hand = []

print(start_deck)

get_card(player=my_hand)
get_card(player=my_hand)
get_card(player=my_hand)
print(my_hand)

get_card(player=dealer_hand)
get_card(player=dealer_hand)
get_card(player=dealer_hand)

print(dealer_hand)

x = get_sum(deck=my_hand)

y = get_sum(deck=dealer_hand)


