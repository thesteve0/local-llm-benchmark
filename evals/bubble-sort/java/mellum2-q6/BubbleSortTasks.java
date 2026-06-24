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
