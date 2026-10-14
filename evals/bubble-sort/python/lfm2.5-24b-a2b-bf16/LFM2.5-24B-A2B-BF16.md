# Code Eval: LFM2.5-24B-A2B-BF16

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

We need to implement bubble sort function `bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]`. The function must not modify the original input list; we need to return a new list (deep copy? At least shallow copy of each dict is fine). Since tasks are dicts, we can copy them via list comprehension copying each dict. Or use `copy.deepcopy` for safety.

We need to implement bubble sort algorithm manually: repeatedly stepping through the list, swapping adjacent elements if they are in wrong order according to sorting rules. Count swaps.

Sorting rules:

- Primary: sort by priority descending (higher priority first). If priority is None, treat as lowest? Actually rule says tasks where priority is None always sort to the end of the list, ordered by created_at ascending among themselves. So effectively, tasks with None priority are considered lower than any non-None priority. Among them, they are sorted by created_at ascending.

Thus sorting order: tasks with priority not None sorted descending by priority; then tasks with priority None sorted ascending by created_at.

But also tiebreaker: when priorities equal (including both None? Actually if both have None, they are considered equal in priority but rule says they sort among themselves by created_at ascending). So we need to treat None as lowest priority. In bubble sort comparisons, we need to decide if element A should be before B.

Define a comparator function that returns True if A should come before B (i.e., A is "less than" B in the desired order). Since bubble sort swaps when elements are out of order: typical bubble sort algorithm: for i from 0 to n-1, for j from 0 to n-i-2: if list[j] > list[j+1] then swap. So we need to define a ">" relation that indicates that the current element should be after the next element (i.e., they are out of order). We'll implement custom compare.

Define function `is_out_of_order(a, b)` returns True if a should come after b (i.e., a > b) according to sorting rules. Then bubble sort will swap when is_out_of_order(list[j], list[j+1]).

Alternatively, we can implement bubble sort with explicit condition: if priority of a < priority of b? Actually descending priority means larger priority first. So for non-None priorities: higher priority should be earlier. So if a.priority is not None and b.priority is not None:

- If a.priority < b.priority => a should come after b (swap needed).
- If a.priority > b.priority => correct order (no swap).
- If either has None: treat None as lowest priority. So if a.priority is None and b.priority is not None: then a should be after b (swap needed). If both are None: then tiebreaker: earlier created_at first. So if a.created_at > b.created_at => swap needed (since later timestamp should come later? Actually ascending order: earlier timestamp first, so smaller created_at should be before larger. So if a.created_at > b.created_at => a is later, should be after b -> swap needed). If a.created_at < b.created_at => correct order.

Thus overall comparator:

Given tasks A and B (dicts), we need to decide if A should be placed before B (i.e., A <= B in sorted order). In bubble sort, we compare adjacent elements: if A > B (i.e., A should come after B) then swap.

Define a function `should_swap(a, b)` that returns True if a is currently before b but should be after b according to sorting rules. That is, if a > b in desired order.

Implementation:

```
def should_swap(a, b):
    # Return True if a should be moved after b (i.e., a > b)
    # Cases:
    # 1. Both have priority not None:
    #   - If a.priority is None: treat as lowest => a should be after b => swap.
    #   - If b.priority is None: then b is lower, so a before b is correct (no swap).
    #   - Else compare priorities descending: if a.priority < b.priority => swap.
    # 2. a.priority is None and b.priority is not None: swap (None lower)
    # 3. Both are None: tiebreaker by created_at ascending: if a.created_at > b.created_at => swap.
```

But careful: If both have priority None, we need to sort by created_at ascending. So earlier timestamp first. In bubble sort, if a.created_at > b.created_at (i.e., later), then a should be after b -> swap.

Edge Cases: tasks may have same priority and same created_at? Then stable order? Not required but can keep as is.

Now bubble sort algorithm:

- Create a copy of the input list: `sorted_tasks = [task.copy() for task in tasks]` (shallow copy of each dict). Or use `list(tasks)` then copy dicts. Since we need not modify original, copying dicts ensures modifications to inner dicts won't affect original? Actually if we only read and swap references, we don't modify the dicts themselves. But to be safe, we can shallow copy each dict.

- Initialize swap_count = 0.

