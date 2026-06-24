# Code Eval: Qwen3.6-35B-A3B-UD-Q4_K_M

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
     - Primary: `"priority"` descending (higher first)
     - Tiebreaker: `"created_at"` ascending (earlier first)
     - `None` priority: always at the end, sorted by `"created_at"` ascending among themselves.
   - **Constraints**:
     - Must use bubble sort.
     - No built-in sort/sorted.
     - Return `(sorted_list, swap_count)`.
     - Do not modify original list (return a new list).
   - **Output**: Clean, documented, idiomatic Python with type hints and docstring.

3.  **Design the Comparison Logic**:
   I need a helper function or inline logic to compare two tasks `a` and `b`.
   Rules for comparison (to determine if `a` should come before `b`):
   - If `a["priority"]` is `None` and `b["priority"]` is not `None`: `a` should come after `b` → `a > b` in sort order.
   - If `a["priority"]` is not `None` and `b["priority"]` is `None`: `a` should come before `b` → `a < b`.
   - If both are `None`: compare by `"created_at"` ascending. If `a["created_at"] > b["created_at"]`, `a` comes after `b`.
   - If both are not `None`:
     - Compare priorities descending: if `a["priority"] < b["priority"]`, `a` comes after `b`.
     - If priorities equal, compare `"created_at"` ascending: if `a["created_at"] > b["created_at"]`, `a` comes after `b`.

   Let's formalize a comparison function `should_swap(a, b)` that returns `True` if `a` should come after `b` (i.e., they are in the wrong order for descending priority/ascending created_at).
   Actually, bubble sort typically swaps adjacent elements if they are in the wrong order. So I'll define a function `is_out_of_order(a, b)` that returns `True` if `a` should be swapped with `b` (i.e., `a` should come after `b`).

   Let's write out the conditions for `is_out_of_order(a, b)`:
   ```python
   def is_out_of_order(a, b):
       a_pri = a["priority"]
       b_pri = b["priority"]
       a_time = a["created_at"]
       b_time = b["created_at"]

       # Handle None priorities
       if a_pri is None and b_pri is not None:
           return True  # a should be after b
       if a_pri is not None and b_pri is None:
           return False # a should be before b

       # Both are None
       if a_pri is None and b_pri is None:
           return a_time > b_time  # ascending created_at

       # Both are not None
       if a_pri < b_pri:
           return True  # descending priority
       if a_pri > b_pri:
           return False
       # Priorities equal
       return a_time > b_time  # ascending created_at
   ```

   Wait, let's double-check the `None` handling rule: "tasks where `priority` is `None` always sort to the end of the list, ordered by `"created_at"` ascending among themselves". This matches the logic above.

   Let's test the logic mentally:
   - `a` pri=3, `b` pri=5 → `a_pri < b_pri` → returns True → swap → correct (5 comes before 3)
   - `a` pri=5, `b` pri=3 → `a_pri > b_pri` → returns False → no swap → correct
   - `a` pri=3, `b` pri=3, `a_time`=1000, `b_time`=500 → `a_time > b_time` → returns True → swap → correct (500 comes before 1000)
   - `a` pri=None, `b` pri=5 → returns True → swap → correct (5 comes before None)
   - `a` pri=5, `b` pri=None → returns False → no swap → correct
   - `a` pri=None, `b` pri=None, `a_time`=1000, `b_time`=500 → returns True → swap → correct (500 before 1000)

   The logic seems solid.

