# Code Eval: NVIDIA-Nemotron-3.5-Lightning-30B-A3B-UD-Q8_K_XL

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

   Let's define the "order" or "key" for each task, but since we can't use sort, we'll just compare directly.

   Let's think about the comparison:
   For two tasks A and B:
   - Get priority_A, priority_B, created_at_A, created_at_B
   - Rule: None priority always at the end.
     - If priority_A is None and priority_B is not None: A should be after B -> swap if A is before B? Wait, in bubble sort, we iterate and swap if left > right (if we want ascending). Here, we want a custom order. Let's define "left should move to the right of right" i.e., they are out of order.
     - Let's define a function `is_out_of_order(a, b)` that returns True if `a` should come after `b` in the final sorted list.

   Let's map out all cases:
   Case 1: a.priority is None, b.priority is not None -> a should be after b -> out of order (True) if a is before b.
   Case 2: a.priority is not None, b.priority is None -> a should be before b -> out of order (False).
   Case 3: both None -> sort by created_at ascending. If a.created_at > b.created_at -> a should be after b -> True. If a.created_at < b.created_at -> False. If equal -> False (stable? not specified, but bubble sort stable if we only swap when strictly out of order).
   Case 4: both not None -> 
       - If a.priority < b.priority -> a should be after b -> True.
       - If a.priority > b.priority -> a should be before b -> False.
       - If a.priority == b.priority -> sort by created_at ascending. If a.created_at > b.created_at -> True. If a.created_at < b.created_at -> False.

   Let's simplify the comparison logic into a single return value for "should swap".
   Actually, I can define a "sort key" tuple for comparison, but since I'm implementing bubble sort manually, I can just write a helper function or inline the logic.

   Let's define a function `compare(a, b)` that returns -1, 0, 1, or a boolean "a should come after b".
   I'll use: `should_swap = not (a is before b)`. Easier: `out_of_order = (a_priority handling) ...`

   Let's just write the condition directly in the bubble sort loop, or a helper.

   Proposed helper:
   ```python
   def _should_swap(task_a, task_b):
       # Returns True if task_a should come after task_b (i.e., they are in wrong order)
       pri_a = task_a["priority"]
       pri_b = task_b["priority"]
       ca = task_a["created_at"]
       cb = task_b["created_at"]
       
       if pri_a is None and pri_b is None:
           return ca > cb  # ascending created_at: if a's timestamp is greater, it should swap (come after)
       if pri_a is None:
           return True  # None always at end, so if a is None and b is not, a should be after b -> swap
       if pri_b is None:
           return False  # b is None, a is not -> a should be before b -> no swap
       # Both have priorities
       if pri_a < pri_b:
           return True  # a has lower priority, should be after b
       if pri_a > pri_b:
           return False  # a has higher priority, should be before b
       # Priorities equal
       return ca > cb  # ascending created_at
   ```

   Let's test this logic against the example:
   tasks = [
       {"name": "bug", "priority": 3, "created_at": 1000},
       {"name": "feature", "priority": 5, "created_at": 2000},
       {"name": "docs", "priority": 3, "created_at": 500},
   ]
   Expected sorted: feature (5,2000), docs (3,500), bug (3,1000)
   Let's simulate bubble sort manually or just trust the logic, but let's test the helper:
   - Compare bug(3,1000) and feature(5,2000): pri_a=3 < pri_b=5 -> should_swap=True -> they would swap. Good, feature should come first.
   - Compare bug(3,1000) and docs(3,500): pri equal, ca=1000 > cb=500 -> should_swap=True -> swap, docs before bug. Good.
   - Compare feature(5,2000) and docs(3,500): pri_a=5 > pri_b=3 -> should_swap=False -> no swap. Good.

   Edge case: None priorities.
   tasks = [
       {"name": "a", "priority": None, "created_at": 100},
       {"name": "b", "priority": 1, "created_at": 50},
       {"name": "c", "priority": None, "created_at": 200},
   ]
   Expected: b first (priority 1), then a and c ordered by created_at ascending: a(100), c(200).
   Let's check helper:
   - a(None,100) and b(1,50): pri_a None -> should_swap=True -> a after b. Good.
   - b(1,50) and c(None,200): pri_b None -> should_swap=False -> b before c. Good.
   - a(None,100) and c(None,200): both None -> ca > cb? 100 > 200 False -> no swap -> a before c. Good. Sorted: b, a, c. Correct.

   Looks solid.

