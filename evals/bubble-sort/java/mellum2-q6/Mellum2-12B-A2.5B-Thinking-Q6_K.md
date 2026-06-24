# Code Eval: Mellum2-12B-A2.5B-Thinking-Q6_K

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

We need to produce a single file BubbleSortTasks.java with a Task record, SortResult record, and static method bubbleSortTasks implementing bubble sort with given rules. Must not modify original list, so we create a copy list. Count swaps. Sorting: primary by priority descending, but priority can be null. Nulls go to end. For non-null, higher priority first. Tiebreaker: createdAt ascending. For null priority, sort by createdAt ascending among themselves.

Implement comparator logic inside bubble sort: for each pair i,i+1, compare tasks a and b. Determine if a should come before b. If yes, no swap. Else swap and increment count.

We need to implement bubble sort: iterate n times, each pass compare adjacent, bubble largest to end. Since we want descending priority, we can treat "larger" as should be earlier. So in bubble sort, we move "larger" elements towards the front? Actually typical bubble sort moves largest to end. If we want descending order, we can move smallest to end. But easier: we can implement standard bubble sort that moves the "greater" element to the right (i.e., if a < b, swap). But we need descending order, so we can define a custom comparison: if a should come before b, then we consider a "greater" than b. So in bubble sort, we compare adjacent elements, and if the left is "less than" the right (i.e., left should come after right), we swap. This will bubble the "greater" elements to the left? Let's think.

Standard bubble sort for ascending order: for i from 0 to n-1, for j from 0 to n-i-1, if arr[j] > arr[j+1], swap. This moves the largest element to the end.

For descending order, we can do if arr[j] < arr[j+1], swap. This moves the smallest element to the end. After n passes, the array is sorted descending.

Thus we can implement bubble sort for descending order using the condition: if compare(a, b) < 0 (i.e., a should come after b), then swap.

We need a helper method compare(Task a, Task b) that returns negative if a should come after b (i.e., a < b in the desired order), zero if equal, positive if a should come before b.

Implementation of compare:

- If a.priority() == null and b.priority() == null: compare createdAt: a.createdAt() < b.createdAt() => a before b => return negative? Wait, we want a before b if createdAt is earlier. So if a.createdAt < b.createdAt, a should come before b => compare returns positive (a > b). If a.createdAt > b.createdAt, a should come after b => compare returns negative. If equal, return 0.

- If a.priority() == null and b.priority() != null: a should come after b => compare returns negative.

- If a.priority() != null and b.priority() == null: a should come before b => compare returns positive.

- If both non-null: compare priority: higher priority first. So if a.priority() > b.priority(), a before b => return positive. If a.priority() < b.priority(), a after b => return negative. If equal, compare createdAt: a.createdAt < b.createdAt => a before b => return positive. If a.createdAt > b.createdAt => a after b => return negative. If equal, return 0.

Thus compare method returns int.

Now bubble sort:

List<Task> list = new ArrayList<>(tasks);
int n = list.size();
int swapCount = 0;
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n - i - 1; j++) {
        Task a = list.get(j);
        Task b = list.get(j + 1);
        if (compare(a, b) < 0) {
            // a should come after b, swap
            list.set(j, b);
            list.set(j + 1, a);
            swapCount++;
        }
    }
}

Return new SortResult(list, swapCount);

We must not modify original input list, so we copy.

Now produce the code with Javadoc.

Task record: public record Task(String name, Integer priority, long createdAt) {}

SortResult record: public record SortResult(List<Task> tasks, int swapCount) {}

Static method: public static SortResult bubbleSortTasks(List<Task> tasks)

Add helper private static int compare(Task a, Task b)

Add Javadoc for records and method.

Make sure to import java.util.*;

Write clean code.

Now produce the final answer.


## Response

```java
import java.util.ArrayList;
import java.util.List;

/**
 * Represents a task with a name, priority (which may be null), and creation timestamp.
 */
public record Task(String name, Integer priority, long createdAt) {
    // No explicit constructor needed; the canonical constructor is generated.
}

/**
 * Holds the result of a bubble sort operation: the sorted list of tasks and the total number of swaps performed.
 */
public record SortResult(List<Task> tasks, int swapCount) {
    // No explicit constructor needed; the canonical constructor is generated.
}

public class BubbleSortTasks {

    /**
     * Sorts a list of tasks using the bubble sort algorithm according to the following rules:
     * <ol>
     *   <li>Primary key: priority descending (higher priority first).</li>
     *   <li>Tiebreaker: createdAt ascending (earlier timestamp first).</li>
     *   <li>Null priority: tasks with {@code null} priority are placed at the end of the list,
     *       ordered by createdAt ascending among themselves.</li>
     * </ol>
     *
     * The original list is not modified; a new sorted list is returned.
     *
     * @param tasks the list of tasks to sort; may be {@code null} or contain {@code null} elements
     * @return a {@link SortResult} containing the sorted list and the total number of swaps performed
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        // Defensive copy to avoid modifying the input list.
        List<Task> list = new ArrayList<>(tasks == null ? 0 : tasks.size());
        if (tasks != null) {
            list.addAll(tasks);
        }

        int n = list.size();
        int swapCount = 0;

        // Standard bubble sort for descending order.
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                Task a = list.get(j);
                Task b = list.get(j + 1);

                // If a should come after b, swap them.
                if (compare(a, b) < 0) {
                    list.set(j, b);
                    list.set(j + 1, a);
                    swapCount++;
                }
            }
        }

        return new SortResult(list, swapCount);
    }

    /**
     * Compares two tasks according to the sorting rules.
     *
     * @param a the first task
     * @param b the second task
     * @return a negative integer if {@code a} should come after {@code b},
     *         zero if they are equal in the sort order,
     *         a positive integer if {@code a} should come before {@code b}
     */
    private static int compare(Task a, Task b) {
        // Handle null priority cases.
        boolean aNull = a.priority() == null;
        boolean bNull = b.priority() == null;

        if (aNull && bNull) {
            // Both null: sort by createdAt ascending.
            return Long.compare(a.createdAt(), b.createdAt());
        } else if (aNull) {
            // a is null, b is not: a comes after b.
            return -1;
        } else if (bNull) {
            // b is null, a is not: a comes before b.
            return 1;
        }

        // Both priorities are non-null.
        int priorityComparison = b.priority().compareTo(a.priority()); // descending
        if (priorityComparison != 0) {
            return priorityComparison;
        }

        // Priorities equal: sort by createdAt ascending.
        return Long.compare(a.createdAt(), b.createdAt());
    }
}
```

## Timings

- Time to first token: 0.31s
- Total generation: 22.89s
- Reasoning tokens: 1131
- Answer tokens: 962
- Total tokens: 2093
