import java.util.ArrayList;
import java.util.List;

/**
 * Provides a bubble‑sort implementation for task records.
 */
public class BubbleSortTasks {

    /**
     * Represents a task record with name, priority and creation timestamp.
     */
    public static class Task {
        public final String name;
        public final Integer priority;   // nullable
        public final long createdAt;

        public Task(String name, Integer priority, long createdAt) {
            this.name = name;
            this.priority = priority;
            this.createdAt = createdAt;
        }
    }

    /**
     * Holds the result of a bubble‑sort operation.
     */
    public static class SortResult {
        public final List<Task> tasks;
        public final int swapCount;

        public SortResult(List<Task> tasks, int swapCount) {
            this.tasks = tasks;
            this.swapCount = swapCount;
        }
    }

    /**
     * Sorts the given list of tasks using bubble sort according to the following rules:
     * <ul>
     *   <li>Primary: priority descending (higher priority first)</li>
     *   <li>Tie‑breaker: createdAt ascending</li>
     *   <li>Tasks with a null priority are placed at the end, ordered by createdAt ascending.</li>
     * </ul>
     *
     * @param tasks the list to sort (the original list is not modified)
     * @return a {@link SortResult} containing the sorted list and the total number of swaps performed
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        // Create a new list so the original input stays unchanged
        List<Task> sorted = new ArrayList<>(tasks);
        int n = sorted.size();
        int swapCount = 0;

        // Classic bubble sort
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                if (isOutOfOrder(sorted[j], sorted[j + 1])) {
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
     * Determines whether element {@code a} should be placed after element {@code b}
     * according to the sorting rules.
     *
     * @param a first element
     * @param b second element
     * @return {@code true} if {@code a} must come after {@code b}
     */
    private static boolean isOutOfOrder(Task a, Task b) {
        boolean aNull = a.priority == null;
        boolean bNull = b.priority == null;

        // Null‑priority tasks always go to the end
        if (aNull && !bNull) {
            return true;               // a should be after b
        }
        if (!aNull && bNull) {
            return false;              // a should be before b
        }

        // Both have non‑null priorities
        if (aNull && bNull) {
            // Both null: earlier createdAt first
            return a.createdAt > b.createdAt;
        }

        // Both have non‑null priorities: priority descending, then createdAt ascending
        int cmp = Integer.compare(b.priority, a.priority); // descending order
        if (cmp != 0) {
            return cmp > 0;            // if b's priority is larger, a is out of order
        }
        // Same priority → earlier createdAt first
        return a.createdAt > b.createdAt;
    }
}
