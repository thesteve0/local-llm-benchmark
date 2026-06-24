"""
bubble_sort.py

Implements a bubble sort algorithm for a list of task dictionaries.

Each task dictionary must contain:
    - "name": str
    - "priority": int or None
    - "created_at": int (unix timestamp)

The sorting order is:
    1. Higher priority first (descending).
    2. For equal priorities, earlier creation time first (ascending).
    3. Tasks with ``None`` priority are placed at the end, ordered by creation time.

The function returns a tuple ``(sorted_list, swap_count)`` where ``swap_count`` is the
total number of element swaps performed during the sort. The original list is not
modified.
"""

from __future__ import annotations

from typing import List, Dict, Tuple


def _is_before(a: Dict[str, object], b: Dict[str, object]) -> bool:
    """
    Determine whether task ``a`` should appear before task ``b`` in the sorted order.

    Parameters
    ----------
    a, b: dict
        Task dictionaries with keys ``"priority"`` and ``"created_at"``.

    Returns
    -------
    bool
        ``True`` if ``a`` precedes ``b``, ``False`` otherwise.
    """
    # Both priorities are None → sort by created_at ascending
    if a["priority"] is None and b["priority"] is None:
        return a["created_at"] < b["created_at"]

    # Only ``a`` has None priority → ``a`` goes after ``b``
    if a["priority"] is None:
        return False

    # Only ``b`` has None priority → ``a`` goes before ``b``
    if b["priority"] is None:
        return True

    # Both priorities are not None
    if a["priority"] != b["priority"]:
        # Higher priority comes first
        return a["priority"] > b["priority"]

    # Equal priorities → earlier created_at comes first
    return a["created_at"] < b["created_at"]


def bubble_sort_tasks(tasks: List[Dict[str, object]]) -> Tuple[List[Dict[str, object]], int]:
    """
    Sort a list of task dictionaries using the bubble sort algorithm.

    The sorting follows these rules:
        - Primary key: ``"priority"`` descending (``None`` values are treated as lowest).
        - Secondary key: ``"created_at"`` ascending.
        - ``None`` priorities are placed at the end of the list, still sorted by ``"created_at"``.

    Parameters
    ----------
    tasks: list[dict]
        List of task dictionaries. Each dictionary must contain the keys
        ``"name"``, ``"priority"``, and ``"created_at"``.

    Returns
    -------
    tuple[list[dict], int]
        A new list containing the sorted tasks and the total number of swaps
        performed during the sort.

    Examples
    --------
    >>> tasks = [
    ...     {"name": "bug",     "priority": 3, "created_at": 1000},
    ...     {"name": "feature", "priority": 5, "created_at": 2000},
    ...     {"name": "docs",    "priority": 3, "created_at": 500},
    ... ]
    >>> sorted_tasks, swaps = bubble_sort_tasks(tasks)
    >>> swaps
    2
    >>> [t["name"] for t in sorted_tasks]
    ['feature', 'docs', 'bug']
    """
    # Work on a copy to avoid mutating the input
    sorted_tasks = list(tasks)
    n = len(sorted_tasks)
    swap_count = 0

    # Classic bubble sort: n-1 passes
    for i in range(n - 1):
        # After each pass, the largest element bubbles to position n-i-1
        swapped = False
        for j in range(0, n - i - 1):
            if not _is_before(sorted_tasks[j], sorted_tasks[j + 1]):
                # Swap adjacent elements
                sorted_tasks[j], sorted_tasks[j + 1] = sorted_tasks[j + 1], sorted_tasks[j]
                swap_count += 1
                swapped = True
        # If no swaps occurred, the list is already sorted
        if not swapped:
            break

    return sorted_tasks, swap_count
