import random
from abc import ABC

# SUIT = ['Буби', 'Черви', 'Пики', 'Крести']
# # Diamonds	Бубны
# # Hearts	Червы/черви
# # Spades	Пики
# # Clubs	Трефы
#
# CARDS_SET = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Туз', 'Король', 'Королева', 'Валет']
# # Ace - Туз
# # King - Крл
# # Q - Королева
# # Jack - Валет
#
# # По сути масти не важны и cards_set не нужен, хватает карты и её масти. ((4*13) * x), где x от 1 и до 4, x - число колодо участвующих в игре
denomination = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Король': 10, 'Королева': 10,
                'Валет': 10, 'Туз': 11}


# class Bank:
#     def __init__(self, balance):
#         self.player_balance = balance
#         self.bid_player: int | None = None


class Card:
    def __init__(self, suit: str, rank: int):
        self.suit: str = suit
        self.rank: int = rank
        self.value: int = self.get_value_by_card()

    def get_value_by_card(self) -> int:
        """Возвращает номинал карты

        :return: Номинал карты
        """
        if self.rank in ['Король', 'Королева', 'Валет']:
            return 10
        elif self.rank == 'Туз':
            return 11
        else:
            return int(self.rank)

    def __str__(self):
        return 'WTF'


class Deck:
    def __init__(self):
        self.suit: list = ['Буби', 'Черви', 'Пики', 'Крести']
        self.card_set: list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Туз', 'Король', 'Королева', 'Валет']
        self.deck: list = [(s, c) for s in self.suit for c in self.card_set]
        random.shuffle(self.deck)

    def deal_cars(self):  # элемент списка
        """Сдать карту"""
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards: list = []
        self.value_deck: int = 0

    def get_card(self, card):
        self.cards.append(card)
        self.value_deck = self.calculate_hand()

    def calculate_hand(self) -> int:
        sum = 0
        is_ace = False
        for el in self.cards:
            if el[1] in ('Туз', 'Ace'):
                is_ace = True
            sum += denomination[el[1]]
        if sum > 21 and is_ace:
            sum -= 10
        return sum

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)


class Player:

    def __init__(self, name: str, balance: int = 0):
        self.name: str = name
        self.hand: Hand = Hand()
        self.player_balance: int = balance

    def hit(self, deck: Deck):
        self.hand.get_card(deck.deal_cars())

    def stand(self):
        print(f'{self.name} stand with {self.hand.calculate_hand()} points and on hand - {self.hand.cards}.')

    def clear_hand(self):
        self.hand.cards = []


class Dealer(Player):
    def __init__(self):
        super().__init__('Dealer')

    def dealer_play(self, deck):
        while self.hand.calculate_hand() < 17:
            self.hit(deck=deck)


class Game:

    def __init__(self):
        self.deck = Deck()
        self.player: Player = Player(name='Doro')
        self.dealer: Dealer = Dealer()

    def calculate_result(self, bid: int) -> None:

        print(f'Счёт игрока - {self.player.hand.value_deck}')
        print(f'Счёт дилера - {self.dealer.hand.value_deck}')
        if self.player.hand.value_deck > 21:
            print('Player проиграл, сожалеем.')
            self.player.player_balance -= bid
        elif self.dealer.hand.value_deck > 21:
            print('Dealer проиграл, поздравляем с победой.')
            self.player.player_balance += bid
        elif self.player.hand.value_deck > self.dealer.hand.value_deck:
            print(
                f'Player победил, поздравляем, дилер проиграл. Результат: {self.player.hand.value_deck} > {self.dealer.hand.value_deck}')
            self.player.player_balance += bid
        elif self.player.hand.value_deck == self.dealer.hand.value_deck:
            print(f'Ничья! Результат: {self.player.hand.value_deck} = {self.dealer.hand.value_deck}')
        else:
            print('Дилер победил! Сожалеем.')
            self.player.player_balance -= bid

    def check_balance(self, bid: int) -> bool:
        return True if self.player.player_balance > bid else False

    def play_blackjack(self):
        print(f'!!!Black Jack!!!')

        self.player.player_balance = int(input('Какой у вас баланс на игру? '))
        is_play_again = True
        while self.player.player_balance > 0 and is_play_again:
            bid = int(input('Введите ставку игры - '))

            # Проверка, что игрок может играть на ставку:
            if not self.check_balance(bid=bid):
                # надо возвращать к вводу ставки,а не выходить
                break

            # Раздача карт
            self.player.hit(deck=self.deck)
            self.dealer.hit(deck=self.deck)
            self.player.hit(deck=self.deck)
            self.dealer.hit(deck=self.deck)

            # Ход игрока
            while self.player.hand.value_deck < 21:
                print(f'Ваша рука: {self.player.hand}')
                action = input('Ваш ход, будете брать ещё карту? (hit/stand/+/-): ').lower()
                if action in ('hit', '+'):
                    self.player.hit(deck=self.deck)
                elif action in ('stand', '-'):
                    self.player.stand()
                    break
                else:
                    print(f'Команда не понятна, введите одну из следующих (mehr, enogh')
                    continue

            # Ход дилера
            while self.dealer.hand.value_deck < 17:
                self.dealer.hit(deck=self.deck)
                print(f'Рука дилера: {self.dealer.hand}')

            # Считаем результаты
            self.calculate_result(bid=bid)

            print(f'Ваш банк = {self.player.player_balance}')
            question = input('Сыграть ещё раз? (+/-/Yes/No): ')
            if question in ('+', 'Yes'):
                self.player.clear_hand()
                self.dealer.clear_hand()
                is_play_again = True
            else:
                is_play_again = False


# def give_up():
#     # сдаться
#     pass
#
#
# def split_hand():
#     # сплит карт, доступно, если у игрока две одинаковые карты
#     pass
#
#
# def doubling_down():
#     # удвоить ставку
#     pass
#
#
# def insurance():
#     # страховка
#     pass
#
#
# def enough(player):
#     # хватит брать карты
#     pass


# play_blackjack()

game = Game()
game.play_blackjack()
