import java.util.ArrayList;
import java.util.List;

public class BubbleSortTasks {

    public static record Task(String name, Integer priority, long createdAt) {}

    public static record SortResult(List<Task> tasks, int swapCount) {}

    /**
     * Bubble sorts a list of tasks without modifying the input.
     * Primary: priority descending, nulls last
     * Tiebreaker: createdAt ascending
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null) {
            return new SortResult(List.of(), 0);
        }

        List<Task> sorted = new ArrayList<>(tasks);
        int n = sorted.size();
        int swapCount = 0;

        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                Task a = sorted.get(j);
                Task b = sorted.get(j + 1);
                if (compare(a, b) > 0) {
                    sorted.set(j, b);
                    sorted.set(j + 1, a);
                    swapCount++;
                    swapped = true;
                }
            }
            if (!swapped) break;
        }

        return new SortResult(sorted, swapCount);
    }

    private static int compare(Task a, Task b) {
        Integer pa = a.priority();
        Integer pb = b.priority();

        if (pa == null && pb == null) {
            return Long.compare(a.createdAt(), b.createdAt());
        }
        if (pa == null) return 1;   // nulls go to end
        if (pb == null) return -1;

        int priCmp = pb.compareTo(pa); // descending
        if (priCmp != 0) return priCmp;
        return Long.compare(a.createdAt(), b.createdAt()); // ascending
    }
}
