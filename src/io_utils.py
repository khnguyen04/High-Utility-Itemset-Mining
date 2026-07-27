"""
io_utils.py
===========

Description
-----------
Utility module for reading and parsing transaction data files used in
High-Utility Itemset Mining. Handles the standard HUIM file format where
each line encodes one transaction as three colon-separated fields:
item names, transaction utility, and per-item utilities.

Main Features
-------------
- Defines the ``Transaction`` type alias as a named tuple of
  (items, per-item utilities, transaction utility).
- Parses raw text files and skips comment lines that begin with
  ``#``, ``%``, or ``@``.
- Converts each valid line into a structured ``Transaction`` object
  ready for consumption by the mining algorithm.

Usage
-----
This module is imported internally by ``algorithm.py``::

    from src.io_utils import load_transactions

    transactions = load_transactions("data/chess.txt")
    for items, utilities, tx_utility in transactions:
        print(items, utilities, tx_utility)
"""

from typing import List, Tuple

# Datatype for 1 transaction: (list item, list utility, transaction utility)
Transaction = Tuple[List[str], List[int], int]


def load_transactions(input_file: str) -> List[Transaction]:
    """
    Load transaction data from input file.

    Args:
        input_file (str): Path to the input file.

    Returns:
        List[Transaction]: List of transactions.
    """
    transactions: List[Transaction] = []

    with open(input_file, "r") as f:
        for line in f:
            if not line.strip() or line[0] in ("#", "%", "@"):
                continue

            items_str, transaction_utility_str, utility_str = line.split(":")
            items = items_str.split()
            utilities = list(map(int, utility_str.split()))
            transaction_utility = int(transaction_utility_str.strip())

            transactions.append((items, utilities, transaction_utility))

    return transactions
