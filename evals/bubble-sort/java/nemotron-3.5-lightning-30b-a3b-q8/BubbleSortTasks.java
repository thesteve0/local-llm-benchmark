import java.util.ArrayList;
import java.util.List;

/**
 * Utility class that provides a bubble sort implementation for task records.
 */
public class BubbleSortTasks {

    /**
     * A task record with a name, optional priority, and creation timestamp.
     */
    public static record Task(String name, Integer priority, long createdAt) {}

    /**
     * Result returned by {@link #bubbleSortTasks(List)}, containing the sorted tasks
     * and the total number of swaps performed.
     */
    public static record SortResult(List<Task> tasks, int swapCount) {}

    /**
     * Sorts the given list of tasks using the bubble sort algorithm.
     * <p>
     * Sorting rules:
     * <ul>
     *   <li>Primary: {@code priority} descending (higher first)</li>
     *   <li>Tiebreaker: equal {@code priority} → {@code createdAt} ascending (earlier first)</li>
     *   <li>Null {@code priority} always sorts to the end, ordered by {@code createdAt} ascending among themselves</li>
     * </ul>
     * </p>
     * The original input list is never modified; a fresh copy is sorted and returned.
     *
     * @param tasks the list of tasks to sort
     * @return a {@link SortResult} with the sorted list and total swap count
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        // Work on a copy so the original list stays untouched
        List<Task> sorted = new ArrayList<>(tasks);
        int n = sorted.size();
        int swapCount = 0;

        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            // After each pass, the "heaviest" (i.e. last in our order) element bubbles to the end
            for (int j = 0; j < n - 1 - i; j++) {
                if (shouldSwap(sorted.get(j), sorted.get(j + 1))) {
                    Task temp = sorted.get(j);
                    sorted.set(j, sorted.get(j + 1));
                    sorted.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // Early exit if the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sorted, swapCount);
    }

    /**
     * Determines whether two tasks are in the wrong order according to the sorting rules.
     * Returns {@code true} if the left task should move right (i.e. a swap is needed).
     */
    private static boolean shouldSwap(Task a, Task b) {
        boolean aNull = a.priority() == null;
        boolean bNull = b.priority() == null;

        // Both have a non-null priority
        if (!aNull && !bNull) {
            // Higher priority comes first → swap if a's priority is lower
            if (a.priority() != b.priority()) {
                return a.priority() < b.priority();
            }
            // Equal priority → earlier timestamp comes first → swap if a is newer
            return a.createdAt() > b.createdAt();
        }

        // a has null priority, b does not → b must come first → swap
        if (aNull && !bNull) {
            return true;
        }

        // a has priority, b has null → a must come first → no swap
        if (!aNull && bNull) {
            return false;
        }

        // Both have null priority → sort by createdAt ascending → swap if a is newer
        return a.createdAt() > b.createdAt();
    }

    // Optional: simple main for manual verification during development
    public static void main(String[] args) {
        List<Task> tasks = List.of(
            new Task("bug",     3, 1000L),
            new Task("feature", 5, 2000L),
            new Task("docs",    3, 500L)
        );

        SortResult result = bubbleSortTasks(tasks);
        System.out.println("Sorted: " + result.tasks());
        System.out.println("Swaps : " + result.swapCount());
        // Expected: [Task(feature,5,2000), Task(docs,3,500), Task(bug,3,1000)], swaps=2
    }
}
