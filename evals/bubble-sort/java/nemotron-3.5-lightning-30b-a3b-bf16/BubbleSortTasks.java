import java.util.ArrayList;
import java.util.List;

/**
 * Utility class that provides a bubble sort implementation for task records.
 * Sorting follows the rules: priority descending, createdAt ascending as tiebreaker,
 * and null priorities always move to the end (ordered by createdAt ascending).
 */
public class BubbleSortTasks {

    /**
     * An immutable record representing a task.
     */
    public record Task(String name, Integer priority, long createdAt) {}

    /**
     * An immutable result container holding the sorted task list and the total
     * number of swaps performed during the bubble sort.
     */
    public record SortResult(List<Task> tasks, int swapCount) {}

    /**
     * Sorts a list of tasks using the bubble sort algorithm.
     *
     * @param tasks the list of tasks to sort; original list is not modified
     * @return a SortResult containing the sorted list and the total swap count
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        // Work on a shallow copy so the original list remains untouched
        List<Task> sorted = new ArrayList<>(tasks);
        int n = sorted.size();
        int swapCount = 0;

        for (int i = 0; i < n; i++) {
            // After each pass, the largest (according to our ordering) element
            // "bubbles up" to its correct position at the end.
            for (int j = 0; j < n - i - 1; j++) {
                Task current = sorted.get(j);
                Task next = sorted.get(j + 1);

                // Swap if current should come after next
                if (shouldSwap(current, next)) {
                    sorted.set(j, next);
                    sorted.set(j + 1, current);
                    swapCount++;
                }
            }
        }

        return new SortResult(sorted, swapCount);
    }

    /**
     * Determines whether two adjacent tasks are in the wrong order (i.e., the
     * left task should come after the right task according to the sorting rules).
     *
     * @param a the left task
     * @param b the right task
     * @return true if {@code a} should be placed after {@code b}, false otherwise
     */
    private static boolean shouldSwap(Task a, Task b) {
        // Both have null priority → order by createdAt ascending
        if (a.priority() == null && b.priority() == null) {
            return a.createdAt() > b.createdAt(); // swap if a's timestamp is later
        }
        // a has null priority, b does not → a must go to the end
        if (a.priority() == null && b.priority() != null) {
            return true;
        }
        // b has null priority, a does not → a stays before b
        if (a.priority() != null && b.priority() == null) {
            return false;
        }

        // Both have non-null priority
        // 1. Higher priority first (descending)
        if (a.priority() != b.priority()) {
            return a.priority() < b.priority(); // swap if a's priority is lower
        }
        // 2. Equal priority → earlier timestamp first (ascending)
        return a.createdAt() > b.createdAt(); // swap if a's timestamp is later
    }

    // -----------------------------------------------------------------------
    // Optional: simple self-test / demonstration
    // -----------------------------------------------------------------------
    public static void main(String[] args) {
        List<Task> tasks = List.of(
            new Task("bug",     3, 1000L),
            new Task("feature", 5, 2000L),
            new Task("docs",    3, 500L)
        );

        SortResult result = bubbleSortTasks(tasks);

        System.out.println("Sorted tasks:");
        result.tasks().forEach(t -> System.out.println("  " + t));

        System.out.println("Swap count: " + result.swapCount());
        // Expected: [feature(5,2000), docs(3,500), bug(3,1000)], swaps = 2
    }
}
