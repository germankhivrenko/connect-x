from abc import ABC
from abc import abstractmethod

from connect_x.game import Token
from connect_x.game import Game
from connect_x.game import AgentContext



class Agent(ABC):
    def __init__(self, label: str, token: Token) -> None:
        self._label = label
        self._token = token

    @property
    def label(self) -> str:
        return self._label

    @property
    def token(self) -> Token:
        return self._token

    def play(self, game: Game) -> None:
        context = game.get_agent_context()
        column = self._choose_column(context)
        game.drop_token(column, self._token.clone())

    @abstractmethod
    def _choose_column(self, context: AgentContext) -> int:
        ...
