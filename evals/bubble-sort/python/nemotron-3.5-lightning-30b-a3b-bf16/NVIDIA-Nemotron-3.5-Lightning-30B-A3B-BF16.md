# Code Eval: NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16

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
     - Do not modify original input list -> return a new list
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

   Let's define the "order" or "key" for each task, or just write the comparison logic.

   Let's think about the comparison:
   For two tasks x and y, we want to determine if x should come before y in the final sorted list.
   Actually, for bubble sort swap condition: we swap if x is "after" y (i.e., x should come after y in the desired order).

   Let's define a function `compare(x, y)` that returns -1, 0, 1 or just a boolean `x should be after y`.

   Let's derive the rules for "x should be after y" (i.e., out of order):
   - If x.priority is None and y.priority is not None: x should be after y (since None goes to end). So swap=True.
   - If x.priority is not None and y.priority is None: x should be before y. So swap=False.
   - If both are None: compare created_at. If x.created_at > y.created_at, then x should be after y (since we want ascending created_at). So swap=True if x.created_at > y.created_at.
   - If both not None:
       - If x.priority < y.priority: x should be after y (we want descending priority). swap=True.
       - If x.priority > y.priority: x should be before y. swap=False.
       - If x.priority == y.priority: 
           - If x.created_at > y.created_at: x should be after y. swap=True.
           - If x.created_at < y.created_at: x should be before y. swap=False.
           - If equal: no swap (or stable, doesn't matter).

   Let's encapsulate this in a helper function or a key-based comparison. Since we can't use sort, we just need the swap condition.

   Alternatively, I can create a "sort key" for each task that maps to a tuple, and then compare those tuples. But bubble sort compares elements directly. I can compute a comparable key for each task, but since priority None needs special handling at the end, I can design a key function that returns a tuple that sorts correctly with standard Python tuple comparison, but I'm implementing bubble manually, so I can just use the comparison logic.

   Let's define a function `order_key(task)` that returns a tuple that, when compared normally, gives the desired order. Then in bubble sort, I just check if `order_key(a) > order_key(b)` (meaning a should come after b). This is clean and easy.

   Let's design `order_key`:
   - We want: 
       - Non-None priority descending -> so we can negate priority: -priority
       - Then created_at ascending -> just created_at
       - None priority should be at the end. If we use -priority, None can't be negated. We can handle None by assigning a very low value for the purpose of sorting, but since we want None at the end, we can assign priority a value that puts them last. For descending order, "last" in terms of priority means lowest priority value. But None should be after all int priorities. So we can map None priority to a very small number, like `-inf` or a large negative, but since we negate for descending, let's think.

   Actually, let's just use the comparison logic directly in the bubble sort loop. It's not too complex.

   Let's define `should_swap(task_a, task_b)`:
       # Returns True if task_a should come after task_b (i.e., they are out of order)
       a_pri = task_a.get("priority")
       b_pri = task_b.get("priority")
       a_ca = task_a.get("created_at")
       b_ca = task_b.get("created_at")

       if a_pri is None and b_pri is not None:
           return True  # a (None) should be after b
       if a_pri is not None and b_pri is None:
           return False  # a (int) should be before b
       if a_pri is None and b_pri is None:
           return a_ca > b_ca  # both None: ascending created_at, so if a's ca > b's ca, a should be after b

       # both not None
       if a_pri < b_pri:
           return True  # a has lower priority, should be after b (descending)
       if a_pri > b_pri:
           return False  # a has higher priority, should be before b
       # priorities equal
       return a_ca > b_ca  # ascending created_at

   This looks correct and covers all cases.

   Let's test with the example:
   tasks = [
       {"name": "bug",     "priority": 3, "created_at": 1000},
       {"name": "feature", "priority": 5, "created_at": 2000},
       {"name": "docs",    "priority": 3, "created_at": 500},
   ]

   Bubble sort passes:
   Initial: [bug(3,1000), feature(5,2000), docs(3,500)]
   Pass 1:
   Compare bug and feature: a_pri=3, b_pri=5. a_pri < b_pri -> should_swap=True -> swap -> [feature(5,2000), bug(3,1000), docs(3,500)], swaps=1
   Compare bug and docs: a_pri=3, b_pri=3. equal. a_ca=1000, b_ca=500. a_ca > b_ca -> should_swap=True -> swap -> [feature(5,2000), docs(3,500), bug(3,1000)], swaps=2
   Pass 2:
   Compare feature and docs: a_pri=5, b_pri=3. a_pri > b_pri -> should_swap=False -> no swap
   Compare docs and bug: a_pri=3, b_pri=3. a_ca=500, b_ca=1000. a_ca > b_ca? 500 > 1000 False -> no swap
   Done. Result: [feature, docs, bug], swaps=2. Matches example perfectly.

   Now, constraints:
   - Must implement bubble sort algorithm. I'll use a standard bubble sort with a swap counter.
   - Do not modify original input list -> make a copy of the list at the start.
   - Return (sorted_list, swap_count).

   Implementation details:
   - Make a deep copy? The tasks are dicts, but we just need a new list of the same dict references (or deep copy). Since we're not modifying the dicts, a shallow copy `tasks.copy()` or `list(tasks)` is enough. But to be safe and idiomatic, I'll do `sorted_tasks = tasks.copy()` or `[task for task in tasks]`. Actually, since we're swapping elements in the list, the dicts themselves are not mutated, just their positions change. So a shallow copy of the list is fine.
   - Bubble sort algorithm: 
        n = len(arr)
        swap_count = 0
        for i in range(n):
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                if should_swap(arr[j], arr[j+1]):
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    swap_count += 1
        return arr, swap_count

   - I should add a docstring, type hints as specified.
   - The function signature must exactly match: `def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:`

   Let's structure the code:

   ```python
   """Bubble sort implementation for task records."""

   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       """
       Sort a list of task dictionaries using bubble sort.

       Sorting rules:
       - Primary: priority descending (higher first)
       - Tiebreaker: created_at ascending (earlier first) when priorities equal
       - Null priority: always sorts to the end, ordered by created_at ascending

       Args:
           tasks: List of dicts with keys "name", "priority" (int or None), "created_at" (int).

       Returns:
           Tuple of (sorted_list, swap_count) where swap_count is the total number of swaps performed.
           The original input list is not modified.
       """
       # Make a shallow copy so original list is not modified
       sorted_tasks = list(tasks)
       n = len(sorted_tasks)
       swap_count = 0

       # Helper to determine if a swap is needed
       def should_swap(a: dict, b: dict) -> bool:
           a_pri = a["priority"]
           b_pri = b["priority"]
           a_ca = a["created_at"]
           b_ca = b["created_at"]

           if a_pri is None and b_pri is not None:
               return True
           if a_pri is not None and b_pri is None:
               return False
           if a_pri is None and b_pri is None:
               return a_ca > b_ca

           # Both priorities are integers
           if a_pri < b_pri:
               return True
           if a_pri > b_pri:
               return False
           # Priorities equal
           return a_ca > b_ca

       # Bubble sort implementation
       for i in range(n):
           # After each pass, the largest (in terms of our ordering) element bubbles to the correct position
           # We track swapped to potentially early-break, but we need exact swap_count, so we'll just run all passes
           for j in range(0, n - i - 1):
               if should_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                   sorted_tasks[j], sorted_tasks[j + 1] = sorted_tasks[j + 1], sorted_tasks[j]
                   swap_count += 1

       return sorted_tasks, swap_count
   ```

   Wait, should I add an optimization like `if not swapped: break`? The problem says "Return a tuple of (sorted_list, swap_count) where swap_count is the total number of element swaps performed during sorting". If I break early, swap_count is still correct for the actual swaps performed. It doesn't violate anything, and it's a standard optimization. I'll include it but it's optional. I'll just do the full passes to be safe and simple, or include the early break with a flag. It doesn't affect correctness of swap_count. I'll just do the standard nested loops without early break to keep swap_count straightforward, or with early break it's fine. I'll just do the full sort.

   Let's double-check the `should_swap` logic with edge cases:
   - None, None, created_at ascending: if a_ca > b_ca -> swap True. Correct, because we want smaller ca first. So if a has larger ca, it should move after b -> swap.
   - None vs int: None always to end. If a is None, b is int -> swap True (a moves after b). If a is int, b is None -> swap False (a stays before b). Correct.
   - Both int: descending priority. a_pri < b_pri -> swap True (a has lower priority, should move after b). a_pri > b_pri -> swap False. Correct.
   - Equal priority: ascending created_at. a_ca > b_ca -> swap True. Correct.

   All good.

   One thing: the input type is `list[dict]`. The dicts have keys "name", "priority", "created_at". I'll assume they always have these keys as per spec.

   I'll write the file content cleanly.

   Let's also consider if the function should handle empty list? Yes, it will just return ([], 0). Fine.

   Final check on the signature: `def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:` - matches.

   I'll produce the Python file content.

## Response

```python
"""Bubble sort implementation for task records."""

from typing import Any


def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sort a list of task dictionaries using the bubble sort algorithm.

    Sorting order:
    - Primary: ``priority`` descending (higher priority comes first)
    - Tiebreaker: ``created_at`` ascending (earlier timestamp comes first) when priorities are equal
    - Null handling: tasks where ``priority`` is ``None`` always sort to the end,
      ordered by ``created_at`` ascending among themselves

    The original input list is **not** modified; a new sorted list is returned
    along with the total number of element swaps performed.

    Args:
        tasks: A list of task dictionaries. Each dictionary must contain:
            - "name" (str)
            - "priority" (int or None)
            - "created_at" (int)

    Returns:
        A tuple ``(sorted_tasks, swap_count)`` where:
        - ``sorted_tasks`` is a new list of task dictionaries sorted per the rules above.
        - ``swap_count`` is the total number of adjacent swaps performed during the sort.
    """
    # Shallow copy so the original list is never mutated
    sorted_tasks = list(tasks)
    n = len(sorted_tasks)
    swap_count = 0

    def _should_swap(a: dict, b: dict) -> bool:
        """
        Return True if element ``a`` should come after element ``b``
        (i.e., they are out of order according to the sorting rules).
        """
        a_pri = a["priority"]
        b_pri = b["priority"]
        a_ca = a["created_at"]
        b_ca = b["created_at"]

        # None priorities always go to the end
        if a_pri is None and b_pri is not None:
            return True
        if a_pri is not None and b_pri is None:
            return False
        if a_pri is None and b_pri is None:
            # Both None: earlier created_at first
            return a_ca > b_ca

        # Both have integer priorities: descending priority
        if a_pri < b_pri:
            return True          # a has lower priority → should move after b
        if a_pri > b_pri:
            return False         # a has higher priority → should move before b

        # Priorities equal: ascending created_at
        return a_ca > b_ca

    # Standard bubble sort with swap counting
    for i in range(n):
        for j in range(0, n - i - 1):
            if _should_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                sorted_tasks[j], sorted_tasks[j + 1] = (
                    sorted_tasks[j + 1],
                    sorted_tasks[j],
                )
                swap_count += 1

    return sorted_tasks, swap_count
```

## Timings

- Time to first token: 1.52s
- Temperature: 0.0
- Total generation: 171.73s
- Reasoning tokens: 3023
- Answer tokens: 690
- Total tokens: 3713

## Server Timings (llama.cpp)

- Prompt tokens: 486
- Prompt eval speed: 320.36 t/s
- Prompt eval time: 1517.04 ms
- Generation tokens: 3713
- Generation speed: 21.81 t/s
- Generation time: 170203.22 ms
