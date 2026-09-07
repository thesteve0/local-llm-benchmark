"""bubble_sort.py – Bubble sort implementation for task records."""

from typing import list, dict, tuple


def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sort a list of task dictionaries using the bubble sort algorithm.

    Sorting order:
    - Primary: ``priority`` descending (higher priority comes first)
    - Tiebreaker: ``created_at`` ascending (earlier timestamp comes first) when priorities are equal
    - Null handling: tasks where ``priority`` is ``None`` always sort to the end of the list,
      ordered by ``created_at`` ascending among themselves

    The original input list is **not** modified; a new sorted list is returned
    together with the total number of element swaps performed.

    Args:
        tasks: A list of dictionaries. Each dictionary must contain:
            - ``"name"`` (str)
            - ``"priority"`` (int or None)
            - ``"created_at"`` (int) – unix timestamp

    Returns:
        A tuple ``(sorted_list, swap_count)`` where:
        - ``sorted_list`` is a new list of task dictionaries ordered per the rules above.
        - ``swap_count`` is the total number of adjacent swaps executed by the bubble sort.

    Constraints:
        - The bubble sort algorithm is implemented manually; no built-in ``sort()``,
          ``sorted()``, or similar is used.
        - The original ``tasks`` list remains unchanged.
    """
    # Shallow copy so the original list is never mutated
    sorted_tasks = list(tasks)
    n = len(sorted_tasks)
    swap_count = 0

    # Determine whether two adjacent tasks are out of order.
    # Returns True if `a` (left) should come after `b` (right) → a swap is needed.
    def _needs_swap(a: dict, b: dict) -> bool:
        pa, pb = a["priority"], b["priority"]
        ca, cb = a["created_at"], b["created_at"]

        # Both priorities are None → sort by created_at ascending
        if pa is None and pb is None:
            return ca > cb

        # a has None priority, b does not → a must go to the end
        if pa is None:
            return True

        # b has None priority, a does not → a stays before b
        if pb is None:
            return False

        # Both have priorities: higher value comes first (descending)
        if pa < pb:
            return True
        if pa > pb:
            return False

        # Priorities are equal → sort by created_at ascending
        return ca > cb

    # Standard bubble sort passes
    for i in range(n):
        # After each outer iteration, the "heaviest" (first-in-order) element
        # has bubbled to the leftmost unsorted position, so we reduce the range.
        for j in range(n - 1 - i):
            if _needs_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                sorted_tasks[j], sorted_tasks[j + 1] = (
                    sorted_tasks[j + 1],
                    sorted_tasks[j],
                )
                swap_count += 1

    return sorted_tasks, swap_count


# ----------------------------------------------------------------------
# Example / quick self-test (can be removed or kept for manual verification)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    example_tasks = [
        {"name": "bug",     "priority": 3, "created_at": 1000},
        {"name": "feature", "priority": 5, "created_at": 2000},
        {"name": "docs",    "priority": 3, "created_at": 500},
    ]

    sorted_tasks, swaps = bubble_sort_tasks(example_tasks)
    print("Sorted tasks:", sorted_tasks)
    print("Swap count :", swaps)
    # Verify original list is untouched
    print("Original   :", example_tasks)
