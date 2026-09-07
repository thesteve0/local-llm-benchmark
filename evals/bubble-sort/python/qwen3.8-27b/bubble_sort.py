"""Bubble sort implementation for task records."""


def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sort task records using bubble sort.

    Tasks are sorted by:
      1. priority descending
      2. created_at ascending
      3. tasks with priority None always come last, ordered by created_at ascending

    Args:
        tasks: A list of task dictionaries. Each task must contain:
            - "name": str
            - "priority": int or None
            - "created_at": int

    Returns:
        A tuple containing:
            - A new list of sorted task dictionaries
            - The total number of swaps performed during sorting

    The original input list is not modified.
    """
    sorted_tasks = list(tasks)
    n = len(sorted_tasks)
    swap_count = 0

    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
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


def _should_swap(left: dict, right: dict) -> bool:
    """
    Return True if the left task should be placed after the right task.

    This helper defines the bubble sort comparison rule:
      - Higher priority comes first.
      - If priorities are equal, earlier created_at comes first.
      - None priority always comes after non-None priority.
    """
    left_priority = left["priority"]
    right_priority = right["priority"]

    if left_priority is None:
        if right_priority is not None:
            return True
        return left["created_at"] > right["created_at"]

    if right_priority is None:
        return False

    if left_priority != right_priority:
        return left_priority < right_priority

    return left["created_at"] > right["created_at"]
