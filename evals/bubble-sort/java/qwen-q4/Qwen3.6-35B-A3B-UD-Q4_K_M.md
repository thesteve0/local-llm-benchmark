# Code Eval: Qwen3.6-35B-A3B-UD-Q4_K_M

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

2.  **Identify Key Components**:
   - `Task` record: `String name`, `Integer priority`, `long createdAt`
   - `SortResult` record: `List<Task> tasks`, `int swapCount`
   - `bubbleSortTasks(List<Task> tasks)` method
   - Bubble sort implementation
   - Sorting logic with null handling
   - Return a new list (copy input first)
   - Count swaps
   - Javadoc documentation

3.  **Design `Task` Record**:
   ```java
   public record Task(String name, Integer priority, long createdAt) {}
   ```
   This matches the requirements exactly.

4.  **Design `SortResult` Record**:
   ```java
   public record SortResult(List<Task> tasks, int swapCount) {}
   ```
   Matches requirements.

5.  **Implement Bubble Sort Logic**:
   - Need to copy the input list to avoid modifying the original.
   - Bubble sort typically uses nested loops. Outer loop for passes, inner loop for comparisons.
   - Comparison logic:
     - If `priority` is null, it should be considered "less than" any non-null priority (so it goes to the end).
     - Compare `priority1` and `priority2`:
       - If both null: compare `createdAt` ascending.
       - If one null: null goes after non-null.
       - If both non-null: compare descending by priority. If equal, compare ascending by `createdAt`.
     - If `taskA` should come after `taskB` in the sorted order, swap them.
   - Wait, bubble sort swaps adjacent elements if they are in the wrong order. So I need a comparator that returns true if `a` should come after `b`.
   - Let's define a helper method or inline logic for comparison:
     ```java
     boolean shouldSwap(Task a, Task b) {
         // We want descending priority, ascending createdAt
         // null priority goes to end
         int cmp = compareTasks(a, b);
         // cmp > 0 means a should come after b, so swap
         return cmp > 0;
     }
     ```
   - Let's write `compareTasks(Task a, Task b)`:
     - Handle nulls first:
       - `a.priority == null && b.priority == null` -> compare `a.createdAt` vs `b.createdAt` (ascending)
       - `a.priority == null` -> a should come after b -> return 1
       - `b.priority == null` -> b should come after a -> return -1
     - Both non-null:
       - Compare priorities descending: `Integer.compare(b.priority, a.priority)`
       - If equal, compare createdAt ascending: `Long.compare(a.createdAt, b.createdAt)`
     - Return result.
   - Let's trace:
     - `a.priority = 3`, `b.priority = 5` -> `Integer.compare(5, 3) = 1` -> a should come after b -> swap. Correct.
     - `a.priority = 3`, `b.priority = 3`, `a.createdAt = 1000`, `b.createdAt = 500` -> priorities equal, `Long.compare(1000, 500) = 1` -> a should come after b -> swap. Correct.
     - `a.priority = null`, `b.priority = 3` -> return 1 -> swap. Correct.
     - `a.priority = 3`, `b.priority = null` -> return -1 -> no swap. Correct.
     - `a.priority = null`, `b.priority = null`, `a.createdAt = 1000`, `b.createdAt = 500` -> `Long.compare(1000, 500) = 1` -> swap. Correct.

   - Bubble sort implementation:
     ```java
     List<Task> sorted = new ArrayList<>(tasks);
     int swapCount = 0;
     int n = sorted.size();
     for (int i = 0; i < n - 1; i++) {
         boolean swapped = false;
         for (int j = 0; j < n - 1 - i; j++) {
             if (shouldSwap(sorted.get(j), sorted.get(j + 1))) {
                 Collections.swap(sorted, j, j + 1);
                 swapCount++;
                 swapped = true;
             }
         }
         if (!swapped) break;
     }
     return new SortResult(sorted, swapCount);
     ```
   - Wait, `Collections.swap` is fine, or I can manually swap to avoid importing `Collections` if I want, but it's standard. I'll just use a temp variable or `Collections.swap`. The constraint says "do not use Collections.sort(), Arrays.sort(), List.sort()", but `Collections.swap` is fine. I'll stick to manual swap to be safe and explicit.
   - Manual swap:
     ```java
     Task temp = sorted.get(j);
     sorted.set(j, sorted.get(j + 1));
     sorted.set(j + 1, temp);
     ```

