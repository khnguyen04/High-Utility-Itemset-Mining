import heapq
from collections import defaultdict
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import time
class AprioriTopK:
    """
    A class for implementing the Apriori algorithm to find the top-K high-utility itemsets from a transaction dataset.
    
    Attributes:
        k (int): The number of top patterns to find. It defines how many of the most useful itemsets to return.
        min_utility (int): The minimum utility threshold for frequent itemsets.
        priority_queue (List[Tuple[int, List[str]]]): A min-heap (priority queue) used to store the top-K itemsets, each element is a tuple 
                                                   containing the utility and the itemset.
        itemsets (List[Tuple[int, List[str]]]): A list of the top-K itemsets along with their utilities, sorted by utility.
        mapItemToTWU (Dict[str, int]): A dictionary mapping items (represented as strings) to their total utility (TWU).
    """
    
    def __init__(self, k: int, m: int) -> None:
        """
        Initializes the AprioriTopK class with the given parameters.
        
        Args:
            k (int): The number of top patterns to find.
            m (int): The minimum utility threshold for frequent itemsets.
        """
        self.k = k                  # Number of top patterns to find
        self.min_utility = m        # Dynamic minimum utility
        self.priority_queue = []    # Min-heap to keep top-k patterns
        self.itemsets = []          # Store final top-k patterns
        self.mapItemToTWU = {}      # Map to store TWU of items

    def run_algorithm(self, input_file: str) -> List[Tuple[int, List[str]]]:
        """
        Runs the Apriori algorithm to find the top-K high-utility itemsets.

        Args:
            input_file (str): The path to the input file containing transaction data.

        Returns:
            List[Tuple[int, List[str]]]: A sorted list of the top-K itemsets, where each itemset is a tuple
                                          of its utility and a list of items in the itemset.
        """
        transactions = []

        # Parse transactions and calculate TWU
        with open(input_file, 'r') as f:
            for line in f:
                # Skip comments and empty lines
                if not line.strip() or line[0] in ['#', '%', '@']:
                    continue

                items_str, transaction_utility_str, utility_str = line.split(':')
                items = list(items_str.split())  # List of items in the transaction
                utilities = list(map(int, utility_str.split()))  # List of utility values for each item
                transaction_utility = int(transaction_utility_str.strip())

                # Record transaction data
                transactions.append((items, utilities, transaction_utility))

                # Update TWU for each item
                for i, item in enumerate(items):
                    self.mapItemToTWU[item] = self.mapItemToTWU.get(item, 0) + utilities[i]

        # Filter items based on TWU
        frequent_items = {
            item: twu for item, twu in self.mapItemToTWU.items()
            if twu >= self.min_utility
        }

        # Generate frequent itemsets of size > 1
        current_itemsets = [[item] for item in frequent_items.keys()]
        k = 2
        while current_itemsets:
            candidates = self._generate_candidates(current_itemsets, k)
            candidate_utility = defaultdict(int)

            # Calculate utility for candidates
            for transaction_items, utilities, _ in transactions:
                item_to_utility = dict(zip(transaction_items, utilities))
                for candidate in candidates:
                    # Check if all items in candidate appear in the transaction
                    if all(item in item_to_utility for item in candidate):
                        # Add the utility of the items in candidate if they exist in transaction
                        candidate_utility[tuple(candidate)] += sum(item_to_utility[item] for item in candidate)

            # Filter candidates based on min_utility
            high_utility_itemsets = {
                tuple(candidate): utility
                for candidate, utility in candidate_utility.items()
                if utility >= self.min_utility and len(candidate) > 1  # Exclude single items
            }

            # Add to priority queue
            for itemset, utility in high_utility_itemsets.items():
                self._save_itemset_to_queue(list(itemset), utility)

            # Update the list of current itemsets for the next iteration
            current_itemsets = [list(itemset) for itemset in high_utility_itemsets.keys()]
            k += 1

        # Store top-k patterns
        self.itemsets = sorted(
            [(utility, itemset) for utility, itemset in self.priority_queue],
            key=lambda x: (-x[0], x[1])
        )
        return self.itemsets

    def _generate_candidates(self, itemsets: List[List[str]], k: int) -> List[List[str]]:
        """
        Generate candidates of size k from itemsets of size k-1.
        
        Args:
            itemsets (List[List[str]]): A list of itemsets (where each itemset is a list of strings representing items).
            k (int): The size of the candidates to generate.

        Returns:
            List[List[str]]: A list of candidates, where each candidate is a list of items.
        """
        candidates = []  
        seen_candidates = set()  
        itemsets = sorted(itemsets)  

        for i in range(len(itemsets)):
            for j in range(i + 1, len(itemsets)):
                candidate = sorted(set(itemsets[i]) | set(itemsets[j]))
                if len(candidate) == k:
                    # Convert candidate to tuple so it can be added to a set (since sets can't contain lists).
                    candidate_tuple = tuple(candidate)
                    if candidate_tuple not in seen_candidates:
                        candidates.append(candidate)
                        seen_candidates.add(candidate_tuple)  # Add candidate to the seen set.

        return candidates

    def _save_itemset_to_queue(self, itemset: List[str], utility: int) -> None:
        """
        Save an itemset to the priority queue and maintain the top-K invariant.

        Args:
            itemset (List[str]): A list of items in the itemset.
            utility (int): The utility of the itemset.
        """
        heapq.heappush(self.priority_queue, (utility, itemset))
        if len(self.priority_queue) > self.k:
            heapq.heappop(self.priority_queue)
        if len(self.priority_queue) == self.k:
            self.min_utility = self.priority_queue[0][0]


if __name__ == "__main__":
    # chess 
    input_file = "chess.txt"
    minU = 60000
    title = 'Chess'
    yti = [0, 5, 10, 15, 20] 

    # # mushroom 
    # input_file = "mushroom.txt"
    # minU = 80000
    # title = 'Mushroom'
    # yti = [0, 5, 10, 15, 20]

    # # connect
    # input_file = "connect.txt"
    # minU = 1350000
    # title = 'Connect'
    # yti = [0, 40, 80, 120]
  
    # process
    k_val = [100, 200, 300, 400, 500, 600]
    times = []
    re = []
    for i in range(6):
        start = time.time()
        al = AprioriTopK(k_val[i], minU)
        result = al.run_algorithm(input_file)
        ex = time.time() - start
        times.append(ex)
        re.append(len(result))
        print(f'Done k = {k_val[i]} has {len(result)} results in {ex} seconds')

    
    # Vẽ đồ thị 
    plt.figure(figsize=(6, 4))
    plt.plot(k_val, times, marker='o', color='r', label='Apriori')
    plt.xlabel('K')
    plt.ylabel('Run Time (seconds)')
    plt.title(title)
    plt.grid(True)
    plt.xticks(k_val)
    plt.yticks(yti)             
    plt.legend()
    # plt.savefig(f'{title}.png')
    plt.show()