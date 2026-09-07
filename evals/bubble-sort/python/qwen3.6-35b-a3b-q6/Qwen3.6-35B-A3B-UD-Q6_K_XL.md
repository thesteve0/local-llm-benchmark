# Code Eval: Qwen3.6-35B-A3B-UD-Q6_K_XL

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

1.  **Understand the Goal**: The user wants a Python function `bubble_sort_tasks` that sorts a list of task dictionaries using the bubble sort algorithm. It must follow specific sorting rules, handle `None` priorities, return a new list, count swaps, and not use built-in sorting functions.

2.  **Analyze Requirements**:
   - **Function Signature**: `def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:`
   - **Input**: List of dicts with keys `"name"`, `"priority"`, `"created_at"`.
   - **Sorting Rules**:
     - Primary: `priority` descending (higher first)
     - Tiebreaker: `created_at` ascending (earlier first)
     - `None` priority: always at the end, sorted by `created_at` ascending among themselves.
   - **Constraints**:
     - Must use bubble sort.
     - No built-in sort/sorted.
     - Return `(sorted_list, swap_count)`.
     - Do not modify original list (return a new list).
   - **Output**: Tuple of sorted list and integer swap count.
   - **Code Quality**: Clean, well-documented, idiomatic, type hints, docstring.

3.  **Determine Sorting Logic**:
   I need a comparison function or logic to decide if two elements should be swapped.
   Let's define a comparison rule for two tasks `a` and `b`:
   - If `a["priority"]` is `None` and `b["priority"]` is not `None`: `a` should come after `b` → swap needed if `a` is before `b`.
   - If `a["priority"]` is not `None` and `b["priority"]` is `None`: `a` should come before `b` → no swap.
   - If both are `None`: compare `created_at` ascending. If `a["created_at"] > b["created_at"]`, swap.
   - If both are not `None`:
     - Compare `priority` descending: if `a["priority"] < b["priority"]`, swap.
     - If equal priority, compare `created_at` ascending: if `a["created_at"] > b["created_at"]`, swap.
     - Otherwise, no swap.

   Let's formalize the condition for swapping `a` and `b` when `a` is immediately before `b`:
   We want to swap if `a` should come *after* `b`.
   So, `should_swap(a, b)` returns `True` if `a` > `b` in our custom order.
   Custom order: Higher priority first, then earlier created_at first, then None priority last.
   Let's define a key function or just inline the comparison.
   Actually, bubble sort typically compares adjacent elements and swaps if they are out of order.
   Let's define a comparison function `is_out_of_order(a, b)`:
   ```python
   def is_out_of_order(a, b):
       # Handle None priorities
       a_none = a["priority"] is None
       b_none = b["priority"] is None

       if a_none and not b_none:
           return True  # a should be after b
       if not a_none and b_none:
           return False # a should be before b
       if a_none and b_none:
           return a["created_at"] > b["created_at"] # ascending created_at

       # Both have priorities
       if a["priority"] < b["priority"]:
           return True  # descending priority
       if a["priority"] > b["priority"]:
           return False
       # Equal priority, ascending created_at
       return a["created_at"] > b["created_at"]
   ```
   Wait, let's double check the `None` handling rule: "tasks where priority is None always sort to the end of the list, ordered by created_at ascending among themselves". This matches the logic above.

   Let's test the logic mentally:
   - `a` priority 3, `b` priority 5 → `a["priority"] < b["priority"]` → True → swap. Correct.
   - `a` priority 5, `b` priority 3 → `a["priority"] > b["priority"]` → False → no swap. Correct.
   - `a` priority 3, `b` priority 3, `a.created` 1000, `b.created` 500 → `a.created > b.created` → True → swap. Correct.
   - `a` priority None, `b` priority 3 → `a_none` True, `b_none` False → True → swap. Correct.
   - `a` priority 3, `b` priority None → `a_none` False, `b_none` True → False → no swap. Correct.
   - `a` priority None, `b` priority None, `a.created` 1000, `b.created` 500 → `a.created > b.created` → True → swap. Correct.

   This logic seems solid.

