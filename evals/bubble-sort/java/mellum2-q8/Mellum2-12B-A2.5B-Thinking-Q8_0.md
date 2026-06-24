# Code Eval: Mellum2-12B-A2.5B-Thinking-Q8_0

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

We need to implement bubble sort for a list of Task records. The sorting rules: primary by priority descending, but null priorities go to end. Tiebreaker: createdAt ascending. For null priorities, they are at end, sorted by createdAt ascending.

We need to return a new list, not modify original. So we can copy the list, then bubble sort on the copy.

We need to count swaps.

Implementation details:

- Define Task record with name, priority (Integer), createdAt.
- Define SortResult record with List<Task> tasks, int swapCount.

- bubbleSortTasks method: takes List<Task> tasks. Create a new ArrayList<Task> list = new ArrayList<>(tasks). Then perform bubble sort on list.

Comparison function: we need a method compare(Task a, Task b) returning negative if a < b (i.e., a should come after b), positive if a > b, zero if equal.

Rules:

- If a.priority == null and b.priority == null: compare createdAt ascending. So a < b if a.createdAt > b.createdAt (since earlier timestamp should come first). So return Long.compare(a.createdAt, b.createdAt). Actually we want ascending: earlier (smaller) comes first. So if a.createdAt < b.createdAt, a should come before b, so a < b is false? Let's define: we want to sort in order: higher priority first, then earlier createdAt. So we can define a comparator:

Comparator<Task> comp = Comparator.comparing(Task::priority, Comparator.nullsLast(Comparator.reverseOrder()))
    .thenComparing(Task::createdAt);

This sorts by priority descending (higher first), nulls last, then createdAt ascending.

But we need to implement bubble sort manually, so we need to implement the comparison logic.

We can write a method int compare(Task a, Task b):

- If a.priority == null && b.priority == null: return Long.compare(a.createdAt, b.createdAt); // ascending
- If a.priority == null: return 1; // a should be after b
- If b.priority == null: return -1; // a should be before b
- Otherwise: // both non-null
   - int cmp = b.priority.compareTo(a.priority); // descending: higher priority first
   - if (cmp != 0) return cmp;
   - return Long.compare(a.createdAt, b.createdAt); // ascending

This implements the rules.

Bubble sort algorithm:

int n = list.size();
int swapCount = 0;
for (int i = 0; i < n - 1; i++) {
    boolean swapped = false;
    for (int j = 0; j < n - 1 - i; j++) {
        Task current = list.get(j);
        Task next = list.get(j + 1);
        if (compare(current, next) > 0) { // current should come after next
            // swap
            list.set(j, next);
            list.set(j + 1, current);
            swapCount++;
            swapped = true;
        }
    }
    if (!swapped) break;
}

After sorting, return new SortResult(list, swapCount);

Edge cases: empty list, single element.

We must not modify original list, so we copy.

Now, write the code with Javadoc.

We need to ensure the class is public, and the records are static inner.

Let's write the code.


## Response

```java
import java.util.ArrayList;
import java.util.List;

/**
 * Implements bubble sort for task records according to specified rules.
 * <p>
 * The sorting order is:
 * <ol>
 *   <li>Primary: priority descending (higher priority first)</li>
 *   <li>Tiebreaker: createdAt ascending (earlier timestamp first)</li>
 *   <li>Null handling: tasks with null priority are placed at the end, sorted by createdAt ascending</li>
 * </ol>
 */
public class BubbleSortTasks {

    /**
     * Represents a task with a name, priority, and creation timestamp.
     * <p>
     * {@code priority} is nullable; {@code null} values are treated as the lowest priority.
     */
    public static record Task(String name, Integer priority, long createdAt) {
        // Record is immutable; no explicit constructor needed
    }

    /**
     * Holds the result of a bubble sort operation.
     *
     * @param tasks    the sorted list of tasks (new list, original unchanged)
     * @param swapCount the total number of swaps performed during sorting
     */
    public static record SortResult(List<Task> tasks, int swapCount) {
        // Record is immutable; no explicit constructor needed
    }

    /**
     * Sorts a list of tasks using the bubble sort algorithm.
     * <p>
     * The original list is not modified; a new sorted list is returned.
     *
     * @param tasks the list of tasks to sort (must not be null)
     * @return a {@link SortResult} containing the sorted list and total swap count
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null) {
            throw new IllegalArgumentException("Input list cannot be null");
        }

        // Create a new list to avoid modifying the original
        List<Task> sortedList = new ArrayList<>(tasks);
        int n = sortedList.size();
        int swapCount = 0;

        // Bubble sort implementation
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                Task current = sortedList.get(j);
                Task next = sortedList.get(j + 1);

                // If current should come after next, swap them
                if (compare(current, next) > 0) {
                    sortedList.set(j, next);
                    sortedList.set(j + 1, current);
                    swapCount++;
                    swapped = true;
                }
            }
            // Optimization: stop if no swaps occurred in a pass
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sortedList, swapCount);
    }

    /**
     * Compares two tasks according to the sorting rules.
     *
     * @param a the first task
     * @param b the second task
     * @return a negative integer if {@code a} should come before {@code b},
     *         a positive integer if {@code a} should come after {@code b},
     *         or zero if they are equal for sorting purposes
     */
    private static int compare(Task a, Task b) {
        // Handle null priorities: they go to the end
        if (a.priority() == null && b.priority() == null) {
            // Both null: sort by createdAt ascending (earlier first)
            return Long.compare(a.createdAt(), b.createdAt());
        }
        if (a.priority() == null) {
            // a is null, b is not: a should come after b
            return 1;
        }
        if (b.priority() == null) {
            // b is null, a is not: a should come before b
            return -1;
        }

        // Both priorities are non-null: sort by priority descending
        int priorityCompare = b.priority().compareTo(a.priority());
        if (priorityCompare != 0) {
            return priorityCompare;
        }

        // Priorities equal: sort by createdAt ascending
        return Long.compare(a.createdAt(), b.createdAt());
    }
}
```

## Timings

- Time to first token: 0.41s
- Total generation: 23.64s
- Reasoning tokens: 805
- Answer tokens: 1074
- Total tokens: 1879
