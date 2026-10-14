# Code Eval: LFM2.5-24B-A2B-BF16

## Prompt

# Bubble Sort Tasks — Java

Implement a bubble sort function for task records.

## Requirements

Write a single file `BubbleSortTasks.java` containing a public class `BubbleSortTasks` with:

1. A **static inner** `Task` record with fields:
   - `String name`
   - `Integer priority` (nullable — use `Integer`, not `int`)
   - `long createdAt`

2. A **static inner** `SortResult` record with fields:
   - `List<Task> tasks` — the sorted list
   - `int swapCount` — total swaps performed

3. A static method:
   ```java
   public static SortResult bubbleSortTasks(List<Task> tasks)
   ```

### Sorting Rules

1. **Primary:** sort by `priority` descending (higher priority comes first)
2. **Tiebreaker:** when priorities are equal, sort by `createdAt` ascending (earlier timestamp comes first)
3. **Null handling:** tasks where `priority` is `null` always sort to the end of the list, ordered by `createdAt` ascending among themselves

### Constraints

- You must implement the bubble sort algorithm — do not use `Collections.sort()`, `Arrays.sort()`, `List.sort()`, or any other sorting utility
- Return a `SortResult` with the sorted list and total swap count
- Do not modify the original input list — return a new list

### Example

```java
List<BubbleSortTasks.Task> tasks = List.of(
    new BubbleSortTasks.Task("bug",     3, 1000),
    new BubbleSortTasks.Task("feature", 5, 2000),
    new BubbleSortTasks.Task("docs",    3, 500)
);

BubbleSortTasks.SortResult result = BubbleSortTasks.bubbleSortTasks(tasks);
// result.tasks() = [Task("feature",5,2000), Task("docs",3,500), Task("bug",3,1000)]
// result.swapCount() = 2
```

Write clean, well-documented, idiomatic Java code. Use Javadoc where appropriate.


## Reasoning

We need to implement a Java file `BubbleSortTasks.java` containing a public class `BubbleSortTasks`. Inside it we need static inner records:

- `Task` record with fields: `String name`, `Integer priority` (nullable), `long createdAt`.
- `SortResult` record with fields: `List<Task> tasks` and `int swapCount`.

We need a static method `public static SortResult bubbleSortTasks(List<Task> tasks)`.

Implementation must use bubble sort algorithm manually, not using built-in sorting utilities.

Constraints:

- Must not modify the original input list; return a new list.
- Sorting rules:
  1. Primary: sort by priority descending (higher priority first).
  2. Tiebreaker: when priorities equal, sort by createdAt ascending (earlier timestamp first).
  3. Null handling: tasks where priority is null always sort to the end of the list, ordered by createdAt ascending among themselves.

Thus we need to implement bubble sort that respects these ordering rules.

We need to count total swaps performed during bubble sort. Swaps happen when two elements are swapped due to being out of order according to the sorting criteria.

Implementation details:

- Since bubble sort works by repeatedly stepping through the list, swapping adjacent elements if they are in wrong order. We'll implement a typical bubble sort: for i from 0 to n-1, for j from 0 to n-i-2 (or n-1 - i - 1?), compare elements at positions j and j+1; if they need to be swapped according to sorting criteria, swap them and increment swapCount.

- Need to define a comparator that defines the order: descending priority, then ascending createdAt for ties. For null priorities: treat as lowest (i.e., after all non-null). Among null priority tasks, sort by createdAt ascending.

Thus we need a method `compare(Task a, Task b)` returning -1 if a should come before b, 1 if after, 0 if equal.

Define:

- If both have non-null priorities: compare a.priority vs b.priority descending: if a.priority > b.priority => a before b (return -1). If less => return 1. If equal => tiebreaker: compare createdAt ascending: if a.createdAt < b.createdAt => a before b (-1), else if > => 1, else 0.

- If a.priority is null and b.priority is non-null: then a (null) should be after b => return 1 (a after b). If both null: compare createdAt ascending: if a.createdAt < b.createdAt => -1; > => 1; else 0.

Thus bubble sort will use this comparator to decide swaps: if compare(a,b) > 0 (i.e., a should be after b), then swap.

Implementation steps:

- Create a copy of the input list: `List<Task> list = new ArrayList<>(tasks);` This ensures we don't modify original.

- Perform bubble sort on `list`.

- Keep `int swapCount = 0;`.

