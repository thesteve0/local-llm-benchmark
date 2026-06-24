# Code Eval: Mellum2-12B-A2.5B-Thinking-Q6_K

## Prompt

# Bubble Sort Tasks — Python

Implement a bubble sort function for task records.

## Requirements

Write a single file `bubble_sort.py` containing a function with this exact signature:

```python
def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
```

Each task dictionary has these keys:
- `"name"`: `str` — task name
- `"priority"`: `int` or `None` — task priority
- `"created_at"`: `int` — unix timestamp

### Sorting Rules

1. **Primary:** sort by `"priority"` descending (higher priority comes first)
2. **Tiebreaker:** when priorities are equal, sort by `"created_at"` ascending (earlier timestamp comes first)
3. **Null handling:** tasks where `priority` is `None` always sort to the end of the list, ordered by `"created_at"` ascending among themselves

### Constraints

- You must implement the bubble sort algorithm — do not use Python's built-in `sort()`, `sorted()`, or any other sorting function
- Return a tuple of `(sorted_list, swap_count)` where `swap_count` is the total number of element swaps performed during sorting
- Do not modify the original input list — return a new list

### Example

```python
tasks = [
    {"name": "bug",     "priority": 3, "created_at": 1000},
    {"name": "feature", "priority": 5, "created_at": 2000},
    {"name": "docs",    "priority": 3, "created_at": 500},
]

sorted_tasks, swaps = bubble_sort_tasks(tasks)
# sorted_tasks = [
#     {"name": "feature", "priority": 5, "created_at": 2000},
#     {"name": "docs",    "priority": 3, "created_at": 500},
#     {"name": "bug",     "priority": 3, "created_at": 1000},
# ]
# swaps = 2
```

Write clean, well-documented, idiomatic Python code. Include type hints and a docstring.


## Reasoning

We need to implement bubble_sort_tasks. Must not use built-in sort. Must return new list and swap count.

We need to define comparison function based on rules: primary priority descending, tiebreaker created_at ascending. Null priority goes to end, ordered by created_at ascending.

Bubble sort: iterate n times, each pass compare adjacent elements, swap if out of order. Count swaps.

We need to copy input list to avoid modifying original.

Implementation details:

def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    # make a shallow copy of list (but dicts are mutable, we should copy each dict? The requirement says do not modify original input list. If we swap references, original list may be modified if we swap elements? Actually swapping elements in a copy will not affect original list because we are swapping references within the copy. The original list remains unchanged. However, if the dicts themselves are mutated, that would affect original. We are not mutating dicts, just reordering. So shallow copy is fine.
    arr = tasks[:]  # shallow copy
    n = len(arr)
    swap_count = 0

    # define a helper to compare two tasks
    def is_less(a: dict, b: dict) -> bool:
        # return True if a should come before b in sorted order
        pa = a.get("priority")
        pb = b.get("priority")
        # handle None: None is considered less than any int? Actually None should be at the end.
        # So if pa is None and pb is not None, a should be after b -> is_less(a,b) should be False.
        # If both are None, compare created_at ascending.
        if pa is None and pb is None:
            return a["created_at"] < b["created_at"]
        if pa is None:
            return False  # a is None, b is not None -> a should be after b
        if pb is None:
            return True   # a is not None, b is None -> a should be before b
        # both are int
        if pa != pb:
            return pa > pb  # higher priority comes first, so a before b if pa > pb
        # same priority, compare created_at ascending
        return a["created_at"] < b["created_at"]

    # bubble sort
    for i in range(n):
        # last i elements are already sorted
        for j in range(0, n - i - 1):
            if is_less(arr[j], arr[j+1]):
                # swap
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swap_count += 1

    return arr, swap_count

That should work.

We need to include docstring and type hints.

Let's write the code.


## Response

```python
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
```

## Timings

- Time to first token: 0.55s
- Total generation: 15.35s
- Reasoning tokens: 692
- Answer tokens: 688
- Total tokens: 1380
