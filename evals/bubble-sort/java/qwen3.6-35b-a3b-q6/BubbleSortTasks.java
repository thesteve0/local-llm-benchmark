import java.util.ArrayList;
import java.util.List;

/**
 * Provides a bubble sort implementation for sorting task records based on
 * priority and creation timestamp.
 */
public class BubbleSortTasks {

    /**
     * Represents a task with a name, optional priority, and creation timestamp.
     */
    public static record Task(String name, Integer priority, long createdAt) {}

    /**
     * Holds the result of a bubble sort operation on tasks.
     */
    public static record SortResult(List<Task> tasks, int swapCount) {}

    /**
     * Sorts a list of tasks using the bubble sort algorithm.
     *
     * <p>Sorting rules:
     * <ol>
     *   <li>Primary: Priority descending (higher priority first)</li>
     *   <li>Tiebreaker: Creation timestamp ascending (earlier first)</li>
     *   <li>Null handling: Tasks with null priority are placed at the end,
     *       sorted by creation timestamp ascending among themselves</li>
     * </ol>
     *
     * @param tasks the list of tasks to sort
     * @return a SortResult containing the sorted list and the total number of swaps performed
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        // Create a new list to ensure the original input is not modified
        List<Task> sorted = new ArrayList<>(tasks);
        int swapCount = 0;
        boolean swapped;

        do {
            swapped = false;
            for (int i = 0; i < sorted.size() - 1; i++) {
                if (shouldSwap(sorted.get(i), sorted.get(i + 1))) {
                    // Manual swap to strictly avoid sorting utilities
                    Task temp = sorted.get(i);
                    sorted.set(i, sorted.get(i + 1));
                    sorted.set(i + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
        } while (swapped);

        return new SortResult(sorted, swapCount);
    }

    /**
     * Determines if task 'a' should be swapped with task 'b' (i.e., if 'a' should come after 'b').
     */
    private static boolean shouldSwap(Task a, Task b) {
        return compareTasks(a, b) > 0;
    }

    /**
     * Compares two tasks according to the sorting rules.
     * Returns negative if a should come before b, positive if a should come after b, zero if equal.
     */
    private static int compareTasks(Task a, Task b) {
        boolean aNull = a.priority == null;
        boolean bNull = b.priority == null;

        if (aNull && bNull) {
            return Long.compare(a.createdAt, b.createdAt);
        }
        if (aNull) {
            return 1; // a goes after b
        }
        if (bNull) {
            return -1; // a goes before b
        }

        // Both have priorities: sort descending by priority
        int priorityCmp = Integer.compare(b.priority, a.priority);
        if (priorityCmp != 0) {
            return priorityCmp;
        }

        // Priorities equal: sort ascending by createdAt
        return Long.compare(a.createdAt, b.createdAt);
    }
}