4.  **Implement Bubble Sort**:
   Standard bubble sort:
   ```python
   n = len(tasks)
   swapped = True
   swap_count = 0
   while swapped:
       swapped = False
       for i in range(n - 1):
           if is_out_of_order(tasks[i], tasks[i+1]):
               tasks[i], tasks[i+1] = tasks[i+1], tasks[i]
               swap_count += 1
               swapped = True
   ```
   Wait, the constraint says "Do not modify the original input list — return a new list". So I need to copy the list first: `tasks = list(tasks)` or `tasks = tasks.copy()`.

   Let's integrate this:
   ```python
   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       # Create a shallow copy to avoid modifying the original list
       sorted_tasks = tasks.copy()
       n = len(sorted_tasks)
       swap_count = 0
       swapped = True

       while swapped:
           swapped = False
           for i in range(n - 1):
               a = sorted_tasks[i]
               b = sorted_tasks[i+1]

               # Determine if a should come after b
               a_pri, b_pri = a["priority"], b["priority"]
               a_time, b_time = a["created_at"], b["created_at"]

               should_swap = False
               if a_pri is None and b_pri is not None:
                   should_swap = True
               elif a_pri is not None and b_pri is None:
                   should_swap = False
               elif a_pri is None and b_pri is None:
                   should_swap = a_time > b_time
               else:
                   if a_pri < b_pri:
                       should_swap = True
                   elif a_pri > b_pri:
                       should_swap = False
                   else:
                       should_swap = a_time > b_time

               if should_swap:
                   sorted_tasks[i], sorted_tasks[i+1] = sorted_tasks[i+1], sorted_tasks[i]
                   swap_count += 1
                   swapped = True

       return sorted_tasks, swap_count
   ```

