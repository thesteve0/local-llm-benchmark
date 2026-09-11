"""Bubble sort implementation for task records."""

from typing import Any


def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sort a list of task dictionaries using the bubble sort algorithm.

    Sorting order:
    - Primary: ``priority`` descending (higher priority comes first)
    - Tiebreaker: ``created_at`` ascending (earlier timestamp comes first) when priorities are equal
    - Null handling: tasks where ``priority`` is ``None`` always sort to the end,
      ordered by ``created_at`` ascending among themselves

    The original input list is **not** modified; a new sorted list is returned
    along with the total number of element swaps performed.

    Args:
        tasks: A list of task dictionaries. Each dictionary must contain:
            - "name" (str)
            - "priority" (int or None)
            - "created_at" (int)

    Returns:
        A tuple ``(sorted_tasks, swap_count)`` where:
        - ``sorted_tasks`` is a new list of task dictionaries sorted per the rules above.
        - ``swap_count`` is the total number of adjacent swaps performed during the sort.
    """
    # Shallow copy so the original list is never mutated
    sorted_tasks = list(tasks)
    n = len(sorted_tasks)
    swap_count = 0

    def _should_swap(a: dict, b: dict) -> bool:
        """
        Return True if element ``a`` should come after element ``b``
        (i.e., they are out of order according to the sorting rules).
        """
        a_pri = a["priority"]
        b_pri = b["priority"]
        a_ca = a["created_at"]
        b_ca = b["created_at"]

        # None priorities always go to the end
        if a_pri is None and b_pri is not None:
            return True
        if a_pri is not None and b_pri is None:
            return False
        if a_pri is None and b_pri is None:
            # Both None: earlier created_at first
            return a_ca > b_ca

        # Both have integer priorities: descending priority
        if a_pri < b_pri:
            return True          # a has lower priority → should move after b
        if a_pri > b_pri:
            return False         # a has higher priority → should move before b

        # Priorities equal: ascending created_at
        return a_ca > b_ca

    # Standard bubble sort with swap counting
    for i in range(n):
        for j in range(0, n - i - 1):
            if _should_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                sorted_tasks[j], sorted_tasks[j + 1] = (
                    sorted_tasks[j + 1],
                    sorted_tasks[j],
                )
                swap_count += 1

    return sorted_tasks, swap_count
