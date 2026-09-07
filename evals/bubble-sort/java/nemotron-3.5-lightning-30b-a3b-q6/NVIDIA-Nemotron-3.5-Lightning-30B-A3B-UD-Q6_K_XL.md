# Code Eval: NVIDIA-Nemotron-3.5-Lightning-30B-A3B-UD-Q6_K_XL

## Prompt

# Bubble Sort Tasks — Java

Implement a bubble sort function for task records.

## Requirements

Write a single file `BubbleSortTasks.java` containing a public class `BubbleSortTasks` with:

1. A **static inner** `Task` record with fields:
   - `String name`
   - `Integer priority` (nullable — use `Integer`, not `int`)
   - `long createdAt`

2. A **static inner** `SortResult` record with fields:
   - `List<Task> tasks` — the sorted list
   - `int swapCount` — total swaps performed

3. A static method:
   ```java
   public static SortResult bubbleSortTasks(List<Task> tasks)
   ```

### Sorting Rules

1. **Primary:** sort by `priority` descending (higher priority comes first)
2. **Tiebreaker:** when priorities are equal, sort by `createdAt` ascending (earlier timestamp comes first)
3. **Null handling:** tasks where `priority` is `null` always sort to the end of the list, ordered by `createdAt` ascending among themselves

### Constraints

- You must implement the bubble sort algorithm — do not use `Collections.sort()`, `Arrays.sort()`, `List.sort()`, or any other sorting utility
- Return a `SortResult` with the sorted list and total swap count
- Do not modify the original input list — return a new list

### Example

```java
List<BubbleSortTasks.Task> tasks = List.of(
    new BubbleSortTasks.Task("bug",     3, 1000),
    new BubbleSortTasks.Task("feature", 5, 2000),
    new BubbleSortTasks.Task("docs",    3, 500)
);

BubbleSortTasks.SortResult result = BubbleSortTasks.bubbleSortTasks(tasks);
// result.tasks() = [Task("feature",5,2000), Task("docs",3,500), Task("bug",3,1000)]
// result.swapCount() = 2
```

Write clean, well-documented, idiomatic Java code. Use Javadoc where appropriate.


## Reasoning

Here's a thinking process:

1.  **Analyze the User's Request:**
   - Need to implement a `BubbleSortTasks.java` file
   - Public class `BubbleSortTasks`
   - Static inner `Task` record with `String name`, `Integer priority`, `long createdAt`
   - Static inner `SortResult` record with `List<Task> tasks`, `int swapCount`
   - Static method `bubbleSortTasks(List<Task> tasks)` returning `SortResult`
   - Sorting rules:
     - Primary: priority descending (higher first)
     - Tiebreaker: createdAt ascending (earlier first) when priorities equal
     - Null handling: null priority always to end, ordered by createdAt ascending among themselves
   - Constraints:
     - Must implement bubble sort algorithm (no Collections.sort, etc.)
     - Return SortResult with sorted list and swap count
     - Do not modify original input list - return a new list
   - Example provided to verify correctness
   - Clean, well-documented, idiomatic Java, Javadoc

2.  **Deconstruct the Sorting Logic:**
   - Need to compare two tasks based on the rules.
   - Let's define a comparison logic that returns negative, zero, positive, but since we're doing bubble sort swaps, we need to know when to swap.
   - Bubble sort typically compares adjacent elements and swaps if they are in the wrong order.
   - "Wrong order" based on rules:
     - If both have non-null priority: higher priority should come first -> if a.priority < b.priority, swap (descending)
     - If priorities equal: earlier createdAt comes first -> if a.createdAt > b.createdAt, swap (ascending)
     - If a.priority is null and b.priority is not null: a should go to end -> swap (a goes after b)
     - If a.priority is not null and b.priority is null: a should come first -> no swap
     - If both have null priority: order by createdAt ascending -> if a.createdAt > b.createdAt, swap
   - Let's formalize a `shouldSwap(Task a, Task b)` logic:
     - Handle null priorities:
       - If a.priority == null && b.priority == null: compare createdAt ascending -> swap if a.createdAt > b.createdAt
       - If a.priority == null && b.priority != null: a should be after b -> swap (true)
       - If a.priority != null && b.priority == null: a should be before b -> no swap (false)
     - If both non-null:
       - Compare priority descending: if a.priority < b.priority -> swap (true)
       - If a.priority > b.priority -> no swap (false)
       - If equal: compare createdAt ascending: if a.createdAt > b.createdAt -> swap (true), else false

   - Let's test with the example:
     - tasks: [Task("bug", 3, 1000), Task("feature", 5, 2000), Task("docs", 3, 500)]
     - Expected result: [Task("feature",5,2000), Task("docs",3,500), Task("bug",3,1000)]
     - swapCount: 2
     - Let's simulate bubble sort manually with the logic:
       - Initial: [bug(3,1000), feature(5,2000), docs(3,500)]
       - Pass 1:
         - Compare bug vs feature: bug.priority=3 < feature.priority=5 -> swap -> [feature(5,2000), bug(3,1000), docs(3,500)], swapCount=1
         - Compare bug vs docs: bug.priority=3 == docs.priority=3 -> createdAt: bug=1000 > docs=500 -> swap -> [feature(5,2000), docs(3,500), bug(3,1000)], swapCount=2
       - Pass 2:
         - Compare feature vs docs: 5 > 3 -> no swap
         - Compare docs vs bug: 3 == 3, 500 < 1000 -> no swap (ascending, so docs before bug, correct order)
       - Done. swapCount=2. Matches example perfectly.

