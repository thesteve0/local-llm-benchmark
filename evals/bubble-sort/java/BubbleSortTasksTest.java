import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class BubbleSortTasksTest {

    static int passed = 0;
    static int failed = 0;

    static void check(String testName, boolean condition, String detail) {
        if (condition) {
            System.out.println("  PASS: " + testName);
            passed++;
        } else {
            System.out.println("  FAIL: " + testName + " — " + detail);
            failed++;
        }
    }

    static List<String> names(List<BubbleSortTasks.Task> tasks) {
        List<String> result = new ArrayList<>();
        for (BubbleSortTasks.Task t : tasks) {
            result.add(t.name());
        }
        return result;
    }

    static List<Integer> priorities(List<BubbleSortTasks.Task> tasks) {
        List<Integer> result = new ArrayList<>();
        for (BubbleSortTasks.Task t : tasks) {
            result.add(t.priority());
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println("Bubble Sort Tasks — Java Test Suite\n");

        // Test 1: empty list
        System.out.println("test_empty_list");
        {
            BubbleSortTasks.SortResult r = BubbleSortTasks.bubbleSortTasks(List.of());
            check("result is empty", r.tasks().isEmpty(), "expected empty list");
            check("swap count is 0", r.swapCount() == 0, "expected 0, got " + r.swapCount());
        }

        // Test 2: single element
        System.out.println("test_single_element");
        {
            List<BubbleSortTasks.Task> input = List.of(new BubbleSortTasks.Task("only", 5, 100));
            BubbleSortTasks.SortResult r = BubbleSortTasks.bubbleSortTasks(input);
            check("single element returned", r.tasks().size() == 1 && r.tasks().get(0).name().equals("only"),
                  "expected [only]");
            check("swap count is 0", r.swapCount() == 0, "expected 0, got " + r.swapCount());
        }

        // Test 3: already sorted
        System.out.println("test_already_sorted");
        {
            List<BubbleSortTasks.Task> input = List.of(
                new BubbleSortTasks.Task("high", 5, 100),
                new BubbleSortTasks.Task("mid", 3, 200),
                new BubbleSortTasks.Task("low", 1, 300)
            );
            BubbleSortTasks.SortResult r = BubbleSortTasks.bubbleSortTasks(input);
            check("order correct", names(r.tasks()).equals(List.of("high", "mid", "low")),
                  "got " + names(r.tasks()));
            check("swap count is 0", r.swapCount() == 0, "expected 0, got " + r.swapCount());
        }

        // Test 4: reverse sorted
        System.out.println("test_reverse_sorted");
        {
            List<BubbleSortTasks.Task> input = List.of(
                new BubbleSortTasks.Task("low", 1, 300),
                new BubbleSortTasks.Task("mid", 3, 200),
                new BubbleSortTasks.Task("high", 5, 100)
            );
            BubbleSortTasks.SortResult r = BubbleSortTasks.bubbleSortTasks(input);
            check("order correct", names(r.tasks()).equals(List.of("high", "mid", "low")),
                  "got " + names(r.tasks()));
            check("swap count is 3", r.swapCount() == 3, "expected 3, got " + r.swapCount());
        }

        // Test 5: tiebreaker by createdAt
        System.out.println("test_tiebreaker_by_created_at");
        {
            List<BubbleSortTasks.Task> input = List.of(
                new BubbleSortTasks.Task("later", 5, 200),
                new BubbleSortTasks.Task("earlier", 5, 100)
            );
            BubbleSortTasks.SortResult r = BubbleSortTasks.bubbleSortTasks(input);
            check("order correct", names(r.tasks()).equals(List.of("earlier", "later")),
                  "got " + names(r.tasks()));
            check("swap count is 1", r.swapCount() == 1, "expected 1, got " + r.swapCount());
        }

        // Test 6: null priority sorts to end
        System.out.println("test_null_priority_sorts_to_end");
        {
            List<BubbleSortTasks.Task> input = List.of(
                new BubbleSortTasks.Task("none", null, 100),
                new BubbleSortTasks.Task("high", 5, 200),
                new BubbleSortTasks.Task("mid", 3, 300)
            );
            BubbleSortTasks.SortResult r = BubbleSortTasks.bubbleSortTasks(input);
            check("order correct", names(r.tasks()).equals(List.of("high", "mid", "none")),
                  "got " + names(r.tasks()));
            check("swap count is 2", r.swapCount() == 2, "expected 2, got " + r.swapCount());
        }

        // Test 7: multiple null priorities
        System.out.println("test_multiple_null_priorities");
        {
            List<BubbleSortTasks.Task> input = List.of(
                new BubbleSortTasks.Task("later_null", null, 400),
                new BubbleSortTasks.Task("earlier_null", null, 50)
            );
            BubbleSortTasks.SortResult r = BubbleSortTasks.bubbleSortTasks(input);
            check("order correct", names(r.tasks()).equals(List.of("earlier_null", "later_null")),
                  "got " + names(r.tasks()));
            check("swap count is 1", r.swapCount() == 1, "expected 1, got " + r.swapCount());
        }

        // Test 8: mixed comprehensive
        System.out.println("test_mixed_comprehensive");
        {
            List<BubbleSortTasks.Task> input = List.of(
                new BubbleSortTasks.Task("d", null, 400),
                new BubbleSortTasks.Task("a", 5, 100),
                new BubbleSortTasks.Task("c", 3, 300),
                new BubbleSortTasks.Task("b", 5, 200),
                new BubbleSortTasks.Task("e", null, 50)
            );
            BubbleSortTasks.SortResult r = BubbleSortTasks.bubbleSortTasks(input);
            check("order correct", names(r.tasks()).equals(List.of("a", "b", "c", "e", "d")),
                  "got " + names(r.tasks()));
            check("priorities correct", priorities(r.tasks()).equals(Arrays.asList(5, 5, 3, null, null)),
                  "got " + priorities(r.tasks()));
            check("swap count is 5", r.swapCount() == 5, "expected 5, got " + r.swapCount());
        }

        // Test 9: all same priority
        System.out.println("test_all_same_priority");
        {
            List<BubbleSortTasks.Task> input = List.of(
                new BubbleSortTasks.Task("c", 3, 300),
                new BubbleSortTasks.Task("a", 3, 100),
                new BubbleSortTasks.Task("b", 3, 200)
            );
            BubbleSortTasks.SortResult r = BubbleSortTasks.bubbleSortTasks(input);
            check("order correct", names(r.tasks()).equals(List.of("a", "b", "c")),
                  "got " + names(r.tasks()));
            check("swap count is 2", r.swapCount() == 2, "expected 2, got " + r.swapCount());
        }

        // Test 10: null sorts after lowest priority
        System.out.println("test_null_sorts_after_lowest_priority");
        {
            List<BubbleSortTasks.Task> input = List.of(
                new BubbleSortTasks.Task("none", null, 100),
                new BubbleSortTasks.Task("lowest", 1, 200)
            );
            BubbleSortTasks.SortResult r = BubbleSortTasks.bubbleSortTasks(input);
            check("order correct", names(r.tasks()).equals(List.of("lowest", "none")),
                  "got " + names(r.tasks()));
            check("swap count is 1", r.swapCount() == 1, "expected 1, got " + r.swapCount());
        }

        // Test 11: input not modified
        System.out.println("test_input_not_modified");
        {
            List<BubbleSortTasks.Task> input = new ArrayList<>(List.of(
                new BubbleSortTasks.Task("low", 1, 300),
                new BubbleSortTasks.Task("high", 5, 100)
            ));
            List<BubbleSortTasks.Task> original = new ArrayList<>(input);
            BubbleSortTasks.bubbleSortTasks(input);
            check("input unchanged", input.equals(original),
                  "input list was modified");
        }

        // Summary
        System.out.println("\n========================================");
        System.out.printf("Results: %d passed, %d failed, %d total%n", passed, failed, passed + failed);
        System.out.println("========================================");
        if (failed > 0) {
            System.exit(1);
        }
    }
}
