from connect_x.agents.cli_user import CLIUser
from connect_x.agents.random import Random
from connect_x.game import ConnectXConfig, Token
from connect_x.game_runner import GameRunner


def main():
    user = CLIUser("user", Token(1))
    random = Random("random", Token(2))
    config = ConnectXConfig()
    runner = GameRunner(config, agents=[user, random])

    result = runner.run()

    print(result)

if __name__ == "__main__":
    main()
