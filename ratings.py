# -*- coding: utf-8 -*-
players = [
    ('Guybrush', 1000),
    ('Elaine', 1700),
    ('Monkey', 800),
    ('LeChuck', 1400),
    ('CrazySailor', 1100),
    ('TalkingHead', 1200),
    ('Largo', 1200),
    ('RonGilbert', 1800),
]


class Player(object):
    def __init__(self, first_name, last_name, rating, games_played):
        self.first_name = first_name
        self.last_name = last_name
        self.rating = rating
        self.number_of_games = games_played

    @property
    def games_played(self):
        return self.number_of_games

    @property
    def koef(self):
        if self.games_played <= 30:
            return 40
        if self.rating < 2400:
            return 20
        return 10

    def expected_value(self, rating_b):
        """
        Calculate expected value for player A
        :param rating_b: rating of the player B (opponent)
        :return: expected value (sum of win probability and draw probability)
        """

        return 1.0 / (1 + 10**float((rating_b - self.rating)/400.0))

    def calc_new_rating(self, player_b, game_result):
        """
        :param player_b: opponent
        :param game_result: only could be one of: 1.0, 0.5, 0.0
        :return: new rating of the player
        """
        expected = self.expected_value(player_b.rating)
        new_rating = self.rating + self.koef * (game_result - expected)
        return new_rating


def report_result(player_a, player_b, game_result):
    """
    Saves game result and modifies ratings of the players
    :param player_a: player A obj
    :param player_b: player B obj
    :param game_result: result of the game from A point of view (A wins => 1.0)
    :return:
    """
    player_a_new_rating = player_a.calc_new_rating(player_b, game_result)
    player_b_new_rating = player_b.calc_new_rating(player_a, 1.0 - game_result)

    # save to history. player A played white, B black. id, a_id, b_id, result.

    # save rating modifications
    player_a.rating = player_a_new_rating
    player_b.rating = player_b_new_rating



def calc_expected(rating_a, rating_b):
    """
    Calculate expected value for player A
    :param rating_a: rating of the player A
    :param rating_b: rating of the player B (opponent)
    :return: expected value (sum of win probability and draw probability)
    """

    return 1.0 / (1 + 10**float((rating_b - rating_a)/400.0))

if __name__ == '__main__':
    for player in players:
        expec = calc_expected(players[-1][1], player[1])
        print(
            'Expect for win of', players[-1][0], 'upon', player[0],
            '{0:.4f}'.format(expec)
        )
        print('    Win case:', (players[-1][1] + 20*(1.0 - expec)))
        print('    Draw case:', (players[-1][1] + 20*(0.5 - expec)))
        print('    Lose case:', (players[-1][1] + 20*(0.0 - expec)))

    player_a = Player(players[0][0], '', players[0][1], 0)
    player_b = Player(players[-1][0], '', players[-1][1], 70)
    print(player_a.rating)
    print(player_b.rating)
    report_result(player_a, player_b, 0.5)
    print("{:.2f}".format(player_a.rating))
    print("{:.2f}".format(player_b.rating))
    print('Success!!')