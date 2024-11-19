from connect_x.game import Game
from connect_x.game import ConnectXConfig
from connect_x.game import Token


def test_game():
    config = ConnectXConfig()
    game = Game(config)
    token_0 = Token(0)

    for _ in range(config.x):
        game.drop_token(0, token_0)

    assert game.is_finished
    assert game.winner == token_0
    assert not game.is_draw


def test_game_draw():
    config = ConnectXConfig(width=2, height=2, x=2)
    game = Game(config)
    token_0 = Token(0)
    token_1 = Token(1)

    game.drop_token(0, token_0)
    game.drop_token(0, token_1)
    game.drop_token(1, token_1)
    game.drop_token(1, token_0)

    assert game.is_finished
    assert game.is_draw
    assert not game.has_winner