3.  **Bubble Sort Implementation Details:**
   - Must not modify original list -> make a copy. `tasks = list(original)` or `[task for task in original]` or `copy.deepcopy` if nested, but dicts are flat enough for `list()` or `[:]`. Since task dicts are simple, `sorted_tasks = tasks[:]` or `list(tasks)` is fine.
   - swap_count: integer, increment each time we actually swap two adjacent elements.
   - Standard bubble sort: 
     ```python
     n = len(arr)
     for i in range(n):
         swapped = False
         for j in range(0, n - i - 1):
             if should_swap(arr[j], arr[j+1]):
                 arr[j], arr[j+1] = arr[j+1], arr[j]
                 swap_count += 1
                 swapped = True
         if not swapped:
             break
     ```
   - Return `(sorted_list, swap_count)`

4.  **Code Structure:**
   - File: `bubble_sort.py`
   - Function: `bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:`
   - Docstring explaining behavior, rules, return value.
   - Type hints.
   - Helper function or inline logic.
   - Clean, idiomatic Python.

   Let's write the code carefully.

   One detail: "Do not modify the original input list — return a new list". I'll copy the list at the start.

   Another detail: swap_count counts total swaps performed. I'll initialize to 0 and increment on each swap.

   Let's write the full code:

   ```python
   """Bubble sort implementation for task records."""

   from typing import list, dict, tuple


   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       """
       Sort a list of task dictionaries using bubble sort.

       Sorting rules:
       - Primary: "priority" descending (higher priority first)
       - Tiebreaker: when priorities are equal, sort by "created_at" ascending (earlier timestamp first)
       - Null handling: tasks where "priority" is None always sort to the end,
         ordered by "created_at" ascending among themselves.

       Args:
           tasks: A list of dictionaries, each with keys "name", "priority" (int or None),
                  and "created_at" (int).

       Returns:
           A tuple containing:
           - A new list of task dictionaries sorted according to the rules.
           - The total number of element swaps performed during sorting.

       Constraints:
           - Implements the bubble sort algorithm; does not use Python's built-in sort/sorted.
           - Does not modify the original input list.
       """
       # Work on a copy so the original list is not modified
       sorted_tasks = tasks[:]  # shallow copy is fine for flat dicts
       n = len(sorted_tasks)
       swap_count = 0

       # Helper to determine if two tasks are in the wrong order
       def _should_swap(a: dict, b: dict) -> bool:
           pri_a = a["priority"]
           pri_b = b["priority"]
           ca = a["created_at"]
           cb = b["created_at"]

           if pri_a is None and pri_b is None:
               # Both None: sort by created_at ascending
               return ca > cb
           if pri_a is None:
               # a is None, b is not -> a should be at the end
               return True
           if pri_b is None:
               # b is None, a is not -> a should come before b
               return False
           # Both have priorities
           if pri_a < pri_b:
               return True  # lower priority should come after
           if pri_a > pri_b:
               return False  # higher priority should come before
           # Priorities equal: sort by created_at ascending
           return ca > cb

       # Standard bubble sort
       for i in range(n):
           swapped = False
           # After each pass, the largest (in terms of our ordering) element bubbles to the end
           for j in range(0, n - i - 1):
               if _should_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                   sorted_tasks[j], sorted_tasks[j + 1] = sorted_tasks[j + 1], sorted_tasks[j]
                   swap_count += 1
                   swapped = True
           if not swapped:
               break

       return sorted_tasks, swap_count
   ```

   Wait, type hints: `list[dict]` is fine, but I should use `from typing import List` if targeting older Python, but the prompt uses `list[dict]` in the signature, which is valid Python 3.9+. I'll just use `list[dict]` and `tuple` as given. I'll add `from __future__ import annotations` if needed, but not necessary. I'll keep it simple.

   Let's double-check the example:
   tasks = [
       {"name": "bug", "priority": 3, "created_at": 1000},
       {"name": "feature", "priority": 5, "created_at": 2000},
       {"name": "docs", "priority": 3, "created_at": 500},
   ]
   Sorted expected: feature, docs, bug. Swaps = 2.

   Let's simulate the code's bubble sort on this:
   Initial: [bug(3,1000), feature(5,2000), docs(3,500)]
   n=3
   i=0:
     j=0: compare bug and feature: pri 3 < 5 -> _should_swap=True -> swap -> [feature, bug, docs], swap_count=1
     j=1: compare bug and docs: pri equal 3==3, ca=1000 > cb=500 -> _should_swap=True -> swap -> [feature, docs, bug], swap_count=2
     end of inner loop. swapped=True
   i=1:
     j=0: compare feature and docs: pri 5 > 3 -> _should_swap=False -> no swap
     end. swapped=False -> break
   Return ([feature, docs, bug], 2). Matches example perfectly.

   Edge cases to consider:
   - Empty list: should return ([], 0). Our code: n=0, loops don't run, returns ([], 0). Good.
   - Single element: returns same list, 0 swaps. Good.
   - All None priorities: sorted by created_at ascending. Let's test mentally: [a(None,300), b(None,100), c(None,200)]
     i=0: j=0: a vs b: both None, ca=300 > cb=100 -> True -> swap -> [b, a, c], count=1
           j=1: a vs c: 200 > 200? ca=200 > cb=200? Actually a has 200? Wait initial: a(300), b(100), c(200). After first swap: [b(100), a(300), c(200)]. j=1: compare a(300) and c(200): ca=300 > cb=200 -> True -> swap -> [b, c, a], count=2.
     i=1: j=0: compare b(100) and c(200): 200 > 100? Actually _should_swap(b,c): both None, ca=100 > cb=200? b's ca is 100, c's ca is 200 -> 100 > 200 False -> no swap.
     End. Result: [b(100), c(200), a(300)]. Correct ascending order. Swaps=2.
   - Mixed None and non-None with equal priorities etc. Seems robust.

   One thing: the prompt says "tasks where `priority` is `None` always sort to the end of the list, ordered by `"created_at"` ascending among themselves". My logic handles that.

   I should also consider if `priority` can be other types? It says `int or None`. So fine.

   Code style: docstring, type hints, comments, helper inside or outside? Inside is fine, keeps it contained. I'll make sure it's clean.

   One minor point: the function signature in prompt has `list[dict]` but dicts have specific keys. I could add a type alias or just use `dict`. The prompt shows `list[dict]` in signature, I'll stick to that or improve slightly. I'll use `list[dict]` as given, but maybe add a comment about expected keys. Or I can use `list[dict[str, int | None | str]]` but that's verbose. I'll just use the exact signature from prompt: `def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:`. I'll add `from typing import Optional` if needed, but not necessary.

   Let's write the final code exactly as required, with proper docstring, and ensure it's a single file `bubble_sort.py`.

   I'll now produce the final answer. I'll output the code block with the file content. I'll also briefly explain the logic if needed, but the prompt just says "Write clean, well-documented, idiomatic Python code." So I'll provide the code.

   One final check: "Do not use Python's built-in `sort()`, `sorted()`, or any other sorting function". My implementation only uses loops and swaps, no sort calls. Good.

   "Return a tuple of `(sorted_list, swap_count)` where `swap_count` is the total number of element swaps performed during sorting". Yes.

   "Do not modify the original input list — return a new list". I do `sorted_tasks = tasks[:]`. Good.

   Everything looks solid. I'll generate the response.✅