6.  **Refine Comparison Logic**:
   Let's write it out carefully:
   ```java
   private static int compareTasks(Task a, Task b) {
       boolean aNull = a.priority == null;
       boolean bNull = b.priority == null;

       if (aNull && bNull) {
           return Long.compare(a.createdAt, b.createdAt);
       }
       if (aNull) {
           return 1; // a goes after b
       }
       if (bNull) {
           return -1; // b goes after a
       }

       // Both non-null
       int priorityCmp = Integer.compare(b.priority, a.priority); // descending
       if (priorityCmp != 0) {
           return priorityCmp;
       }
       return Long.compare(a.createdAt, b.createdAt); // ascending
   }
   ```
   This looks solid.

7.  **Check Constraints**:
   - Single file `BubbleSortTasks.java`
   - `Task` record with specified fields
   - `SortResult` record with specified fields
   - Static method `bubbleSortTasks`
   - Sorting rules: priority desc, createdAt asc, null priority to end
   - Must implement bubble sort
   - Return `SortResult` with sorted list and swap count
   - Do not modify original list
   - Clean, documented, idiomatic Java, Javadoc

   All constraints met.

8.  **Structure the File**:
   ```java
   import java.util.ArrayList;
   import java.util.List;

   /**
    * Task record representing a task with a name, optional priority, and creation timestamp.
    */
   public record Task(String name, Integer priority, long createdAt) {}

   /**
    * Record holding the result of a bubble sort operation on tasks.
    */
   public record SortResult(List<Task> tasks, int swapCount) {}

   /**
    * Utility class providing bubble sort functionality for Task records.
    */
   public class BubbleSortTasks {

       /**
        * Sorts a list of tasks using the bubble sort algorithm.
        * ...
        */
       public static SortResult bubbleSortTasks(List<Task> tasks) {
           // implementation
       }

       // helper method
   }
   ```
   Wait, Java doesn't allow multiple top-level public classes/records in one file unless they are in separate files, or only one is public. The prompt says "Write a single file `BubbleSortTasks.java` containing...". I'll make `BubbleSortTasks` the public class, and `Task` and `SortResult` package-private (or just non-public) to fit in one file, or I can make them all non-public. Actually, in Java, you can have multiple classes in one file, but only one can be `public`. I'll make `Task` and `SortResult` package-private (default visibility) and `BubbleSortTasks` public. Or I can just put them all in the same file without `public` on the records, and `public class BubbleSortTasks`. That's standard.

   Alternatively, I can make `Task` and `SortResult` static nested classes inside `BubbleSortTasks`, but the prompt says "A `Task` record (or class) with fields... A `SortResult` record (or class) with fields...". It's cleaner to keep them as top-level but non-public, or just put them in the same file. I'll stick to top-level but non-public for records, and public for the main class. Actually, it's fine to just make them all `public` if I don't declare the file name restriction strictly, but Java compiler requires the public class name to match the file name. I'll make `BubbleSortTasks` public, and the records package-private. Or I can just make them all `public` and assume the file is named accordingly, but only one can be public. I'll follow standard practice: `public class BubbleSortTasks`, and `record Task(...)`, `record SortResult(...)`.

   Wait, the prompt says "Write a single file `BubbleSortTasks.java` containing:". I'll just provide the code with `public class BubbleSortTasks` and package-private records. That's fine.

   Let's draft the code carefully.

   ```java
   import java.util.ArrayList;
   import java.util.List;

   /**
    * Represents a task with a name, optional priority, and creation timestamp.
    */
   record Task(String name, Integer priority, long createdAt) {}

   /**
    * Holds the result of sorting tasks, including the sorted list and the number of swaps performed.
    */
   record SortResult(List<Task> tasks, int swapCount) {}

   /**
    * Provides bubble sort functionality for {@link Task} records.
    */
   public class BubbleSortTasks {

       /**
        * Sorts a list of tasks using the bubble sort algorithm.
        *
        * <p>Sorting rules:
        * <ol>
        *   <li>Primary: descending by {@code priority} (higher priority first)</li>
        *   <li>Tiebreaker: ascending by {@code createdAt} (earlier timestamp first)</li>
        *   <li>Null handling: tasks with {@code null} priority are placed at the end,
        *       ordered by {@code createdAt} ascending among themselves</li>
        * </ol>
        *
        * @param tasks the list of tasks to sort
        * @return a {@link SortResult} containing the sorted list and total swap count
        */
       public static SortResult bubbleSortTasks(List<Task> tasks) {
           // Create a new list to avoid modifying the original input
           List<Task> sorted = new ArrayList<>(tasks);
           int swapCount = 0;
           int n = sorted.size();

           for (int i = 0; i < n - 1; i++) {
               boolean swapped = false;
               for (int j = 0; j < n - 1 - i; j++) {
                   if (shouldSwap(sorted.get(j), sorted.get(j + 1))) {
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
        * Determines if task {@code a} should be swapped with task {@code b}
        * to maintain the correct sort order.
        *
        * @param a the first task
        * @param b the second task
        * @return {@code true} if {@code a} should come after {@code b} in the sorted list
        */
       private static boolean shouldSwap(Task a, Task b) {
           return compareTasks(a, b) > 0;
       }

       /**
        * Compares two tasks according to the sorting rules.
        *
        * @return negative if a should come before b, zero if equal, positive if a should come after b
        */
       private static int compareTasks(Task a, Task b) {
           boolean aNull = a.priority == null;
           boolean bNull = b.priority == null;

           // Both have null priority: sort by createdAt ascending
           if (aNull && bNull) {
               return Long.compare(a.createdAt, b.createdAt);
           }
           // a has null priority, b does not: a goes after b
           if (aNull) {
               return 1;
           }
           // b has null priority, a does not: b goes after a
           if (bNull) {
               return -1;
           }

           // Both have non-null priority: sort descending by priority
           int priorityCmp = Integer.compare(b.priority, a.priority);
           if (priorityCmp != 0) {
               return priorityCmp;
           }

           // Priorities are equal: sort ascending by createdAt
           return Long.compare(a.createdAt, b.createdAt);
       }
   }
   ```

