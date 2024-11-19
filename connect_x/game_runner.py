from dataclasses import dataclass

from connect_x.game import Game, ConnectXConfig
from connect_x.agent import Agent


@dataclass(frozen=True)
class GameResult:
    winner: str | None
    is_draw: bool


class GameRunner:
    def __init__(self, config: ConnectXConfig, agents: list[Agent]) -> None:
        self._config = config
        self._agents = agents

    def run(self) -> GameResult:
        game = Game(self._config)

        # TODO: don't like it
        while not game.is_finished:
            for agent in self._agents:
                agent.play(game)
                if game.is_finished:
                    break

        winner_label = None
        for agent in self._agents:
            if game.winner == agent.token:
                winner_label = agent.label

        return GameResult(
            winner=winner_label,
            is_draw=game.is_draw,
        )
