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

def equal_result(sum_player: int, sum_dealer: int) -> int:
    print(f'Счёт игрока - {sum_player}')
    print(f'Счёт дилера - {sum_dealer}')
    if sum_player > 21:
        print('Player проиграл, сожалеем.')
        return 0
    elif sum_dealer > 21:
        print('Dealer проиграл, поздравляем с победой.')
        return 1
    elif sum_player > sum_dealer:
        print(f'Player победил, поздравляем, дилер проиграл. Результат: {sum_player} > {sum_dealer}')
        return 1
    elif sum_player == sum_dealer:
        print(f'Ничья! Результат: {sum_player} = {sum_dealer}')
        return 2
    else:
        print('Дилер победил! Сожалеем.')
        return 0

def calculate_player_bank(player, bid: int):
    pass

def play_blackjack():
    print(f'!!!Приветствую в игре BlackJack!!!')

    players_bank = float(input('На сколько будете играть? Ввевдите сумму (это общая сумма, которая у вас есть на начало игры) = '))

    is_play_again = True
    while players_bank > 0 and is_play_again:
        bid = int(input('Введите ставку игры - '))
        start_deck = generate_deck(suit=SUIT, card_set=CARDS_SET)
        player_hand = [start_deck.pop(), start_deck.pop()]
        dealer_hand = [start_deck.pop(), start_deck.pop()]

        # Ход игрока
        while calculate_hand(player_hand) < 21:
            print(f'Ваша рука: {player_hand}')
            action = input('Ваш ход, будете брать ещё карту? (more/enogh/+/-): ').lower()
            if action in ('more', '+'):
                player_hand.append(start_deck.pop())
                print(f'У вас на руках: {player_hand}, ваш счёт: {calculate_hand(player_hand)}')
            elif action in ('enogh', '-'):
                break
            else:
                print(f'Команда не понятна, введите одну из следующих (mehr, enogh')
                continue

            # Ход дилера
        while calculate_hand(dealer_hand) < 17:
            dealer_hand.append(start_deck.pop())
            print(f'Рука дилера: {dealer_hand}')

        # Считаем результаты
        x = equal_result(sum_player=calculate_hand(player_hand), sum_dealer=calculate_hand(dealer_hand))
        if x == 1:
            players_bank += bid
        elif x == 2:
            continue
        else:
            players_bank -= bid

        print(f'Ваш банк = {players_bank}')
        question = input('Сыграть ещё раз? (+/-/Yes/No): ')
        if question in ('+', 'Yes'):
            is_play_again = True
        else:
            is_play_again = False


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