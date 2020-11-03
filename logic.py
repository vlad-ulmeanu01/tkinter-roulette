from enum import Enum
import random
from collections import namedtuple


class TypeOfBet(Enum):
    SINGLE_NUMBER = 35
    SPLIT_BET = 17
    CORNER_BET = 8
    STREET_BET = 11
    LINE_BET = 2
    DOZENS = 0
    ODD_OR_EVEN = 1


class States(Enum):
    WIN = 0
    LOSS = 1
    NOT_ENOUGH_MONEY = 2


State = namedtuple("State", "state number won")
Player = namedtuple("Player", "name money number_of_games won_games money_won money_lost")


class Game:
    def __init__(self):
        self.players = [Player("Player1", 500, 0, 0, 0, 0), Player("Player2", 500, 0, 0, 0, 0),
                        Player("Computer", 500, 0, 0, 0, 0)]
        self.winning_numbers = []
        self.frequency = dict.fromkeys([x for x in range(36 + 1)], 0)

    def bet(self, player_id, amount, type_of_bet, numbers):  # player "player" makes a bet, returns state: win / loss
        # amount = the amount to be bet
        # type_of_bet = the type of bet; must have the type TypeOfBet
        # numbers = the numbers on which the bet was placed

        if self.players[player_id].money < amount:
            return State(States.NOT_ENOUGH_MONEY, 0)

        number = random.randint(1, 36)

        if type(numbers) is not list:
            print("Error in placing a bet, numbers is not a list")

        self.winning_numbers.append(number)
        self.frequency[number] = self.frequency[number]

        win = False
        if number in numbers:
            win = True

        if win:
            if type_of_bet is TypeOfBet.DOZENS:
                odds = 1
            else:
                odds = type_of_bet.value

            self.players[player_id] = Player(self.players[player_id].name,
                                             self.players[player_id].money + amount * odds,
                                             self.players[player_id].number_of_games + 1,
                                             self.players[player_id].won_games + 1,
                                             self.players[player_id].money_won + amount * odds,
                                             self.players[player_id].money_lost
                                             )

            return State(States.WIN, number, amount * odds)
        else:
            self.players[player_id] = Player(self.players[player_id].name,
                                             self.players[player_id].money - amount,
                                             self.players[player_id].number_of_games + 1,
                                             self.players[player_id].won_games,
                                             self.players[player_id].money_won,
                                             self.players[player_id].money_lost + amount
                                             )

            return State(States.LOSS, number, -amount)

    def get_player(self, player_id):  # gets a player
        return self.players[player_id]

    def computer_player_bet(self):
        max_value = 0
        max_key = 0
        for key, value in self.frequency.items():
            if max_value < value:
                max_value = value
                max_key = key

        return self.bet(2, 1, TypeOfBet.SINGLE_NUMBER, [max_key])