- n = len(sorted_tasks)

- For i in range(n):
    - swapped = False
    - For j in range(0, n - i - 1):
        - if should_swap(sorted_tasks[j], sorted_tasks[j+1]): # a before b but out of order => swap
            - swap the elements: sorted_tasks[j], sorted_tasks[j+1] = sorted_tasks[j+1], sorted_tasks[j]
            - swap_count += 1
            - swapped = True
    - If not swapped: break (optional optimization)

- Return (sorted_tasks, swap_count)

Complexities: O(n^2) worst-case.

Now we need to ensure that tasks with None priority are placed at the end. Our comparator ensures that any element with non-None priority will be before any with None priority because if a.priority is not None and b.priority is None => should_swap(a,b) returns True (a should be after b? Wait: In bubble sort we compare a (at index j) and b (j+1). If a has non-None priority, b has None, then according to sorting rules, a should come before b (since None tasks go to the end). So if a is before b but a should be before b, no swap needed. But our comparator for should_swap returns True when a should be after b. Let's test: a.priority=3, b.priority=None => According to rules, a should be before b (since None tasks go to end). So they are in correct order; we should not swap. In bubble sort, if a is before b and they are in correct order, no swap. But our comparator must return False for that case.

Thus need to define should_swap such that it returns True only when a > b (i.e., a should be after b). So for a.priority not None, b.priority None: a should be before b => not swapped => should_swap(a,b) = False. However if a.priority is None and b.priority not None: then a should be after b => swap needed => should_swap(a,b) = True.

Thus implement accordingly.

Now tiebreaker for equal priorities (including both None). For non-None equal priority: order by created_at ascending. So if a.created_at > b.created_at => a should be after b => swap needed => should_swap(a,b)=True. If a.created_at < b.created_at => correct order.

For both None: same tiebreaker: earlier timestamp first. So if a.created_at > b.created_at => swap needed.

Now also need to handle case where priorities are equal but one is None? Actually rule says tasks with priority None always sort to the end, ordered by created_at ascending among themselves. So they are not mixed with non-None tasks. So we treat None as lower than any number.

Implementation details:

Define helper functions inside bubble_sort_tasks or outside. Since only need comparator, can embed logic.

Pseudo-code:

```
def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    # Copy tasks
    sorted_tasks = [task.copy() for task in tasks]
    n = len(sorted_tasks)
    swap_count = 0

    def should_swap(a: dict, b: dict) -> bool:
        # Determine if a is before b but should be after b (i.e., out of order)
        # Get priority values
        a_pri = a.get("priority")
        b_pri = b.get("priority")
        a_ts = a.get("created_at")
        b_ts = b.get("created_at")

        # Case: both have non-None priorities
        if a_pri is not None and b_pri is not None:
            if a_pri < b_pri:
                return True  # a should be after b
            elif a_pri > b_pri:
                return False
            else:  # equal priority
                # tiebreaker by created_at ascending
                if a_ts > b_ts:
                    return True
                else:
                    return False
        # Case: a has None, b has non-None -> a should be after b => swap needed
        elif a_pri is None and b_pri is not None:
            return True
        # Case: a has non-None, b has None -> correct order (a before b)
        elif a_pri is not None and b_pri is None:
            return False
        # Both are None
        else:  # both priorities are None
            if a_ts > b_ts:
                return True
            else:
                return False

    # Bubble sort
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if should_swap(sorted_tasks[j], sorted_tasks[j+1]):
                sorted_tasks[j], sorted_tasks[j+1] = sorted_tasks[j+1], sorted_tasks[j]
                swap_count += 1
                swapped = True
        if not swapped:
            break

    return (sorted_tasks, swap_count)
```

Check with example:

tasks = [
 {"name": "bug", "priority": 3, "created_at": 1000},
 {"name": "feature", "priority": 5, "created_at": 2000},
 {"name": "docs", "priority": 3, "created_at": 500},
]

Let's simulate:

sorted_tasks initially: same order.

First pass i=0:
j=0: compare bug (prio 3) vs feature (prio5). a_pri=3,b_pri=5 => a_pri < b_pri => should_swap returns True (since a should be after b). Indeed bubble sort will swap them. After swap: list becomes [feature, bug, docs]. swap_count=1.

j=1: compare bug (prio3) vs docs (prio3). Both non-None equal priority. Tiebreaker: created_at: bug 1000, docs 500. a_ts=1000 > b_ts=500 => should_swap returns True (a should be after b). So swap: list becomes [feature, docs, bug]. swap_count=2.

End of pass i=0: swapped=True.

Second pass i=1:
n=3, range(0,n-i-1)=range(0,1) => j=0 only.
Now list: [feature (prio5), docs (prio3, ts500), bug (prio3,ts1000)]

Compare feature vs docs: a_pri5 > b_pri3 => no swap.

j loop ends. swapped=False? Actually after j=0 no swap, so swapped remains False. Then break out of outer loop (since no swaps). So final sorted list: [feature, docs, bug] matches expected.

swap_count=2. Good.

Now test scenario with None priorities:

Suppose tasks = [
 {"name":"A","priority":None,"created_at":100},
 {"name":"B","priority":3,"created_at":200},
 {"name":"C","priority":None,"created_at":50},
 {"name":"D","priority":1,"created_at":300},
]

We expect sorted order: tasks with priority 3 first (descending), then priority 1, then None tasks sorted by created_at ascending.

So expected order: B (prio3), D (prio1), C (None, ts50), A (None, ts100). Wait tiebreaker: among None tasks, earlier timestamp first: C (50) then A (100). So final: [B, D, C, A].

Let's test bubble sort manually:

Initial list: [A(None,100), B(3,200), C(None,50), D(1,300)]

We'll simulate algorithm.

First pass i=0:
j=0: compare A vs B: a_pri None, b_pri 3 => should_swap returns True (a should be after b). Swap => [B, A, C, D]; swap_count=1.
j=1: compare A (None) vs C (None): both None. Tiebreaker: a_ts=100 > b_ts=50 => should_swap returns True (a after b). Swap => [B, C, A, D]; swap_count=2.
j=2: compare A (None) vs D (1): a_pri None, b_pri 1 => should_swap returns True? Actually a is None, b has priority 1. According to rule, None tasks go to end, so a should be after b => swap needed. So swap => [B, C, D, A]; swap_count=3.

End of pass: swapped=True.

Second pass i=1:
Now list: [B(3,200), C(None,50), D(1,300), A(None,100)]

j=0: compare B vs C: a_pri 3 > b_pri None => should_swap returns False (a before b correct). No swap.
j=1: compare C vs D: a_pri None, b_pri 1 => should_swap True (a after b). Swap => [B, D, C, A]; swap_count=4.
j=2: compare C vs A: both None: a_ts=50 < b_ts=100 => no swap (since earlier first). Actually tiebreaker: if a_ts > b_ts => swap. Here a_ts=50 < 100 => correct order, no swap.

After pass: swapped=True.

Third pass i=2:
List: [B(3,200), D(1,300), C(None,50), A(None,100)]

j=0: compare B vs D: a_pri3 > b_pri1 => no swap.
j=1: compare D vs C: a_pri1 > b_priNone? Actually b_pri None => should_swap returns True (a before b but should be after). So swap => [B, C, D, A]; swap_count=5.

Now list: [B, C, D, A] (but note C is None now at index1). Continue j=2? Actually range(0,n-i-1) = range(0, 4-2-1=1?) Wait n=4, i=2 => n-i-1 = 4-2-1 =1 => j runs 0..0 only. So after swap at j=0? Let's recalc: For i=2 (third pass), j goes from 0 to n - i - 2? Actually typical bubble sort inner loop: for j in range(0, n - i - 1): That means last index is n-i-2. So for n=4:
- i=0: j=0..1 (two comparisons)
- i=1: j=0..1? Wait n-i-1 = 4-1-1=2 => j=0,1 (two comparisons)
- i=2: n-i-1 = 4-2-1=1 => j=0 only.
Thus after swap at j=0 in i=2 pass, we break out? Actually swapped=True.

Now i=3: loop ends because range(0,n) will be done. But we can break early if no swaps.

But final list after third pass: [B, C, D, A]? Let's see: After swap at j=0 in i=2 pass: we swapped D and C? Actually at i=2, j=0: compare B (index0) vs C (index1)? Wait after previous passes, the list is [B, C, D, A] before i=2? Let's track more carefully.

We need to simulate fully. But anyway final sorted order should be [B, D, C, A] according to expected. Our algorithm may produce that after further passes.

Let's continue simulation:

After pass i=1 (second pass) we had list: [B, D, C, A] (swap at j=1). Actually earlier we swapped C and D at j=1 in second pass? Let's re-evaluate.

We started with initial list: [A(None), B(3), C(None), D(1)]

After first pass (i=0):
- After swaps: [B, C, D, A] (I think). Let's recompute step by step:

Initial: idx0=A(None,100), idx1=B(3,200), idx2=C(None,50), idx3=D(1,300)

Pass i=0:
j=0: compare A vs B => swap => [B, A, C, D]
j=1: compare A (now at idx1) vs C => both None? Actually after swap, A is at index1, C at index2. Compare A(None) vs C(None): tiebreaker: a_ts=100 > b_ts=50 => swap => [B, C, A, D]
j=2: compare A (idx2) vs D (idx3): a_pri None vs b_pri 1 => swap => [B, C, D, A]

So after first pass: list = [B(3), C(None,50), D(1), A(None,100)]

swap_count=3.

Second pass i=1:
Now n=4, inner loop j from 0 to n-i-2? Actually range(0, n - i - 1) = range(0, 4-1-1=2) => j=0,1.

List: [B, C, D, A]

j=0: compare B vs C: a_pri3 > b_pri None => should_swap returns False (correct order). No swap.
j=1: compare C vs D: a_pri None, b_pri 1 => should_swap True (swap needed). So swap => [B, D, C, A]; swap_count=4.

After pass i=1: list = [B, D, C, A].

Third pass i=2:
Inner loop j from 0 to n - i - 1 = 4-2-1=1 => j=0 only.

List: [B, D, C, A]
j=0: compare B vs D: a_pri3 > b_pri1 => no swap.
No more swaps. swapped=False? Actually we didn't swap, so swapped remains False. Since swapped=False, break out of outer loop.

Thus final list = [B, D, C, A] which matches expected order: priority descending: B (3), D (1), then None tasks sorted by created_at ascending: C (50) then A (100). Good.

swap_count=4? Actually we counted swaps: first pass 3, second pass 1 => total 4. That's correct.

Thus algorithm works.

Now need to ensure that bubble sort does not modify original list. We used copy of each dict. However, swapping references only changes order in new list; original list remains unchanged. Good.

Potential issues: The comparator uses .get("priority") and .get("created_at"). Since tasks are guaranteed to have these keys, but we can still use direct access. But using .get is safe.

Now about type hints: function signature includes list[dict] and returns tuple[list[dict], int]. We'll import from typing? In Python 3.9+ you can use built-in generics for list and dict. The problem states "list[dict]" etc. We'll just annotate accordingly.

Docstring: Should describe function, parameters, return, sorting rules.

Implementation details:

- Use `from typing import List, Dict, Tuple`? Not needed if using built-in generics. But to be safe, we can import from typing for older versions. However the problem says "Write a single file bubble_sort.py containing a function with this exact signature". So we must match signature exactly: def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:. That's fine.

We'll include type hints inside.

Now test with given example:

tasks = [
    {"name": "bug", "priority": 3, "created_at": 1000},
    {"name": "feature", "priority": 5, "created_at": 2000},
    {"name": "docs", "priority": 3, "created_at": 500},
]

sorted_tasks, swaps = bubble_sort_tasks(tasks)
Expected sorted_tasks: feature (prio5), docs (prio3, ts500), bug (prio3, ts1000). swaps=2.

Our algorithm yields that. Let's test mentally:

Initial copy: same order.

First pass:
j=0: compare bug vs feature: a_pri3 < b_pri5 => swap => [feature, bug, docs]; swaps=1.
j=1: compare bug (prio3) vs docs (prio3): tiebreaker: bug ts1000 > docs ts500 => swap => [feature, docs, bug]; swaps=2.

Second pass:
j=0: compare feature vs docs: a_pri5 > b_pri3 => no swap.
No swaps => break. Return sorted list and swaps=2. Good.

Now test with tasks containing None priorities:

tasks = [
    {"name": "A", "priority": None, "created_at": 100},
    {"name": "B", "priority": 3, "created_at": 200},
    {"name": "C", "priority": None, "created_at": 50},
    {"name": "D", "priority": 1, "created_at": 300},
]

We expect sorted_tasks = [B, D, C, A], swaps=4 as earlier.

Let's simulate quickly: Already did above. Should work.

Edge Cases:

- Empty list: tasks = [] => n=0. Outer loop range(0) does nothing. swap_count=0. Return ([], 0). Works.

- Single element: returns same list, swaps=0.

- All tasks have same priority and created_at? Then tiebreaker doesn't change order; bubble sort may still swap if comparator says out-of-order? If priorities equal and created_at equal, then should_swap returns False (since a_ts > b_ts is false). So no swaps. Good.

- Mixed None and non-None with same priority? Not possible because None is not comparable to int. But rule: None tasks always go to end. So if there are tasks with priority 0? That's allowed (int). Then they will be sorted among themselves by descending priority (0). None tasks go after all.

Potential bug: In comparator, when both priorities are None, we compare created_at ascending. However, what about tasks where priority is None but created_at missing? Not needed.

Now ensure that bubble sort algorithm stops early if no swaps. That's optional but good.

Complexities: O(n^2) time, O(n) space for copy.

Now code style: Provide docstring with description of sorting rules and swap counting.

Potential improvements: Use local function for swapping to avoid repeated attribute access? Not needed.

Now let's write final code.

We'll create file bubble_sort.py:

```
"""bubble_sort.py - Implement bubble sort for task records."""

from typing import List, Dict, Tuple

def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sort a list of task dictionaries using the bubble sort algorithm.

    The sorting order is defined as:
    1. Primary key: ``priority`` in descending order (higher priority first).
       Tasks with ``priority`` equal to ``None`` are treated as lowest priority
       and are placed after all tasks with a concrete priority.
    2. Tiebreaker: when priorities are equal, sort by ``created_at`` in ascending
       order (earlier timestamps first).
    3. For tasks whose ``priority`` is ``None``, the secondary ordering is also
       ``created_at`` ascending.

    Parameters
    ----------
    tasks : list[dict]
        List of task dictionaries. Each dictionary must contain the keys
        ``"name"`` (str), ``"priority"`` (int or None) and ``"created_at"``
        (int).

    Returns
    -------
    tuple[list[dict], int]
        A tuple containing:
        - The sorted list of tasks (a new list; the original ``tasks`` is not
          modified).
        - The total number of swaps performed during the sorting process.
    """
    # Create a shallow copy of each task to avoid mutating the input.
    sorted_tasks: List[dict] = [task.copy() for task in tasks]
    n = len(sorted_tasks)
    swap_count = 0

    def should_swap(a: dict, b: dict) -> bool:
        """
        Return True if element ``a`` (currently before ``b``) is out of order
        and must be moved after ``b`` according to the sorting rules.
        """
        a_pri = a.get("priority")
        b_pri = b.get("priority")
        a_ts = a.get("created_at")
        b_ts = b.get("created_at")

        # Both have concrete priorities
        if a_pri is not None and b_pri is not None:
            if a_pri < b_pri:
                return True          # lower priority should come later
            if a_pri > b_pri:
                return False         # higher priority is already before
            # Equal priorities: tie‑breaker by created_at ascending
            return a_ts > b_ts

        # a has None priority, b has a concrete priority -> a must go after b
        if a_pri is None and b_pri is not None:
            return True

        # a has concrete priority, b is None -> correct order (a before b)
        if a_pri is not None and b_pri is None:
            return False

        # Both priorities are None: order by created_at ascending
        return a_ts > b_ts

    # Bubble sort
    for i in range(n):
        swapped = False
        # After each pass, the last i elements are already in place
        for j in range(0, n - i - 1):
            if should_swap(sorted_tasks[j], sorted_tasks[j + 1]):
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
```

Check that we imported List and Tuple from typing. The signature uses list[dict] etc. In Python 3.9+ you can use built-in generics without importing. But to be safe for older versions, we can import. However the problem didn't specify imports; but it's okay.

Now test with example:

We'll run mental test: Already did.

Potential issues: The comparator returns True when a_ts > b_ts for equal priorities or both None. That ensures ascending order (earlier first). Good.

Now check scenario where priority is same and created_at same: Should not swap. Example: tasks = [{"name":"a","priority":3,"created_at":100}, {"name":"b","priority":3,"created_at":100}]. In should_swap: a_pri == b_pri, a_ts > b_ts? false (equal). So returns False => no swap. Good.

Now test scenario where priority is None and created_at equal: Should not swap. Works.

Now ensure that we treat tasks with priority None as lower than any int. In comparator, if a_pri is None and b_pri is not None => return True (swap). That ensures None goes after. If both None => tiebreaker.

Edge Cases: What about tasks where priority is negative? Works fine.

Now confirm that we didn't use built-in sort. We used bubble sort manually.

Now final code includes docstring, type hints, comments.

Potential improvements: Use `from __future__ import annotations` for forward references? Not needed.

Now produce final answer: Provide the code block with file name bubble_sort.py.

We'll include explanation in answer? The user asked "Write clean, well-documented, idiomatic Python code." So we just output the code. Possibly also brief description. But likely they want just the code. We'll provide code with comments.

Thus final.


## Response



**File:** `bubble_sort.py`

```python
"""bubble_sort.py – Bubble‑sort implementation for task records.

The function sorts a list of task dictionaries according to the following rules:
1. Primary key: ``priority`` in descending order (higher priority first).
2. Tiebreaker: when priorities are equal, sort by ``created_at`` ascending
   (earlier timestamps first).
3. Tasks whose ``priority`` is ``None`` are placed after all tasks with a concrete
   priority and are ordered among themselves by ``created_at`` ascending.

The implementation follows the classic bubble‑sort algorithm, counts every swap,
and returns a new list without modifying the original input.
"""

from typing import List, Dict, Tuple

def bubble_sort_tasks(tasks: list[dict]) -> tuple[list[dict], int]:
    """
    Sort tasks using bubble sort.

    Parameters
    ----------
    tasks : list[dict]
        List of task dictionaries. Each dictionary must contain the keys
        ``"name"`` (str), ``"priority"`` (int or None) and ``"created_at"`` (int).

    Returns
    -------
    tuple[list[dict], int]
        A tuple ``(sorted_list, swap_count)`` where ``sorted_list`` is a new list
        containing the tasks in the required order and ``swap_count`` is the total
        number of element swaps performed during sorting.
    """
    # Create a shallow copy of each task to avoid mutating the original list.
    sorted_tasks: List[dict] = [task.copy() for task in tasks]
    n = len(sorted_tasks)
    swap_count = 0

    def should_swap(a: dict, b: dict) -> bool:
        """
        Determine whether element ``a`` (currently before ``b``) is out of order
        and must be moved after ``b`` according to the sorting rules.
        """
        a_pri = a.get("priority")
        b_pri = b.get("priority")
        a_ts = a.get("created_at")
        b_ts = b.get("created_at")

        # Both tasks have concrete priorities
        if a_pri is not None and b_pri is not None:
            if a_pri < b_pri:
                return True          # lower priority should come later
            if a_pri > b_pri:
                return False         # higher priority already before
            # Equal priorities → tie‑breaker by created_at ascending
            return a_ts > b_ts

        # a has None priority, b has a concrete priority → a must go after b
        if a_pri is None and b_pri is not None:
            return True

        # a has concrete priority, b is None → correct order (a before b)
        if a_pri is not None and b_pri is None:
            return False

        # Both priorities are None → order by created_at ascending
        return a_ts > b_ts

    # Classic bubble sort with early exit when no swaps occur
    for i in range(n):
        swapped = False
        # After each outer pass, the last i elements are already sorted
        for j in range(0, n - i - 1):
            if should_swap(sorted_tasks[j], sorted_tasks[j + 1]):
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
```

## Timings

- Time to first token: 1.94s
- Temperature: 0.0
- Total generation: 617.71s
- Reasoning tokens: 6357
- Answer tokens: 883
- Total tokens: 7240

## Server Timings (llama.cpp)

- Prompt tokens: 470
- Prompt eval speed: 242.36 t/s
- Prompt eval time: 1939.26 ms
- Generation tokens: 7240
- Generation speed: 11.76 t/s
- Generation time: 615762.29 ms
