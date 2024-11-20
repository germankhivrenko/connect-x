import os
import platform
from dataclasses import dataclass
import random

from connect_x.game import Game, ConnectXConfig
from connect_x.agent import Agent


@dataclass(frozen=True)
class GameResult:
    winner: str | None
    is_draw: bool


class GameRunner:
    def __init__(self, config: ConnectXConfig, agents: list[Agent]) -> None:
        self._config = config
        # copy and shuffle
        self._agents = agents[:]
        random.shuffle(self._agents)

    def run(self) -> GameResult:
        game = Game(self._config)

        # TODO: don't like it
        while not game.is_finished:
            for agent in self._agents:
                # TODO: make optional
                self._render(game.get_agent_context())  # TODO: agent_context -> context
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

    def _render(self, context) -> None:
        # TODO: move to CLI Render
        self._clear()
        config = context.config
        grid = context.grid
        for i in range(config.height - 1, -1, -1):
            row = "|"
            for j in range(config.width):
                row += " " if grid[i][j].is_empty else str(grid[i][j].token)
                row += "|"
            # row += "|"
            print(row)
            print("-" * len(row))

    def _clear(self) -> None:
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