3.  **Algorithm Structure:**
   - Make a copy of the input list to avoid modifying original.
   - Implement standard bubble sort with a swap counter.
   - Use the comparison logic inside the inner loop.
   - After sorting, return new SortResult(copy, swapCount).

   Bubble sort typical structure:
   ```java
   List<Task> sorted = new ArrayList<>(tasks);
   int n = sorted.size();
   int swapCount = 0;
   boolean swapped;
   for (int i = 0; i < n - 1; i++) {
       swapped = false;
       for (int j = 0; j < n - 1 - i; j++) {
           if (shouldSwap(sorted.get(j), sorted.get(j+1))) {
               Collections.swap(sorted, j, j+1); // or manual swap
               swapCount++;
               swapped = true;
           }
       }
       if (!swapped) break;
   }
   ```
   Wait, can I use `Collections.swap`? The constraint says "do not use `Collections.sort()`, `Arrays.sort()`, `List.sort()`, or any other sorting utility". `Collections.swap` is not a sorting utility, it's a utility to swap two elements. It's fine to use, but I can also do manual swap with temp variable to be safe. I'll just use a manual swap to avoid any ambiguity, or use `Collections.swap` - either is fine. I'll do manual swap for clarity and strictness.

   Actually, let's check: "do not use ... any other sorting utility". `Collections.swap` is not a sorting utility, it's a helper. I'll use manual swap to be purely algorithmic.

