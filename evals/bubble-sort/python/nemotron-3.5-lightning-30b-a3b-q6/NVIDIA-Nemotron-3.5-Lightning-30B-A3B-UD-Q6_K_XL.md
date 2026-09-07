# Code Eval: NVIDIA-Nemotron-3.5-Lightning-30B-A3B-UD-Q6_K_XL

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

Here's a thinking process:

1.  **Analyze the User's Request:**
   - Need to implement a `bubble_sort` function in a file `bubble_sort.py`
   - Function signature: `def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:`
   - Each task dict has keys: `"name"`, `"priority"` (int or None), `"created_at"` (int)
   - Sorting rules:
     - Primary: priority descending (higher first)
     - Tiebreaker: created_at ascending (earlier first) when priorities equal
     - Null handling: priority=None always sorts to the end, ordered by created_at ascending among themselves
   - Constraints:
     - Must implement bubble sort algorithm (no built-in sort/sorted)
     - Return tuple (sorted_list, swap_count)
     - Do not modify original input list -> return new list
   - Example provided to verify understanding

2.  **Deconstruct the Sorting Logic:**
   - Need a comparison function or inline logic to determine if two tasks should be swapped based on the rules.
   - Let's define the ordering clearly:
     - If both priorities are None: sort by created_at ascending
     - If one is None and the other isn't: the non-None one comes first (None goes to end)
     - If both have priorities:
       - Higher priority comes first (descending)
       - If equal priority: earlier created_at comes first (ascending)
   - I need to translate this into a "should swap" condition for bubble sort.
   - In bubble sort, we typically swap adjacent elements if they are in the wrong order. So I need a function `should_swap(a, b)` that returns True if `a` should come after `b` (i.e., they are out of order).

   Let's define the "order" or "key" for each task, but since we can't use sort, we'll just compare directly.

   Let's think about the comparison:
   For two tasks A and B:
   - Get priority_A, priority_B, created_at_A, created_at_B
   - Case 1: Both priorities are None
       - They should be ordered by created_at ascending. So if A.created_at > B.created_at, they are out of order (swap if A is before B). Actually, in bubble sort ascending, we swap if left > right. So if A is left, B is right, and A.created_at > B.created_at, swap.
   - Case 2: One is None, one is not
       - Non-None should come first. So if A has None and B has priority, A should be after B -> swap if A is left, B is right and A.priority is None and B.priority is not None.
       - If A has priority and B has None, A should be before B -> no swap.
   - Case 3: Both have priorities
       - Compare priorities: if A.priority < B.priority, then A should be after B -> swap (since we want descending priority). If A.priority > B.priority, no swap. If equal, go to created_at.
       - If priorities equal: if A.created_at > B.created_at, swap (want ascending created_at). If A.created_at < B.created_at, no swap.

   Let's formalize the "should_swap" logic for bubble sort (left element vs right element, swap if left should come after right):
   ```python
   def should_swap(a, b):
       pa, pb = a['priority'], b['priority']
       ca, cb = a['created_at'], b['created_at']
       
       # Both None
       if pa is None and pb is None:
           return ca > cb  # swap if a's created_at is later (want ascending)
       
       # One is None
       if pa is None:  # a is None, b is not -> a should be after b -> swap
           return True
       if pb is None:  # b is None, a is not -> a should be before b -> no swap
           return False
       
       # Both have priorities
       if pa < pb:
           return True  # a has lower priority, should be after b
       if pa > pb:
           return False  # a has higher priority, should be before b
       
       # Priorities equal
       return ca > cb  # swap if a's created_at is later (want ascending)
   ```

   Let's test this logic against the example:
   Example tasks:
   - bug: p=3, ca=1000
   - feature: p=5, ca=2000
   - docs: p=3, ca=500

   Expected sorted: feature (p=5), docs (p=3, ca=500), bug (p=3, ca=1000)
   Swaps = 2

   Let's simulate bubble sort manually with the logic.
   Initial list (copy): [bug, feature, docs]
   Bubble sort passes: typically outer loop n-1, inner loop n-1-i.
   We swap adjacent if should_swap(left, right).

   Pass 1:
   - Compare bug (p=3, ca=1000) and feature (p=5, ca=2000):
       pa=3, pb=5 -> pa < pb -> should_swap=True -> swap -> [feature, bug, docs], swaps=1
   - Compare bug (p=3, ca=1000) and docs (p=3, ca=500):
       pa=3, pb=3 equal -> ca=1000 > cb=500 -> should_swap=True -> swap -> [feature, docs, bug], swaps=2
   Pass 2:
   - Compare feature (p=5, ca=2000) and docs (p=3, ca=500):
       pa=5 > pb=3 -> should_swap=False -> no swap
   Done. Total swaps=2. List: [feature, docs, bug]. Matches example perfectly.

   Now test null handling edge cases mentally:
   - Tasks with None priority should go to end, ordered by created_at ascending.
   - If we have [task_none1(ca=100), task_none2(ca=50), task_p1(p=1, ca=200)]
   - Expected: [task_p1, task_none2(ca=50), task_none1(ca=100)]
   - Let's trace should_swap for none vs none: ca > cb -> swap if left has later ca. Good.
   - none vs priority: should_swap returns True (none should be after). Good.
   - priority vs none: should_swap returns False (priority before none). Good.

   Looks solid.

