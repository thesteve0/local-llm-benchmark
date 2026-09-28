"""Bubble sort for prioritized task records.

This module provides :func:`bubble_sort_tasks`, which orders a collection of
task dictionaries using the classic bubble sort algorithm while honouring a
specific set of ordering rules.
"""


def _should_swap(a: dict, b: dict) -> bool:
    """Return ``True`` when task ``a`` must come after task ``b``.

    The ordering rules implemented here are, in priority order:

    1. **Priority (descending):** a task with a higher ``"priority"`` value
       comes first.
    2. **Creation time (ascending):** when two tasks share the same priority,
       the one created earlier (smaller ``"created_at"``) comes first.
    3. **Null priority:** tasks whose ``"priority"`` is ``None`` always sort to
       the very end, ordered by ``"created_at"`` ascending among themselves.

    Args:
        a: The left-hand task being compared.
        b: The right-hand task being compared.

    Returns:
        ``True`` if ``a`` and ``b`` are out of order and should be swapped,
        ``False`` otherwise.
    """
    a_null = a["priority"] is None
    b_null = b["priority"] is None

    # Both tasks lack a priority -> fall back to creation time.
    if a_null and b_null:
        return a["created_at"] > b["created_at"]

    # Only ``a`` lacks a priority -> ``a`` belongs at the end.
    if a_null:
        return True

    # Only ``b`` lacks a priority -> ``a`` belongs before ``b``.
    if b_null:
        return False

    # Both have priorities -> higher priority wins.
    if a["priority"] != b["priority"]:
        return a["priority"] < b["priority"]

    # Equal priorities -> earlier creation time wins.
    return a["created_at"] > b["created_at"]


def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """Sort ``tasks`` by priority and creation time using bubble sort.

    The tasks are ordered by ``"priority"`` in descending order, breaking ties
    by ``"created_at"`` in ascending order. Tasks with a ``None`` priority are
    always placed at the end, ordered by ``"created_at"`` ascending.

    The algorithm is implemented manually (no use of ``sort``/``sorted``) and
    returns the number of element swaps performed.

    Args:
        tasks: The list of task dictionaries to sort. Each dictionary must
            contain the keys ``"name"``, ``"priority"`` (``int`` or ``None``)
            and ``"created_at"`` (``int``).

    Returns:
        A tuple ``(sorted_tasks, swap_count)`` where ``sorted_tasks`` is a new
        list containing the tasks in sorted order and ``swap_count`` is the
        total number of adjacent swaps performed during sorting. The original
        ``tasks`` list is left untouched.
    """
    # Work on a shallow copy so the caller's list is never mutated.
    ordered = list(tasks)
    n = len(ordered)
    swap_count = 0

    for pass_number in range(n - 1):
        # Track whether any swap happened this pass so we can stop early when
        # the list is already sorted (optimisation, not required for correctness).
        swapped = False

        # After each pass the largest remaining element is "bubbled" to its
        # final position, so we can ignore the last ``pass_number`` elements.
        for index in range(n - 1 - pass_number):
            if _should_swap(ordered[index], ordered[index + 1]):
                ordered[index], ordered[index + 1] = ordered[index + 1], ordered[index]
                swap_count += 1
                swapped = True

        if not swapped:
            break

    return ordered, swap_count


if __name__ == "__main__":
    demo_tasks = [
        {"name": "bug", "priority": 3, "created_at": 1000},
        {"name": "feature", "priority": 5, "created_at": 2000},
        {"name": "docs", "priority": 3, "created_at": 500},
    ]

    sorted_tasks, swaps = bubble_sort_tasks(demo_tasks)
    print(f"Swaps: {swaps}")
    for task in sorted_tasks:
        print(f"  {task['name']:<8} priority={task['priority']} created_at={task['created_at']}")
