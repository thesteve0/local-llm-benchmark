# Code Eval: Mellum2-12B-A2.5B-Thinking-Q6_K

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

We need to implement bubble sort for the given records. The sorting rules: primary by priority descending, but if priority is null, those go to end. Among nulls, sort by createdAt ascending. For non-null priorities, sort by priority descending, and if equal, by createdAt ascending.

We need to implement bubble sort manually, not using any built-in sort. We'll create a copy of the input list to avoid modifying original. Then we'll perform bubble sort: iterate through the list, comparing adjacent elements, swapping if they are out of order. Count swaps.

Comparison logic: we need a method to compare two Task objects according to the rules. Let's define a helper method `int compare(Task a, Task b)`.

Comparison rules:

- If a.priority == null and b.priority == null: compare createdAt ascending => return Long.compare(a.createdAt, b.createdAt).
- If a.priority == null: a should come after b => return 1 (since we want descending priority, null is lowest).
- If b.priority == null: b should come after a => return -1.
- If a.priority != null and b.priority != null: compare priority descending => Integer.compare(b.priority, a.priority). If equal, compare createdAt ascending => Long.compare(a.createdAt, b.createdAt).

Note: The compare method should return negative if a < b, zero if equal, positive if a > b.

In bubble sort, we swap if `compare(list.get(j), list.get(j+1)) > 0` (i.e., current element is greater than next, so they are out of order).

We need to count swaps. Each time we swap, increment swapCount.

After bubble sort, return a new SortResult with the sorted list and swapCount.

We must ensure we don't modify the original list. So we create a new ArrayList<Task> sortedTasks = new ArrayList<>(tasks); then sort that.

Edge cases: empty list, list with one element.

Let's write the code.

We'll use Java 16+ for records.

Javadoc: document the class, records, method, parameters, return value.

Let's write the code.


## Response

```java
import java.util.ArrayList;
import java.util.List;

/**
 * Implements bubble sort for task records.
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
     * Priority may be {@code null}, which indicates the lowest priority.
     */
    public static record Task(String name, Integer priority, long createdAt) {
    }

    /**
     * Represents the result of a bubble sort operation.
     *
     * @param tasks    the sorted list of tasks
     * @param swapCount the total number of swaps performed during sorting
     */
    public static record SortResult(List<Task> tasks, int swapCount) {
    }

    /**
     * Sorts a list of tasks using the bubble sort algorithm.
     * <p>
     * The original list is not modified. The sorting follows these rules:
     * <ul>
     *   <li>Tasks with higher priority come first</li>
     *   <li>If priorities are equal, tasks with earlier creation timestamps come first</li>
     *   <li>Tasks with null priority are placed at the end, sorted by creation timestamp ascending</li>
     * </ul>
     *
     * @param tasks the list of tasks to sort (must not be {@code null})
     * @return a {@link SortResult} containing the sorted list and the total swap count
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null) {
            throw new IllegalArgumentException("Input list cannot be null");
        }

        // Create a new list to avoid modifying the original
        List<Task> sortedTasks = new ArrayList<>(tasks);
        int n = sortedTasks.size();
        int swapCount = 0;

        // Perform bubble sort
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                Task current = sortedTasks.get(j);
                Task next = sortedTasks.get(j + 1);

                // If current should come after next, swap them
                if (compare(current, next) > 0) {
                    sortedTasks.set(j, next);
                    sortedTasks.set(j + 1, current);
                    swapCount++;
                    swapped = true;
                }
            }
            // If no swaps occurred, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sortedTasks, swapCount);
    }

    /**
     * Compares two tasks according to the sorting rules.
     *
     * @param a the first task
     * @param b the second task
     * @return a negative integer if {@code a} should come before {@code b},
     *         zero if they are equal,
     *         a positive integer if {@code a} should come after {@code b}
     */
    private static int compare(Task a, Task b) {
        // Both priorities are null: sort by createdAt ascending
        if (a.priority == null && b.priority == null) {
            return Long.compare(a.createdAt, b.createdAt);
        }

        // Only a's priority is null: a should come after b
        if (a.priority == null) {
            return 1;
        }

        // Only b's priority is null: b should come after a
        if (b.priority == null) {
            return -1;
        }

        // Both priorities are non-null: sort by priority descending, then by createdAt ascending
        int priorityComparison = Integer.compare(b.priority, a.priority);
        if (priorityComparison != 0) {
            return priorityComparison;
        }
        return Long.compare(a.createdAt, b.createdAt);
    }
}
```

## Timings

- Time to first token: 0.44s
- Total generation: 17.43s
- Reasoning tokens: 526
- Answer tokens: 1052
- Total tokens: 1578