4.  **Implement Bubble Sort**:
   Standard bubble sort:
   ```python
   n = len(tasks)
   sorted_tasks = tasks.copy() # or list(tasks)
   swap_count = 0
   for i in range(n):
       swapped = False
       for j in range(0, n - i - 1):
           if is_out_of_order(sorted_tasks[j], sorted_tasks[j+1]):
               sorted_tasks[j], sorted_tasks[j+1] = sorted_tasks[j+1], sorted_tasks[j]
               swap_count += 1
               swapped = True
       if not swapped:
           break
   return sorted_tasks, swap_count
   ```
   Wait, the constraint says "Do not modify the original input list — return a new list". `list(tasks)` or `tasks.copy()` works.

   Let's refine the comparison logic to be inline or a helper function inside the main function to keep it self-contained. I'll put it inside or just write it out clearly.

   Actually, I can make it more concise:
   ```python
   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       arr = list(tasks)
       n = len(arr)
       swap_count = 0

       for i in range(n):
           swapped = False
           for j in range(0, n - i - 1):
               a, b = arr[j], arr[j+1]
               a_none = a["priority"] is None
               b_none = b["priority"] is None

               should_swap = False
               if a_none and not b_none:
                   should_swap = True
               elif not a_none and b_none:
                   should_swap = False
               elif a_none and b_none:
                   should_swap = a["created_at"] > b["created_at"]
               else:
                   if a["priority"] < b["priority"]:
                       should_swap = True
                   elif a["priority"] > b["priority"]:
                       should_swap = False
                   else:
                       should_swap = a["created_at"] > b["created_at"]

               if should_swap:
                   arr[j], arr[j+1] = arr[j+1], arr[j]
                   swap_count += 1
                   swapped = True
           if not swapped:
               break

       return arr, swap_count
   ```

   This is correct but a bit verbose. I can extract the comparison logic into a nested function or just keep it clean. I'll stick with a nested helper for readability.

   Let's consider edge cases:
   - Empty list: `n=0`, loops won't run, returns `([], 0)`. Correct.
   - Single element: `n=1`, inner loop range(0, 0) doesn't run, returns `([task], 0)`. Correct.
   - All `None` priorities: sorts by `created_at` ascending. Correct.
   - Mixed priorities: works as specified.

   One minor thing: The problem says `list[dict]` and `tuple[list[dict], int]`. I should use `typing.List` and `typing.Tuple` if Python < 3.9, but the prompt uses `list[dict]` which is Python 3.9+ syntax. I'll stick with that, or add `from __future__ import annotations` if needed, but it's fine as is. I'll assume modern Python.

   Let's verify the example:
   ```python
   tasks = [
       {"name": "bug",     "priority": 3, "created_at": 1000},
       {"name": "feature", "priority": 5, "created_at": 2000},
       {"name": "docs",    "priority": 3, "created_at": 500},
   ]
   ```
   Initial: `[bug(3,1000), feature(5,2000), docs(3,500)]`
   Pass 1:
   - j=0: compare bug(3,1000) and feature(5,2000). priority 3 < 5 → swap. `arr` becomes `[feature, bug, docs]`. swaps=1.
   - j=1: compare bug(3,1000) and docs(3,500). priority equal, created 1000 > 500 → swap. `arr` becomes `[feature, docs, bug]`. swaps=2.
   Pass 2:
   - j=0: compare feature(5,2000) and docs(3,500). priority 5 > 3 → no swap.
   - swapped is False? Wait, in pass 1, swapped was True. In pass 2, no swaps happen, so `swapped` remains False, loop breaks.
   Result: `[feature, docs, bug]`, swaps=2. Matches example exactly.

   The logic is solid.

