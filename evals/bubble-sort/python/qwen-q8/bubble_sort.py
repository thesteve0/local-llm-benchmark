def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sorts a list of task dictionaries using the bubble sort algorithm.

    Sorting Rules:
        1. Primary:   Sort by 'priority' descending (higher priority first)
        2. Tiebreaker: When priorities are equal, sort by 'created_at' ascending (earlier first)
        3. Null Handling: Tasks with 'priority' == None are always pushed to the end,
                          ordered by 'created_at' ascending among themselves.

    Args:
        tasks: List of task dictionaries containing 'name', 'priority', and 'created_at'.

    Returns:
        A tuple of (sorted_list, swap_count) where swap_count is the total number of 
        element swaps performed during the sorting process.
    """
    # Create a shallow copy to ensure the original list remains unmodified
    arr = tasks.copy()
    n = len(arr)
    swap_count = 0

    def should_swap(a: dict, b: dict) -> bool:
        """
        Determines if task 'a' should be placed after task 'b'.
        Returns True if a swap is needed to maintain the correct order.
        """
        a_pri, b_pri = a["priority"], b["priority"]
        a_time, b_time = a["created_at"], b["created_at"]

        # Handle None priorities: None always goes to the end
        if a_pri is None and b_pri is not None:
            return True
        if a_pri is not None and b_pri is None:
            return False
        if a_pri is None and b_pri is None:
            return a_time > b_time

        # Both have valid priorities
        if a_pri < b_pri:
            return True
        if a_pri > b_pri:
            return False
        # Priorities are equal; compare by created_at ascending
        return a_time > b_time

    # Standard optimized bubble sort
    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if should_swap(arr[j], arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swap_count += 1
                swapped = True
        # If no swaps occurred, the list is already sorted
        if not swapped:
            break

    return arr, swap_count


if __name__ == "__main__":
    # Example usage
    tasks = [
        {"name": "bug",     "priority": 3, "created_at": 1000},
        {"name": "feature", "priority": 5, "created_at": 2000},
        {"name": "docs",    "priority": 3, "created_at": 500},
    ]

    sorted_tasks, swaps = bubble_sort_tasks(tasks)
    print("Sorted Tasks:")
    for t in sorted_tasks:
        print(f"  {t}")
    print(f"Total Swaps: {swaps}")
