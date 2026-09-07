# Code Eval: Muse-Glimmer-30B-UD-Q6_K_XL

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

# Bubble Sort Tasks — Python

Implement a bubble sort function for task records.

Requirements...

We need to write single file bubble_sort.py containing function with exact signature.

We must implement bubble sort algorithm — do not use built-in sort.

Return tuple (sorted_list, swap_count). Do not modify original input list — return new list.

Sorting rules:
Primary: priority descending (higher first)
Tiebreaker: when priorities equal, sort by created_at ascending
Null handling: tasks where priority is None always sort to end, ordered by created_at ascending among themselves

Need to define comparison.

We need to be careful about comparison logic for None.

We can define a key for comparison: For each task, we need to compare.

We can define a comparator function less_than? Bubble sort typically swaps if a > b according to order.

We want final order ascending? Let's define order: we want first element to be "best". So we want to bubble larger elements forward? Standard bubble sort swaps adjacent if left > right (according to desired order). Let's define comparison: a should come before b if a is "better". So if a is better than b, keep order. If a is worse than b, swap.

We need to define better.

Rules:
priority descending: higher priority better.
If priority is None, it's worst.

If both have priority not None:
compare priority descending.
If equal, compare created_at ascending: smaller created_at better.

If one has priority None and other not None: non-None better.

If both None: compare created_at ascending.

So we can define a tuple key for sorting: For Python sort, we would use key = (-priority if priority is not None else inf?, created_at). But we need custom comparator.

Simpler: define function is_better(a,b) returns True if a should come before b.

Implementation:

def is_better(a,b):
    pa = a['priority']
    pb = b['priority']
    if pa is None and pb is None:
        return a['created_at'] < b['created_at']
    if pa is None:
        return False # a is worse
    if pb is None:
        return True # a is better
    if pa != pb:
        return pa > pb
    # equal priority
    return a['created_at'] < b['created_at']

Then bubble sort: for i in range(n-1): for j in range(n-1-i): if not is_better(tasks[j], tasks[j+1]): swap. Because if a is not better than b, then b should come before a, swap.

Alternatively define should_swap(a,b): if a is worse than b.

Let's test with example.

tasks:
bug p3 c1000
feature p5 c2000
docs p3 c500

i=0
j=0: compare bug vs feature. is_better(bug,feature)? pa3 vs5 => 3>5? false => not better => swap. swap count1. list: feature, bug, docs
j=1: compare bug vs docs. is_better(bug,docs)? pa equal 3, created 1000 <500? false => not better => swap. swap count2. list: feature, docs, bug
i=1
j=0: compare feature vs docs. is_better? 5>3 true => no swap
Done. swaps=2 matches example.

Edge cases: None handling.

If pa is None, is_better returns False if pb is not None. So a worse. Good.

If both None, compare created_at.

Now need to not modify original list. So copy list: tasks_copy = [dict(t) for t in tasks]? Or shallow copy list then elements are dicts. If we just copy list via list(tasks), the dicts are same objects but we don't modify dicts, only reorder. That's fine. Requirement "Do not modify the original input list — return a new list". So list copy is enough. Could also deep copy but not needed.

Return tuple (sorted_list, swap_count)

Implement bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:

Make copy.

n = len(tasks_copy)

swap_count =0

for i in range(n):
  swapped = False
  for j in range(n-1-i):
    a = tasks_copy[j]
    b = tasks_copy[j+1]
    if not is_better(a,b):
        tasks_copy[j], tasks_copy[j+1] = tasks_copy[j+1], tasks_copy[j]
        swap_count+=1
        swapped=True
  if not swapped:
    break

Return tasks_copy, swap_count

Need type hints and docstring.

Potential nuance: Null handling: tasks where priority is None always sort to end, ordered by created_at ascending among themselves. Our is_better handles that: if pa is None and pb is None -> compare created_at. If pa is None and pb not None -> a worse. If pa not None and pb is None -> a better. So None items will bubble to end.

But what about comparison between two None items with different created_at? Works.

Edge: priority could be 0? int or None. So fine.

Complexities fine.

Potential nuance: bubble sort algorithm typically stops early. That's okay.

Make sure function signature exact.

Write clean code.

Maybe also provide if __name__ == '__main__' test? Not required.

The prompt says write single file bubble_sort.py containing function. Probably just provide code.

We should output code block.

Make sure imports? Not needed.

Type hints: list[dict] works in Python 3.9+. Use from __future__ import annotations? Might be okay.

Use typing: List[Dict] maybe safer. But signature specified list[dict]. Use that.

Docstring: describe.

Potential pitfalls: When priorities equal and both None? Already handled.

