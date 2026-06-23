import java.util.ArrayList;
import java.util.List;

public class BubbleSortTasks {

    public record Task(String name, Integer priority, long createdAt) {}

    public record SortResult(List<Task> tasks, int swapCount) {}

    public static SortResult bubbleSortTasks(List<Task> tasks) {
        List<Task> working = new ArrayList<>(tasks);
        int n = working.size();
        int swapCount = 0;

        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (shouldSwap(working.get(j), working.get(j + 1))) {
                    Task temp = working.get(j);
                    working.set(j, working.get(j + 1));
                    working.set(j + 1, temp);
                    swapCount++;
                }
            }
        }

        return new SortResult(working, swapCount);
    }

    private static boolean shouldSwap(Task a, Task b) {
        Integer aPri = a.priority();
        Integer bPri = b.priority();

        if (aPri == null && bPri == null) {
            return a.createdAt() > b.createdAt();
        }
        if (aPri == null) return true;
        if (bPri == null) return false;

        if (!aPri.equals(bPri)) {
            return aPri < bPri;
        }
        return a.createdAt() > b.createdAt();
    }
}