5.  **Refine & Optimize**:
   The inline comparison logic is a bit verbose. I can extract it into a helper function or keep it inline but cleaner. Since it's a single file, a nested helper or just inline is fine. I'll keep it inline for performance/clarity, but structure it well. Actually, a helper function inside or outside is fine. I'll put it inside or just use a clear conditional block.

   Let's consider using a tuple comparison trick? Not really, because of `None` handling and mixed descending/ascending. The explicit logic is safer and clearer.

   Wait, bubble sort can be optimized with an early exit if no swaps occur in a pass. I already have `swapped` flag. That's good.

   Let's check the example:
   ```python
   tasks = [
       {"name": "bug",     "priority": 3, "created_at": 1000},
       {"name": "feature", "priority": 5, "created_at": 2000},
       {"name": "docs",    "priority": 3, "created_at": 500},
   ]
   ```
   Pass 1:
   - i=0: bug(3,1000) vs feature(5,2000) → pri 3 < 5 → should_swap=True → swap → [feature, bug, docs], swaps=1
   - i=1: bug(3,1000) vs docs(3,500) → pri equal, time 1000 > 500 → should_swap=True → swap → [feature, docs, bug], swaps=2
   Pass 2:
   - i=0: feature(5,2000) vs docs(3,500) → pri 5 > 3 → should_swap=False
   - i=1: docs(3,500) vs bug(3,1000) → pri equal, time 500 < 1000 → should_swap=False
   No swaps → done.
   Result: swaps=2. Matches example.

   One minor thing: `tasks.copy()` creates a shallow copy, which is fine since we're only swapping references to dicts, not modifying dict contents.

   Let's structure the code properly with type hints, docstring, and maybe a helper function for readability.

   ```python
   from typing import Any

   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       """
       Sorts a list of task dictionaries using the bubble sort algorithm.

       Sorting rules:
           1. Primary: priority descending (higher first)
           2. Tiebreaker: created_at ascending (earlier first)
           3. None priorities are placed at the end, sorted by created_at ascending.

       Args:
           tasks: List of task dictionaries with keys 'name', 'priority', 'created_at'.

       Returns:
           A tuple containing the sorted list and the total number of swaps performed.
       """
       # Work on a copy to avoid mutating the original list
       arr = tasks.copy()
       n = len(arr)
       swap_count = 0
       swapped = True

       while swapped:
           swapped = False
           for i in range(n - 1):
               a = arr[i]
               b = arr[i + 1]

               a_pri, b_pri = a["priority"], b["priority"]
               a_time, b_time = a["created_at"], b["created_at"]

               # Determine if a should be swapped with b
               if a_pri is None and b_pri is not None:
                   should_swap = True
               elif a_pri is not None and b_pri is None:
                   should_swap = False
               elif a_pri is None and b_pri is None:
                   should_swap = a_time > b_time
               else:
                   if a_pri < b_pri:
                       should_swap = True
                   elif a_pri > b_pri:
                       should_swap = False
                   else:
                       should_swap = a_time > b_time

               if should_swap:
                   arr[i], arr[i + 1] = arr[i + 1], arr[i]
                   swap_count += 1
                   swapped = True

       return arr, swap_count
   ```

   Wait, `typing.Any` isn't needed. I'll stick to standard type hints. The signature uses `list[dict]` which is valid in Python 3.9+. I'll assume modern Python.

   Let's double-check the constraints:
   - "You must implement the bubble sort algorithm — do not use Python's built-in `sort()`, `sorted()`, or any other sorting function" -> Checked.
   - "Return a tuple of `(sorted_list, swap_count)`" -> Checked.
   - "Do not modify the original input list — return a new list" -> Checked (`tasks.copy()`).
   - Type hints and docstring -> Checked.

   One potential improvement: The comparison logic can be slightly cleaner. I'll extract it to a nested function or keep it as is. It's fine as is.

   Let's consider edge cases:
   - Empty list: `n=0`, loop doesn't run, returns `([], 0)`. Correct.
   - Single element: `n=1`, loop doesn't run, returns `([task], 0)`. Correct.
   - All `None` priorities: sorted by `created_at` ascending. Correct.
   - All same priority: sorted by `created_at` ascending. Correct.
   - Mixed `None` and numbers: `None`s go to end. Correct.

   Is there any issue with `tasks.copy()`? It's a shallow copy, which is exactly what we want for bubble sort swapping references.

   One thing: The problem says `list[dict]` in the signature. I'll keep it exactly as requested.

   Let's verify the comparison logic once more carefully:
   Rule 1: priority descending. So if `a_pri < b_pri`, `a` should come after `b` → swap.
   Rule 2: created_at ascending. So if `a_time > b_time`, `a` should come after `b` → swap.
   Rule 3: None at end. So if `a_pri is None` and `b_pri is not None`, `a` should come after `b` → swap.
   If `a_pri is not None` and `b_pri is None`, `a` should come before `b` → no swap.
   If both None, compare created_at ascending → swap if `a_time > b_time`.

   All conditions match `should_swap = True` when `a` should be after `b`.
   The logic is correct.

   I'll write out the final code. I'll add a helper function for clarity, or just keep it inline. Inline is fine. I'll make sure it's well-documented.

   One minor point: `list[dict]` syntax requires Python 3.9+. The prompt uses it, so it's fine. I'll stick to it.

   Final check of the code structure:
   ```python
   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       """..."""
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

               should_swap = False
               if a_pri is None and b_pri is not None:
                   should_swap = True
               elif a_pri is not None and b_pri is None:
                   should_swap = False
               elif a_pri is None and b_pri is None:
                   should_swap = a_time > b_time
               else:
                   if a_pri < b_pri:
                       should_swap = True
                   elif a_pri > b_pri:
                       should_swap = False
                   else:
                       should_swap = a_time > b_time

               if should_swap:
                   sorted_tasks[i], sorted_tasks[i + 1] = sorted_tasks[i + 1], sorted_tasks[i]
                   swap_count += 1
                   swapped = True

       return sorted_tasks, swap_count
   ```

   This looks solid. I'll add type hints for the inner variables if needed, but not strictly necessary. I'll keep it clean.
   I should also consider if `tasks` could be `None`? The type hint says `list[dict]`, so assume valid input.
   I'll wrap it in a proper file structure as requested.

   One thing: The prompt says "Write a single file `bubble_sort.py` containing a function with this exact signature". I'll provide just the code block.

   I'll also add a quick test/example in a `if __name__ == "__main__":` block to demonstrate it works, though not strictly required. It's good practice.

   Let's verify the example output matches exactly:
   Input:
   ```python
   tasks = [
       {"name": "bug",     "priority": 3, "created_at": 1000},
       {"name": "feature", "priority": 5, "created_at": 2000},
       {"name": "docs",    "priority": 3, "created_at": 500},
   ]
   ```
   Output:
   `sorted_tasks` matches example.
   `swaps` = 2. Matches example.

   All good.

   One minor improvement: I can make the comparison logic slightly more Pythonic by using a tuple key, but the constraint says "implement the bubble sort algorithm", and using a key function might be seen as bypassing the spirit, though it's fine. But explicit comparison is safer and clearer for bubble sort. I'll stick to explicit.

   Actually, I can simplify the comparison using a helper function that returns a comparison value, but explicit `if/elif` is fine.

   I'll produce the final code.
   I'll make sure to include proper docstring, type hints, and comments.
   Ready.✅
   Output matches requirements.
   One detail: `list[dict]` is valid in Python 3.9+. I'll assume that's fine. If they want compatibility with 3.8, they'd use `List[Dict]` from `typing`, but the prompt uses `list[dict]`, so I'll stick to it.

   Final code structure:
   ```python
   def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
       """..."""
       ...
   ```
   All set. Output matches.✅
   I will generate the response now. 
   Self-Correction/Verification during thought:
   Wait, let's double check the `None` handling rule: "tasks where `priority` is `None` always sort to the end of the list, ordered by `"created_at"` ascending among themselves".
   My logic:
   `if a_pri is None and b_pri is not None: should_swap = True` -> correct, None goes after non-None.
   `elif a_pri is not None and b_pri is None: should_swap = False` -> correct.
   `elif a_pri is None and b_pri is None: should_swap = a_time > b_time` -> correct, ascending time.
   `else:` (both not None) -> handles priority desc, then time asc.
   This covers all cases correctly.

   One edge case: What if `created_at` is also `None`? The prompt says `"created_at": int`, so it's always an int. No need to handle `None` for `created_at`.

   The code is robust. I'll present it. 
   I'll also add a small test block to show it works, as is standard.
   All constraints met.
   Proceed. 
   Output generation. 
   [Done] 
   *Self-Correction/Refinement during generation prep*: 
   I should make sure the function signature exactly matches: `def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:`
   I'll keep it exactly as requested.
   I'll add type hints for internal variables if needed, but not required.
   I'll ensure the docstring is comprehensive.
   The code is ready.✅
   Output matches response. 
   Proceeds. 
   [Output Generation] -> *See response.* 
   *(Note: I'll make sure the code is clean and well-formatted.)*
   All good. 
   [Final Check of the Prompt]: "Write a single file `bubble_sort.py` containing a function with this exact signature:" -> I will provide the full file content.
   "Include type hints and a docstring." -> Done.
   "Do not modify the original input list — return a new list" -> `tasks.copy()` handles this.
   "Return a tuple of `(sorted_list, swap_count)`" -> Done.
   "You must implement the bubble sort algorithm" -> Done.
   All constraints satisfied.✅
   Output matches. 
   [Done]


## Response

Here's the complete, well-documented implementation in `bubble_sort.py`:

```python
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
```

### Key Implementation Details:
1. **Non-Mutation**: `tasks.copy()` creates a shallow copy, ensuring the original list remains untouched while allowing efficient reference swapping.
2. **Comparison Logic**: Explicitly handles all three sorting rules in a single pass per adjacent pair. `None` priorities are correctly pushed to the end, and tiebreakers are applied only when necessary.
3. **Early Exit Optimization**: The `swapped` flag breaks the outer loop as soon as a full pass completes without any swaps, improving best-case time complexity to `O(n)`.
4. **Swap Counting**: Every successful adjacent swap increments `swap_count`, exactly matching the algorithm's execution trace.
5. **Type Hints & Docstring**: Fully compliant with modern Python typing standards and includes comprehensive documentation.

## Timings

- Time to first token: 0.57s
- Total generation: 91.16s
- Reasoning tokens: 4477
- Answer tokens: 962
- Total tokens: 5439
