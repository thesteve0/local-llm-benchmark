def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sorts a list of task dictionaries using the bubble sort algorithm.

    Sorting Rules:
        1. Primary: priority descending (higher priority comes first)
        2. Tiebreaker: created_at ascending (earlier timestamp comes first)
        3. Null handling: tasks with priority=None are always placed at the end,
           sorted by created_at ascending among themselves

    Args:
        tasks: List of dictionaries containing 'name', 'priority', and 'created_at' keys.

    Returns:
        A tuple of (sorted_list, swap_count) where swap_count is the total number 
        of element swaps performed during the sorting process.
    """
    # Create a shallow copy to ensure the original list is not modified
    arr = list(tasks)
    n = len(arr)
    swap_count = 0

    def should_swap(a: dict, b: dict) -> bool:
        """
        Returns True if element `a` should be placed after element `b` 
        (i.e., they are currently out of order according to the sorting rules).
        """
        a_none = a["priority"] is None
        b_none = b["priority"] is None

        # Rule 3: None priorities always sink to the end
        if a_none and not b_none:
            return True
        if not a_none and b_none:
            return False

        # If both are None, sort by created_at ascending
        if a_none and b_none:
            return a["created_at"] > b["created_at"]

        # Rule 1: Sort by priority descending
        if a["priority"] < b["priority"]:
            return True
        if a["priority"] > b["priority"]:
            return False

        # Rule 2: Equal priority, sort by created_at ascending
        return a["created_at"] > b["created_at"]

    # Standard bubble sort with early-exit optimization
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if should_swap(arr[j], arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swap_count += 1
                swapped = True
        # If no swaps occurred in a pass, the list is already sorted
        if not swapped:
            break

    return arr, swap_count