## Response

Here's a clean, idiomatic implementation of `bubble_sort.py` that follows all the specified rules:

```python
"""Bubble sort for task records with custom priority/timestamp ordering."""

from typing import list, dict, tuple


def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sort a list of task dictionaries using the bubble sort algorithm.

    Sorting rules:
    - Primary:  `"priority"` descending  (higher priority comes first)
    - Tiebreaker: when priorities are equal, sort by `"created_at"` ascending
                  (earlier timestamp comes first)
    - Null handling: tasks where `"priority"` is `None` always sort to the end,
      ordered by `"created_at"` ascending among themselves

    Args:
        tasks: A list of dictionaries. Each dict must contain:
               - "name"        : str
               - "priority"    : int or None
               - "created_at"  : int (unix timestamp)

    Returns:
        A tuple of `(sorted_list, swap_count)`:
        - sorted_list: a new list sorted per the rules above (original list unchanged)
        - swap_count: total number of adjacent swaps performed during sorting

    Constraints:
        - Implements bubble sort manually — no built-in `sort()`/`sorted()` used.
        - Does not modify the input list.
    """
    # Work on a shallow copy so the original list is never mutated
    sorted_tasks = tasks[:]
    n = len(sorted_tasks)
    swap_count = 0

    def _should_swap(a: dict, b: dict) -> bool:
        """
        Return True if task `a` should appear after task `b` (i.e. they are out of order).
        """
        pri_a, pri_b = a["priority"], b["priority"]
        ca, cb = a["created_at"], b["created_at"]

        # Both None → sort by created_at ascending
        if pri_a is None and pri_b is None:
            return ca > cb

        # a is None, b is not → None always goes to the end
        if pri_a is None:
            return True

        # b is None, a is not → a stays before the None block
        if pri_b is None:
            return False

        # Both have priorities
        if pri_a < pri_b:
            return True       # lower priority should come after
        if pri_a > pri_b:
            return False      # higher priority should come before

        # Priorities equal → sort by created_at ascending
        return ca > cb

    # Standard bubble sort with early termination
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if _should_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                sorted_tasks[j], sorted_tasks[j + 1] = (
                    sorted_tasks[j + 1],
                    sorted_tasks[j],
                )
                swap_count += 1
                swapped = True
        if not swapped:
            break

    return sorted_tasks, swap_count
```

