import java.util.ArrayList;
import java.util.List;

/**
 * Represents a task with a name, priority (which may be null), and creation timestamp.
 */
public record Task(String name, Integer priority, long createdAt) {
    // No explicit constructor needed; the canonical constructor is generated.
}

/**
 * Holds the result of a bubble sort operation: the sorted list of tasks and the total number of swaps performed.
 */
public record SortResult(List<Task> tasks, int swapCount) {
    // No explicit constructor needed; the canonical constructor is generated.
}

public class BubbleSortTasks {

    /**
     * Sorts a list of tasks using the bubble sort algorithm according to the following rules:
     * <ol>
     *   <li>Primary key: priority descending (higher priority first).</li>
     *   <li>Tiebreaker: createdAt ascending (earlier timestamp first).</li>
     *   <li>Null priority: tasks with {@code null} priority are placed at the end of the list,
     *       ordered by createdAt ascending among themselves.</li>
     * </ol>
     *
     * The original list is not modified; a new sorted list is returned.
     *
     * @param tasks the list of tasks to sort; may be {@code null} or contain {@code null} elements
     * @return a {@link SortResult} containing the sorted list and the total number of swaps performed
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        // Defensive copy to avoid modifying the input list.
        List<Task> list = new ArrayList<>(tasks == null ? 0 : tasks.size());
        if (tasks != null) {
            list.addAll(tasks);
        }

        int n = list.size();
        int swapCount = 0;

        // Standard bubble sort for descending order.
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                Task a = list.get(j);
                Task b = list.get(j + 1);

                // If a should come after b, swap them.
                if (compare(a, b) < 0) {
                    list.set(j, b);
                    list.set(j + 1, a);
                    swapCount++;
                }
            }
        }

        return new SortResult(list, swapCount);
    }

    /**
     * Compares two tasks according to the sorting rules.
     *
     * @param a the first task
     * @param b the second task
     * @return a negative integer if {@code a} should come after {@code b},
     *         zero if they are equal in the sort order,
     *         a positive integer if {@code a} should come before {@code b}
     */
    private static int compare(Task a, Task b) {
        // Handle null priority cases.
        boolean aNull = a.priority() == null;
        boolean bNull = b.priority() == null;

        if (aNull && bNull) {
            // Both null: sort by createdAt ascending.
            return Long.compare(a.createdAt(), b.createdAt());
        } else if (aNull) {
            // a is null, b is not: a comes after b.
            return -1;
        } else if (bNull) {
            // b is null, a is not: a comes before b.
            return 1;
        }

        // Both priorities are non-null.
        int priorityComparison = b.priority().compareTo(a.priority()); // descending
        if (priorityComparison != 0) {
            return priorityComparison;
        }

        // Priorities equal: sort by createdAt ascending.
        return Long.compare(a.createdAt(), b.createdAt());
    }
}
