def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Bubble sort tasks by priority descending, then created_at ascending.
    Tasks with priority None are placed at the end ordered by created_at.

    Args:
        tasks: list of dicts with keys "name", "priority", "created_at"

    Returns:
        tuple[list[dict], int]: (sorted list copy, number of swaps performed)
    """
    # work on a shallow copy to keep the original list intact
    arr = tasks[:]  # dict objects are not mutated, only reordered
    n = len(arr)

    def is_better(a: dict, b: dict) -> bool:
        pa = a.get("priority")
        pb = b.get("priority")
        # both None -> tie-break by created_at
        if pa is None and pb is None:
            return a["created_at"] < b["created_at"]
        # None is always worse
        if pa is None:
            return False
        if pb is None:
            return True
        # primary: priority descending
        if pa != pb:
            return pa > pb
        # tie-breaker: created_at ascending
        return a["created_at"] < b["created_at"]

    swaps = 0
    for i in range(n):
        swapped = False
        # last i elements are already in place
        for j in range(n - 1 - i):
            a = arr[j]
            b = arr[j + 1]
            if not is_better(a, b):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return arr, swaps
