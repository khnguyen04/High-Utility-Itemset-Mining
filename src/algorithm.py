"""
algorithm.py
============

Description
-----------
Implementation of the Apriori Top-K High-Utility Itemset Mining algorithm.
The algorithm uses a level-wise (breadth-first) candidate generation strategy
combined with a min-heap to maintain the K highest-utility itemsets found so far.
The minimum utility threshold is raised dynamically as the heap fills up,
enabling aggressive pruning of low-utility candidates.

Main Features
-------------
- Computes the Transaction Weighted Utility (TWU) for each item to prune
  unpromising items early before the main search begins.
- Generates candidate itemsets of size k by joining itemsets of size k-1
  using the Apriori join step.
- Calculates the actual utility of each candidate against the full transaction
  database.
- Maintains the Top-K result set using a min-heap for memory-efficient storage.
- Dynamically raises ``min_utility`` once the heap reaches capacity K, using
  the smallest utility in the heap as the new pruning threshold.

Usage
-----
This module is invoked through ``main.py``. To use it directly::

    from src.algorithm import AprioriTopK

    algo = AprioriTopK(k=100, m=60000)
    results = algo.run_algorithm("data/chess.txt")
    for utility, itemset in results:
        print(utility, itemset)
"""

import heapq
from collections import defaultdict
from typing import Dict, List, Tuple

from .io_utils import Transaction, load_transactions

Itemset = List[str]
UtilityItemset = Tuple[int, Itemset]

class AprioriTopK:
    """
    Implement Apriori algorithm to find the top-K high-utility itemsets
    from a set of transactions.

    Attributes:
        k: Number of top-K patterns to find.
        min_utility: Minimum utility threshold (dynamically updated during the running process to prune candidates).
        priority_queue: Min-heap save top-K itemset, each element is a tuple (utility, itemset).
        itemsets: List of top-K itemsets, sorted by utility.
        mapItemToTWU: Dict mapping items to their total TWU (Transaction Weighted Utility).
    """

    def __init__(self, k: int, m: int) -> None:
        """
        Args:
            k: Number of top-K patterns to find.
            m: Initial minimum utility threshold.
        """
        self.k = k
        self.min_utility = m
        self.priority_queue: List[UtilityItemset] = []
        self.itemsets: List[UtilityItemset] = []
        self.mapItemToTWU: Dict[str, int] = {}

    def run_algorithm(self, input_file: str) -> List[UtilityItemset]:
        """
        Run the algorithm on the transaction dataset and return top-K itemsets.

        Args:
            input_file: Path to the transaction data file.

        Returns:
            List of top-K itemsets, each element is a tuple (utility, itemset),
            sorted by utility in descending order.
        """
        transactions: List[Transaction] = load_transactions(input_file)

        # Calculate TWU for each item
        self.mapItemToTWU = {}
        for items, utilities, _ in transactions:
            for i, item in enumerate(items):
                self.mapItemToTWU[item] = self.mapItemToTWU.get(item, 0) + utilities[i]

        # Filter item by TWU
        frequent_items = {
            item: twu
            for item, twu in self.mapItemToTWU.items()
            if twu >= self.min_utility
        }

        # Generate itemset with size > 1
        current_itemsets = [[item] for item in frequent_items.keys()]
        k = 2
        while current_itemsets:
            candidates = self._generate_candidates(current_itemsets, k)
            candidate_utility: Dict[Tuple[str, ...], int] = defaultdict(int)

            for transaction_items, utilities, _ in transactions:
                item_to_utility = dict(zip(transaction_items, utilities))
                for candidate in candidates:
                    if all(item in item_to_utility for item in candidate):
                        candidate_utility[tuple(candidate)] += sum(
                            item_to_utility[item] for item in candidate
                        )

            high_utility_itemsets = {
                candidate: utility
                for candidate, utility in candidate_utility.items()
                if utility >= self.min_utility and len(candidate) > 1
            }

            for itemset, utility in high_utility_itemsets.items():
                self._save_itemset_to_queue(list(itemset), utility)

            current_itemsets = [list(itemset) for itemset in high_utility_itemsets.keys()]
            k += 1

        self.itemsets = sorted(
            [(utility, itemset) for utility, itemset in self.priority_queue],
            key=lambda x: (-x[0], x[1]),
        )
        return self.itemsets

    def _generate_candidates(self, itemsets: List[Itemset], k: int) -> List[Itemset]:
        """
        Generate candidate with size k from itemset with size k-1.

        Args:
            itemsets: list of itemset.
            k: size of candidate.

        Returns:
            List of candidate, no duplicate.
        """
        candidates: List[Itemset] = []
        seen_candidates = set()
        itemsets = sorted(itemsets)

        for i in range(len(itemsets)):
            for j in range(i + 1, len(itemsets)):
                candidate = sorted(set(itemsets[i]) | set(itemsets[j]))
                if len(candidate) == k:
                    candidate_tuple = tuple(candidate)
                    if candidate_tuple not in seen_candidates:
                        candidates.append(candidate)
                        seen_candidates.add(candidate_tuple)

        return candidates

    def _save_itemset_to_queue(self, itemset: Itemset, utility: int) -> None:
        """
        Save itemset to priority queue and maintain top-K invariant.

        Args:
            itemset: itemset to save.
            utility: utility corresponding to itemset.
        """
        heapq.heappush(self.priority_queue, (utility, itemset))
        if len(self.priority_queue) > self.k:
            heapq.heappop(self.priority_queue)
        if len(self.priority_queue) == self.k:
            self.min_utility = self.priority_queue[0][0]
