from connect_x.agent import Agent
from connect_x.game import AgentContext


class CLIUser(Agent):
    def _choose_column(self, context: AgentContext) -> int:
        return self._read_column(context)

    def _read_column(self, context: AgentContext) -> int:
        config = context.config
        column = None

        while column is None:
            # TODO: move to a func
            try:
                # self._clear()
                user_input = input(f"Your turn, choose from 0 to {config.width - 1}: ")
                column = int(user_input)

                if column < 0 or column >= config.width:  # or cell is not empty
                    raise ValueError(f"Column index is out of range.")
            except ValueError as exc:
                column = None  # reset
                print(exc)

        return column