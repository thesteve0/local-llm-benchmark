import java.util.ArrayList;
import java.util.List;

/**
 * Utility class that provides a bubble sort implementation for task records.
 * Sorting follows priority descending, createdAt ascending tie-breaking,
 * and null-priority tasks always move to the end.
 */
public class BubbleSortTasks {

    /**
     * Represents a task with a name, optional priority, and creation timestamp.
     */
    public static record Task(String name, Integer priority, long createdAt) {}

    /**
     * Result returned by {@link #bubbleSortTasks(List)}, containing the sorted
     * task list and the total number of swaps performed.
     */
    public static record SortResult(List<Task> tasks, int swapCount) {}

    /**
     * Sorts the given list of tasks using the bubble sort algorithm.
     * <p>
     * Sorting order:
     * <ul>
     *   <li>Primary: {@code priority} descending (higher values first)</li>
     *   <li>Tiebreaker: {@code createdAt} ascending (earlier timestamps first) when priorities are equal</li>
     *   <li>Null priority: always placed at the end of the list, ordered by {@code createdAt} ascending among themselves</li>
     * </ul>
     * </p>
     * The original input list is <strong>not</strong> modified; a new sorted list is returned.
     *
     * @param tasks the list of tasks to sort; may be empty but must not be {@code null} in normal use
     * @return a {@link SortResult} containing the sorted list and the total swap count
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null || tasks.isEmpty()) {
            return new SortResult(List.of(), 0);
        }

        // Work on a fresh copy so the original list stays untouched
        List<Task> sorted = new ArrayList<>(tasks);
        int n = sorted.size();
        int swapCount = 0;

        boolean swapped;
        for (int i = 0; i < n - 1; i++) {
            swapped = false;
            // After each pass, the largest (according to our order) element "bubbles" to its final position
            for (int j = 0; j < n - 1 - i; j++) {
                Task current = sorted.get(j);
                Task next = sorted.get(j + 1);

                if (shouldSwap(current, next)) {
                    // Manual swap – no sorting utilities used
                    Task temp = current;
                    sorted.set(j, next);
                    sorted.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // If no swaps occurred in a full pass, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sorted, swapCount);
    }

    /**
     * Determines whether two adjacent tasks are in the wrong order and should be swapped.
     *
     * @param a the left task
     * @param b the right task
     * @return {@code true} if {@code a} and {@code b} violate the desired sort order
     */
    private static boolean shouldSwap(Task a, Task b) {
        // Both priorities are null → order by createdAt ascending
        if (a.priority == null && b.priority == null) {
            return a.createdAt > b.createdAt;
        }
        // a has null priority, b does not → a must move to the end
        if (a.priority == null && b.priority != null) {
            return true;
        }
        // a has a value, b is null → a stays before b
        if (a.priority != null && b.priority == null) {
            return false;
        }

        // Both priorities are non-null
        // Higher priority should come first → swap if a's priority is lower
        if (a.priority < b.priority) {
            return true;
        }
        if (a.priority > b.priority) {
            return false;
        }

        // Priorities equal → order by createdAt ascending
        return a.createdAt > b.createdAt;
    }

    // ----------------------------------------------------------------------
    // Optional simple main for manual verification
    // ----------------------------------------------------------------------
    public static void main(String[] args) {
        List<Task> tasks = List.of(
            new Task("bug",     3, 1000L),
            new Task("feature", 5, 2000L),
            new Task("docs",    3, 500L)
        );

        SortResult result = bubbleSortTasks(tasks);

        System.out.println("Sorted tasks: " + result.tasks());
        System.out.println("Swap count:   " + result.swapCount());
        System.out.println("Original list unchanged: " + tasks);
    }
}
