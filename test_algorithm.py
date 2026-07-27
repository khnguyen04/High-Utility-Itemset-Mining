"""
test_algorithm.py
=================

Description
-----------
Lightweight smoke-test suite for the ``AprioriTopK`` algorithm
(``src.algorithm``). Uses a small, hand-crafted transaction dataset
written to a temporary file so that no external data files are required
to run the tests.

Main Features
-------------
- Defines a self-contained sample transaction dataset (``SAMPLE_DATA``)
  that covers multiple item combinations and utility values.
- Writes the sample data to a ``tempfile`` and cleans it up automatically
  after each test, keeping the workspace free of test artefacts.
- Verifies that ``run_algorithm`` returns results sorted in descending
  order of utility.
- Verifies that the number of returned itemsets never exceeds K.

Usage
-----
Run directly as a script or via any test runner::

    # Run as a standalone script
    python test_algorithm.py

    # Run with pytest (auto-discovers test_ functions)
    pytest test_algorithm.py -v
"""

import os
import tempfile

from src.algorithm import AprioriTopK

SAMPLE_DATA = """\
3 5 1 2 4 6:30:1 3 5 10 6 5
3 5 2 4:20:3 3 8 6
3 1 4:8:1 5 2
3 5 1 7:27:6 6 10 5
3 5 2 7:11:2 3 4 2
"""


def _write_sample_file() -> str:
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w") as f:
        f.write(SAMPLE_DATA)
    return path


def test_run_algorithm_returns_sorted_results():
    k = 5
    m = 1
    path = _write_sample_file()
    try:
        algo = AprioriTopK(k=k, m=m)
        results = algo.run_algorithm(path)

        # Results must be sorted in descending order of utility
        utilities = [utility for utility, _ in results]
        assert utilities == sorted(utilities, reverse=True)

        # Do not exceed k results
        assert len(results) <= k
        print(results)
    finally:
        os.remove(path)


if __name__ == "__main__":
    test_run_algorithm_returns_sorted_results()
    print("OK")
