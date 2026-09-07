# Code Eval: Qwen3.8-27B-UD-Q6_K_XL

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

We need answer user's request: implement bubble_sort.py. Need produce final code likely with explanation? User asks write single file. We need provide code. Need ensure bubble sort, no built-in sort. Need handle None priority to end, priority desc, created_at asc. Return new list, swap_count total swaps. Need clean documented idiomatic Python. Need think about bubble sort details and swap count. Need maybe stable? Bubble sort can be stable if only swap when strictly out of order. Need define comparison function: returns True if a should come before b? For bubble sort, we can bubble larger (according to order) to right. Need count swaps. Need not modify original list: copy list (shallow copy) enough? Task dicts not modified. Return new list. Could use list(tasks). Need type hints. Python 3.9+ list[dict]. Need maybe from __future__? Not necessary if modern. But if environment older? Requirement exact signature uses list[dict], tuple[list[dict], int], so Python 3.9+. Fine.

Need implement bubble sort. Need decide algorithm. Standard:
def bubble_sort_tasks(tasks):
    arr = list(tasks)
    n = len(arr)
    swaps = 0
    for i in range(n-1):
        swapped = False
        for j in range(n-1-i):
            if _should_swap(arr[j], arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swaps += 1
                swapped = True
        if not swapped: break
    return arr, swaps

Need _should_swap(a,b): True if a should come after b (i.e. b before a). Sorting order: None last. For non-None: higher priority first; if equal priority, earlier created_at first. So a before b if:
- a.priority is not None and b.priority is None => a before b, so should_swap false.
- a.priority is None and b.priority is not None => a after b, should_swap true.
- both None: earlier created_at before later; if a.created_at > b.created_at then swap. If equal? stable no swap.
- both non-None: if a.priority < b.priority => swap; if equal and a.created_at > b.created_at => swap; else false.
Could implement key tuple? But cannot use sorted, but can use tuple comparison? It's not sorting function. Could define _sort_key(task): (0 if priority is not None else 1, -priority if not None else 0, created_at). Then compare keys: if key(a) > key(b): swap. But priority None: -None invalid. Use 0. This is clean. But is using tuple comparison okay? Yes not sorting. But maybe to be explicit. Need ensure priority descending: key second = -priority. For None, group 1, second 0, third created_at. For non-None group 0, second -priority, third created_at. Then order ascending by key. If key(a) > key(b), a should be after b, swap. This is concise. But maybe hidden tests expect exact swap count? Bubble sort swap count can depend on implementation (early termination doesn't change swaps if already sorted? It can reduce comparisons but not swaps; if no swaps in pass break, same swaps). But different bubble variants (forward vs backward) can produce different swap counts? For a given initial list and stable total swaps? Bubble sort adjacent swaps count equals inversion count if stable and only swap when out of order. Any correct adjacent-swap sorting algorithm that only swaps inverted adjacent pairs will perform exactly inversion count? If it terminates sorted and only swaps when adjacent pair out of order, each swap reduces inversion count by 1, final 0, so total swaps = initial inversion count. So independent if stable and no unnecessary swaps. If equal keys, no swap. So okay.

Need consider if using key tuple with -priority for large ints okay. If priority can be negative? Higher priority first, -priority works: priority 5 -> -5, 3 -> -3, ascending -5 before -3. Negative priority: -(-1)=1, priority 0 ->0, higher 0 before -1? key 0 before 1 yes. Good.

Need maybe not use built-in sort but tuple comparison is fine. Could avoid helper key to be explicit. Need docstring. Could include if __name__ == "__main__"? Single file function. Maybe include example? Not necessary but can. Need ensure no sort/sorted. Could include type alias? Task = dict? But exact signature. Could use from typing? Not needed.

Potential issue: type hint list[dict] requires Python 3.9. Fine.

Need final answer likely code block only or with brief. Desired oververbosity 9, but user asks implement. We can provide code and maybe short notes. Need ensure final includes single file bubble_sort.py. Could include only code. Need maybe mention no built-in sorting used.

