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