from dataclasses import dataclass

from connect_x.game_runner import GameRunner


@dataclass(frozen=True)
class SuiteStats:
    run_count: int
    win_ratios: dict[str, float]


class GameSuite:
    def __init__(self, runner: GameRunner, run_count: int) -> None:
        self._runner = runner
        self._run_count = run_count

    def run(self) -> SuiteStats:
        run_count = self._run_count
        win_counts = {}
        draw_count = 0
        for _ in range(run_count):
            result = self._runner.run()

            if result.is_draw:
                draw_count += 1
            else:
                win_counts[result.winner] = win_counts.get(result.winner, 0) + 1

        win_ratios={label: count / run_count for label, count in win_counts.items()}
        win_ratios["__DRAW__"] = draw_count / run_count

        return SuiteStats(
            run_count=run_count,
            win_ratios=win_ratios,
        )