3.  **Implementation Details:**
   - File: `bubble_sort.py`
   - Function: `bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]`
   - Must not modify original list -> make a deep copy? Tasks are dicts, shallow copy of list is enough if we don't mutate dicts. But to be safe, we can `list(tasks)` or `[task.copy() for task in tasks]`. Since we only swap references, a shallow copy of the list is sufficient. The dicts themselves won't be modified, just their order changes. So `sorted_tasks = list(tasks)` is fine.
   - Implement bubble sort with swap counter.
   - Include type hints and docstring.

   Let's write the code:

   ```python
   """Bubble sort implementation for task records."""

   from typing import list, dict, tuple


   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       """
       Sort a list of task dictionaries using bubble sort.

       Sorting order:
       - Primary: priority descending (higher priority first)
       - Tiebreaker: created_at ascending (earlier timestamp first) when priorities are equal
       - Null priority: tasks with priority=None always sort to the end,
         ordered by created_at ascending among themselves.

       Args:
           tasks: A list of dictionaries, each with keys "name", "priority" (int or None),
                  and "created_at" (int unix timestamp).

       Returns:
           A tuple containing:
           - A new list of task dictionaries sorted according to the rules.
           - The total number of element swaps performed during sorting.

       Constraints:
           - Implements the bubble sort algorithm; does not use built-in sort/sorted.
           - Does not modify the original input list.
       """
       # Work on a shallow copy so the original list is not modified
       sorted_tasks = list(tasks)
       n = len(sorted_tasks)
       swap_count = 0

       # Helper to determine if a swap is needed between left and right
       def should_swap(a: dict, b: dict) -> bool:
           pa, pb = a["priority"], b["priority"]
           ca, cb = a["created_at"], b["created_at"]

           # Both priorities are None: sort by created_at ascending
           if pa is None and pb is None:
               return ca > cb

           # a has None priority, b does not: a should go to the end -> swap
           if pa is None:
               return True

           # b has None priority, a does not: a should stay before b -> no swap
           if pb is None:
               return False

           # Both have priorities: higher priority comes first (descending)
           if pa < pb:
               return True
           if pa > pb:
               return False

           # Priorities are equal: sort by created_at ascending
           return ca > cb

       # Standard bubble sort
       for i in range(n):
           # After each pass, the largest (in terms of our ordering) element bubbles to the front? 
           # Actually, with should_swap, the "heaviest" or first-in-order element will bubble to the leftmost position.
           # Standard optimization: last i elements are already in place.
           for j in range(0, n - i - 1):
               if should_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                   sorted_tasks[j], sorted_tasks[j + 1] = sorted_tasks[j + 1], sorted_tasks[j]
                   swap_count += 1

       return sorted_tasks, swap_count
   ```

   Wait, let's double-check the bubble sort loop invariant. 
   Standard bubble sort: 
   for i in range(n):
       for j in range(0, n - i - 1):
           compare j and j+1
   After first pass, the largest element is at position n-1.
   In our case, "largest" meaning the one that should come last according to our ordering. 
   Let's verify with example: 
   Initial: [bug, feature, docs] (indices 0,1,2)
   n=3
   i=0: j from 0 to 1
       j=0: compare 0,1 -> should_swap(bug, feature) -> True -> swap -> [feature, bug, docs]
       j=1: compare 1,2 -> should_swap(bug, docs) -> True -> swap -> [feature, docs, bug]
   i=1: j from 0 to 0
       j=0: compare 0,1 -> should_swap(feature, docs) -> pa=5 > pb=3 -> False -> no swap
   i=2: j from 0 to -1 -> loop ends.
   Result: [feature, docs, bug], swaps=2. Correct.

   The algorithm is correct.

   One small thing: the type hints. The user specified `list[dict]` but in the signature they wrote `list[dict]`. I should use proper typing. In Python 3.9+, `list[dict]` is fine. I'll use `list[dict]` or `List[Dict]` from typing. I'll stick to the exact signature style they gave, but add imports if needed. They wrote `def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:`. I'll match that exactly, maybe add `from __future__ import annotations` if needed, but it's fine.

   Let's check the exact signature requirement: `def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:`. I'll use that exactly.

   Also, the helper function inside is fine, or I could just inline the logic. Keeping it clean with a helper is good.

   Let's consider edge cases:
   - Empty list: should return ([], 0). The loops will just not execute, swap_count=0. Correct.
   - Single element: returns same list, 0 swaps. Correct.
   - All None priorities: should sort by created_at ascending. should_swap handles both None -> ca > cb. Bubble sort will sort ascending. Correct.
   - Mix of None and non-None: None always to end. should_swap handles it. Correct.

   One detail: "Do not modify the original input list — return a new list". I do `sorted_tasks = list(tasks)`. This creates a new list with references to the same dicts. Since we only swap references in the list and never modify the dicts, the original list's order remains unchanged, and the dicts are the same objects. That satisfies "do not modify the original input list". If they meant don't modify the dicts either, they'd usually say "deep copy" or "do not mutate". I think shallow copy of list is standard for such tasks. I'll add a comment or just do it. To be absolutely safe regarding dict mutation, I could deep copy, but that's overkill and not implied. I'll stick with `list(tasks)`.

   Let's write the final code carefully.

   One more check on the type hints: The user wrote `list[dict]` and `tuple[list[dict], int]`. In Python 3.8, you'd need `from typing import List, Tuple`. I'll just use the exact syntax they provided, which works in Python 3.9+. I'll include a `from typing import ...` just in case, or I can use built-in generics. I'll just write the function with the exact signature as given, and maybe add a comment. Actually, I'll just use `list[dict]` and `tuple[list[dict], int]` directly; it's valid syntax now.

   Final code structure:
   ```python
   """File: bubble_sort.py

   Implements bubble sort for task records with custom ordering rules.
   """

   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       """
       Sort tasks by priority (descending), created_at (ascending) as tiebreaker,
       with None priorities pushed to the end.

       Args:
           tasks: list of dicts with keys "name", "priority" (int|None), "created_at" (int).

       Returns:
           tuple of (sorted_list, swap_count).
       """
       sorted_tasks = list(tasks)
       n = len(sorted_tasks)
       swaps = 0

       def needs_swap(a, b):
           pa, pb = a["priority"], b["priority"]
           ca, cb = a["created_at"], b["created_at"]

           if pa is None and pb is None:
               return ca > cb
           if pa is None:
               return True
           if pb is None:
               return False
           if pa < pb:
               return True
           if pa > pb:
               return False
           return ca > cb

       for i in range(n):
           for j in range(n - 1 - i):
               if needs_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                   sorted_tasks[j], sorted_tasks[j + 1] = sorted_tasks[j + 1], sorted_tasks[j]
                   swaps += 1

       return sorted_tasks, swaps
   ```

   Wait, `range(n - 1 - i)` is same as `range(0, n - i - 1)`. I'll use `range(n - 1 - i)` for simplicity, starting from 0 implicitly.

   Let's test with example in mind: works.
   I'll produce the final answer with the file content. I'll make sure the docstring and comments are clean. I'll also include a `if __name__ == "__main__":` block maybe for demonstration, but not required. The prompt says "Write clean, well-documented, idiomatic Python code. Include type hints and a docstring." I'll stick to the function and module-level doc.

   One thing: the prompt says "Implement a bubble sort function for task records." and "Write a single file `bubble_sort.py` containing a function with this exact signature". So I'll just provide the file content.

   I'll output the Python code.