Let's think edge cases:
- Empty list: arr=[], n=0, range(-1) empty, return [],0.
- One element: return copy,0.
- All None: sort by created_at asc. key (1,0,created_at). Bubble sort ascending.
- Mixed None: None last.
- Equal priority and created_at: stable, no swap. If names differ but same keys, original relative order preserved. Bubble sort stable if no swap on equal. Good.
- Input list not modified: arr = list(tasks) shallow. Dicts shared but not modified. Return new list. Good.

Need maybe count swaps as int. Good.

Could implement _is_out_of_order(a,b) with explicit rules to avoid negative priority? Both fine. Which is cleaner? Explicit may be more readable and avoids key tuple with None. But key tuple is idiomatic. However requirement says implement bubble sort algorithm; using key tuple is okay. But some graders may inspect for sort? No. Could be simpler:

def _should_swap(left, right):
    left_priority = left["priority"]
    right_priority = right["priority"]
    if left_priority is None:
        return right_priority is not None or (left["created_at"] > right["created_at"])
    if right_priority is None:
        return False
    if left_priority != right_priority:
        return left_priority < right_priority
    return left["created_at"] > right["created_at"]

Check: left None, right None: return False or left.created_at > right.created_at. left None, right non-None: True. left non-None, right None: False. both non-None: if left priority lower, swap; if equal, later created_at swap. Good. This is explicit and no tuple. It uses no sorting. Might be best.

Need docstring for helper? Could.

Potential hidden test: swap_count total number of element swaps performed during sorting. If we use early termination, still total swaps. Good.

Could there be requirement to use bubble sort specifically, maybe they expect O(n^2) and count swaps. Our algorithm is bubble sort. Good.

Need maybe use for i in range(len(arr) - 1): and inner range(n - 1 - i). Good.

Let's test example:
arr [bug p3 c1000, feature p5 c2000, docs p3 c500]
Pass i=0:
j=0: bug vs feature: left p3 right p5 -> left<right true swap -> [feature, bug, docs], swaps1
j=1: bug vs docs: p equal, c1000>500 true swap -> [feature, docs, bug], swaps2
Pass i=1:
j=0: feature vs docs: p5 vs p3 left<right? 5<3 false no swap. swapped false break. return swaps2. Good.

Need maybe if list already sorted, swaps 0. Good.

Could there be issue with type hints: tuple[list[dict], int] requires from __future__? In Python 3.9, built-in tuple generic okay? PEP 585 in 3.9. Yes.

Need final: maybe:
```python
"""Bubble sort implementation for task records."""

def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """..."""
    sorted_tasks = list(tasks)
    n = len(sorted_tasks)
    swap_count = 0

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if _should_swap(sorted_tasks[j], sorted_tasks[j + 1]):
                sorted_tasks[j], sorted_tasks[j + 1] = sorted_tasks[j + 1], sorted_tasks[j]
                swap_count += 1
                swapped = True
        if not swapped:
            break

    return sorted_tasks, swap_count

def _should_swap(left: dict, right: dict) -> bool:
    ...
```

Need maybe type dict[str, object]? But signature uses dict. Helper can be dict. Could use Task = dict? Not necessary.

Need ensure no use of sorted/sort. We don't.

Could include main demo? If single file, maybe not. If include if __name__ == "__main__": with example, it's okay but not required. Might be considered extra but fine. User asks containing a function. Could keep only function and helper. Clean.

Need think about "Do not use Python's built-in sort(), sorted(), or any other sorting function". We don't. Tuple comparison not sorting. Good.

Potential nuance: "swap_count is the total number of element swaps performed during sorting". If we use early exit, no extra swaps. Good.

Potential nuance: "Do not modify original input list — return a new list". We copy list. But if tasks is tuple? Signature list, but list(tasks) works. Good.

Potential nuance: priority int or None. created_at int. Good.

Could there be hidden tests checking that original list object not same? We return new list. Good.

Could there be hidden tests checking dictionaries not mutated? We don't mutate.

Could there be hidden tests checking stable order for equal priority and created_at? Our no swap on equal preserves. Good.