9.  **Verify against Requirements**:
   - Single file `BubbleSortTasks.java`? Yes.
   - `Task` record with `String name`, `Integer priority`, `long createdAt`? Yes.
   - `SortResult` record with `List<Task> tasks`, `int swapCount`? Yes.
   - Static method `bubbleSortTasks(List<Task> tasks)`? Yes.
   - Sorting rules: priority desc, createdAt asc, null priority to end? Yes.
   - Must implement bubble sort? Yes, nested loops with adjacent swaps.
   - Return `SortResult` with sorted list and swap count? Yes.
   - Do not modify original input list? Yes, `new ArrayList<>(tasks)` creates a copy.
   - Clean, documented, idiomatic Java, Javadoc? Yes.
   - Example check:
     Input: `[("bug", 3, 1000), ("feature", 5, 2000), ("docs", 3, 500)]`
     Pass 1:
     j=0: compare `bug`(3,1000) vs `feature`(5,2000). priorityCmp = compare(5,3)=1 > 0 -> swap. List: `[feature, bug, docs]`, swaps=1
     j=1: compare `bug`(3,1000) vs `docs`(3,500). priorityCmp=0. createdAtCmp = compare(1000,500)=1 > 0 -> swap. List: `[feature, docs, bug]`, swaps=2
     Pass 2:
     j=0: compare `feature`(5,2000) vs `docs`(3,500). priorityCmp=1 > 0 -> swap. List: `[docs, feature, bug]`, swaps=3
     j=1: compare `feature`(5,2000) vs `bug`(3,1000). priorityCmp=1 > 0 -> swap. List: `[docs, bug, feature]`, swaps=4
     Wait, this doesn't match the example output! The example says:
     `result.tasks() = [Task("feature",5,2000), Task("docs",3,500), Task("bug",3,1000)]`
     `result.swapCount() = 2`
     Let's trace carefully. Bubble sort typically bubbles the largest element to the end. But here, "largest" means highest priority. So highest priority should end up at the beginning? Or end?
     Standard bubble sort moves the largest element to the end of the array after each pass. If we want descending order, the "largest" (highest priority) should be at the beginning. So we should bubble the *smallest* element to the end, or reverse the comparison direction.
     Actually, bubble sort can be implemented to bubble the smallest to the end (for ascending) or largest to the end (for descending). The standard implementation I wrote bubbles the "largest" (according to comparator) to the end. But if comparator says `a` should come after `b` when `a.priority < b.priority`, then `a` is "smaller". So it bubbles smaller to the end, resulting in descending order at the front. That's correct.
     Let's re-trace with the example carefully.
     Initial: `[bug(3,1000), feature(5,2000), docs(3,500)]`
     Pass 1 (i=0):
     j=0: compare bug(3,1000) and feature(5,2000).
     priorityCmp = Integer.compare(5, 3) = 1. Since 1 > 0, shouldSwap returns true. Swap.
     List: `[feature(5,2000), bug(3,1000), docs(3,500)]`. swaps=1.
     j=1: compare bug(3,1000) and docs(3,500).
     priorityCmp = 0. createdAtCmp = Long.compare(1000, 500) = 1. shouldSwap true. Swap.
     List: `[feature(5,2000), docs(3,500), bug(3,1000)]`. swaps=2.
     End of pass 1. `swapped=true`.
     Pass 2 (i=1):
     j=0: compare feature(5,2000) and docs(3,500).
     priorityCmp = Integer.compare(5, 3) = 1. shouldSwap true. Swap.
     List: `[docs(3,500), feature(5,2000), bug(3,1000)]`. swaps=3.
     j=1: loop ends because `n-1-i` = 3-1-1 = 1. So j goes 0 to 0.
     Wait, standard bubble sort inner loop: `for (int j = 0; j < n - 1 - i; j++)`
     For n=3:
     i=0: j < 2 -> j=0, j=1
     i=1: j < 1 -> j=0
     So after pass 1, the last element is in place. In my trace, after pass 1, the list is `[feature, docs, bug]`. The last element `bug` is in place? But `bug` has priority 3, `docs` has priority 3. They are equal priority. `createdAt` for `docs` is 500, `bug` is 1000. So `docs` should come before `bug`. So `[feature, docs, bug]` is actually correctly sorted!
     Why did pass 2 swap `feature` and `docs`? Because `feature` (5) > `docs` (3), so `feature` should come before `docs`. But my comparator says `shouldSwap` is true if `a` should come *after* `b`. So if `a` is `feature` and `b` is `docs`, `feature` should come *before* `docs`, so `shouldSwap` should be false.
     Let's check my comparator logic:
     `Integer.compare(b.priority, a.priority)` -> `Integer.compare(3, 5)` = -1.
     So `priorityCmp` = -1. `shouldSwap` returns false.
     Ah! I made a mistake in my manual trace. `Integer.compare(b.priority, a.priority)` compares `b` to `a`. So for `feature`(5) vs `docs`(3), it's `compare(3, 5)` = -1. So `shouldSwap` is false. No swap.
     So pass 2 does nothing. `swapped` remains false. Loop breaks.
     Final list: `[feature, docs, bug]`. Swaps: 2.
     Matches example exactly! Great.

   One minor thing: `Integer.compare(b.priority, a.priority)` is correct for descending.
   Let's double check the null handling logic in the comparator.
   If `a.priority` is null, `b.priority` is 3. `aNull=true`, `bNull=false`. Returns 1. `shouldSwap` true. `a` swaps with `b`. So null goes to the right. Correct.
   If both null, compares createdAt ascending. Correct.
   All good.

   Check constraints again: "Do not modify the original input list — return a new list". `new ArrayList<>(tasks)` does this.
   "You must implement the bubble sort algorithm — do not use Collections.sort()...". Checked.
   "Return a SortResult with the sorted list and total swap count". Checked.
   "Write clean, well-documented, idiomatic Java code. Use Javadoc where appropriate." Checked.

   One detail: The prompt says `Task` record and `SortResult` record. I'll make them package-private to fit in one file with `public class BubbleSortTasks`. That's standard Java practice. I'll add a note if needed, but it's fine.

   I should also consider if `tasks` could be null. The prompt doesn't specify, but it's good practice to handle it or assume non-null. I'll assume non-null as per typical coding challenge constraints, but I can add a null check or just let it throw NPE naturally. I'll stick to assuming valid input as per example.

   Let's structure the final code carefully.

   ```java
   import java.util.ArrayList;
   import java.util.List;

   /**
    * Represents a task with a name, optional priority, and creation timestamp.
    */
   record Task(String name, Integer priority, long createdAt) {}

   /**
    * Holds the result of sorting tasks, including the sorted list and the number of swaps performed.
    */
   record SortResult(List<Task> tasks, int swapCount) {}

   /**
    * Provides bubble sort functionality for {@link Task} records.
    */
   public class BubbleSortTasks {

       /**
        * Sorts a list of tasks using the bubble sort algorithm.
        *
        * <p>Sorting rules:
        * <ol>
        *   <li>Primary: descending by {@code priority} (higher priority first)</li>
        *   <li>Tiebreaker: ascending by {@code createdAt} (earlier timestamp first)</li>
        *   <li>Null handling: tasks with {@code null} priority are placed at the end,
        *       ordered by {@code createdAt} ascending among themselves</li>
        * </ol>
        *
        * @param tasks the list of tasks to sort
        * @return a {@link SortResult} containing the sorted list and total swap count
        * @throws IllegalArgumentException if {@code tasks} is null
        */
       public static SortResult bubbleSortTasks(List<Task> tasks) {
           if (tasks == null) {
               throw new IllegalArgumentException("Input list cannot be null");
           }

           // Create a defensive copy to avoid modifying the original list
           List<Task> sorted = new ArrayList<>(tasks);
           int swapCount = 0;
           int n = sorted.size();

           for (int i = 0; i < n - 1; i++) {
               boolean swapped = false;
               for (int j = 0; j < n - 1 - i; j++) {
                   if (shouldSwap(sorted.get(j), sorted.get(j + 1))) {
                       // Swap adjacent elements
                       Task temp = sorted.get(j);
                       sorted.set(j, sorted.get(j + 1));
                       sorted.set(j + 1, temp);
                       swapCount++;
                       swapped = true;
                   }
               }
               // Optimization: if no swaps occurred in a pass, the list is sorted
               if (!swapped) {
                   break;
               }
           }

           return new SortResult(sorted, swapCount);
       }

       /**
        * Determines if task {@code a} should be swapped with task {@code b}
        * to maintain the correct sort order.
        *
        * @param a the first task
        * @param b the second task
        * @return {@code true} if {@code a} should come after {@code b} in the sorted list
        */
       private static boolean shouldSwap(Task a, Task b) {
           return compareTasks(a, b) > 0;
       }

       /**
        * Compares two tasks according to the specified sorting rules.
        *
        * @return negative if {@code a} should come before {@code b},
        *         zero if they are equivalent in sort order,
        *         positive if {@code a} should come after {@code b}
        */
       private static int compareTasks(Task a, Task b) {
           boolean aNull = a.priority == null;
           boolean bNull = b.priority == null;

           // Both have null priority: sort by createdAt ascending
           if (aNull && bNull) {
               return Long.compare(a.createdAt, b.createdAt);
           }
           // a has null priority, b does not: a goes after b
           if (aNull) {
               return 1;
           }
           // b has null priority, a does not: b goes after a
           if (bNull) {
               return -1;
           }

           // Both have non-null priority: sort descending by priority
           int priorityCmp = Integer.compare(b.priority, a.priority);
           if (priorityCmp != 0) {
               return priorityCmp;
           }

           // Priorities are equal: sort ascending by createdAt
           return Long.compare(a.createdAt, b.createdAt);
       }
   }
   ```

   Check imports: `java.util.ArrayList`, `java.util.List`. Good.
   Check record syntax: Java 14+ supports compact records. The prompt uses `record` keyword, so Java 14+ is assumed.
   Check method signature: `public static SortResult bubbleSortTasks(List<Task> tasks)` matches exactly.
   Check constraints: All met.
   One thing: `Integer.compare(b.priority, a.priority)` works correctly. `Long.compare(a.createdAt, b.createdAt)` works correctly.
   The code is clean and well-documented.
   I'll output this exactly.
   I should make sure the file name matches the public class name. The prompt says `BubbleSortTasks.java`, so `public class BubbleSortTasks` is correct.
   I'll present the code block directly.
   All good.
   Final review of the prompt: "Write a single file `BubbleSortTasks.java` containing: 1. A `Task` record... 2. A `SortResult` record... 3. A static method..."
   I'll put everything in one block.
   Ready.✅
   Output matches response. 
   One minor point: `List<Task> tasks` in the example is `List.of(...)`, which returns an immutable list. `new ArrayList<>(tasks)` handles it fine.
   The code is robust.
   I will generate the response now. 
   Self-Correction/Verification during thought:
   - Check bubble sort optimization: `if (!swapped) break;` is standard and correct.
   - Check null handling: The prompt says "tasks where priority is null always sort to the end of the list, ordered by createdAt ascending among themselves". My code does exactly that.
   - Check swap count: Incremented exactly when a swap happens. Correct.
   - Check immutability: `new ArrayList<>(tasks)` creates a shallow copy. Since `Task` is a record (immutable), this is safe.
   - All constraints satisfied.
   Output matches. 
   Proceeds. 
   [Output Generation] -> *Proceeds*
   *(Self-Correction/Refinement during drafting)*: 
   I should ensure the records are defined properly. In Java, you can have multiple top-level classes/records in one file, but only one can be `public`. I'll keep `Task` and `SortResult` package-private (default visibility) and `BubbleSortTasks` public. This is standard and compiles correctly in `BubbleSortTasks.java`. I'll add a comment if necessary, but it's fine.
   The code looks solid. I'll output it. 
   All steps verified.✅
   Output Generation. 
   [Done] 
   *Output Generation* (matches the final code block)
   ```java
   import java.util.ArrayList;
   import java.util.List;

   /**
    * Represents a task with a name, optional priority, and creation timestamp.
    */
   record Task(String name, Integer priority, long createdAt) {}

   /**
    * Holds the result of sorting tasks, including the sorted list and the number of swaps performed.
    */
   record SortResult(List<Task> tasks, int swapCount) {}

   /**
    * Provides bubble sort functionality for {@link Task} records.
    */
   public class BubbleSortTasks {
       // ... rest of the code
   }
   ```
   Perfect.✅
   Output matches response. 
   [Final Check of the Prompt]: "Write a single file `BubbleSortTasks.java` containing: 1. A `Task` record... 2. A `SortResult` record... 3. A static method..."
   All good.
   Proceeds. 
   [Output Generation] -> *Proceeds* (produces the final response)
   *(Note: I'll make sure the formatting is exact and matches Java conventions.)*
   All set. 
   [Output] -> *Proceeds*


## Response

Here is the complete, single-file implementation meeting all your requirements:

```java
import java.util.ArrayList;
import java.util.List;

/**
 * Represents a task with a name, optional priority, and creation timestamp.
 */
record Task(String name, Integer priority, long createdAt) {}

/**
 * Holds the result of sorting tasks, including the sorted list and the number of swaps performed.
 */
record SortResult(List<Task> tasks, int swapCount) {}

/**
 * Provides bubble sort functionality for {@link Task} records.
 */
public class BubbleSortTasks {

    /**
     * Sorts a list of tasks using the bubble sort algorithm.
     *
     * <p>Sorting rules:
     * <ol>
     *   <li>Primary: descending by {@code priority} (higher priority first)</li>
     *   <li>Tiebreaker: ascending by {@code createdAt} (earlier timestamp first)</li>
     *   <li>Null handling: tasks with {@code null} priority are placed at the end,
     *       ordered by {@code createdAt} ascending among themselves</li>
     * </ol>
     *
     * @param tasks the list of tasks to sort
     * @return a {@link SortResult} containing the sorted list and total swap count
     * @throws IllegalArgumentException if {@code tasks} is null
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null) {
            throw new IllegalArgumentException("Input list cannot be null");
        }

        // Create a defensive copy to avoid modifying the original list
        List<Task> sorted = new ArrayList<>(tasks);
        int swapCount = 0;
        int n = sorted.size();

        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                if (shouldSwap(sorted.get(j), sorted.get(j + 1))) {
                    // Swap adjacent elements
                    Task temp = sorted.get(j);
                    sorted.set(j, sorted.get(j + 1));
                    sorted.set(j + 1, temp);
                    swapCount++;
                    swapped = true;
                }
            }
            // Optimization: if no swaps occurred in a pass, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sorted, swapCount);
    }

    /**
     * Determines if task {@code a} should be swapped with task {@code b}
     * to maintain the correct sort order.
     *
     * @param a the first task
     * @param b the second task
     * @return {@code true} if {@code a} should come after {@code b} in the sorted list
     */
    private static boolean shouldSwap(Task a, Task b) {
        return compareTasks(a, b) > 0;
    }

    /**
     * Compares two tasks according to the specified sorting rules.
     *
     * @return negative if {@code a} should come before {@code b},
     *         zero if they are equivalent in sort order,
     *         positive if {@code a} should come after {@code b}
     */
    private static int compareTasks(Task a, Task b) {
        boolean aNull = a.priority == null;
        boolean bNull = b.priority == null;

        // Both have null priority: sort by createdAt ascending
        if (aNull && bNull) {
            return Long.compare(a.createdAt, b.createdAt);
        }
        // a has null priority, b does not: a goes after b
        if (aNull) {
            return 1;
        }
        // b has null priority, a does not: b goes after a
        if (bNull) {
            return -1;
        }

        // Both have non-null priority: sort descending by priority
        int priorityCmp = Integer.compare(b.priority, a.priority);
        if (priorityCmp != 0) {
            return priorityCmp;
        }

        // Priorities are equal: sort ascending by createdAt
        return Long.compare(a.createdAt, b.createdAt);
    }
}
```

### Key Implementation Details:
1. **Immutability & Safety**: `new ArrayList<>(tasks)` creates a shallow copy, ensuring the original input list remains untouched.
2. **Bubble Sort Optimization**: The `swapped` flag breaks early if a full pass completes without swaps, improving best-case time complexity to `O(n)`.
3. **Null Handling**: Explicitly checks for `null` priorities first. `null` values are treated as "smaller" than any non-null value, naturally bubbling them to the end while preserving `createdAt` ordering among themselves.
4. **Comparator Logic**: 
   - `Integer.compare(b.priority, a.priority)` achieves descending order.
   - `Long.compare(a.createdAt, b.createdAt)` achieves ascending order.
   - Returns `> 0` when `a` should appear after `b`, triggering a swap.
5. **Java Records**: Uses modern Java records for concise, immutable data carriers with auto-generated constructors, accessors, `equals()`, `hashCode()`, and `toString()`.

## Timings

- Time to first token: 0.50s
- Total generation: 134.01s
- Reasoning tokens: 6669
- Answer tokens: 1262
- Total tokens: 7931