## Response

```python
"""bubble_sort.py – Bubble sort implementation for task records."""

from typing import list, dict, tuple


def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sort a list of task dictionaries using the bubble sort algorithm.

    Sorting order:
    - Primary: ``priority`` descending (higher priority comes first)
    - Tiebreaker: ``created_at`` ascending (earlier timestamp comes first) when priorities are equal
    - Null handling: tasks where ``priority`` is ``None`` always sort to the end of the list,
      ordered by ``created_at`` ascending among themselves

    The original input list is **not** modified; a new sorted list is returned
    together with the total number of element swaps performed.

    Args:
        tasks: A list of dictionaries. Each dictionary must contain:
            - ``"name"`` (str)
            - ``"priority"`` (int or None)
            - ``"created_at"`` (int) – unix timestamp

    Returns:
        A tuple ``(sorted_list, swap_count)`` where:
        - ``sorted_list`` is a new list of task dictionaries ordered per the rules above.
        - ``swap_count`` is the total number of adjacent swaps executed by the bubble sort.

    Constraints:
        - The bubble sort algorithm is implemented manually; no built-in ``sort()``,
          ``sorted()``, or similar is used.
        - The original ``tasks`` list remains unchanged.
    """
    # Shallow copy so the original list is never mutated
    sorted_tasks = list(tasks)
    n = len(sorted_tasks)
    swap_count = 0

    # Determine whether two adjacent tasks are out of order.
    # Returns True if `a` (left) should come after `b` (right) → a swap is needed.
    def _needs_swap(a: dict, b: dict) -> bool:
        pa, pb = a["priority"], b["priority"]
        ca, cb = a["created_at"], b["created_at"]

        # Both priorities are None → sort by created_at ascending
        if pa is None and pb is None:
            return ca > cb

        # a has None priority, b does not → a must go to the end
        if pa is None:
            return True

        # b has None priority, a does not → a stays before b
        if pb is None:
            return False

        # Both have priorities: higher value comes first (descending)
        if pa < pb:
            return True
        if pa > pb:
            return False

        # Priorities are equal → sort by created_at ascending
        return ca > cb

    # Standard bubble sort passes
    for i in range(n):
        # After each outer iteration, the "heaviest" (first-in-order) element
        # has bubbled to the leftmost unsorted position, so we reduce the range.
        for j in range(n - 1 - i):
            if _needs_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                sorted_tasks[j], sorted_tasks[j + 1] = (
                    sorted_tasks[j + 1],
                    sorted_tasks[j],
                )
                swap_count += 1

    return sorted_tasks, swap_count


# ----------------------------------------------------------------------
# Example / quick self-test (can be removed or kept for manual verification)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    example_tasks = [
        {"name": "bug",     "priority": 3, "created_at": 1000},
        {"name": "feature", "priority": 5, "created_at": 2000},
        {"name": "docs",    "priority": 3, "created_at": 500},
    ]

    sorted_tasks, swaps = bubble_sort_tasks(example_tasks)
    print("Sorted tasks:", sorted_tasks)
    print("Swap count :", swaps)
    # Verify original list is untouched
    print("Original   :", example_tasks)
```

## Timings

- Time to first token: 0.96s
- Total generation: 84.66s
- Reasoning tokens: 3612
- Answer tokens: 940
- Total tokens: 4552

## Server Timings (llama.cpp)

- Prompt tokens: 486
- Prompt eval speed: 507.69 t/s
- Prompt eval time: 957.27 ms
- Generation tokens: 4552
- Generation speed: 54.38 t/s
- Generation time: 83692.73 ms
