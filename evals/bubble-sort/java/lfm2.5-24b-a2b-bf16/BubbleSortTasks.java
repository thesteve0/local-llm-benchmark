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
