def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    working = [dict(t) for t in tasks]
    n = len(working)
    swap_count = 0

    def should_swap(a, b):
        a_pri = a["priority"]
        b_pri = b["priority"]
        if a_pri is None and b_pri is None:
            return a["created_at"] > b["created_at"]
        if a_pri is None:
            return True
        if b_pri is None:
            return False
        if a_pri != b_pri:
            return a_pri < b_pri
        return a["created_at"] > b["created_at"]

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if should_swap(working[j], working[j + 1]):
                working[j], working[j + 1] = working[j + 1], working[j]
                swap_count += 1

    return working, swap_count
