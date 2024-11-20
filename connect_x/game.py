from dataclasses import dataclass


@dataclass
class ConnectXConfig:
    width: int = 6
    height: int = 7
    x: int = 4  # number of subsequent token to win


class Token:
    def __init__(self, color: int) -> None:
        self._color = color

    @property
    def color(self) -> int:
        return self._color

    def clone(self) -> "Token":
        return Token(self.color)

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.color == other.color
        return False

    def __hash__(self):
        return hash(self._color)

    def __str__(self):
        return str(self._color)


# TODO: check best practices
class NonEmptyCell(Exception):
    pass


class Cell:
    def __init__(self) -> None:
        self._token: Token | None = None
        self._up_count: int = 0
        self._right_count: int = 0
        self._down_count: int = 0
        self._left_count: int = 0

    @property
    def token(self) -> Token | None:
        return self._token

    @property
    def is_empty(self) -> bool:
        return self._token is None

    @property
    def up_count(self) -> int:
        return self._up_count

    @property
    def right_count(self) -> int:
        return self._right_count

    @property
    def down_count(self) -> int:
        return self._down_count

    @property
    def left_count(self) -> int:
        return self._left_count

    def set_token(self, token: Token) -> None:
        if not self.is_empty:
            raise NonEmptyCell("The cell already has a token.")
        self._token = token

    def set_up_count(self, inc: int) -> None:
        self._up_count += inc

    def set_right_count(self, inc: int) -> None:
        self._right_count += inc

    def set_down_count(self, inc: int) -> None:
        self._down_count += inc

    def set_left_count(self, inc: int) -> None:
        self._left_count += inc


class InvalidInput(Exception):
    pass


class GameFinished(Exception):
    pass


@dataclass(frozen=True)
class AgentContext:
    config: ConnectXConfig
    grid: list[list[Cell]]  # TODO: Grid type


@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0

    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return self + (-other)

    def __mul__(self, scalar: int) -> "Point":
        return Point(scalar * self.x, scalar * self.y)

    def __rmul__(self, scalar: int) -> "Point":
        return self * scalar

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Game:
    def __init__(self, config: ConnectXConfig) -> None:
        self._config = config
        # TODO: Point based grid
        # TODO: change logic where (0, 0) is top left point
        self._grid = [[Cell() for _ in range(config.width)] for _ in range(config.height)]
        self._lowest_empty = [0] * config.width
        self._winner: Token | None = None
        self._token_count = 0

    @property
    def is_finished(self) -> bool:
        return self.has_winner or self.is_draw

    @property
    def winner(self) -> Token | None:
        return self._winner

    @property
    def has_winner(self) -> bool:
        return self.winner is not None

    @property
    def is_draw(self) -> bool:
        config = self._config
        max_token_count = config.height * config.width
        return self._token_count >= max_token_count

    def get_agent_context(self) -> AgentContext:
        return AgentContext(
            config=self._config,
            grid=self._grid,
        )

    def drop_token(self, column_idx: int, token: Token) -> None:
        if self.is_finished:
            raise GameFinished("Game is finished.")

        self._validate_input(column_idx)
        config = self._config

        row_idx = self._lowest_empty[column_idx]
        self._lowest_empty[column_idx] += 1

        cell = self._grid[row_idx][column_idx]
        cell.set_token(token)

        # update counters for the token dropped (right, down, left)
        curr_position = Point(x=column_idx, y=row_idx)
        right_cell = self._get_cell(curr_position + Point(x=1, y=0))
        if right_cell and right_cell.token == cell.token:
            cell.set_right_count(right_cell.right_count + 1)

        down_cell = self._get_cell(curr_position + Point(x=0, y=-1))
        if down_cell and down_cell.token == cell.token:
            cell.set_down_count(down_cell.down_count + 1)

        left_cell = self._get_cell(curr_position + Point(x=-1, y=0))
        if left_cell and left_cell.token == cell.token:
            cell.set_left_count(left_cell.left_count + 1)

        # update counters for adj
        if right_cell and right_cell.token == cell.token:
            right_cell.set_left_count(cell.left_count + 1)
        if down_cell and down_cell.token == cell.token:
            # TODO: check if need to check up_count
            down_cell.set_up_count(cell.up_count + 1)
        if left_cell and left_cell.token == cell.token:
            left_cell.set_right_count(cell.right_count + 1)

        # check for win
        if (cell.up_count + cell.down_count + 1 >= config.x
                or cell.right_count + cell.left_count + 1 >= config.x):
            self._winner = cell.token

        self._token_count += 1

    def _validate_input(self, column_idx: int) -> None:
        # should raise or return bool?
        if column_idx < 0 or column_idx >= self._config.width:
            raise InvalidInput("The column index is out of range.")
        if not self._grid[self._config.height - 1][column_idx].is_empty:
            raise InvalidInput("The cell is not empty.")

    def _get_cell(self, point: Point) -> Cell | None:
        config = self._config
        if (point.x < 0 or point.x >= config.width
                or point.y < 0 or point.y >= config.height):
            return None
        return self._grid[point.y][point.x]