Alternative approach: define comparison key for bubble sort using tuple: we can map priority to a sortable value: For None, we want it to be smallest in descending order, i.e., treat as -inf. So we can define effective priority: if priority is None -> -1? But priority could be negative? Possibly int. Safer to use custom comparator.

Implementation details: ensure we don't use sorted.

Return new list.

Potential nuance: swap_count counts total swaps performed. Good.

Edge case empty list: return [],0

Edge case single element: return copy,0

Make sure not to modify original: tasks_copy = tasks[:] . That's shallow copy.

Potential nuance: dicts mutable, but we don't modify them.

Provide final answer.

Maybe also include helper function _should_swap.

Let's produce final code.

Add docstring:

def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    ...
    Returns (sorted_tasks, swap_count)
    """

Implementation.

Potential improvement: Use local variables for speed.

Make sure code is idiomatic.

Let's produce final output.

Possibly they want to ensure bubble sort algorithm implemented correctly: typical bubble sort passes.

We could also implement optimized bubble sort with last swap index.

But fine.

Potential nuance: The sorting rules for None: tasks where priority is None always sort to end, ordered by created_at ascending among themselves. Our comparator ensures that None items are worse than any non-None. Among themselves, created_at ascending. Good.

What about tiebreaker when priorities equal but one is None? Can't happen because equal means both None or both same int.

Edge: priority None vs priority None but created_at equal? Stable? Swap not needed.

All good.

Let's produce final answer with code.

Maybe add __all__.

Provide final code snippet.

Ensure file name bubble_sort.py.

Output code.

Potential test: tasks with None.

tasks = [
 {"name":"a","priority":None,"created_at":100},
 {"name":"b","priority":None,"created_at":50},
 {"name":"c","priority":1,"created_at":200}
]
Expected order: c, b, a? Wait b created 50 < a 100, so b before a. So c first, then b, then a.

Our comparator: compare c vs a: pa=1 not None, pb=None => is_better true => no swap. c vs b? Actually order after sort.

Let's simulate: list [a,b,c]
i0 j0 a vs b: both None, created 100 <50? false => swap => [b,a,c] swap1
j1 a vs c: pa None, pb 1 => is_better false => swap => [b,c,a] swap2
i1 j0 b vs c: pa None vs1 => is_better false => swap => [c,b,a] swap3
i2 j0 c vs b: is_better true => no swap
Result [c,b,a] correct.

Swap count 3.

Seems fine.

Potential nuance: The bubble sort algorithm typically compares adjacent and swaps if left should be after right. We used not is_better.

Alternative definition: swap if a is worse than b.

Works.

Make sure type hints: tuple[list[dict], int]

Python 3.9+ supports list[dict].

If using older, might need from typing import List, Dict, Tuple. But spec says list[dict].

We'll assume Python 3.10+.

Provide final code.

Maybe add small guard.

Let's output final answer.

Potential improvements: Use copy.deepcopy? Not needed.

Return new list.

Ok.

Provide final code block.

Let's produce final response.

## Response

```python
def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Bubble sort tasks by priority descending, then created_at ascending.
    Tasks with priority None are placed at the end ordered by created_at.

    Args:
        tasks: list of dicts with keys "name", "priority", "created_at"

    Returns:
        tuple[list[dict], int]: (sorted list copy, number of swaps performed)
    """
    # work on a shallow copy to keep the original list intact
    arr = tasks[:]  # dict objects are not mutated, only reordered
    n = len(arr)

    def is_better(a: dict, b: dict) -> bool:
        pa = a.get("priority")
        pb = b.get("priority")
        # both None -> tie-break by created_at
        if pa is None and pb is None:
            return a["created_at"] < b["created_at"]
        # None is always worse
        if pa is None:
            return False
        if pb is None:
            return True
        # primary: priority descending
        if pa != pb:
            return pa > pb
        # tie-breaker: created_at ascending
        return a["created_at"] < b["created_at"]

    swaps = 0
    for i in range(n):
        swapped = False
        # last i elements are already in place
        for j in range(n - 1 - i):
            a = arr[j]
            b = arr[j + 1]
            if not is_better(a, b):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return arr, swaps
```

The function implements classic bubble sort without using `sort`/`sorted`, returns a new list and the total swap count, and respects the required priority / `created_at` / `None` ordering.

## Timings

- Time to first token: 2.55s
- Total generation: 341.70s
- Reasoning tokens: 1999
- Answer tokens: 416
- Total tokens: 2415

## Server Timings (llama.cpp)

- Prompt tokens: 502
- Prompt eval speed: 237.14 t/s
- Prompt eval time: 2116.93 ms
- Generation tokens: 2415
- Generation speed: 7.11 t/s
- Generation time: 339567.76 ms
