from connect_x.agents.random import Random
from connect_x.game import ConnectXConfig, Token
from connect_x.game_runner import GameRunner
from connect_x.game_suite import GameSuite


def main():
    random_1 = Random("random_1", Token(1))
    random_2 = Random("random_2", Token(2))
    config = ConnectXConfig()
    runner = GameRunner(config, agents=[random_1, random_2])
    suite = GameSuite(runner, 100)

    stats = suite.run()

    print(stats)

if __name__ == "__main__":
    main()
