import random
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def add_card(self):  # элемент списка
        """Сдать одну карту"""
        return self.deck.pop()


class Hand:
    # # По сути масти не важны и cards_set не нужен, хватает карты и её масти. ((4*13) * x), где x от 1 и до 4, x - число колодо участвующих в игре
    DENOMINATION = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Король': 10,
                    'Королева': 10,
                    'Валет': 10, 'Туз': 11}

    def __init__(self):
        self.cards: list = []
        self.value_deck: int = 0

    def get_card(self, card):
        self.cards.append(card)
        self.value_deck = self.calculate_hand()

    def calculate_hand(self) -> int:
        result = 0
        is_ace = False
        for el in self.cards:
            if el[1] in ('Туз', 'Ace'):
                is_ace = True
            result += Hand.DENOMINATION[el[1]]
        if result > 21 and is_ace:
            result -= 10
        return result

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)


class Player:

    def __init__(self, name: str, balance: int = 0):
        self.name: str = name
        self.hand: Hand = Hand()
        self.balance: int = balance
        self.bet: int = 0

    def hit(self, deck: Deck) -> None:
        """Игрок берёт одну карту

        :param deck: Текущая игровая колода
        :return: None
        """
        self.hand.get_card(deck.add_card())

    def check_valid_bet(self, amount: int) -> int:
        """Сделать ставку

        :param amount: ставка
        :return: None
        """
        while True:
            try:
                if amount < 0:
                    logger.info('Ставка должна быть больше 0')
                elif amount > self.balance:
                    logger.info('Недостаточно средств для того, что бы сделать ставку')
                else:
                    return amount
            except ValueError:
                logger.error(f'Введено не корректное значение {amount}')

    def place_bet(self):
        """Размещает ставку."""
        bet = 0
        while isinstance(bet, int):
            amount = int(input('Введите ставку игры - '))
            bet = self.check_valid_bet(amount=amount)
        self.balance -= bet
        self.bet = bet
        logger.info(f"{self.name} делает ставку: {bet}")

    def stand(self) -> None:
        """Игрок больше не берёт карт, остановился

        :return: None
        """
        print(f'{self.name} stand with {self.hand.calculate_hand()} points and on hand - {self.hand.cards}.')
        logger.info(f'{self.name} stand with {self.hand.calculate_hand()} points and on hand - {self.hand.cards}.')

    def clear_hand(self) -> None:
        """Очистка "руки" игрока

        :return: None
        """
        self.hand.cards = []

    def double_down(self, deck: Deck) -> None:
        """Удвоить ставку

        :param deck: Текущая рука игрока
        :return:
        """
        if len(self.hand.cards) == 2:
            self.balance -= self.bet
            self.bet *= 2
            self.hit(deck=deck)


class Dealer(Player):
    def __init__(self):
        super().__init__('Dealer')

    def dealer_play(self, deck: Deck) -> None:
        while self.hand.calculate_hand() < 17:
            self.hit(deck=deck)
            print(f'Рука дилера => {self.hand.calculate_hand()}')


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
        elif self.dealer.hand.value_deck > 21:
            print('Dealer проиграл, поздравляем с победой.')
            self.player.balance += bid
        elif self.player.hand.value_deck > self.dealer.hand.value_deck:
            print(
                f'Player победил, поздравляем, дилер проиграл. Результат: {self.player.hand.value_deck} > {self.dealer.hand.value_deck}')
            self.player.balance += bid
        elif self.player.hand.value_deck == self.dealer.hand.value_deck:
            print(f'Ничья! Результат: {self.player.hand.value_deck} = {self.dealer.hand.value_deck}')
        else:
            print('Дилер победил! Сожалеем.')

    def check_balance(self, bid: int) -> bool:
        return True if self.player.balance > bid else False

    def clean_all_hands(self) -> None:
        """Очищаем все руки

        :return: None
        """
        self.player.clear_hand()
        self.dealer.clear_hand()

    def play_blackjack(self):
        print(f'!!!Black Jack!!!')

        self.player.balance = int(input('Какой у вас баланс на игру? '))
        is_play_again = True
        while self.player.balance > 0 and is_play_again:
            # Проверка, что игрок может играть на ставку:
            self.player.place_bet()

            # Раздача карт
            self.player.hit(deck=self.deck)
            self.dealer.hit(deck=self.deck)
            self.player.hit(deck=self.deck)
            self.dealer.hit(deck=self.deck)

            # Ход игрока
            while self.player.hand.value_deck < 21:
                print(f'Ваша рука: {self.player.hand}')
                action = input('Ваш ход, будете брать ещё карту? (hit/stand/+/-/double/*): ').lower()
                if action in ('hit', '+'):
                    self.player.hit(deck=self.deck)
                elif action in ('double', '*'):
                    self.player.double_down(deck=self.deck)
                elif action in ('stand', '-'):
                    self.player.stand()
                    break
                else:
                    print(f'Команда не понятна, введите одну из следующих (mehr, enogh')
                    continue

            # Ход дилера
            self.dealer.dealer_play(deck=self.deck)
            # while self.dealer.hand.value_deck < 17:
            #     self.dealer.hit()
            #     print(f'Рука дилера: {self.dealer.hand}')

            # Считаем результаты
            self.calculate_result(bid=bet)

            print(f'Ваш банк = {self.player.balance}')
            question = input('Сыграть ещё раз? (+/-/Yes/No): ')
            if question in ('+', 'Yes'):
                self.clean_all_hands()
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


if __name__ == '__main__':
    game = Game()
    game.play_blackjack()