**How it works:**
- A shallow copy of the input list is made immediately so the original is never touched.
- An inner helper `_should_swap` encodes the full ordering logic: `None` priorities always lose to any integer priority, higher integer priorities come first, and ties are broken by `created_at` ascending.
- The bubble sort loops compare adjacent elements and swap when `_should_swap` returns `True`, incrementing `swap_count` each time.
- The outer loop includes an early-exit optimization (`swapped` flag) that keeps the algorithm efficient on nearly-sorted data while still respecting the bubble sort paradigm.

**Example usage:**
```python
tasks = [
    {"name": "bug",     "priority": 3, "created_at": 1000},
    {"name": "feature", "priority": 5, "created_at": 2000},
    {"name": "docs",    "priority": 3, "created_at": 500},
]

sorted_tasks, swaps = bubble_sort_tasks(tasks)
# sorted_tasks == [
#     {"name": "feature", "priority": 5, "created_at": 2000},
#     {"name": "docs",    "priority": 3, "created_at": 500},
#     {"name": "bug",     "priority": 3, "created_at": 1000},
# ]
# swaps == 2
```

## Timings

- Time to first token: 1.03s
- Total generation: 104.51s
- Reasoning tokens: 3814
- Answer tokens: 1071
- Total tokens: 4885

## Server Timings (llama.cpp)

- Prompt tokens: 486
- Prompt eval speed: 477.61 t/s
- Prompt eval time: 1017.56 ms
- Generation tokens: 4885
- Generation speed: 47.19 t/s
- Generation time: 103486.13 ms
