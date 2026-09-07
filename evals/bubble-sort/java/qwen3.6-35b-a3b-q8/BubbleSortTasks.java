import java.util.ArrayList;
import java.util.List;

/**
 * Provides a bubble sort implementation for sorting task records
 * based on priority and creation timestamp.
 */
public class BubbleSortTasks {

    /**
     * Represents a task with a name, optional priority, and creation timestamp.
     *
     * @param name       the name of the task
     * @param priority   the priority level (null tasks are sorted to the end)
     * @param createdAt  the timestamp when the task was created
     */
    public static record Task(String name, Integer priority, long createdAt) {}

    /**
     * Holds the result of a bubble sort operation on tasks.
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
     *   <li>Tiebreaker: Creation timestamp ascending (earlier timestamp first)</li>
     *   <li>Null handling: Tasks with {@code null} priority are sorted to the end,
     *       ordered by {@code createdAt} ascending among themselves</li>
     * </ol>
     *
     * @param tasks the list of tasks to sort
     * @return a {@link SortResult} containing the sorted list and the total number of swaps performed
     * @throws IllegalArgumentException if the input list is null
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null) {
            throw new IllegalArgumentException("Input list cannot be null");
        }
        if (tasks.isEmpty()) {
            return new SortResult(new ArrayList<>(), 0);
        }

        // Create a new list to avoid modifying the original input
        List<Task> sortedTasks = new ArrayList<>(tasks);
        int swapCount = 0;
        int n = sortedTasks.size();

        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                if (compareTasks(sortedTasks.get(j), sortedTasks.get(j + 1)) > 0) {
                    // Swap adjacent elements
                    Task temp = sortedTasks.get(j);
                    sortedTasks.set(j, sortedTasks.get(j + 1));
                    sortedTasks.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // If no swaps occurred in this pass, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sortedTasks, swapCount);
    }

    /**
     * Compares two tasks according to the defined sorting rules.
     *
     * @param a the first task
     * @param b the second task
     * @return negative if {@code a} should precede {@code b}, positive if {@code a} should follow {@code b},
     *         or zero if they are considered equal in order
     */
    private static int compareTasks(Task a, Task b) {
        boolean aNull = a.priority == null;
        boolean bNull = b.priority == null;

        // Both have null priorities: sort by createdAt ascending
        if (aNull && bNull) {
            return Long.compare(a.createdAt, b.createdAt);
        }
        // Only a has null priority: a goes after b
        if (aNull) {
            return 1;
        }
        // Only b has null priority: a goes before b
        if (bNull) {
            return -1;
        }

        // Both have non-null priorities: sort by priority descending
        int priorityCompare = Integer.compare(b.priority, a.priority);
        if (priorityCompare != 0) {
            return priorityCompare;
        }

        // Priorities are equal: sort by createdAt ascending
        return Long.compare(a.createdAt, b.createdAt);
    }
}
