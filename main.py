"""
main.py
=======

Description
-----------
Entry-point script for running benchmark experiments with the Apriori
Top-K High-Utility Itemset Mining algorithm across multiple values of K.
Measures wall-clock execution time for each run and produces a runtime
comparison line chart using Matplotlib.

Main Features
-------------
- Pre-configured dataset profiles (Chess, Mushroom, Connect) that specify
  the input file path, initial minimum utility threshold, chart title, and
  Y-axis ticks.
- Iterates over a fixed sequence of K values (100 – 600) and records the
  execution time and number of discovered itemsets for each run.
- Delegates mining to ``AprioriTopK`` (``src.algorithm``) and chart
  rendering to ``plot_runtime`` (``src.visualization``).
- Optionally saves the output chart to ``outputs/<Dataset>.png`` and/or
  suppresses the interactive display window.

Usage
-----
Run from the project root directory with the virtual environment active::

    # Default dataset (chess), show plot interactively
    python main.py

    # Choose a specific dataset
    python main.py --dataset mushroom

    # Save the figure without displaying it
    python main.py --dataset connect --save-fig --no-show

Available CLI arguments:
    --dataset   {chess, mushroom, connect}  Dataset to benchmark (default: chess)
    --save-fig                              Save the chart to outputs/<Dataset>.png
    --no-show                               Do not open the interactive plot window
"""

import argparse
import time
from dataclasses import dataclass
from typing import List

from src.algorithm import AprioriTopK
from src.visualization import plot_runtime


@dataclass
class DatasetConfig:
    input_file: str
    min_utility: int
    title: str
    yticks: List[int]


# Dataset configs
DATASETS = {
    "chess": DatasetConfig(
        input_file="data/chess.txt",
        min_utility=60000,
        title="Chess",
        yticks=[0, 5, 10, 15, 20],
    ),
    "mushroom": DatasetConfig(
        input_file="data/mushroom.txt",
        min_utility=80000,
        title="Mushroom",
        yticks=[0, 5, 10, 15, 20],
    ),
    "connect": DatasetConfig(
        input_file="data/connect.txt",
        min_utility=1350000,
        title="Connect",
        yticks=[0, 40, 80, 120],
    ),
}

K_VALUES = [100, 200, 300, 400, 500, 600]


def run(dataset_name: str, save_fig: bool = False, show_fig: bool = True) -> None:
    """Run algorithm for a dataset and plot the runtime."""
    config = DATASETS[dataset_name]

    times: List[float] = []
    result_counts: List[int] = []

    for k in K_VALUES:
        start = time.time()
        algo = AprioriTopK(k, config.min_utility)
        result = algo.run_algorithm(config.input_file)
        elapsed = time.time() - start

        times.append(elapsed)
        result_counts.append(len(result))
        print(f"Done k = {k} has {len(result)} results in {elapsed} seconds")

    save_path = f"outputs/{config.title}.png" if save_fig else None
    plot_runtime(
        K_VALUES,
        times,
        config.title,
        yticks=config.yticks,
        save_path=save_path,
        show=show_fig,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Algorithm")
    parser.add_argument(
        "--dataset",
        choices=list(DATASETS.keys()),
        default="chess",
        help="Dataset to run",
    )
    parser.add_argument(
        "--save-fig",
        action="store_true",
        help="Save figure to file",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Don't show figure",
    )
    args = parser.parse_args()

    run(args.dataset, save_fig=args.save_fig, show_fig=not args.no_show)


if __name__ == "__main__":
    main()
