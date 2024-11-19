from connect_x.agent import Agent
from connect_x.game import AgentContext
import random


class Random(Agent):
    def _choose_column(self, context: AgentContext) -> int:
        config = context.config
        grid = context.grid
        return random.choice([i for i in range(config.width) if grid[config.height - 1][i].is_empty])
