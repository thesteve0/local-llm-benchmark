# Code Eval: Qwen3.6-35B-A3B-Q8_0

## Prompt

# Bubble Sort Tasks — Java

Implement a bubble sort function for task records.

## Requirements

Write a single file `BubbleSortTasks.java` containing:

1. A `Task` record (or class) with fields:
   - `String name`
   - `Integer priority` (nullable — use `Integer`, not `int`)
   - `long createdAt`

2. A `SortResult` record (or class) with fields:
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
List<Task> tasks = List.of(
    new Task("bug",     3, 1000),
    new Task("feature", 5, 2000),
    new Task("docs",    3, 500)
);

SortResult result = BubbleSortTasks.bubbleSortTasks(tasks);
// result.tasks() = [Task("feature",5,2000), Task("docs",3,500), Task("bug",3,1000)]
// result.swapCount() = 2
```

Write clean, well-documented, idiomatic Java code. Use Javadoc where appropriate.


## Reasoning

Here's a thinking process:

1.  **Understand the Goal**: The user wants a Java implementation of a bubble sort algorithm specifically for a `Task` record. The sorting needs to follow specific rules: primary sort by `priority` descending, tiebreaker by `createdAt` ascending, and `null` priorities go to the end. The output should be a `SortResult` containing the sorted list and the number of swaps. The original list must not be modified.

2.  **Analyze Requirements**:
   - **Records**: `Task` (name: String, priority: Integer, createdAt: long) and `SortResult` (tasks: List<Task>, swapCount: int).
   - **Method**: `public static SortResult bubbleSortTasks(List<Task> tasks)`
   - **Sorting Rules**:
     - Primary: `priority` descending (higher first)
     - Tiebreaker: `createdAt` ascending (earlier first)
     - Null priority: always at the end, sorted by `createdAt` ascending among themselves
   - **Constraints**:
     - Must use bubble sort
     - No built-in sorting utilities
     - Return new list (don't modify input)
     - Clean, documented, idiomatic Java
   - **Example**: Provided to verify logic.

3.  **Design `Task` Record**:
   ```java
   public record Task(String name, Integer priority, long createdAt) {}
   ```
   Wait, the prompt says "record (or class)". I'll use a record as it's modern Java (14+). I should make sure it's immutable and has proper fields.

4.  **Design `SortResult` Record**:
   ```java
   public record SortResult(List<Task> tasks, int swapCount) {}
   ```

5.  **Implement Bubble Sort Logic**:
   - Need to create a copy of the input list to avoid modifying the original.
   - Bubble sort typically uses nested loops. Outer loop runs `n-1` times, inner loop runs `n-1-i` times.
   - Comparison logic needs to handle:
     - Both priorities non-null
     - One null, one non-null
     - Both null
   - Let's define a comparison function or inline it:
     - If `p1 == null` and `p2 == null`: compare `createdAt` ascending
     - If `p1 == null` and `p2 != null`: `p1` should come after `p2` (return 1)
     - If `p1 != null` and `p2 == null`: `p1` should come before `p2` (return -1)
     - If both non-null:
       - If `p1 != p2`: compare descending (`p2 - p1` or `Integer.compare(p2, p1)`)
       - If `p1 == p2`: compare `createdAt` ascending (`Long.compare(t1.createdAt, t2.createdAt)`)
   - Bubble sort swaps adjacent elements if they are in the wrong order. So if `compare(t1, t2) > 0`, swap.
   - Count swaps.

   Let's draft the comparison logic carefully:
   ```java
   private static int compareTasks(Task t1, Task t2) {
       boolean p1Null = t1.priority() == null;
       boolean p2Null = t2.priority() == null;

       if (p1Null && p2Null) {
           return Long.compare(t1.createdAt(), t2.createdAt());
       }
       if (p1Null) {
           return 1; // t1 goes after t2
       }
       if (p2Null) {
           return -1; // t1 goes before t2
       }

       // Both non-null
       int priorityCmp = Integer.compare(t2.priority(), t1.priority()); // descending
       if (priorityCmp != 0) {
           return priorityCmp;
       }
       return Long.compare(t1.createdAt(), t2.createdAt()); // ascending
   }
   ```
   Wait, bubble sort swaps if `compareTasks(t1, t2) > 0`. Let's verify:
   - If `t1` should come after `t2`, `compareTasks` returns positive. We swap. Correct.
   - Example: `t1` priority 3, `t2` priority 5. `Integer.compare(5, 3)` = 1. Positive -> swap. Correct.
   - Example: `t1` priority 3, `t2` priority 3, `t1.createdAt` 1000, `t2.createdAt` 500. `priorityCmp` = 0. `Long.compare(1000, 500)` = 1. Positive -> swap. Correct (earlier createdAt should come first).
   - Example: `t1` priority null, `t2` priority 5. `p1Null` true, `p2Null` false -> returns 1. Positive -> swap. Correct (null goes to end).
   - Example: `t1` priority 5, `t2` priority null. Returns -1. Negative -> no swap. Correct.

   This comparison logic works perfectly for bubble sort's "swap if out of order" condition.

6.  **Implement Bubble Sort Algorithm**:
   ```java
   public static SortResult bubbleSortTasks(List<Task> tasks) {
       if (tasks == null || tasks.isEmpty()) {
           return new SortResult(Collections.emptyList(), 0);
       }

       // Create a mutable copy to avoid modifying the original
       List<Task> sortedTasks = new ArrayList<>(tasks);
       int swapCount = 0;
       int n = sortedTasks.size();

       for (int i = 0; i < n - 1; i++) {
           boolean swapped = false;
           for (int j = 0; j < n - 1 - i; j++) {
               if (compareTasks(sortedTasks.get(j), sortedTasks.get(j + 1)) > 0) {
                   // Swap
                   Task temp = sortedTasks.get(j);
                   sortedTasks.set(j, sortedTasks.get(j + 1));
                   sortedTasks.set(j + 1, temp);
                   swapCount++;
                   swapped = true;
               }
           }
           if (!swapped) break; // Optimization: early exit if no swaps
       }

       return new SortResult(sortedTasks, swapCount);
   }
   ```

   Wait, the example says:
   Input: `Task("bug", 3, 1000)`, `Task("feature", 5, 2000)`, `Task("docs", 3, 500)`
   Expected output: `[Task("feature",5,2000), Task("docs",3,500), Task("bug",3,1000)]`
   Expected swapCount: 2

   Let's trace bubble sort on this:
   Initial: `[bug(3,1000), feature(5,2000), docs(3,500)]`
   i=0, j=0: compare bug(3,1000) vs feature(5,2000). priority 3 vs 5. desc -> feature first. compare returns 1. Swap.
   List: `[feature(5,2000), bug(3,1000), docs(3,500)]`, swaps=1
   i=0, j=1: compare bug(3,1000) vs docs(3,500). priority equal. createdAt 1000 vs 500. asc -> docs first. compare returns 1. Swap.
   List: `[feature(5,2000), docs(3,500), bug(3,1000)]`, swaps=2
   i=1, j=0: compare feature(5,2000) vs docs(3,500). priority 5 vs 3. desc -> feature first. compare returns -1. No swap.
   End. Total swaps = 2. Matches example!

   The algorithm works correctly.

7.  **Consider Edge Cases & Constraints**:
   - Null input list? The prompt says `List<Task> tasks`. I'll handle null gracefully or assume non-null per typical API contracts, but adding a null check is safe.
   - Empty list? Handled.
   - Single element? Handled.
   - All null priorities? Handled.
   - The constraint says "Do not modify the original input list — return a new list". `new ArrayList<>(tasks)` does exactly that.
   - "You must implement the bubble sort algorithm — do not use Collections.sort()..." Checked.
   - "Return a SortResult with the sorted list and total swap count". Checked.
   - "Use Javadoc where appropriate". I'll add Javadoc to the class, records, and method.

   One minor point: `List.of()` returns an immutable list. `new ArrayList<>(tasks)` creates a mutable copy. That's fine.
   Should I make `Task` and `SortResult` public? Yes.
   Should I put them in the same file? Yes, "Write a single file `BubbleSortTasks.java`". In Java, only one public class per file, so I'll make `BubbleSortTasks` the public class, and `Task` and `SortResult` package-private or static nested. Actually, records can be top-level in the same file if only one is public. I'll make `Task` and `SortResult` static nested records inside `BubbleSortTasks` to keep it in one file cleanly, or just top-level non-public records. The prompt says "Write a single file `BubbleSortTasks.java` containing: 1. A Task record... 2. A SortResult record... 3. A static method...". I'll make them static nested for simplicity, or just separate top-level classes in the same file (Java allows multiple non-public top-level classes in one file). I'll go with static nested to avoid filename conflicts, but the prompt says "containing: 1. A Task record...". I'll just define them as static nested records inside `BubbleSortTasks`. Actually, it's cleaner to make them top-level but non-public, or just static nested. I'll stick to static nested for a single-file submission, but I'll make sure the structure matches the prompt.

   Wait, the prompt says:
   ```java
   public record Task(String name, Integer priority, long createdAt) {}
   public record SortResult(List<Task> tasks, int swapCount) {}
   public static SortResult bubbleSortTasks(List<Task> tasks)
   ```
   I'll define them as static nested records inside `BubbleSortTasks` to keep it strictly one file with one public class. Or I can just make them top-level non-public. I'll go with static nested for simplicity.

   Let's draft the full code:

   ```java
   import java.util.ArrayList;
   import java.util.Collections;
   import java.util.List;

   /**
    * Provides a bubble sort implementation for sorting Task records based on
    * priority and creation timestamp.
    */
   public class BubbleSortTasks {

       /**
        * Represents a task with a name, optional priority, and creation timestamp.
        */
       public static record Task(String name, Integer priority, long createdAt) {}

       /**
        * Holds the result of a sorting operation, including the sorted list and swap count.
        */
       public static record SortResult(List<Task> tasks, int swapCount) {}

       /**
        * Sorts a list of tasks using the bubble sort algorithm.
        *
        * @param tasks the list of tasks to sort
        * @return a SortResult containing the sorted list and the total number of swaps performed
        */
       public static SortResult bubbleSortTasks(List<Task> tasks) {
           if (tasks == null || tasks.isEmpty()) {
               return new SortResult(Collections.emptyList(), 0);
           }

           // Create a mutable copy to ensure the original list is not modified
           List<Task> sortedTasks = new ArrayList<>(tasks);
           int swapCount = 0;
           int n = sortedTasks.size();

           for (int i = 0; i < n - 1; i++) {
               boolean swapped = false;
               for (int j = 0; j < n - 1 - i; j++) {
                   if (compareTasks(sortedTasks.get(j), sortedTasks.get(j + 1)) > 0) {
                       // Swap adjacent elements
                       Task temp = sortedTasks.get(j);
                       sortedTasks.set(j, sortedTasks.get(j + 1));
                       sortedTasks.set(j + 1, temp);
                       swapCount++;
                       swapped = true;
                   }
               }
               // If no swaps occurred, the list is already sorted
               if (!swapped) {
                   break;
               }
           }

           return new SortResult(sortedTasks, swapCount);
       }

       /**
        * Compares two tasks to determine their relative order for sorting.
        * Returns a positive value if t1 should come after t2, negative if before, zero if equal.
        */
       private static int compareTasks(Task t1, Task t2) {
           boolean p1Null = t1.priority() == null;
           boolean p2Null = t2.priority() == null;

           // Both have null priority: sort by createdAt ascending
           if (p1Null && p2Null) {
               return Long.compare(t1.createdAt(), t2.createdAt());
           }
           // t1 has null priority, t2 does not: t1 goes after t2
           if (p1Null) {
               return 1;
           }
           // t2 has null priority, t1 does not: t1 goes before t2
           if (p2Null) {
               return -1;
           }

           // Both have non-null priorities: sort descending
           int priorityCmp = Integer.compare(t2.priority(), t1.priority());
           if (priorityCmp != 0) {
               return priorityCmp;
           }

           // Priorities are equal: sort by createdAt ascending
           return Long.compare(t1.createdAt(), t2.createdAt());
       }
   }
   ```

8.  **Review & Refine**:
   - Check constraints: "Do not modify the original input list — return a new list". `new ArrayList<>(tasks)` creates a shallow copy. Since `Task` is a record (immutable), shallow copy is fine.
   - Check sorting rules: Primary priority desc, tiebreaker createdAt asc, null priority at end sorted by createdAt asc. All handled correctly in `compareTasks`.
   - Check bubble sort: Standard implementation with early exit optimization. Counts swaps correctly.
   - Check example: Matches exactly.
   - Check Java idioms: Uses records, `Integer.compare`, `Long.compare`, proper Javadoc, early exit optimization, defensive copying.
   - One thing: `Collections.emptyList()` is fine, but maybe `List.of()` is better for modern Java? `Collections.emptyList()` is fine. I'll stick with it or use `List.of()`. Actually, `Collections.emptyList()` is standard.
   - Should I make `Task` and `SortResult` top-level or static nested? The prompt says "Write a single file `BubbleSortTasks.java` containing: 1. A Task record... 2. A SortResult record... 3. A static method...". It's common to put them as static nested records in a single-file submission. I'll keep them static nested. Alternatively, I can make them top-level non-public classes. I'll stick with static nested for cleanliness, but I'll add a comment if needed. Actually, Java allows multiple top-level classes in one file as long as only one is public. I'll make `Task` and `SortResult` top-level non-public to strictly follow "containing: 1. A Task record...". But static nested is fine too. I'll go with static nested to avoid any confusion about file structure. Actually, the prompt says "A Task record (or class) with fields...". I'll just define them as static nested records inside `BubbleSortTasks`. It's standard for single-file coding challenges.

   Let's double check the `compareTasks` logic for nulls:
   If `t1.priority() == null` and `t2.priority() == null`, we compare `createdAt` ascending. Correct.
   If `t1.priority() == null` and `t2.priority() != null`, we return 1, meaning `t1` > `t2`, so they swap. `t1` moves right. Correct.
   If `t1.priority() != null` and `t2.priority() == null`, we return -1, meaning `t1` < `t2`, no swap. `t1` stays left. Correct.
   All good.

   One minor point: `Integer.compare(t2.priority(), t1.priority())` for descending. If `t2.priority()` is 5 and `t1.priority()` is 3, `compare(5, 3)` is 1. Positive -> swap. Correct.
   If `t2.priority()` is 3 and `t1.priority()` is 5, `compare(3, 5)` is -1. Negative -> no swap. Correct.

   The code looks solid. I'll add proper imports and ensure formatting is clean.
   I'll also consider if `List<Task>` should be unmodifiable in the result? The prompt says "return a new list", doesn't specify immutability. `ArrayList` is fine.

   Let's verify the example manually again with the code:
   Input: `[bug(3,1000), feature(5,2000), docs(3,500)]`
   i=0:
     j=0: compare(bug, feature) -> p1=3, p2=5 -> compare(5,3)=1 > 0 -> swap. List: `[feature, bug, docs]`, swaps=1
     j=1: compare(bug, docs) -> p1=3, p2=3 -> priorityCmp=0 -> compare(1000,500)=1 > 0 -> swap. List: `[feature, docs, bug]`, swaps=2
   i=1:
     j=0: compare(feature, docs) -> p1=5, p2=3 -> compare(3,5)=-1 -> no swap.
   Loop ends. Result: `[feature, docs, bug]`, swaps=2. Matches example exactly.

   One detail: `List.of()` in the example creates an immutable list. `new ArrayList<>(tasks)` handles it fine.
   I'll make sure the code compiles mentally:
   - `import java.util.ArrayList;`
   - `import java.util.Collections;`
   - `import java.util.List;`
   - Records are Java 14+, but widely supported. The prompt says "record (or class)", so records are fine.
   - `Integer.compare` and `Long.compare` are Java 7+.
   - All good.

   I will structure the final output exactly as requested. I'll put `Task` and `SortResult` as static nested records for a single-file solution, but I'll also mention they can be top-level if preferred. Actually, I'll just make them top-level non-public classes in the same file to strictly match "containing: 1. A Task record... 2. A SortResult record...". Java allows this. I'll stick to static nested for simplicity, it's standard.

   Wait, the prompt says:
   ```java
   public record Task(String name, Integer priority, long createdAt) {}
   public record SortResult(List<Task> tasks, int swapCount) {}
   public static SortResult bubbleSortTasks(List<Task> tasks)
   ```
   This implies they might be top-level. I'll make them top-level non-public records in the same file. It's cleaner.

   Let's draft it carefully.

   ```java
   import java.util.ArrayList;
   import java.util.Collections;
   import java.util.List;

   /**
    * Represents a task with a name, optional priority, and creation timestamp.
    */
   record Task(String name, Integer priority, long createdAt) {}

   /**
    * Holds the result of a sorting operation, including the sorted list and swap count.
    */
   record SortResult(List<Task> tasks, int swapCount) {}

   /**
    * Provides a bubble sort implementation for sorting Task records based on
    * priority and creation timestamp.
    */
   public class BubbleSortTasks {

       /**
        * Sorts a list of tasks using the bubble sort algorithm.
        *
        * @param tasks the list of tasks to sort
        * @return a SortResult containing the sorted list and the total number of swaps performed
        */
       public static SortResult bubbleSortTasks(List<Task> tasks) {
           // ... implementation
       }

       // ... compareTasks
   }
   ```
   This works. I'll proceed with this structure.

   One thing: `List.of()` in the example uses `new Task(...)`. Records generate constructors automatically. So `new Task("bug", 3, 1000)` works.

   Final check of the prompt: "Do not modify the original input list — return a new list". `new ArrayList<>(tasks)` does this.
   "You must implement the bubble sort algorithm — do not use Collections.sort()..." Checked.
   "Return a SortResult with the sorted list and total swap count". Checked.
   "Write clean, well-documented, idiomatic Java code. Use Javadoc where appropriate." Checked.

   I'll add comments explaining the bubble sort steps and the comparison logic. I'll also ensure the code handles edge cases like null input gracefully.

   One minor improvement: Instead of `Collections.emptyList()`, I can just return `new SortResult(List.of(), 0)` or handle null/empty at the start. I'll keep `Collections.emptyList()` or `List.of()`. `List.of()` is fine.

   Let's write out the full solution. 
   I'll make sure the comparison logic is clearly documented.
   I'll verify the swap counting: bubble sort typically counts each swap. The example says 2 swaps for 3 elements, which matches my trace.
   All good.
   Output matches requirements.
   Proceed. 
   Self-Correction/Refinement during thought:
   Should I make `Task` and `SortResult` public? The prompt says "A Task record (or class) with fields...". It doesn't specify visibility. I'll make them package-private (default) to keep the file clean, or public if needed. I'll stick with default visibility for records, and public for the main class. Actually, in Java, if they are in the same file, they can be top-level. I'll make them `public static record` inside `BubbleSortTasks` to avoid any file naming issues and keep everything self-contained. The prompt says "Write a single file `BubbleSortTasks.java` containing: 1. A Task record...". Static nested is perfectly fine and often preferred in single-file submissions. I'll go with static nested.

   Actually, I'll just define them as static nested records. It's cleaner.

   Code structure:
   ```java
   import java.util.ArrayList;
   import java.util.Collections;
   import java.util.List;

   public class BubbleSortTasks {

       public static record Task(String name, Integer priority, long createdAt) {}

       public static record SortResult(List<Task> tasks, int swapCount) {}

       public static SortResult bubbleSortTasks(List<Task> tasks) { ... }

       private static int compareTasks(Task t1, Task t2) { ... }
   }
   ```
   This is standard and clean.

   One detail: `Integer.compare(t2.priority(), t1.priority())` works, but `t2.priority() - t1.priority()` could overflow if priorities are extreme, but `Integer.compare` is safe. I'll stick with `Integer.compare`.

   All set. Generating response. 
   I will produce the complete Java code block as requested. I'll add comprehensive Javadoc and comments. I'll ensure it strictly follows the constraints. No extra fluff.
   Ready. 
   Output matches the final code.✅
   Self-Correction/Verification during generation prep:
   - Check constraint: "Do not modify the original input list — return a new list". `new ArrayList<>(tasks)` creates a new list. The elements are references to the same Task objects, but since Task is a record (immutable), this is safe and standard. If they wanted deep copy, they'd specify, but typically shallow copy of immutable objects is fine. I'll note it if needed, but it's standard.
   - Check constraint: "bubble sort algorithm". Implemented with O(n^2) nested loops, early exit optimization.
   - Check constraint: "null handling". Handled correctly.
   - Example matches.
   - All good.
   Proceeds. 
   Output generation. 
   [Done] 
   *Self-Correction/Note during thought*: 
   Wait, `List.of()` in the example creates an immutable list. `new ArrayList<>(tasks)` works fine. 
   I'll make sure the code compiles mentally one last time.
   `import java.util.ArrayList;`
   `import java.util.Collections;`
   `import java.util.List;`
   `public class BubbleSortTasks { ... }`
   All imports are there.
   The method signature matches exactly.
   The records match exactly.
   The sorting rules match exactly.
   The constraints match exactly.
   Ready. 
   Output matches the response. 
   [Proceeds]


## Response

Here is the complete, single-file implementation meeting all your requirements:

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Provides a bubble sort implementation for sorting Task records based on
 * priority and creation timestamp.
 */
public class BubbleSortTasks {

    /**
     * Represents a task with a name, optional priority, and creation timestamp.
     *
     * @param name       the name of the task
     * @param priority   the priority level (null tasks sort to the end)
     * @param createdAt  the timestamp when the task was created
     */
    public static record Task(String name, Integer priority, long createdAt) {}

    /**
     * Holds the result of a sorting operation, including the sorted list and swap count.
     *
     * @param tasks      the sorted list of tasks
     * @param swapCount  the total number of swaps performed during sorting
     */
    public static record SortResult(List<Task> tasks, int swapCount) {}

    /**
     * Sorts a list of tasks using the bubble sort algorithm.
     *
     * <p>Sorting rules:
     * <ol>
     *   <li>Primary: Priority descending (higher priority first)</li>
     *   <li>Tiebreaker: Creation timestamp ascending (earlier first)</li>
     *   <li>Null priorities always sort to the end, ordered by timestamp ascending</li>
     * </ol>
     *
     * @param tasks the list of tasks to sort
     * @return a SortResult containing the sorted list and the total number of swaps performed
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null || tasks.isEmpty()) {
            return new SortResult(Collections.emptyList(), 0);
        }

        // Create a mutable copy to ensure the original list is never modified
        List<Task> sortedTasks = new ArrayList<>(tasks);
        int swapCount = 0;
        int n = sortedTasks.size();

        // Standard bubble sort with early-exit optimization
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                // If adjacent elements are out of order, swap them
                if (compareTasks(sortedTasks.get(j), sortedTasks.get(j + 1)) > 0) {
                    Task temp = sortedTasks.get(j);
                    sortedTasks.set(j, sortedTasks.get(j + 1));
                    sortedTasks.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // If no swaps occurred in a pass, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sortedTasks, swapCount);
    }

    /**
     * Compares two tasks to determine their relative order for sorting.
     *
     * @return positive if t1 should come after t2, negative if before, zero if equal
     */
    private static int compareTasks(Task t1, Task t2) {
        boolean p1Null = t1.priority() == null;
        boolean p2Null = t2.priority() == null;

        // Both have null priority: sort by createdAt ascending
        if (p1Null && p2Null) {
            return Long.compare(t1.createdAt(), t2.createdAt());
        }
        // t1 has null priority, t2 does not: t1 goes after t2
        if (p1Null) {
            return 1;
        }
        // t2 has null priority, t1 does not: t1 goes before t2
        if (p2Null) {
            return -1;
        }

        // Both have non-null priorities: sort descending
        int priorityCmp = Integer.compare(t2.priority(), t1.priority());
        if (priorityCmp != 0) {
            return priorityCmp;
        }

        // Priorities are equal: sort by createdAt ascending
        return Long.compare(t1.createdAt(), t2.createdAt());
    }
}
```

### Key Implementation Details:
1. **Immutability & Safety**: Uses `new ArrayList<>(tasks)` to create a shallow copy. Since `Task` is a record (immutable), this safely prevents modification of the original input while maintaining reference efficiency.
2. **Bubble Sort Optimization**: Includes the standard `swapped` flag early-exit. If a full pass completes without swaps, the algorithm terminates immediately, improving best-case performance to `O(n)`.
3. **Comparison Logic**: Centralized in `compareTasks()` to keep the sorting loop clean. Handles all three sorting rules explicitly:
   - Null priorities are pushed to the end using simple `1`/`-1` returns.
   - Non-null priorities use `Integer.compare(t2, t1)` for descending order.
   - Timestamps use `Long.compare()` for ascending order.
4. **Swap Counting**: Increments exactly once per actual element swap, matching the example output.
5. **Modern Java**: Leverages records, `Integer.compare`, `Long.compare`, and standard library collections for idiomatic, readable code. Javadoc covers all public APIs and complex logic.

## Timings

- Time to first token: 0.53s
- Total generation: 133.66s
- Reasoning tokens: 5610
- Answer tokens: 1269
- Total tokens: 6879
