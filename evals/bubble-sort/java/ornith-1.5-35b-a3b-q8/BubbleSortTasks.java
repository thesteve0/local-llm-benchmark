import java.util.ArrayList;
import java.util.List;

/**
 * Implements a bubble sort for task records.
 *
 * <p>Tasks are ordered by:
 * <ol>
 *   <li><b>Priority</b> in descending order (higher priority first).</li>
 *   <li><b>Creation time</b> in ascending order as a tiebreaker when priorities are equal.</li>
 *   <li>Tasks with a {@code null} priority are always placed at the end of the list,
 *       ordered among themselves by creation time ascending.</li>
 * </ol>
 *
 * <p>The original input list is never modified; a new list is returned.
 */
public class BubbleSortTasks {

    /**
     * Represents a single task to be sorted.
     *
     * @param name      the task's name
     * @param priority  the task's priority, or {@code null} to indicate an unassigned
     *                  priority (such tasks sort to the end of the list)
     * @param createdAt the timestamp (in milliseconds) when the task was created
     */
    public record Task(String name, Integer priority, long createdAt) {
    }

    /**
     * The outcome of sorting a list of tasks.
     *
     * @param tasks     the sorted list of tasks
     * @param swapCount the total number of element swaps performed during sorting
     */
    public record SortResult(List<Task> tasks, int swapCount) {
    }

    /**
     * Sorts the given tasks using the bubble sort algorithm.
     *
     * <p>The comparison rules are:
     * <ol>
     *   <li>Higher {@link Task#priority()} comes first (descending).</li>
     *   <li>When priorities are equal, earlier {@link Task#createdAt()} comes first (ascending).</li>
     *   <li>Tasks with a {@code null} priority always sort to the end, ordered by
     *       {@code createdAt} ascending among themselves.</li>
     * </ol>
     *
     * @param tasks the tasks to sort; may be {@code null} or empty
     * @return a {@link SortResult} containing the sorted tasks and the number of swaps performed
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        // Work on a copy so the caller's list is never mutated.
        List<Task> sorted = (tasks == null)
                ? new ArrayList<>()
                : new ArrayList<>(tasks);

        int swapCount = 0;
        int n = sorted.size();

        // Standard bubble sort with an early-exit optimization: if a full pass
        // performs no swaps, the list is already sorted and we can stop.
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                if (compare(sorted.get(j), sorted.get(j + 1)) > 0) {
                    swap(sorted, j, j + 1);
                    swapCount++;
                    swapped = true;
                }
            }
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sorted, swapCount);
    }

    /**
     * Compares two tasks according to the sorting rules.
     *
     * @return a negative value if {@code a} should come before {@code b},
     *         a positive value if {@code a} should come after {@code b},
     *         or {@code 0} if they are considered equal in ordering
     */
    private static int compare(Task a, Task b) {
        // Null priorities always sort to the end.
        if (a.priority == null && b.priority == null) {
            return Long.compare(a.createdAt, b.createdAt);
        }
        if (a.priority == null) {
            return 1; // a is null → a comes after b
        }
        if (b.priority == null) {
            return -1; // b is null → a comes before b
        }

        // Both have priorities: higher priority first (descending).
        int priorityCompare = Integer.compare(b.priority, a.priority);
        if (priorityCompare != 0) {
            return priorityCompare;
        }

        // Equal priority: earlier creation time first (ascending).
        return Long.compare(a.createdAt, b.createdAt);
    }

    /**
     * Swaps the elements at the two given indices in place.
     */
    private static void swap(List<Task> list, int i, int j) {
        Task temp = list.get(i);
        list.set(i, list.get(j));
        list.set(j, temp);
    }

    /**
     * Demonstrates the sort using the documented example.
     */
    public static void main(String[] args) {
        List<Task> tasks = List.of(
                new Task("bug",     3, 1000),
                new Task("feature", 5, 2000),
                new Task("docs",    3, 500)
        );

        SortResult result = bubbleSortTasks(tasks);

        System.out.println("Sorted tasks:");
        for (Task task : result.tasks()) {
            System.out.println("  " + task);
        }
        System.out.println("Swap count: " + result.swapCount());
    }
}
