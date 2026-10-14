"""bubble_sort.py – Bubble‑sort implementation for task records.

The function sorts a list of task dictionaries according to the following rules:
1. Primary key: ``priority`` in descending order (higher priority first).
2. Tiebreaker: when priorities are equal, sort by ``created_at`` ascending
   (earlier timestamps first).
3. Tasks whose ``priority`` is ``None`` are placed after all tasks with a concrete
   priority and are ordered among themselves by ``created_at`` ascending.

The implementation follows the classic bubble‑sort algorithm, counts every swap,
and returns a new list without modifying the original input.
"""

from typing import List, Dict, Tuple

def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sort tasks using bubble sort.

    Parameters
    ----------
    tasks : list[dict]
        List of task dictionaries. Each dictionary must contain the keys
        ``"name"`` (str), ``"priority"`` (int or None) and ``"created_at"`` (int).

    Returns
    -------
    tuple[list[dict], int]
        A tuple ``(sorted_list, swap_count)`` where ``sorted_list`` is a new list
        containing the tasks in the required order and ``swap_count`` is the total
        number of element swaps performed during sorting.
    """
    # Create a shallow copy of each task to avoid mutating the original list.
    sorted_tasks: List[dict] = [task.copy() for task in tasks]
    n = len(sorted_tasks)
    swap_count = 0

    def should_swap(a: dict, b: dict) -> bool:
        """
        Determine whether element ``a`` (currently before ``b``) is out of order
        and must be moved after ``b`` according to the sorting rules.
        """
        a_pri = a.get("priority")
        b_pri = b.get("priority")
        a_ts = a.get("created_at")
        b_ts = b.get("created_at")

        # Both tasks have concrete priorities
        if a_pri is not None and b_pri is not None:
            if a_pri < b_pri:
                return True          # lower priority should come later
            if a_pri > b_pri:
                return False         # higher priority already before
            # Equal priorities → tie‑breaker by created_at ascending
            return a_ts > b_ts

        # a has None priority, b has a concrete priority → a must go after b
        if a_pri is None and b_pri is not None:
            return True

        # a has concrete priority, b is None → correct order (a before b)
        if a_pri is not None and b_pri is None:
            return False

        # Both priorities are None → order by created_at ascending
        return a_ts > b_ts

    # Classic bubble sort with early exit when no swaps occur
    for i in range(n):
        swapped = False
        # After each outer pass, the last i elements are already sorted
        for j in range(0, n - i - 1):
            if should_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                # Swap adjacent elements
                sorted_tasks[j], sorted_tasks[j + 1] = (
                    sorted_tasks[j + 1],
                    sorted_tasks[j],
                )
                swap_count += 1
                swapped = True
        if not swapped:
            break

    return (sorted_tasks, swap_count)
