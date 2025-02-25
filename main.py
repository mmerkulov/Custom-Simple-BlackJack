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

# По сути масти не важны и cards_set не нужен, хватает карты и её масти. ((4*13) * x), где x от 1 и до 4, x - число колодо участвующих в игре
denomination = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Король': 10, 'Королева': 10, 'Валет': 10, 'Туз': 11}

def generate_deck(suit: list, card_set: list) -> list:
    deck = [(s, c) for s in suit for c in card_set]
    random.shuffle(deck)
    return deck

def calculate_hand(deck: list) -> int:
    sum = 0
    is_ace = False
    for el in deck:
        if el[1] in ('Туз', 'Ace'):
            is_ace = True
        sum += denomination[el[1]]
    if sum > 21 and is_ace:
        sum -= 10
    return sum

def equal_result(sum_player: int, sum_dealer: int) -> str:
    if sum_player > 21:
        return 'Player проиграл, сожалеем.'
    elif sum_dealer > 21:
        return 'Dealer проиграл, поздравляем с победой.'
    elif sum_player > sum_dealer:
        return f'Player победил, поздравляем, дилер проиграл. Результат: {sum_player} > {sum_dealer}'
    elif sum_player == sum_dealer:
        return f'Ничья! Результат: {sum_player} = {sum_dealer}'
    else:
        return 'Дилер победил! Сожалеем.'

def put_money_in_bank():
    pass

def play_blackjack():
    print(f'!!!Приветствую в игре BlackJack!!!')
    start_deck = generate_deck(suit=SUIT, card_set=CARDS_SET)
    player_hand = [start_deck.pop(), start_deck.pop()]
    dealer_hand = [start_deck.pop(), start_deck.pop()]

    # Ход игрока
    while calculate_hand(player_hand) < 21:
        print(f'Ваша рука: {player_hand}')
        action = input('Ваш ход, будете брать ещё карту? (more/enogh): ').lower()
        if action == 'more':
            player_hand.append(start_deck.pop())
            print(f'У вас на руках: {player_hand}, ваш счёт: {calculate_hand(player_hand)}')
        elif action == 'enogh':
            break
        else:
            print(f'Команда не понятна, введите одну из следующих (mehr, enogh')
            continue

    # Ход дилера
    while calculate_hand(dealer_hand) < 17:
        dealer_hand.append(start_deck.pop())

    # Считаем результаты
    print(equal_result(sum_player=calculate_hand(player_hand), sum_dealer=calculate_hand(dealer_hand)))

def give_up():
    # сдаться
    pass

def split_hand():
    # сплит карт, доступно, если у игрока две одинаковые карты
    pass

def doubling_down():
    # удвоить ставку
    pass

def insurance():
    # страховка
    pass

def enough(player):
    # хватит брать карты
    pass


play_blackjack()