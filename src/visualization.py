"""
visualization.py
================

Description
-----------
Visualization utilities for plotting runtime performance of the Apriori
Top-K High-Utility Itemset Mining algorithm. Provides a convenience
wrapper around Matplotlib to produce clean, labelled line charts that
compare algorithm execution time across different values of K.

Main Features
-------------
- Plots runtime (in seconds) against a sequence of K values on a
  Matplotlib line chart with markers.
- Supports optional custom Y-axis tick positions for fine-grained
  chart readability.
- Can save the generated figure to disk (PNG/SVG/PDF) via ``save_path``.
- Can suppress interactive display (e.g. for batch/headless runs) via
  the ``show`` flag.

Usage
-----
This module is invoked by ``main.py`` after all experiments finish::

    from src.visualization import plot_runtime

    plot_runtime(
        k_values=[100, 200, 300],
        times=[1.2, 3.4, 7.8],
        title="Chess",
        yticks=[0, 5, 10],
        save_path="outputs/Chess.png",
        show=True,
    )
"""

from typing import List, Optional, Sequence

import matplotlib.pyplot as plt


def plot_runtime(
    k_values: Sequence[int],
    times: Sequence[float],
    title: str,
    yticks: Optional[List[int]] = None,
    save_path: Optional[str] = None,
    show: bool = True,
) -> None:
    """
    Plot the runtime of the Apriori algorithm.
    
    Args:
        k_values: List of K values.
        times: Runtime corresponding to each K.
        title: Title of the plot (usually the name of the dataset).
        yticks: List of Y values to display (optional).
        save_path: Path to save the plot (optional).
        show: Whether to display the plot (default: True).
    """
    plt.figure(figsize=(6, 4))
    plt.plot(k_values, times, marker="o", color="r", label="Apriori")
    plt.xlabel("K")
    plt.ylabel("Run Time (seconds)")
    plt.title(title)
    plt.grid(True)
    plt.xticks(list(k_values))
    if yticks is not None:
        plt.yticks(yticks)
    plt.legend()

    if save_path:
        plt.savefig(save_path)
    if show:
        plt.show()
