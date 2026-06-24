import java.util.ArrayList;
import java.util.List;

public class BubbleSortTasks {

    /**
     * Represents a task with a name, optional priority, and creation timestamp.
     */
    public static record Task(String name, Integer priority, long createdAt) {}

    /**
     * Represents the result of a bubble sort operation on tasks.
     */
    public static record SortResult(List<Task> tasks, int swapCount) {}

    /**
     * Sorts a list of tasks using the bubble sort algorithm.
     *
     * <p>Sorting rules:
     * <ol>
     *   <li>Primary: {@code priority} descending (higher priority first)</li>
     *   <li>Tiebreaker: {@code createdAt} ascending (earlier timestamp first)</li>
     *   <li>Null handling: tasks with {@code null} priority sort to the end, 
     *       ordered by {@code createdAt} ascending among themselves</li>
     * </ol>
     *
     * @param tasks the list of tasks to sort
     * @return a {@link SortResult} containing the sorted list and the total number of swaps performed
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null || tasks.isEmpty()) {
            return new SortResult(new ArrayList<>(), 0);
        }

        // Create a mutable copy to strictly avoid modifying the original input list
        List<Task> sortedTasks = new ArrayList<>(tasks);
        int swapCount = 0;
        boolean swapped;

        for (int i = 0; i < sortedTasks.size() - 1; i++) {
            swapped = false;
            for (int j = 0; j < sortedTasks.size() - 1 - i; j++) {
                Task current = sortedTasks.get(j);
                Task next = sortedTasks.get(j + 1);

                if (shouldSwap(current, next)) {
                    // Swap adjacent elements
                    sortedTasks.set(j, next);
                    sortedTasks.set(j + 1, current);
                    swapCount++;
                    swapped = true;
                }
            }
            // Optimization: if no swaps occurred in a pass, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sortedTasks, swapCount);
    }

    /**
     * Determines if the first task should be swapped with the second task
     * based on the specified sorting rules.
     *
     * @param a the first task
     * @param b the second task
     * @return true if {@code a} should come after {@code b} (triggering a swap), false otherwise
     */
    private static boolean shouldSwap(Task a, Task b) {
        boolean aNull = a.priority == null;
        boolean bNull = b.priority == null;

        if (aNull && bNull) {
            // Both null: ascending createdAt
            return a.createdAt > b.createdAt;
        }
        if (aNull) {
            // a is null, b is not: a should come after b
            return true;
        }
        if (bNull) {
            // b is null, a is not: a should come before b
            return false;
        }

        // Both non-null: descending priority
        int priorityCmp = Integer.compare(b.priority, a.priority);
        if (priorityCmp != 0) {
            return priorityCmp > 0; // a has lower priority, so swap
        }

        // Equal priority: ascending createdAt
        return a.createdAt > b.createdAt;
    }
}
