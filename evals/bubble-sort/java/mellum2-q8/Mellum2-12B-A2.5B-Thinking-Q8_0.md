# Code Eval: Mellum2-12B-A2.5B-Thinking-Q8_0

## Prompt

# Bubble Sort Tasks — Java

Implement a bubble sort function for task records.

## Requirements

Write a single file `BubbleSortTasks.java` containing:

1. A `Task` record (or class) with fields:
   - `String name`
   - `Integer priority` (nullable — use `Integer`, not `int`)
   - `long createdAt`

2. A `SortResult` record (or class) with fields:
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
List<Task> tasks = List.of(
    new Task("bug",     3, 1000),
    new Task("feature", 5, 2000),
    new Task("docs",    3, 500)
);

SortResult result = BubbleSortTasks.bubbleSortTasks(tasks);
// result.tasks() = [Task("feature",5,2000), Task("docs",3,500), Task("bug",3,1000)]
// result.swapCount() = 2
```

Write clean, well-documented, idiomatic Java code. Use Javadoc where appropriate.


## Reasoning

We need to produce a single file BubbleSortTasks.java with a Task record, SortResult record, and static method bubbleSortTasks implementing bubble sort with custom comparator as described, handling nulls, counting swaps, not modifying original list. Provide Javadoc. Ensure we use Java 17+ features (records). Provide code.


## Response

**BubbleSortTasks.java**

```java
import java.util.ArrayList;
import java.util.List;

/**
 * Utility class that provides a bubble‑sort implementation for {@link Task} objects.
 *
 * <p>The sorting order is:
 * <ol>
 *   <li>Higher {@code priority} first (descending).</li>
 *   <li>If priorities are equal, earlier {@code createdAt} first (ascending).</li>
 *   <li>Tasks with a {@code null} priority are placed at the end of the list,
 *       ordered by {@code createdAt} ascending among themselves.</li>
 * </ol>
 *
 * <p>The method returns a {@link SortResult} containing the newly sorted list
 * and the total number of swaps performed during the bubble‑sort process.
 * The original input list is never modified.
 */
public final class BubbleSortTasks {

    // Prevent instantiation
    private BubbleSortTasks() { }

    /**
     * A simple data holder for a task.
     *
     * @param name      the name of the task (e.g. "bug", "feature")
     * @param priority  the priority of the task; may be {@code null}
     * @param createdAt the epoch‑millisecond timestamp when the task was created
     */
    public record Task(String name, Integer priority, long createdAt) { }

    /**
     * Holds the result of a bubble‑sort operation.
     *
     * @param tasks     the sorted list of tasks
     * @param swapCount the total number of element swaps performed
     */
    public record SortResult(List<Task> tasks, int swapCount) { }

    /**
     * Sorts a list of {@link Task} objects using the bubble‑sort algorithm.
     *
     * @param tasks the list to sort; may be {@code null} or contain {@code null} elements
     * @return a {@link SortResult} containing a new sorted list and the swap count
     *
     * @throws IllegalArgumentException if {@code tasks} is {@code null}
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null) {
            throw new IllegalArgumentException("Input list cannot be null");
        }

        // Work on a defensive copy so the original list is never mutated.
        List<Task> workingList = new ArrayList<>(tasks);
        int n = workingList.size();
        int swapCount = 0;

        // Classic bubble‑sort: repeat passes until no swaps are needed.
        boolean swapped;
        for (int i = 0; i < n - 1; i++) {
            swapped = false;
            // After each pass, the largest element among the unsorted part
            // bubbles to its final position at index n‑i‑1.
            for (int j = 0; j < n - i - 1; j++) {
                Task current = workingList.get(j);
                Task next    = workingList.get(j + 1);

                if (shouldSwap(current, next)) {
                    // Swap in the list.
                    workingList.set(j, next);
                    workingList.set(j + 1, current);
                    swapCount++;
                    swapped = true;
                }
            }
            // If no swaps occurred, the list is already sorted.
            if (!swapped) {
                break;
            }
        }

        return new SortResult(workingList, swapCount);
    }

    /**
     * Determines whether two {@link Task} objects should be swapped
     * according to the required ordering rules.
     *
     * @param a the first task
     * @param b the second task
     * @return {@code true} if {@code a} should appear after {@code b} in the sorted list
     */
    private static boolean shouldSwap(Task a, Task b) {
        // Both priorities are non‑null → compare descending.
        if (a.priority() != null && b.priority() != null) {
            int cmp = b.priority().compareTo(a.priority()); // descending
            if (cmp != 0) {
                return cmp < 0; // swap if b has lower priority
            }
            // Priorities equal → compare createdAt ascending.
            return a.createdAt() > b.createdAt();
        }

        // One or both priorities are null.
        // Null priority always goes to the end.
        if (a.priority() == null && b.priority() != null) {
            return false; // a (null) should stay after b (non‑null)
        }
        if (a.priority() != null && b.priority() == null) {
            return true;  // a (non‑null) should stay before b (null)
        }

        // Both priorities are null → order by createdAt ascending.
        return a.createdAt() > b.createdAt();
    }
}
```

### How It Works
1. **Defensive Copy** – A new `ArrayList` is created from the input list so the original data stays untouched.
2. **Bubble‑Sort Loop** – The outer loop runs at most `n‑1` passes. The inner loop compares adjacent elements and swaps them when the required order is violated.
3. **Comparison Logic** – The private `shouldSwap` method encodes the three sorting rules:
   * Higher `priority` first (descending).
   * If priorities tie, earlier `createdAt` first (ascending).
   * `null` priorities are treated as the lowest value and are placed at the end, still ordered by `createdAt`.
4. **Swap Counting** – Every time a swap occurs, `swapCount` is incremented.
5. **Result** – After the loops finish, a `SortResult` containing the sorted list and the total swap count is returned.

The implementation adheres strictly to the requirement of using the bubble‑sort algorithm and avoids any built‑in sorting utilities.

## Timings

- Time to first token: 0.31s
- Total generation: 18.69s
- Reasoning tokens: 85
- Answer tokens: 1397
- Total tokens: 1482