- For each pass, for each j from 0 to list.size() - i - 2 (or typical nested loops: for (int i = 0; i < n; i++) { for (int j = 0; j < n - i - 1; j++) { ... } }).

- In inner loop, get `Task a = list.get(j); Task b = list.get(j+1);` If compare(a,b) > 0 => swap them: `Collections.swap(list, j, j+1);` Or manually swap using temp variable. Then increment swapCount.

- After loops, return new SortResult(list, swapCount).

SortResult is a record with fields tasks and swapCount. Since it's a record, we can define as:

```
public record SortResult(List<Task> tasks, int swapCount) {}
```

But need to ensure that the list is not modified after returning? The requirement: return a SortResult with sorted list and total swap count. It's okay.

Now about bubble sort algorithm: We must implement manually; using Collections.swap is allowed (it's not sorting utility). That's fine.

Edge Cases:

- Input list may be empty or null? Probably not, but we can handle: if tasks == null => return new SortResult(new ArrayList<>(), 0) maybe. But spec says List<Task> tasks; assume non-null.

- Null priorities: treat as described.

Testing with example:

Input tasks:
1. Task("bug", 3, 1000)
2. Task("feature",5,2000)
3. Task("docs",3,500)

Sorted order expected: feature (priority 5), docs (priority 3, createdAt 500), bug (priority 3, createdAt 1000). That's exactly as example.

Let's simulate bubble sort:

Initial list: [bug(3,1000), feature(5,2000), docs(3,500)]

We need to get final sorted order: [feature, docs, bug].

Swap count: Let's compute manually:

- Compare bug vs feature: priority 3 vs 5 => bug should be after feature => swap needed. So swap positions 0 and 1: list becomes [feature, bug, docs]; swapCount=1.

Now compare bug (now at index1) vs docs: bug priority 3, docs priority 3 equal; tiebreaker createdAt: bug 1000 > docs 500 => bug should be after docs => swap needed. So swap indices 1 and 2: list becomes [feature, docs, bug]; swapCount=2.

Now bubble sort passes done? Actually typical bubble sort would continue passes but no more swaps needed. So total swaps = 2. That's matches example.

Thus algorithm works.

Implementation details:

- Need to import java.util.*.

- The class `BubbleSortTasks` must be public top-level.

- Inside, static inner records: `Task` and `SortResult`.

- Provide Javadoc comments for the method and classes.

Potential pitfalls:

- Since we need to not modify original list, we copy it. Use `new ArrayList<>(tasks)`.

- The comparator must be consistent with sorting rules.

- Ensure that bubble sort uses the comparator correctly: if compare(a,b) > 0 => a should come after b => swap.

- For null priorities: treat as lowest; but also need to ensure stable ordering among null tasks based on createdAt ascending.

Implementation of compare:

```
private static int compare(Task a, Task b) {
    boolean aNull = a.priority == null;
    boolean bNull = b.priority == null;
    if (aNull && !bNull) {
        // a is null => after b
        return 1;
    } else if (!aNull && bNull) {
        // b is null => a before b
        return -1;
    } else if (!aNull && !bNull) {
        // both non-null
        int cmp = Integer.compare(b.priority, a.priority); // descending: larger first => if a > b => -1? Let's compute.
        // Actually we want a before b if a.priority > b.priority. So compare returns negative if a should be before b.
        // So we can do: if a.priority > b.priority => return -1; else if < => 1; else tie.
        if (a.priority != b.priority) {
            return Integer.compare(a.priority, b.priority); // ascending? Wait: descending means larger first. If a.priority > b.priority, then a should come before b => compare returns -1. So we can do: return Integer.compare(b.priority, a.priority). Because if a.priority=5, b.priority=3 => b.priority (3) vs a.priority (5) => 3-5 = -2? Actually Integer.compare(3,5) = -2 => negative => indicates a before b? Let's test: compare(a,b) returns negative if a should be before b. So we want negative when a.priority > b.priority. Using Integer.compare(b.priority, a.priority) yields: b=3, a=5 => compare(3,5) = -2 (negative). Good. If a.priority < b.priority, e.g., a=3,b=5 => compare(5,3)=2 positive => a after b. So that works.

        // tiebreaker:
        if (a.createdAt != b.createdAt) {
            return Long.compare(a.createdAt, b.createdAt); // ascending: smaller createdAt first => negative if a earlier.
        }
        return 0;
    } else { // both null
        // order by createdAt ascending
        return Long.compare(a.createdAt, b.createdAt);
    }
}
```

But careful: In the case where both non-null and equal priority, we need tiebreaker: earlier createdAt first. So after comparing priorities (descending), if equal, compare createdAt ascending.

Thus final comparator:

```
if (aNull != bNull) {
   // null handling
} else if (a.priority == null && b.priority == null) {
   // both null: compare createdAt asc
} else {
   // both non-null
   int cmp = Integer.compare(b.priority, a.priority); // descending
   if (cmp != 0) return cmp;
   // tie: compare createdAt asc
   return Long.compare(a.createdAt, b.createdAt);
}
```

But need to handle nulls: If aNull && !bNull => a after b => return 1; if !aNull && bNull => a before b => -1.

Thus:

```
if (aNull && !bNull) return 1;
if (!aNull && bNull) return -1;
```

Now for both non-null: as above.

Edge Cases: If both null, we treat as createdAt ascending.

Now bubble sort loops:

```
int n = list.size();
int swapCount = 0;
for (int i = 0; i < n; i++) {
    boolean swapped = false;
    for (int j = 0; j < n - i - 1; j++) {
        Task a = list.get(j);
        Task b = list.get(j+1);
        if (compare(a, b) > 0) {
            // swap
            Task temp = a;
            list.set(j, b);
            list.set(j+1, temp);
            swapCount++;
            swapped = true;
        }
    }
    if (!swapped) break; // optional optimization
}
```

But careful: The bubble sort typical algorithm uses `for (int i = 0; i < n; i++)` and inner loop goes to `n - i - 1`. That's fine.

Now after sorting, return new SortResult(list, swapCount).

Potential issues: Since we used `list.set(j, b)` etc., but we need to ensure that swapping works correctly. Actually typical bubble sort uses a temporary variable:

```
Task temp = list.get(j);
list.set(j, list.get(j+1));
list.set(j+1, temp);
```

But we already have references a and b; we can just assign.

Now about immutability: The Task record is immutable (record). So swapping references is fine.

Now about returning SortResult: Since it's a record with fields tasks and swapCount. We'll define:

```
public record SortResult(List<Task> tasks, int swapCount) {}
```

But note that the order of fields matters; we need to match requirement: fields: `List<Task> tasks` and `int swapCount`. So record definition: `public record SortResult(List<Task> tasks, int swapCount) {}`.

Now about Javadoc: Provide documentation for class and method.

Potential improvements: Use `Collections.swap(list, j, j+1)` but that's okay.

Now test with example:

We'll simulate quickly.

Implementation details:

- In bubble sort, we need to compare using comparator. Since comparator returns -1,0,1. We'll implement as static method `private static int compare(Task a, Task b)`.

Now let's think about null handling: Suppose tasks have null priority. According to spec: tasks where priority is null always sort to the end of list, ordered by createdAt ascending among themselves.

Our comparator ensures that any task with null priority will be considered greater than any non-null (return 1 when aNull && !bNull). That means in bubble sort, if a has null and b doesn't, compare returns >0 => swap => a moves rightwards (to later positions). This will push null tasks to the end. Among null tasks themselves, they are compared by createdAt ascending: if both null, compare returns Long.compare(a.createdAt,b.createdAt) which sorts ascending.

Thus correct.

Now about swap count: Should count each swap of adjacent elements. Our algorithm increments swapCount for each swap. That's fine.

Now ensure we don't modify original list: We copy to new ArrayList.

Potential issues: The comparator uses `Integer.compare(b.priority, a.priority)` for descending. However if priorities are equal, we skip that and go to tiebreaker. But note that if both non-null and equal priority, then `Integer.compare(b.priority, a.priority)` returns 0; then we go to tiebreaker.

Now about createdAt: It's a long. Use `Long.compare(a.createdAt, b.createdAt)`.

Now about null tasks: If both null, we compare createdAt ascending.

Alright.

Now code skeleton:

```
import java.util.*;

public class BubbleSortTasks {

    /**
     * Represents a task record with name, optional priority, and creation timestamp.
     */
    public record Task(String name, Integer priority, long createdAt) {}

    /**
     * Holds the result of a bubble sort operation: the sorted list and the number of swaps performed.
     */
    public record SortResult(List<Task> tasks, int swapCount) {}

    /**
     * Sorts the given list of tasks using bubble sort according to the specified ordering rules:
     * <ul>
     *   <li>Primary: priority descending (higher priority first)</li>
     *   <li>Tiebreaker: createdAt ascending</li>
     *   <li>Tasks with null priority are placed at the end, ordered by createdAt ascending.</li>
     * </ul>
     *
     * @param tasks the list of tasks to sort (will not be modified)
     * @return a SortResult containing the sorted list and total swap count
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        // Create a mutable copy to avoid modifying the original list
        List<Task> list = new ArrayList<>(tasks);
        int n = list.size();
        int swapCount = 0;

        // Bubble sort implementation
        for (int i = 0; i < n; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                Task a = list.get(j);
                Task b = list.get(j + 1);
                if (compare(a, b) > 0) {
                    // Swap adjacent elements
                    Task temp = a;
                    list.set(j, b);
                    list.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // If no swaps occurred in this pass, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(list, swapCount);
    }

    /**
     * Compares two tasks according to the sorting rules.
     *
     * @param a first task
     * @param b second task
     * @return negative if a should come before b, positive if a should come after b, zero if equal
     */
    private static int compare(Task a, Task b) {
        boolean aNull = a.priority == null;
        boolean bNull = b.priority == null;

        // Null priority tasks are placed at the end
        if (aNull && !bNull) {
            return 1; // a after b
        } else if (!aNull && bNull) {
            return -1; // a before b
        }

        // Both have non-null priorities or both null
        if (!aNull && !bNull) {
            // Primary: priority descending
            int cmp = Integer.compare(b.priority, a.priority);
            if (cmp != 0) {
                return cmp;
            }
            // Tiebreaker: createdAt ascending
            return Long.compare(a.createdAt, b.createdAt);
        } else {
            // Both null: order by createdAt ascending
            return Long.compare(a.createdAt, b.createdAt);
        }
    }
}
```

Check for correctness.

Now test with example:

Input tasks:

- Task("bug", 3, 1000)
- Task("feature",5,2000)
- Task("docs",3,500)

Let's simulate bubble sort:

list = [bug, feature, docs]

n=3

i=0:
- j=0: a=bug, b=feature. compare(bug, feature): both non-null; priority 3 vs 5 => cmp = Integer.compare(5,3) = 2? Wait: b.priority=5, a.priority=3 => Integer.compare(5,3)=2 >0 => return 2 => indicates bug after feature => swap. So swapCount=1. list becomes [feature, bug, docs].
- j=1: a=bug (now at index1), b=docs. compare(bug, docs): priorities equal (3 vs 3) => cmp = Integer.compare(3,3)=0; tiebreaker: createdAt 1000 vs 500 => Long.compare(1000,500) = 1? Actually Long.compare(a.createdAt,b.createdAt) returns positive if a > b. Here a.createdAt=1000 > b.createdAt=500 => returns 1 => indicates bug after docs => swap. So swapCount=2. list becomes [feature, docs, bug].

After inner loop, swapped=true.

i=1:
- j=0: a=feature, b=docs. compare(feature, docs): priorities 5 vs 3 => cmp = Integer.compare(3,5) = -2? Wait: b.priority=3, a.priority=5 => Integer.compare(3,5) = -2 <0 => indicates feature before docs (good). No swap.
- j=1: not executed because n-i-1 = 3-1-1=1? Actually for i=1, inner loop runs j< n-i-1 = 3-1-1 =1 => j=0 only. So no more swaps.

swapped remains false after pass? Actually swapped was set to false at start of each i iteration; after first pass swapped=true; after second pass, we didn't swap anything, so swapped stays false, break out.

Thus final list: [feature, docs, bug] as expected. swapCount=2.

Works.

Now test null priority scenario:

Suppose tasks: [Task("a", null, 100), Task("b", 5, 200), Task("c", null, 50)]

Sorted order should be: b (priority 5), then a and c sorted by createdAt ascending among nulls: a (100) vs c (50) => c first? Wait: null tasks sorted by createdAt ascending: earlier timestamp first. So c (50) before a (100). So final list: [b, c, a].

Let's simulate bubble sort:

list = [a(null), b(5), c(null)]

n=3

i=0:
- j=0: compare(a,c?) Actually j=0: a=Task("a", null,100), b=Task("b",5,200). Compare: aNull && !bNull => return 1 => swap. So list becomes [b, a, c]; swapCount=1.
- j=1: now a=Task("a",null,100) at index1, b=Task("c",null,50) at index2. Both null: compare returns Long.compare(100,50)=1 => indicates a after c => swap. So list becomes [b,c,a]; swapCount=2.

i=1:
- j=0: compare(b,c): b non-null, c null => return -1? Actually !aNull && bNull => return -1 => no swap.
- swapped remains false? Actually after first pass swapped=true. In second pass, we start with swapped=false; inner loop j runs only up to n-i-1 = 3-1-1=1 => j=0 only. Since compare(b,c) returns -1 (b before c), no swap. swapped stays false => break.

Result: [b,c,a] as expected. swapCount=2.

Thus works.

Now ensure that we didn't modify original list: we used new ArrayList copy.

Now about returning SortResult: The record's constructor expects tasks and swapCount. We'll pass list and swapCount.

Potential issues: The record's fields are final; but that's fine.

Now about imports: Need java.util.*.

Now about Javadoc: Provide class-level and method-level docs.

Now about naming: The static inner records must be public? Not required but can be. We'll keep them public for external use.

Thus final code:

```
import java.util.ArrayList;
import java.util.List;

/**
 * Provides a bubble sort implementation for task records.
 */
public class BubbleSortTasks {

    /**
     * Represents a task with a name, optional priority, and creation timestamp.
     */
    public record Task(String name, Integer priority, long createdAt) {
        // No additional methods needed
    }

    /**
     * Holds the result of a bubble sort operation: the sorted list of tasks and the number of swaps performed.
     */
    public record SortResult(List<Task> tasks, int swapCount) {
        // No additional methods needed
    }

    /**
     * Sorts the given list of tasks using bubble sort according to the following rules:
     * <ol>
     *   <li>Primary: priority descending (higher priority first)</li>
     *   <li>Tiebreaker: createdAt ascending</li>
     *   <li>Tasks with a null priority are placed at the end of the list, ordered by createdAt ascending.</li>
     * </ol>
     *
     * The original input list is not modified; a new list containing the sorted tasks is returned.
     *
     * @param tasks the list of tasks to sort
     * @return a {@link SortResult} containing the sorted list and the total number of swaps performed
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        // Create a mutable copy to avoid modifying the original list
        List<Task> list = new ArrayList<>(tasks);
        int n = list.size();
        int swapCount = 0;

        // Bubble sort implementation
        for (int i = 0; i < n; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                Task a = list.get(j);
                Task b = list.get(j + 1);
                if (compare(a, b) > 0) {
                    // Swap adjacent elements
                    Task temp = a;
                    list.set(j, b);
                    list.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // If no swaps occurred in this pass, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(list, swapCount);
    }

    /**
     * Compares two tasks according to the sorting rules.
     *
     * @param a first task
     * @param b second task
     * @return negative if a should come before b, positive if a should come after b, zero if they are equal
     */
    private static int compare(Task a, Task b) {
        boolean aNull = a.priority == null;
        boolean bNull = b.priority == null;

        // Null priority tasks are placed at the end of the list
        if (aNull && !bNull) {
            return 1; // a after b
        } else if (!aNull && bNull) {
            return -1; // a before b
        }

        // Both have non-null priorities or both are null
        if (!aNull && !bNull) {
            // Primary: priority descending
            int cmp = Integer.compare(b.priority, a.priority);
            if (cmp != 0) {
                return cmp;
            }
            // Tiebreaker: createdAt ascending
            return Long.compare(a.createdAt, b.createdAt);
        } else {
            // Both null: order by createdAt ascending
            return Long.compare(a.createdAt, b.createdAt);
        }
    }
}
```

That should satisfy.

Now check for any missing imports: We used ArrayList and List; need import java.util.*; but we can just import java.util.*.

Potential compile errors: The record definitions inside class must be public? Not required but okay.

Now test with example:

We'll run mental simulation: Already did.

Now think about edge cases: If tasks is empty, list size 0 => loops not executed; swapCount=0; returns SortResult(empty list,0). Works.

If tasks contains only null priority tasks: They will be sorted by createdAt ascending. Our comparator handles both null case: compare returns Long.compare(a.createdAt,b.createdAt). Bubble sort will sort them accordingly. Since all have null priority, they are considered equal in primary, then tiebreaker sorts by createdAt ascending. Works.

If tasks contains duplicate priorities and same createdAt? Then order is stable? Bubble sort is not stable but since we only swap when compare >0, if equal (compare returns 0) no swap; thus relative order of equal elements remains as original. That's fine.

Now about swap count: Should count each adjacent swap. Our algorithm increments for each swap. Good.

Now about not using any sorting utilities: We used only loops and manual swaps. Good.

Now about returning new list: Yes.

Now about Javadoc: Provided.

Thus final answer: Provide the code in a single file `BubbleSortTasks.java`.

Potential improvements: Use `Collections.swap` but it's okay.

Now produce final output.


## Response



**BubbleSortTasks.java**

```java
import java.util.ArrayList;
import java.util.List;

/**
 * Provides a bubble‑sort implementation for task records.
 */
public class BubbleSortTasks {

    /**
     * Represents a task with a name, an optional priority and a creation timestamp.
     */
    public record Task(String name, Integer priority, long createdAt) {
        // The record is immutable by design.
    }

    /**
     * Holds the result of a bubble‑sort operation: the sorted list of tasks
     * and the total number of swaps performed during sorting.
     */
    public record SortResult(List<Task> tasks, int swapCount) {
        // No additional methods are required.
    }

    /**
     * Sorts the given list of tasks using the bubble‑sort algorithm according to the
     * following rules:
     * <ol>
     *   <li><b>Primary:</b> priority in descending order (higher priority first).</li>
     *   <li><b>Tiebreaker:</b> when priorities are equal, createdAt in ascending order.</li>
     *   <li><b>Null handling:</b> tasks whose priority is {@code null} are placed at the
     *       end of the list and ordered by createdAt ascending among themselves.</li>
     * </ol>
     *
     * The original input list is not modified; a new list containing the sorted tasks
     * is returned.
     *
     * @param tasks the list of tasks to sort (may be empty)
     * @return a {@link SortResult} with the sorted list and the total swap count
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        // Create a mutable copy so the original list stays unchanged.
        List<Task> list = new ArrayList<>(tasks);
        int n = list.size();
        int swapCount = 0;

        // Classic bubble sort with early exit when no swaps occur.
        for (int i = 0; i < n; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                Task a = list.get(j);
                Task b = list.get(j + 1);
                if (compare(a, b) > 0) {
                    // Adjacent elements are out of order → swap them.
                    Task temp = a;
                    list.set(j, b);
                    list.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // If no swaps happened in this pass, the list is already sorted.
            if (!swapped) {
                break;
            }
        }

        return new SortResult(list, swapCount);
    }

    /**
     * Compares two tasks according to the sorting rules defined for
     * {@link #bubbleSortTasks(List)}.
     *
     * @param a first task
     * @param b second task
     * @return negative if a should come before b,
     *         positive if a should come after b,
     *         zero if they are considered equal.
     */
    private static int compare(Task a, Task b) {
        boolean aNull = a.priority == null;
        boolean bNull = b.priority == null;

        // Null priority tasks must be placed at the end of the list.
        if (aNull && !bNull) {
            return 1;          // a after b
        } else if (!aNull && bNull) {
            return -1;         // a before b
        }

        // Both have non‑null priorities or both are null.
        if (!aNull && !bNull) {
            // Primary: priority descending.
            int cmp = Integer.compare(b.priority, a.priority);
            if (cmp != 0) {
                return cmp;
            }
            // Tiebreaker: createdAt ascending.
            return Long.compare(a.createdAt, b.createdAt);
        } else {
            // Both null → order by createdAt ascending.
            return Long.compare(a.createdAt, b.createdAt);
        }
    }
}
```

**Explanation of the implementation**

* **Records** – `Task` and `SortResult` are immutable records that hold the required fields.
* **Bubble sort** – The algorithm iterates over the list, swapping adjacent elements whenever they violate the ordering defined by `compare`.  
  The comparator implements the three sorting rules:
  1. Higher priority comes first (descending).
  2. If priorities are equal, earlier `createdAt` comes first.
  3. Tasks with a `null` priority are moved to the end and then sorted by `createdAt`.
* **Swap counting** – Every time two elements are swapped, `swapCount` is incremented.
* **Non‑mutating** – A new `ArrayList` is created from the input list; the original list is never altered.

The code follows Java conventions, includes Javadoc comments, and satisfies all the requirements of the task.

## Timings

- Time to first token: 1.99s
- Temperature: 0.0
- Total generation: 599.51s
- Reasoning tokens: 5677
- Answer tokens: 1159
- Total tokens: 6836

## Server Timings (llama.cpp)

- Prompt tokens: 472
- Prompt eval speed: 237.67 t/s
- Prompt eval time: 1985.91 ms
- Generation tokens: 6836
- Generation speed: 11.44 t/s
- Generation time: 597516.50 ms
