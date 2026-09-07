import java.util.ArrayList;
import java.util.List;

/**
 * Utility class for sorting task records using the bubble sort algorithm.
 */
public class BubbleSortTasks {

    /**
     * Immutable task record.
     *
     * @param name      human-readable task name
     * @param priority  nullable priority; higher values are more important
     * @param createdAt timestamp used as a tiebreaker
     */
    public static record Task(String name, Integer priority, long createdAt) {
    }

    /**
     * Result of sorting a list of tasks.
     *
     * @param tasks     newly created list containing the sorted tasks
     * @param swapCount total number of adjacent swaps performed during sorting
     */
    public static record SortResult(List<Task> tasks, int swapCount) {
    }

    /**
     * Sorts tasks by priority descending, then by createdAt ascending.
     * Tasks with a null priority are sorted to the end, ordered by createdAt ascending.
     *
     * @param tasks input list of tasks; if null, treated as an empty list
     * @return a new {@link SortResult} containing the sorted tasks and swap count
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        List<Task> sorted = tasks == null ? new ArrayList<>() : new ArrayList<>(tasks);
        int swapCount = bubbleSort(sorted);
        return new SortResult(sorted, swapCount);
    }

    /**
     * Performs an in-place bubble sort on the provided list.
     *
     * @param tasks list to sort
     * @return total number of swaps performed
     */
    private static int bubbleSort(List<Task> tasks) {
        int n = tasks.size();
        int swapCount = 0;

        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;

            for (int j = 0; j < n - i - 1; j++) {
                if (compareTasks(tasks.get(j), tasks.get(j + 1)) > 0) {
                    Task temp = tasks.get(j);
                    tasks.set(j, tasks.get(j + 1));
                    tasks.set(j + 1, temp);

                    swapCount++;
                    swapped = true;
                }
            }

            if (!swapped) {
                break;
            }
        }

        return swapCount;
    }

    /**
     * Compares two tasks according to the required ordering.
     *
     * @param a first task
     * @param b second task
     * @return negative if {@code a} should come before {@code b},
     *         zero if they are equivalent,
     *         positive if {@code a} should come after {@code b}
     */
    private static int compareTasks(Task a, Task b) {
        if (a == null && b == null) {
            return 0;
        }
        if (a == null) {
            return 1;
        }
        if (b == null) {
            return -1;
        }

        boolean aPriorityNull = a.priority() == null;
        boolean bPriorityNull = b.priority() == null;

        if (aPriorityNull && bPriorityNull) {
            return Long.compare(a.createdAt(), b.createdAt());
        }

        if (aPriorityNull) {
            return 1;
        }

        if (bPriorityNull) {
            return -1;
        }

        int priorityComparison = Integer.compare(b.priority(), a.priority());
        if (priorityComparison != 0) {
            return priorityComparison;
        }

        return Long.compare(a.createdAt(), b.createdAt());
    }
}
