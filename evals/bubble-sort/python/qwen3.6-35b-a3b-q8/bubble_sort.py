def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sorts a list of task dictionaries using the bubble sort algorithm.

    Sorting rules:
    1. Primary: sort by 'priority' descending (higher priority comes first)
    2. Tiebreaker: when priorities are equal, sort by 'created_at' ascending
    3. Null handling: tasks with 'priority' == None are placed at the end,
       sorted by 'created_at' ascending among themselves.

    Args:
        tasks: List of task dictionaries containing 'name', 'priority', and 'created_at'.

    Returns:
        A tuple of (sorted_list, swap_count) where swap_count is the total number
        of element swaps performed during the sorting process.
    """
    if not tasks:
        return [], 0

    # Create a shallow copy to ensure the original list is not modified
    arr = tasks.copy()
    n = len(arr)
    swap_count = 0

    def should_swap(a: dict, b: dict) -> bool:
        """
        Determines if element a should be swapped with element b.
        Returns True if a should come after b according to the sorting rules.
        """
        a_pri, b_pri = a["priority"], b["priority"]

        # Rule 3: None priorities always go to the end
        if a_pri is None and b_pri is not None:
            return True
        if a_pri is not None and b_pri is None:
            return False

        # Rule 1: Descending priority (higher priority comes first)
        if a_pri != b_pri:
            return a_pri < b_pri

        # Rule 2: Ascending created_at when priorities are equal
        return a["created_at"] > b["created_at"]

    # Standard optimized bubble sort
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if should_swap(arr[j], arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swap_count += 1
                swapped = True
        if not swapped:
            break

    return arr, swap_count
