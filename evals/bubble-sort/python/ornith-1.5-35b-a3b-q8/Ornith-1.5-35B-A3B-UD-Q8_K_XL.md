# Code Eval: Ornith-1.5-35B-A3B-UD-Q8_K_XL

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

Let me analyze this problem carefully.

I need to implement a bubble sort function that sorts task records according to specific rules.

Let me understand the sorting rules:
1. **Primary:** sort by `"priority"` descending (higher priority comes first)
2. **Tiebreaker:** when priorities are equal, sort by `"created_at"` ascending (earlier timestamp comes first)
3. **Null handling:** tasks where `priority` is `None` always sort to the end of the list, ordered by `"created_at"` ascending among themselves

Let me think about the comparison logic. I need a function that compares two tasks and determines their order.

For bubble sort, I need to determine when to swap two adjacent elements. Let me think about a comparison function `should_swap(a, b)` that returns True if `a` should come after `b` (i.e., they're out of order and need to be swapped).

Let me define the comparison:
- If `a.priority` is None and `b.priority` is None: order by created_at ascending. Swap if `a.created_at > b.created_at`.
- If `a.priority` is None and `b.priority` is not None: `a` should come after `b`, so swap (a is out of order).
- If `a.priority` is not None and `b.priority` is None: `a` should come before `b`, so no swap.
- If both priorities are not None:
  - If `a.priority > b.priority`: `a` should come first, no swap.
  - If `a.priority < b.priority`: `a` should come after, swap.
  - If `a.priority == b.priority`: order by created_at ascending. Swap if `a.created_at > b.created_at`.

Let me verify with the example:
```python
tasks = [
    {"name": "bug",     "priority": 3, "created_at": 1000},
    {"name": "feature", "priority": 5, "created_at": 2000},
    {"name": "docs",    "priority": 3, "created_at": 500},
]
```

Expected output:
```python
sorted_tasks = [
    {"name": "feature", "priority": 5, "created_at": 2000},
    {"name": "docs",    "priority": 3, "created_at": 500},
    {"name": "bug",     "priority": 3, "created_at": 1000},
]
swaps = 2
```

Let me trace through bubble sort:
Initial: [bug(3,1000), feature(5,2000), docs(3,500)]

Pass 1:
- Compare bug(3,1000) and feature(5,2000): bug.priority=3 < feature.priority=5, so bug should come after feature. Swap. → [feature(5,2000), bug(3,1000), docs(3,500)]. swaps=1
- Compare bug(3,1000) and docs(3,500): priorities equal (3==3), created_at: 1000 > 500, so bug should come after docs. Swap. → [feature(5,2000), docs(3,500), bug(3,1000)]. swaps=2

Pass 2:
- Compare feature(5,2000) and docs(3,500): feature.priority=5 > docs.priority=3, no swap.
- Compare docs(3,500) and bug(3,1000): priorities equal, 500 < 1000, no swap.

No swaps in pass 2, so we can stop.

Total swaps = 2. ✓

Great, my logic works.

Now let me think about the bubble sort implementation. Standard bubble sort:

```python
def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    result = list(tasks)  # copy
    n = len(result)
    swap_count = 0
    
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if should_swap(result[j], result[j + 1]):
                result[j], result[j + 1] = result[j + 1], result[j]
                swap_count += 1
                swapped = True
        if not swapped:
            break
    
    return result, swap_count
```

Now let me write the comparison function. I'll make it a nested helper or a module-level function.

Let me think about whether to use a comparison function that returns -1, 0, 1 or a boolean `should_swap`. The boolean approach is cleaner for bubble sort.

Let me write a helper function `_should_swap(a, b)` that returns True if `a` should come after `b`.

Actually, let me think about a cleaner way. I could define a comparison function that returns a value indicating order, then use it. But for bubble sort, the boolean is fine.

Let me write the code:

```python
"""Bubble sort implementation for prioritized task records."""

from typing import Optional


def _should_swap(a: dict, b: dict) -> bool:
    """Return True if task ``a`` should be placed after task ``b``.

    Ordering rules:
        1. Higher ``priority`` comes first (descending).
        2. Equal priorities are broken by earlier ``created_at`` (ascending).
        3. Tasks with ``priority is None`` always sort last, ordered by
           ``created_at`` ascending among themselves.
    """
    a_none = a["priority"] is None
    b_none = b["priority"] is None

    # Both have no priority -> order by created_at ascending.
    if a_none and b_none:
        return a["created_at"] > b["created_at"]

    # Only ``a`` has no priority -> ``a`` belongs after ``b``.
    if a_none:
        return True

    # Only ``b`` has no priority -> ``a`` belongs before ``b``.
    if b_none:
        return False

    # Both have priorities -> higher priority first.
    if a["priority"] != b["priority"]:
        return a["priority"] < b["priority"]

    # Equal priorities -> earlier created_at first.
    return a["created_at"] > b["created_at"]


def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """Sort a list of task records using bubble sort.

    ...
    """
    result = list(tasks)
    n = len(result)
    swap_count = 0

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if _should_swap(result[j], result[j + 1]):
                result[j], result[j + 1] = result[j + 1], result[j]
                swap_count += 1
                swapped = True
        if not swapped:
            break

    return result, swap_count
```

Wait, I need to be careful about the "do not modify the original input list" requirement. `list(tasks)` creates a shallow copy of the list, which is fine because we're only reordering references to the dicts, not modifying the dicts themselves. The dicts themselves are not modified. Good.

Let me also think about edge cases:
- Empty list: `n = 0`, the outer loop `range(-1)` doesn't execute, returns `([], 0)`. Good.
- Single element: `n = 1`, outer loop `range(0)` doesn't execute, returns `([task], 0)`. Good.

Let me double check the type hints. The signature uses `list[dict]` and `tuple[list[dict], int]`, which requires Python 3.9+. The `priority` can be `int or None`, so I should use `Optional[int]` in the helper, but the helper takes `dict` so it's fine.

Actually, let me reconsider. The problem says the signature is exactly:
```python
def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
```

So I should keep that exact signature. My implementation matches.

Let me think about whether I should add a `if __name__ == "__main__":` block with the example. It might be nice for demonstration but not required. I'll add a small demonstration to make it runnable and testable.

Actually, let me reconsider the docstring for the main function to be thorough.

Let me also think about whether the comparison is stable and correct. Bubble sort with a proper comparison is stable if we only swap when strictly out of order (i.e., we don't swap when equal). My `_should_swap` returns True only when `a` should strictly come after `b`. When they're "equal" in ordering (same priority, same created_at), it returns False, so no swap, preserving stability. Good.

Let me verify the null handling more carefully. Consider:
```python
tasks = [
    {"name": "a", "priority": None, "created_at": 300},
    {"name": "b", "priority": 5, "created_at": 100},
    {"name": "c", "priority": None, "created_at": 200},
]
```

Expected: b(5,100), c(None,200), a(None,300)

Let me trace:
Initial: [a(None,300), b(5,100), c(None,200)]

Pass 1:
- Compare a(None,300) and b(5,100): a_none=True, b_none=False → return True (swap). → [b(5,100), a(None,300), c(None,200)]. swaps=1
- Compare a(None,300) and c(None,200): both None → a.created_at=300 > c.created_at=200 → return True (swap). → [b(5,100), c(None,200), a(None,300)]. swaps=2

Pass 2:
- Compare b(5,100) and c(None,200): b_none=False, a... wait let me recompute. a=b(5,100), b=c(None,200). a_none=False, b_none=True → return False (no swap).
- Compare c(None,200) and a(None,300): both None → 200 > 300? No → return False (no swap).

No swaps, stop. Result: [b(5,100), c(None,200), a(None,300)]. ✓

The logic is correct.

Now let me finalize the code. I'll make it clean and well-documented.

Let me reconsider whether to use `Optional` import. Since the helper takes dicts, I don't strictly need it. But for clarity in the docstring, I can mention it. I'll keep the import minimal. Actually, I don't need `Optional` since I'm not annotating the dict values. Let me remove it to keep things clean. Actually, it doesn't hurt to not import it. Let me not import it.

Hmm, but maybe I should annotate the helper more precisely. Let me keep it simple with `dict`.

Let me write the final version.

Actually, let me reconsider the structure. Some might prefer a single comparison function returning an ordering value. But the boolean approach is idiomatic and clear for bubble sort. I'll go with it.

Let me also add a `__main__` demonstration block that runs the example and prints results, which makes the file self-testing.

Let me write it out:

```python
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
```

This looks good. Let me double-check the example once more with the code.

demo_tasks = [bug(3,1000), feature(5,2000), docs(3,500)]
n = 3

Pass 0:
- index 0: _should_swap(bug, feature): a.priority=3, b.priority=5, not null, 3 != 5, 3 < 5 → True. Swap. [feature, bug, docs]. swaps=1, swapped=True
- index 1: _should_swap(bug, docs): a.priority=3, b.priority=3, equal, created_at 1000 > 500 → True. Swap. [feature, docs, bug]. swaps=2, swapped=True

Pass 1:
- index 0: _should_swap(feature, docs): 5 != 3, 5 < 3? No → False. No swap.
- index 1: _should_swap(docs, bug): 3 == 3, 500 > 1000? No → False. No swap.
- swapped=False → break

Result: [feature(5,2000), docs(3,500), bug(3,1000)], swaps=2. ✓

The output matches the expected.

Let me verify the original list is not modified. `ordered = list(tasks)` creates a new list. We only reorder within `ordered`. The dicts themselves are shared but not modified. So `demo_tasks` remains unchanged. Good.

I think this is a solid, clean implementation. Let me finalize.

One more consideration: the problem says "Write clean, well-documented, idiomatic Python code. Include type hints and a docstring." I've done all of that.

Let me reconsider whether I should keep the `if __name__ == "__main__"` block. It's helpful for demonstration and testing, and doesn't interfere with importing the module. I'll keep it but make it concise.

Actually, I realize I should double check: is there any issue with the early termination optimization affecting swap_count? No — the early termination only stops when no swaps occur, which means the list is already fully sorted, so no further swaps would happen anyway. The swap_count is accurate.

Let me also make sure the code handles the case where priorities could be negative integers. The comparison `a["priority"] < b["priority"]` works fine with negatives. Good.

I'm confident in the solution. Let me write the final answer.

I'll present the code with a brief explanation.


## Response

# Bubble Sort for Task Records

Here's a clean, well-documented implementation:

```python
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
```

## How it works

**The comparison helper (`_should_swap`)** is the heart of the logic. It returns `True` only when the two adjacent tasks are genuinely out of order, which keeps the sort **stable** (equal elements never get needlessly swapped). The three rules are handled as a clear cascade:

| Case | Result |
|------|--------|
| Both `priority is None` | Order by `created_at` ascending |
| Only `a` is `None` | `a` goes after `b` (swap) |
| Only `b` is `None` | `a` goes before `b` (no swap) |
| Priorities differ | Higher priority first |
| Priorities equal | Earlier `created_at` first |

**The bubble sort itself** uses the standard two-loop structure with an early-termination optimization: if a full pass makes no swaps, the list is sorted and we stop.

## Verification against the example

Tracing `[bug(3,1000), feature(5,2000), docs(3,500)]`:

- **Pass 1:** `bug` vs `feature` → swap (3 < 5) → `swaps=1`; `bug` vs `docs` → swap (equal priority, 1000 > 500) → `swaps=2`
- **Pass 2:** no swaps → early exit

Result: `[feature(5,2000), docs(3,500), bug(3,1000)]` with `swaps = 2` ✓

The original list is preserved because `ordered = list(tasks)` creates a shallow copy — only references are reordered, never the dictionaries themselves.

## Timings

- Time to first token: 0.82s
- Temperature: 0.0
- Total generation: 127.58s
- Reasoning tokens: 4225
- Answer tokens: 1495
- Total tokens: 5720

## Server Timings (llama.cpp)

- Prompt tokens: 488
- Prompt eval speed: 599.01 t/s
- Prompt eval time: 814.68 ms
- Generation tokens: 5720
- Generation speed: 45.12 t/s
- Generation time: 126754.34 ms