Could there be hidden tests checking swap count for specific sequence? Inversion count. Let's verify with None handling. Inversion defined by comparator. Our swaps count equals inversions if comparator transitive. Is comparator transitive? Yes total preorder. Let's test: A p None c100, B p1 c200, C p2 c300. Order C,B,A. Inversions? A before B? A should after B => inversion. A before C inversion. B before C? B p1 after C p2 => inversion. total 3. Bubble: [A,B,C]
j0 A vs B: A None, B non => swap [B,A,C] 1
j1 A vs C: swap [B,C,A] 2
next B vs C: B p1 < C p2 swap [C,B,A] 3. Good.

Could there be issue with negative priorities and explicit comparator: left_priority < right_priority means lower priority should be after higher. If left -1, right 0: -1<0 true swap, so 0 before -1. Good.

Need maybe include comments. Good.

Now final answer. Need maybe not too verbose. Provide code block. Ensure exact file name? Could say Save as bubble_sort.py. Final with code.

Double-check no built-in sorting: We use list(), range, len. Fine.

Could use `swapped` variable. Good.

Let's consider if `tasks` contains dicts missing keys? Not required.

Potential issue: type hint `list[dict]` in function signature exact. We must use exact. We can add helper with type hints. Good.

Need maybe docstring includes Args, Returns, Example. Good.

Let's craft final:

```python
"""Bubble sort for task records.

This module implements a stable bubble sort that orders tasks by priority
descending, then creation time ascending, with null priorities last.
"""

def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """Sort task records using bubble sort.

    Args:
        tasks: List of task dictionaries with keys "name", "priority",
            and "created_at".

    Returns:
        A tuple containing:
        - A new list of task dictionaries sorted by priority descending,
          then created_at ascending. Tasks with priority None are placed
          after all non-null priorities and sorted by created_at ascending.
        - The total number of adjacent swaps performed.

    The input list is not modified.
    """
    sorted_tasks = list(tasks)
    n = len(sorted_tasks)
    swap_count = 0

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
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


def _should_swap(left: dict, right: dict) -> bool:
    """Return True if `left` should be placed after `right`."""
    left_priority = left["priority"]
    right_priority = right["priority"]

    if left_priority is None:
        if right_priority is not None:
            return True
        return left["created_at"] > right["created_at"]

    if right_priority is None:
        return False

    if left_priority != right_priority:
        return left_priority < right_priority

    return left["created_at"] > right["created_at"]
```

This is good. Need maybe no module docstring? Fine.

Could there be a linter issue with line break assignment? Fine.

Need final only. Ensure no analysis. Done.


## Response

```python
"""Bubble sort implementation for task records."""


def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sort task records using bubble sort.

    Tasks are sorted by:
      1. priority descending
      2. created_at ascending
      3. tasks with priority None always come last, ordered by created_at ascending

    Args:
        tasks: A list of task dictionaries. Each task must contain:
            - "name": str
            - "priority": int or None
            - "created_at": int

    Returns:
        A tuple containing:
            - A new list of sorted task dictionaries
            - The total number of swaps performed during sorting

    The original input list is not modified.
    """
    sorted_tasks = list(tasks)
    n = len(sorted_tasks)
    swap_count = 0

    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
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


def _should_swap(left: dict, right: dict) -> bool:
    """
    Return True if the left task should be placed after the right task.

    This helper defines the bubble sort comparison rule:
      - Higher priority comes first.
      - If priorities are equal, earlier created_at comes first.
      - None priority always comes after non-None priority.
    """
    left_priority = left["priority"]
    right_priority = right["priority"]

    if left_priority is None:
        if right_priority is not None:
            return True
        return left["created_at"] > right["created_at"]

    if right_priority is None:
        return False

    if left_priority != right_priority:
        return left_priority < right_priority

    return left["created_at"] > right["created_at"]
```

## Timings

- Time to first token: 4.17s
- Total generation: 425.27s
- Reasoning tokens: 3048
- Answer tokens: 507
- Total tokens: 3555

## Server Timings (llama.cpp)

- Prompt tokens: 530
- Prompt eval speed: 127.11 t/s
- Prompt eval time: 4169.57 ms
- Generation tokens: 3555
- Generation speed: 8.44 t/s
- Generation time: 421083.64 ms