4.  **Drafting the Code:**

   ```java
   import java.util.ArrayList;
   import java.util.List;

   public class BubbleSortTasks {

       /**
        * Represents a task with a name, priority, and creation timestamp.
         */
       public record Task(String name, Integer priority, long createdAt) {}

       /**
        * Result of sorting tasks, containing the sorted list and the number of swaps performed.
         */
       public record SortResult(List<Task> tasks, int swapCount) {}

       /**
         * Sorts a list of tasks using the bubble sort algorithm.
         * <p>
         * Sorting rules:
         * <ul>
         *   <li>Primary: priority descending (higher first)</li>
         *   <li>Tiebreaker: createdAt ascending (earlier first) when priorities are equal</li>
         *   <li>Null priority: always sorts to the end, ordered by createdAt ascending among null-priority tasks</li>
         * </ul>
         * </p>
         * @param tasks the list of tasks to sort; not modified
         * @return a SortResult containing the sorted list and total swap count
         */
       public static SortResult bubbleSortTasks(List<Task> tasks) {
           // Return empty result if input is empty or null
           if (tasks == null || tasks.isEmpty()) {
               return new SortResult(List.of(), 0);
           }

           // Create a copy to avoid modifying the original list
           List<Task> sorted = new ArrayList<>(tasks);
           int n = sorted.size();
           int swapCount = 0;

           for (int i = 0; i < n - 1; i++) {
               boolean swapped = false;
               for (int j = 0; j < n - 1 - i; j++) {
                   Task current = sorted.get(j);
                   Task next = sorted.get(j + 1);

                   if (shouldSwap(current, next)) {
                       // Manual swap
                       sorted.set(j, next);
                       sorted.set(j + 1, current);
                       swapCount++;
                       swapped = true;
                   }
               }
               if (!swapped) {
                   break;
               }
           }

           return new SortResult(sorted, swapCount);
       }

       /**
        * Determines whether two tasks should be swapped to maintain the desired sort order.
        * @param a the first task (left side)
        * @param b the second task (right side)
        * @return true if a and b are in the wrong order and should be swapped
        */
       private static boolean shouldSwap(Task a, Task b) {
           // Both have null priority: order by createdAt ascending
           if (a.priority == null && b.priority == null) {
               return a.createdAt > b.createdAt;
           }
           // a has null priority, b does not: a should go to the end (after b)
           if (a.priority == null && b.priority != null) {
               return true;
           }
           // a does not have null priority, b has: a should come before b
           if (a.priority != null && b.priority == null) {
               return false;
           }
           // Both have non-null priority
           // Higher priority first (descending)
           if (a.priority < b.priority) {
               return true;
           }
           if (a.priority > b.priority) {
               return false;
           }
           // Priorities equal: order by createdAt ascending
           return a.createdAt > b.createdAt;
       }

       // Optional: main method for quick testing
       public static void main(String[] args) {
           List<Task> tasks = List.of(
               new Task("bug", 3, 1000L),
               new Task("feature", 5, 2000L),
               new Task("docs", 3, 500L)
           );

           SortResult result = bubbleSortTasks(tasks);
           System.out.println("Sorted tasks: " + result.tasks());
           System.out.println("Swap count: " + result.swapCount());
           // Verify original not modified
           System.out.println("Original: " + tasks);
       }
   }
   ```

   Let's double-check the logic with edge cases:
   - Null priorities at end, ordered by createdAt ascending: 
     - Tasks: [Task("a", null, 3000), Task("b", null, 1000), Task("c", null, 2000)]
     - Expected sorted: [b(1000), c(2000), a(3000)] (ascending createdAt)
     - Bubble sort simulation:
       - j=0: a(null,3000) vs b(null,1000): both null, a.createdAt > b.createdAt -> swap -> [b, a, c], count=1
       - j=1: a(null,3000) vs c(null,2000): both null, a.createdAt > c.createdAt -> swap -> [b, c, a], count=2
       - Pass 2: b vs c: 1000 < 2000 -> no swap; c vs a: 2000 < 3000 -> no swap. Done. Result [b, c, a]. Correct.
   - Mixed null and non-null:
     - [Task("a", 2, 100), Task("b", null, 500), Task("c", 1, 200)]
     - Expected: non-null descending: a(2), c(1), then nulls by createdAt: b
     - So [a, c, b]
     - Simulate:
       - Initial: [a(2,100), b(null,500), c(1,200)]
       - Pass 1:
         - j=0: a vs b: a.priority=2 != null, b.priority=null -> shouldSwap returns false (a before b). No swap.
         - j=1: b vs c: b.priority=null, c.priority=1 != null -> shouldSwap returns true (b after c). Swap -> [a, c, b], count=1
       - Pass 2:
         - j=0: a vs c: both non-null, 2 > 1 -> no swap.
       - Done. [a, c, b]. Correct.

   - What about equal priorities, one null one non-null? Handled by null checks first.
   - What if priority is 0? Integer can be 0. Descending: 0 < something? Yes, works fine.
   - The `shouldSwap` logic seems solid.

   One small thing: in `bubbleSortTasks`, I have `if (tasks == null || tasks.isEmpty()) return new SortResult(List.of(), 0);`. The problem says "Do not modify the original input list — return a new list". If the input list is empty, returning an empty list is fine. If null, maybe handle gracefully. I'll keep it, or maybe just assume non-null per typical coding challenges, but handling null is safer. I'll just do `if (tasks == null || tasks.isEmpty())` or simply let the `new ArrayList<>(tasks)` handle empty, and if null, it'll throw NPE which is acceptable, but I'll add a check. Actually, I'll just let it flow naturally or add a simple check. I'll keep the check.

   Wait, `List.of()` returns an immutable list. `SortResult` field `List<Task> tasks` - should it be immutable? The problem doesn't specify, but returning a new sorted list is fine. I'll just use `ArrayList` for the result.

   Check the record definitions: `public static inner Task record` and `SortResult record`. In Java, records can be static inner records. Syntax: `public static record Task(...) {}` inside class. That's valid in Java 16+. I'll use that.

   Let's structure the file properly.

   One detail: The example uses `new BubbleSortTasks.Task("bug", 3, 1000)`. Since it's a record, constructor is `Task(String name, Integer priority, long createdAt)`. I'll make sure types match.

   Final code review:
   - Class `BubbleSortTasks` public
   - Static inner records `Task` and `SortResult`
   - Static method `bubbleSortTasks(List<Task> tasks)` returns `SortResult`
   - Bubble sort implementation
   - Custom comparison `shouldSwap`
   - No use of sorting utilities
   - Returns new list, original unchanged
   - Javadoc
   - Main optional but good for verification

   I'll produce the exact file content as requested. I'll make sure imports are only what's needed: `java.util.ArrayList`, `java.util.List`. No `Collections` needed if I do manual swap.

   Let's write the code carefully.

   Potential pitfall: `shouldSwap` private method. I'll include it.

   Another thing: bubble sort optimization with `swapped` flag is standard and doesn't affect correctness.

   I'll now output the final code.✅


