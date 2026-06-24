import java.util.ArrayList;
import java.util.List;

/**
 * Represents a task with a name, optional priority, and creation timestamp.
 */
record Task(String name, Integer priority, long createdAt) {}

/**
 * Holds the result of sorting tasks, including the sorted list and the number of swaps performed.
 */
record SortResult(List<Task> tasks, int swapCount) {}

/**
 * Provides bubble sort functionality for {@link Task} records.
 */
public class BubbleSortTasks {

    /**
     * Sorts a list of tasks using the bubble sort algorithm.
     *
     * <p>Sorting rules:
     * <ol>
     *   <li>Primary: descending by {@code priority} (higher priority first)</li>
     *   <li>Tiebreaker: ascending by {@code createdAt} (earlier timestamp first)</li>
     *   <li>Null handling: tasks with {@code null} priority are placed at the end,
     *       ordered by {@code createdAt} ascending among themselves</li>
     * </ol>
     *
     * @param tasks the list of tasks to sort
     * @return a {@link SortResult} containing the sorted list and total swap count
     * @throws IllegalArgumentException if {@code tasks} is null
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null) {
            throw new IllegalArgumentException("Input list cannot be null");
        }

        // Create a defensive copy to avoid modifying the original list
        List<Task> sorted = new ArrayList<>(tasks);
        int swapCount = 0;
        int n = sorted.size();

        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                if (shouldSwap(sorted.get(j), sorted.get(j + 1))) {
                    // Swap adjacent elements
                    Task temp = sorted.get(j);
                    sorted.set(j, sorted.get(j + 1));
                    sorted.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // Optimization: if no swaps occurred in a pass, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sorted, swapCount);
    }

    /**
     * Determines if task {@code a} should be swapped with task {@code b}
     * to maintain the correct sort order.
     *
     * @param a the first task
     * @param b the second task
     * @return {@code true} if {@code a} should come after {@code b} in the sorted list
     */
    private static boolean shouldSwap(Task a, Task b) {
        return compareTasks(a, b) > 0;
    }

    /**
     * Compares two tasks according to the specified sorting rules.
     *
     * @return negative if {@code a} should come before {@code b},
     *         zero if they are equivalent in sort order,
     *         positive if {@code a} should come after {@code b}
     */
    private static int compareTasks(Task a, Task b) {
        boolean aNull = a.priority == null;
        boolean bNull = b.priority == null;

        // Both have null priority: sort by createdAt ascending
        if (aNull && bNull) {
            return Long.compare(a.createdAt, b.createdAt);
        }
        // a has null priority, b does not: a goes after b
        if (aNull) {
            return 1;
        }
        // b has null priority, a does not: b goes after a
        if (bNull) {
            return -1;
        }

        // Both have non-null priority: sort descending by priority
        int priorityCmp = Integer.compare(b.priority, a.priority);
        if (priorityCmp != 0) {
            return priorityCmp;
        }

        // Priorities are equal: sort ascending by createdAt
        return Long.compare(a.createdAt, b.createdAt);
    }
}
