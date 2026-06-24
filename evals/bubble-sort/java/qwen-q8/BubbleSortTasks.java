import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Provides a bubble sort implementation for sorting Task records based on
 * priority and creation timestamp.
 */
public class BubbleSortTasks {

    /**
     * Represents a task with a name, optional priority, and creation timestamp.
     *
     * @param name       the name of the task
     * @param priority   the priority level (null tasks sort to the end)
     * @param createdAt  the timestamp when the task was created
     */
    public static record Task(String name, Integer priority, long createdAt) {}

    /**
     * Holds the result of a sorting operation, including the sorted list and swap count.
     *
     * @param tasks      the sorted list of tasks
     * @param swapCount  the total number of swaps performed during sorting
     */
    public static record SortResult(List<Task> tasks, int swapCount) {}

    /**
     * Sorts a list of tasks using the bubble sort algorithm.
     *
     * <p>Sorting rules:
     * <ol>
     *   <li>Primary: Priority descending (higher priority first)</li>
     *   <li>Tiebreaker: Creation timestamp ascending (earlier first)</li>
     *   <li>Null priorities always sort to the end, ordered by timestamp ascending</li>
     * </ol>
     *
     * @param tasks the list of tasks to sort
     * @return a SortResult containing the sorted list and the total number of swaps performed
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null || tasks.isEmpty()) {
            return new SortResult(Collections.emptyList(), 0);
        }

        // Create a mutable copy to ensure the original list is never modified
        List<Task> sortedTasks = new ArrayList<>(tasks);
        int swapCount = 0;
        int n = sortedTasks.size();

        // Standard bubble sort with early-exit optimization
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                // If adjacent elements are out of order, swap them
                if (compareTasks(sortedTasks.get(j), sortedTasks.get(j + 1)) > 0) {
                    Task temp = sortedTasks.get(j);
                    sortedTasks.set(j, sortedTasks.get(j + 1));
                    sortedTasks.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // If no swaps occurred in a pass, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sortedTasks, swapCount);
    }

    /**
     * Compares two tasks to determine their relative order for sorting.
     *
     * @return positive if t1 should come after t2, negative if before, zero if equal
     */
    private static int compareTasks(Task t1, Task t2) {
        boolean p1Null = t1.priority() == null;
        boolean p2Null = t2.priority() == null;

        // Both have null priority: sort by createdAt ascending
        if (p1Null && p2Null) {
            return Long.compare(t1.createdAt(), t2.createdAt());
        }
        // t1 has null priority, t2 does not: t1 goes after t2
        if (p1Null) {
            return 1;
        }
        // t2 has null priority, t1 does not: t1 goes before t2
        if (p2Null) {
            return -1;
        }

        // Both have non-null priorities: sort descending
        int priorityCmp = Integer.compare(t2.priority(), t1.priority());
        if (priorityCmp != 0) {
            return priorityCmp;
        }

        // Priorities are equal: sort by createdAt ascending
        return Long.compare(t1.createdAt(), t2.createdAt());
    }
}