## Response

```java
import java.util.ArrayList;
import java.util.List;

/**
 * Utility class that provides a bubble sort implementation for task records.
 * Sorting follows priority descending, createdAt ascending tie-breaking,
 * and null-priority tasks always move to the end.
 */
public class BubbleSortTasks {

    /**
     * Represents a task with a name, optional priority, and creation timestamp.
     */
    public static record Task(String name, Integer priority, long createdAt) {}

    /**
     * Result returned by {@link #bubbleSortTasks(List)}, containing the sorted
     * task list and the total number of swaps performed.
     */
    public static record SortResult(List<Task> tasks, int swapCount) {}

    /**
     * Sorts the given list of tasks using the bubble sort algorithm.
     * <p>
     * Sorting order:
     * <ul>
     *   <li>Primary: {@code priority} descending (higher values first)</li>
     *   <li>Tiebreaker: {@code createdAt} ascending (earlier timestamps first) when priorities are equal</li>
     *   <li>Null priority: always placed at the end of the list, ordered by {@code createdAt} ascending among themselves</li>
     * </ul>
     * </p>
     * The original input list is <strong>not</strong> modified; a new sorted list is returned.
     *
     * @param tasks the list of tasks to sort; may be empty but must not be {@code null} in normal use
     * @return a {@link SortResult} containing the sorted list and the total swap count
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null || tasks.isEmpty()) {
            return new SortResult(List.of(), 0);
        }

        // Work on a fresh copy so the original list stays untouched
        List<Task> sorted = new ArrayList<>(tasks);
        int n = sorted.size();
        int swapCount = 0;

        boolean swapped;
        for (int i = 0; i < n - 1; i++) {
            swapped = false;
            // After each pass, the largest (according to our order) element "bubbles" to its final position
            for (int j = 0; j < n - 1 - i; j++) {
                Task current = sorted.get(j);
                Task next = sorted.get(j + 1);

                if (shouldSwap(current, next)) {
                    // Manual swap – no sorting utilities used
                    Task temp = current;
                    sorted.set(j, next);
                    sorted.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // If no swaps occurred in a full pass, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sorted, swapCount);
    }

    /**
     * Determines whether two adjacent tasks are in the wrong order and should be swapped.
     *
     * @param a the left task
     * @param b the right task
     * @return {@code true} if {@code a} and {@code b} violate the desired sort order
     */
    private static boolean shouldSwap(Task a, Task b) {
        // Both priorities are null → order by createdAt ascending
        if (a.priority == null && b.priority == null) {
            return a.createdAt > b.createdAt;
        }
        // a has null priority, b does not → a must move to the end
        if (a.priority == null && b.priority != null) {
            return true;
        }
        // a has a value, b is null → a stays before b
        if (a.priority != null && b.priority == null) {
            return false;
        }

        // Both priorities are non-null
        // Higher priority should come first → swap if a's priority is lower
        if (a.priority < b.priority) {
            return true;
        }
        if (a.priority > b.priority) {
            return false;
        }

        // Priorities equal → order by createdAt ascending
        return a.createdAt > b.createdAt;
    }

    // ----------------------------------------------------------------------
    // Optional simple main for manual verification
    // ----------------------------------------------------------------------
    public static void main(String[] args) {
        List<Task> tasks = List.of(
            new Task("bug",     3, 1000L),
            new Task("feature", 5, 2000L),
            new Task("docs",    3, 500L)
        );

        SortResult result = bubbleSortTasks(tasks);

        System.out.println("Sorted tasks: " + result.tasks());
        System.out.println("Swap count:   " + result.swapCount());
        System.out.println("Original list unchanged: " + tasks);
    }
}
```

## Timings

- Time to first token: 0.97s
- Total generation: 81.73s
- Reasoning tokens: 3214
- Answer tokens: 1174
- Total tokens: 4388

## Server Timings (llama.cpp)

- Prompt tokens: 485
- Prompt eval speed: 503.55 t/s
- Prompt eval time: 963.15 ms
- Generation tokens: 4388
- Generation speed: 54.32 t/s
- Generation time: 80760.21 ms
