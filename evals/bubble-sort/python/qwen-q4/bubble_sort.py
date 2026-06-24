def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sorts a list of task dictionaries using the bubble sort algorithm.

    Sorting Rules:
        1. Primary:   Sort by 'priority' descending (higher priority first).
        2. Tiebreaker: When priorities are equal, sort by 'created_at' ascending (earlier first).
        3. Null Handling: Tasks with 'priority' == None are placed at the end, 
                           sorted by 'created_at' ascending among themselves.

    Args:
        tasks: List of task dictionaries containing 'name', 'priority', and 'created_at'.

    Returns:
        A tuple containing:
            - sorted_tasks: A new list of tasks sorted according to the rules.
            - swap_count:   The total number of adjacent swaps performed during sorting.
    """
    # Create a shallow copy to ensure the original list is not mutated
    sorted_tasks = tasks.copy()
    n = len(sorted_tasks)
    swap_count = 0
    swapped = True

    while swapped:
        swapped = False
        for i in range(n - 1):
            a = sorted_tasks[i]
            b = sorted_tasks[i + 1]

            a_pri, b_pri = a["priority"], b["priority"]
            a_time, b_time = a["created_at"], b["created_at"]

            # Determine if 'a' should be swapped with 'b' (i.e., a should come after b)
            should_swap = False
            if a_pri is None and b_pri is not None:
                should_swap = True
            elif a_pri is not None and b_pri is None:
                should_swap = False
            elif a_pri is None and b_pri is None:
                should_swap = a_time > b_time
            else:
                # Both have valid priorities
                if a_pri < b_pri:
                    should_swap = True
                elif a_pri > b_pri:
                    should_swap = False
                else:
                    # Priorities are equal, use created_at ascending
                    should_swap = a_time > b_time

            if should_swap:
                sorted_tasks[i], sorted_tasks[i + 1] = sorted_tasks[i + 1], sorted_tasks[i]
                swap_count += 1
                swapped = True

    return sorted_tasks, swap_count


# --- Example Usage ---
if __name__ == "__main__":
    tasks = [
        {"name": "bug",     "priority": 3, "created_at": 1000},
        {"name": "feature", "priority": 5, "created_at": 2000},
        {"name": "docs",    "priority": 3, "created_at": 500},
    ]

    sorted_tasks, swaps = bubble_sort_tasks(tasks)
    
    print("Original list id:", id(tasks))
    print("Sorted list id:  ", id(sorted_tasks))
    print("Swaps performed: ", swaps)
    print("\nSorted Tasks:")
    for t in sorted_tasks:
        print(f"  {t}")