5.  **Refine Code Structure**:
   I'll write it cleanly with type hints, docstring, and comments.
   I'll use a nested function for comparison to keep the main loop clean.
   I'll make sure to handle the `None` priority correctly.
   I'll add `from __future__ import annotations` just in case, but it's not strictly necessary. I'll stick to standard Python 3.9+ syntax as requested.

   Let's draft it:

   ```python
   from __future__ import annotations
   from typing import List, Tuple

   def bubble_sort_tasks(tasks: List[dict]) -> Tuple[List[dict], int]:
       """
       Sorts a list of task dictionaries using the bubble sort algorithm.

       Sorting rules:
           1. Primary: priority descending (higher first)
           2. Tiebreaker: created_at ascending (earlier first)
           3. None priorities are pushed to the end, sorted by created_at ascending

       Args:
           tasks: List of task dictionaries with 'name', 'priority', and 'created_at' keys.

       Returns:
           A tuple containing the sorted list and the total number of swaps performed.
       """
       # Create a shallow copy to avoid modifying the original list
       arr = list(tasks)
       n = len(arr)
       swap_count = 0

       def should_swap(a: dict, b: dict) -> bool:
           """Returns True if a should come after b (i.e., they are out of order)."""
           a_none = a["priority"] is None
           b_none = b["priority"] is None

           if a_none and not b_none:
               return True
           if not a_none and b_none:
               return False
           if a_none and b_none:
               return a["created_at"] > b["created_at"]

           # Both have valid priorities
           if a["priority"] < b["priority"]:
               return True
           if a["priority"] > b["priority"]:
               return False
           # Equal priority, sort by created_at ascending
           return a["created_at"] > b["created_at"]

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
   ```

   Wait, `List` and `Tuple` from `typing` are fine, but the prompt uses `list[dict]` and `tuple[list[dict], int]`. I'll stick to the prompt's syntax for type hints to be consistent, or use `typing` if needed. Python 3.9+ supports `list[dict]` natively. I'll just use the prompt's signature exactly.

   Let's check if there's any issue with `should_swap` being defined inside. It's fine.
   Could I make it more efficient/cleaner? The comparison logic is clear.
   One thing: `a["priority"]` might be missing? The prompt says each task dictionary has these keys. So safe.
   I'll add a quick check or just assume valid input as per spec.

   Let's test mentally with another case:
   `tasks = [{"priority": None, "created_at": 300}, {"priority": 2, "created_at": 100}]`
   `a_none=True, b_none=False` → `should_swap` returns True → swap. Correct.
   `tasks = [{"priority": None, "created_at": 300}, {"priority": None, "created_at": 100}]`
   `a_none=True, b_none=True` → `300 > 100` → True → swap. Correct.

   All good.

   I should ensure the function signature matches exactly:
   `def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:`
   I'll use that exactly.

   One minor point: bubble sort optimization with `swapped` flag is standard and good.
   I'll add comments explaining the sorting rules implementation.
   I'll make sure the docstring is comprehensive.

   Final check of the prompt: "Do not modify the original input list — return a new list". `list(tasks)` does a shallow copy, which is fine since we're only swapping references to dicts, not modifying the dicts themselves. If we were modifying dict contents, we'd need `copy.deepcopy`, but we're not. So `list(tasks)` is correct and efficient.

   Code structure:
   ```python
   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       """..."""
       arr = list(tasks)
       n = len(arr)
       swap_count = 0

       def is_out_of_order(a: dict, b: dict) -> bool:
           # ... logic ...
           pass

       # bubble sort loops
       # ...
       return arr, swap_count
   ```

   I'll write it out carefully.
   One thing: `list[dict]` syntax requires Python 3.9+. I'll assume that's fine. If I want to be safe, I can use `typing.List` but the prompt explicitly uses `list[dict]`. I'll stick to it.

   Let's draft the final response.
   I'll include type hints, docstring, and clean code.
   I'll also add a small test block in comments or just leave it as requested. The prompt says "Write a single file bubble_sort.py containing a function...". I'll provide just the function as requested, but I can wrap it in a complete file structure.

   One detail: `should_swap` logic can be slightly condensed but readability is better with explicit branches. I'll keep it explicit.

   Let's verify the tiebreaker rule again: "when priorities are equal, sort by created_at ascending (earlier timestamp comes first)". My code: `return a["created_at"] > b["created_at"]` for swap condition. If `a.created > b.created`, swap → `b` comes first. Correct.

   All constraints met.
   I will produce the final code. 
   I'll make sure to handle the `None` priority correctly with clear comments.
   I'll add `from __future__ import annotations` just in case the environment is older, but it's optional. I'll skip it to keep it clean, as `list[dict]` is already used in the prompt.

   Final code structure:
   ```python
   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       """
       Sorts a list of task dictionaries using the bubble sort algorithm.

       Sorting Rules:
           1. Primary: priority descending (higher priority first)
           2. Tiebreaker: created_at ascending (earlier timestamp first)
           3. None priorities are always placed at the end, sorted by created_at ascending

       Args:
           tasks: List of dictionaries containing 'name', 'priority', and 'created_at' keys.

       Returns:
           A tuple of (sorted_list, swap_count) where swap_count is the number of swaps performed.
       """
       # Create a new list to avoid modifying the original input
       arr = list(tasks)
       n = len(arr)
       swap_count = 0

       def should_swap(a: dict, b: dict) -> bool:
           """Returns True if a should be placed after b (i.e., they are out of order)."""
           a_none = a["priority"] is None
           b_none = b["priority"] is None

           # Rule 3: None priorities always go to the end
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
   ```

   This looks solid. I'll present it as requested.
   One minor consideration: The prompt says `list[dict]` and `tuple[list[dict], int]`. I'll keep that exact signature.
   I'll add a brief explanation if needed, but the code is self-contained.
   All constraints checked:
   - Bubble sort implemented? Yes.
   - No built-in sort? Yes.
   - Returns tuple of (sorted_list, swap_count)? Yes.
   - Doesn't modify original? Yes, `list(tasks)` creates a new list.
   - Handles None priorities correctly? Yes.
   - Type hints and docstring? Yes.
   - Clean and idiomatic? Yes.

   Ready. Output matches response.✅
   I will generate the response now. 
   Self-Correction/Verification during thought:
   Wait, `list(tasks)` creates a shallow copy. If the original list contains mutable dicts, swapping references in the copy won't affect the original list's order. That's correct. The requirement "Do not modify the original input list" refers to the list structure/order, not the dict contents. So `list(tasks)` is perfect.
   The comparison logic handles all cases correctly.
   The bubble sort implementation is standard with early exit optimization.
   Type hints match exactly.
   I'll output the code block. 
   One thing: I'll make sure the function signature exactly matches the prompt, including the `list[dict]` syntax. Python 3.9+ supports it. I'll assume that's fine.
   All good. 
   Proceeds. 
   Output Generation. 
   [Done] 
   *Self-Correction/Refinement during generation prep*: 
   I should ensure the code is strictly within `bubble_sort.py` as requested. I'll provide just the function as requested, but formatted as a complete file content. I'll add a `if __name__ == "__main__":` block with the example to demonstrate it works, but keep it optional or commented out to strictly follow "containing a function". The prompt says "Write a single file bubble_sort.py containing a function with this exact signature". I'll just provide the function. I'll add the example in a test block if needed, but it's fine.

   Final check of the code:
   ```python
   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       ...
   ```
   Matches exactly.
   I'll produce it. 
   Output matches the refined code.✅
   [Output Generation] -> *Proceeds*


## Response

Here's the complete, well-documented implementation in `bubble_sort.py`:

```python
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
```

### Key Implementation Details:
1. **Non-Mutating**: `list(tasks)` creates a new list object, guaranteeing the original input remains untouched.
2. **Comparison Logic**: The nested `should_swap` function cleanly encapsulates the three sorting rules. It returns `True` when adjacent elements are out of order, triggering a swap.
3. **Early Exit**: The `swapped` flag optimizes best-case performance to `O(n)` when the list is already sorted.
4. **Type Hints & Docstring**: Matches the requested signature exactly and includes comprehensive documentation for maintainability.
5. **No Built-ins**: Pure algorithmic implementation without `sort()`, `sorted()`, or `key` functions.

## Timings

- Time to first token: 0.86s
- Total generation: 104.67s
- Reasoning tokens: 4691
- Answer tokens: 783
- Total tokens: 5474

## Server Timings (llama.cpp)

- Prompt tokens: 488
- Prompt eval speed: 573.59 t/s
- Prompt eval time: 850.78 ms
- Generation tokens: 5474
- Generation speed: 52.72 t/s
- Generation time: 103807.31 ms
