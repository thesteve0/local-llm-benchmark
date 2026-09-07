"""Bubble sort for task records with custom priority/timestamp ordering."""

from typing import list, dict, tuple


def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sort a list of task dictionaries using the bubble sort algorithm.

    Sorting rules:
    - Primary:  `"priority"` descending  (higher priority comes first)
    - Tiebreaker: when priorities are equal, sort by `"created_at"` ascending
                  (earlier timestamp comes first)
    - Null handling: tasks where `"priority"` is `None` always sort to the end,
      ordered by `"created_at"` ascending among themselves

    Args:
        tasks: A list of dictionaries. Each dict must contain:
               - "name"        : str
               - "priority"    : int or None
               - "created_at"  : int (unix timestamp)

    Returns:
        A tuple of `(sorted_list, swap_count)`:
        - sorted_list: a new list sorted per the rules above (original list unchanged)
        - swap_count: total number of adjacent swaps performed during sorting

    Constraints:
        - Implements bubble sort manually — no built-in `sort()`/`sorted()` used.
        - Does not modify the input list.
    """
    # Work on a shallow copy so the original list is never mutated
    sorted_tasks = tasks[:]
    n = len(sorted_tasks)
    swap_count = 0

    def _should_swap(a: dict, b: dict) -> bool:
        """
        Return True if task `a` should appear after task `b` (i.e. they are out of order).
        """
        pri_a, pri_b = a["priority"], b["priority"]
        ca, cb = a["created_at"], b["created_at"]

        # Both None → sort by created_at ascending
        if pri_a is None and pri_b is None:
            return ca > cb

        # a is None, b is not → None always goes to the end
        if pri_a is None:
            return True

        # b is None, a is not → a stays before the None block
        if pri_b is None:
            return False

        # Both have priorities
        if pri_a < pri_b:
            return True       # lower priority should come after
        if pri_a > pri_b:
            return False      # higher priority should come before

        # Priorities equal → sort by created_at ascending
        return ca > cb

    # Standard bubble sort with early termination
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if _should_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                sorted_tasks[j], sorted_tasks[j + 1] = (
                    sorted_tasks[j + 1],
                    sorted_tasks[j],
                )
                swap_count += 1
                swapped = True
        if not swapped:
            break

    return sorted_tasks, swap_count
tasks = [
    {"name": "bug",     "priority": 3, "created_at": 1000},
    {"name": "feature", "priority": 5, "created_at": 2000},
    {"name": "docs",    "priority": 3, "created_at": 500},
]

sorted_tasks, swaps = bubble_sort_tasks(tasks)
# sorted_tasks == [
#     {"name": "feature", "priority": 5, "created_at": 2000},
#     {"name": "docs",    "priority": 3, "created_at": 500},
#     {"name": "bug",     "priority": 3, "created_at": 1000},
# ]
# swaps == 2
