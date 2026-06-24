from __future__ import annotations

from typing import List, Dict, Tuple


def bubble_sort_tasks(tasks: List[Dict]) -> Tuple[List[Dict], int]:
    """
    Sort a list of task dictionaries using the bubble sort algorithm.

    Sorting Rules:
    1. Primary key: ``"priority"`` descending (higher priority first).
    2. Tiebreaker: ``"created_at"`` ascending (earlier timestamp first).
    3. ``"priority"`` is ``None``: these tasks are placed at the end,
       ordered by ``"created_at"`` ascending.

    The original list is not modified; a new sorted list is returned together
    with the total number of element swaps performed during sorting.

    Args:
        tasks: A list of dictionaries, each with the keys:
            - ``"name"`` (str): task name
            - ``"priority"`` (int or None): task priority
            - ``"created_at"`` (int): Unix timestamp

    Returns:
        A tuple containing:
        - ``sorted_tasks``: The sorted list of task dictionaries.
        - ``swap_count``: The total number of swaps performed.
    """
    # Create a shallow copy to avoid mutating the input list.
    arr = tasks[:]
    n = len(arr)
    swap_count = 0

    def is_less(a: Dict, b: Dict) -> bool:
        """
        Determine if task ``a`` should appear before task ``b`` in the sorted order.

        Returns:
            True if ``a`` precedes ``b``, False otherwise.
        """
        pa = a.get("priority")
        pb = b.get("priority")

        # Both priorities are None → sort by created_at ascending.
        if pa is None and pb is None:
            return a["created_at"] < b["created_at"]

        # ``a`` has None priority, ``b`` does not → ``a`` goes to the end.
        if pa is None:
            return False

        # ``b`` has None priority, ``a`` does not → ``a`` comes before ``b``.
        if pb is None:
            return True

        # Both priorities are integers.
        if pa != pb:
            # Higher priority comes first.
            return pa > pb

        # Same priority → sort by created_at ascending.
        return a["created_at"] < b["created_at"]

    # Classic bubble sort.
    for i in range(n):
        # After each outer iteration, the last ``i`` elements are sorted.
        for j in range(0, n - i - 1):
            if is_less(arr[j], arr[j + 1]):
                # Swap adjacent elements.
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swap_count += 1

    return arr, swap_count
