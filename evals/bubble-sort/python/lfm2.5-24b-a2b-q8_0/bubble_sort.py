def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sorts a list of task dictionaries using the bubble sort algorithm.

    The sorting order is:
        1. Primary key: ``priority`` descending (higher priority first).
        2. Secondary key (tiebreaker): ``created_at`` ascending
           (earlier timestamp first) when priorities are equal.
        3. Tasks with ``priority`` equal to ``None`` are placed at the end
           of the list, ordered by ``created_at`` ascending among themselves.

    Parameters
    ----------
    tasks : list[dict]
        List of task records. Each record must contain the keys
        ``"name"`` (str), ``"priority"`` (int or None) and
        ``"created_at"`` (int).

    Returns
    -------
    tuple[list[dict], int]
        A tuple containing:
        - The sorted list of tasks (a new list; the original ``tasks``
          is not modified).
        - The total number of swaps performed during the bubble sort.
    """
    # Create a shallow copy so the original list stays untouched
    sorted_tasks = [task for task in tasks]
    n = len(sorted_tasks)
    swap_count = 0

    def is_out_of_order(a: dict, b: dict) -> bool:
        """
        Returns True if ``a`` should appear after ``b`` in the final ordering.
        """
        pa = a.get("priority")
        pb = b.get("priority")
        ca = a.get("created_at")
        cb = b.get("created_at")

        # Both have concrete priorities
        if pa is not None and pb is not None:
            if pa < pb:
                return True          # lower priority → should be later
            if pa > pb:
                return False         # higher priority → already before
            # Equal priority: use created_at ascending
            if ca > cb:
                return True
            return False

        # a has None priority, b does not → None must go to the end
        if pa is None and pb is not None:
            return True
        # a has a priority, b is None → correct order
        if pa is not None and pb is None:
            return False

        # Both are None: order by created_at ascending
        if ca > cb:
            return True
        return False

    # Classic bubble sort
    for i in range(n):
        swapped = False
        # After each pass the last i elements are already in place
        for j in range(0, n - i - 1):
            if is_out_of_order(sorted_tasks[j], sorted_tasks[j + 1]):
                # Swap adjacent elements
                sorted_tasks[j], sorted_tasks[j + 1] = (
                    sorted_tasks[j + 1],
                    sorted_tasks[j],
                )
                swap_count += 1
                swapped = True
        if not swapped:
            break

    return (sorted_tasks, swap_count)
