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
     *   <li>Null priorities are sorted to the end, ordered by timestamp ascending</li>
     * </ol>
     *
     * @param tasks the list of tasks to sort
     * @return a {@link SortResult} containing the sorted list and the total number of swaps
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null || tasks.isEmpty()) {
            return new SortResult(List.of(), 0);
        }

        // Create a mutable copy to ensure the original list is not modified
        List<Task> sorted = new ArrayList<>(tasks);
        int swapCount = 0;
        boolean swapped;

        for (int i = 0; i < sorted.size() - 1; i++) {
            swapped = false;
            for (int j = 0; j < sorted.size() - 1 - i; j++) {
                if (compareTasks(sorted.get(j), sorted.get(j + 1)) > 0) {
                    // Swap adjacent elements
                    Task temp = sorted.get(j);
                    sorted.set(j, sorted.get(j + 1));
                    sorted.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // If no swaps occurred, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sorted, swapCount);
    }

    /**
     * Compares two tasks according to the sorting rules.
     *
     * @param a the first task
     * @param b the second task
     * @return negative if a should come before b, positive if a should come after b, zero if equal
     */
    private static int compareTasks(Task a, Task b) {
        boolean aNull = a.priority == null;
        boolean bNull = b.priority == null;

        // Both have null priorities: sort by createdAt ascending
        if (aNull && bNull) {
            return Long.compare(a.createdAt, b.createdAt);
        }
        // a has null priority, b does not: a goes after b
        if (aNull) {
            return 1;
        }
        // b has null priority, a does not: a goes before b
        if (bNull) {
            return -1;
        }

        // Both have priorities: sort by priority descending
        int priorityCompare = Integer.compare(b.priority, a.priority);
        if (priorityCompare != 0) {
            return priorityCompare;
        }

        // Priorities are equal: sort by createdAt ascending
        return Long.compare(a.createdAt, b.createdAt);
    }
}
