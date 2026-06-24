# Code Eval: Qwen3.6-35B-A3B-UD-Q4_K_M

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

1.  **Understand the Goal**: The user wants a Java class `BubbleSortTasks` containing a `Task` record, a `SortResult` record, and a `bubbleSortTasks` method that sorts a list of `Task` objects using the bubble sort algorithm according to specific rules.

2.  **Analyze Requirements**:
   - **Class Structure**: Single file `BubbleSortTasks.java`, public class `BubbleSortTasks`.
   - **Inner Records**:
     - `Task`: `String name`, `Integer priority`, `long createdAt`. Static inner.
     - `SortResult`: `List<Task> tasks`, `int swapCount`. Static inner.
   - **Method**: `public static SortResult bubbleSortTasks(List<Task> tasks)`
   - **Sorting Rules**:
     1. Primary: `priority` descending (higher first)
     2. Tiebreaker: `createdAt` ascending (earlier first)
     3. Null handling: `priority == null` goes to the end, sorted by `createdAt` ascending among themselves.
   - **Constraints**:
     - Must use bubble sort (no built-in sort utilities)
     - Return `SortResult` with sorted list and swap count
     - Do not modify original list (return a new list)
   - **Example**: Provided to verify logic.

3.  **Design the Sorting Logic (Bubble Sort)**:
   - Bubble sort works by repeatedly stepping through the list, comparing adjacent elements, and swapping them if they are in the wrong order.
   - Need to handle the custom comparison logic.
   - Comparison logic for two tasks `a` and `b`:
     - If `a.priority` is null and `b.priority` is not null: `a` should come after `b` → return 1 (or false for swap condition)
     - If `a.priority` is not null and `b.priority` is null: `a` should come before `b` → return -1
     - If both are null: compare by `createdAt` ascending → `Long.compare(a.createdAt, b.createdAt)`
     - If both are not null: compare by `priority` descending → `Integer.compare(b.priority, a.priority)`. If equal, compare by `createdAt` ascending → `Long.compare(a.createdAt, b.createdAt)`
   - Actually, it's easier to write a helper method or inline the comparison for bubble sort.
   - Bubble sort typically uses a boolean flag `swapped` to optimize (stop if no swaps in a pass).
   - Need to count swaps.
   - Must copy the list first to avoid modifying the original.

   Let's draft the comparison logic carefully:
   ```java
   private static boolean shouldSwap(Task a, Task b) {
       // We want descending priority, ascending createdAt
       // Null priority goes to end
       boolean aNull = a.priority == null;
       boolean bNull = b.priority == null;

       if (aNull && bNull) {
           // Both null: ascending createdAt
           return a.createdAt > b.createdAt;
       } else if (aNull) {
           // a is null, b is not: a should be after b, so swap if a is before b
           return true;
       } else if (bNull) {
           // b is null, a is not: a should be before b, so no swap
           return false;
       } else {
           // Both non-null: descending priority
           if (!a.priority.equals(b.priority)) {
               return a.priority < b.priority; // swap if a has lower priority
           } else {
               // Equal priority: ascending createdAt
               return a.createdAt > b.createdAt;
           }
       }
   }
   ```
   Wait, bubble sort swaps adjacent elements if they are in the wrong order. So `shouldSwap(a, b)` returns true if `a` should come after `b`.
   Let's verify with the example:
   Tasks: (bug, 3, 1000), (feature, 5, 2000), (docs, 3, 500)
   Initial: [bug(3,1000), feature(5,2000), docs(3,500)]
   Pass 1:
   - Compare bug(3,1000) vs feature(5,2000): priority 3 < 5, so bug should be after feature. Swap. List: [feature(5,2000), bug(3,1000), docs(3,500)]. Swaps=1.
   - Compare bug(3,1000) vs docs(3,500): priority equal. createdAt 1000 > 500, so bug should be after docs. Swap. List: [feature(5,2000), docs(3,500), bug(3,1000)]. Swaps=2.
   Pass 2:
   - Compare feature(5,2000) vs docs(3,500): priority 5 > 3, no swap.
   - Compare docs(3,500) vs bug(3,1000): priority equal, createdAt 500 < 1000, no swap.
   No swaps in pass 2. Stop.
   Result: [feature, docs, bug], swaps=2. Matches example!

   The comparison logic seems correct.

4.  **Implement Bubble Sort**:
   ```java
   public static SortResult bubbleSortTasks(List<Task> tasks) {
       if (tasks == null || tasks.isEmpty()) {
           return new SortResult(Collections.emptyList(), 0);
       }

       // Create a new list to avoid modifying the original
       List<Task> sortedTasks = new ArrayList<>(tasks);
       int swapCount = 0;
       boolean swapped;

       for (int i = 0; i < sortedTasks.size() - 1; i++) {
           swapped = false;
           for (int j = 0; j < sortedTasks.size() - 1 - i; j++) {
               Task a = sortedTasks.get(j);
               Task b = sortedTasks.get(j + 1);
               if (shouldSwap(a, b)) {
                   // Swap
                   Task temp = a;
                   sortedTasks.set(j, b);
                   sortedTasks.set(j + 1, temp);
                   swapCount++;
                   swapped = true;
               }
           }
           if (!swapped) break;
       }

       return new SortResult(sortedTasks, swapCount);
   }
   ```

   Wait, `Collections.emptyList()` requires import. I'll use `List.of()` or just `new ArrayList<>()` for empty. Actually, `tasks.isEmpty()` check is fine. I'll just return `new SortResult(new ArrayList<>(), 0)` or handle null/empty gracefully. The problem says "do not modify the original input list — return a new list", so `new ArrayList<>(tasks)` is correct.

   Let's refine the comparison logic into a private static method or inline it. I'll keep it as a private static method for clarity.

   One detail: `Integer` comparison. `a.priority < b.priority` works due to auto-unboxing, but if `priority` is null, we already handled it. So it's safe. But to be strictly safe and idiomatic, I'll use `Integer.compare(b.priority, a.priority)` for descending, but since I already filtered nulls, direct comparison is fine. I'll stick to `a.priority < b.priority` for simplicity, or use `Integer.compare`. Actually, `Integer.compare(b.priority, a.priority)` is cleaner.

   Let's rewrite `shouldSwap` carefully:
   ```java
   private static boolean shouldSwap(Task a, Task b) {
       boolean aNull = a.priority == null;
       boolean bNull = b.priority == null;

       if (aNull && bNull) {
           return a.createdAt > b.createdAt;
       }
       if (aNull) {
           return true; // a should be after b
       }
       if (bNull) {
           return false; // a should be before b
       }

       // Both non-null
       int priorityCmp = Integer.compare(b.priority, a.priority); // descending
       if (priorityCmp != 0) {
           return priorityCmp > 0; // a.priority < b.priority -> swap
       }
       // Equal priority, ascending createdAt
       return a.createdAt > b.createdAt;
   }
   ```
   Wait, `Integer.compare(b.priority, a.priority)` returns:
   - positive if b > a (so a < b) -> should swap
   - negative if b < a (so a > b) -> should not swap
   - zero if equal
   So `priorityCmp > 0` means `b.priority > a.priority`, which means `a` has lower priority, so `a` should come after `b`. Correct.

   Actually, I can simplify:
   ```java
   private static boolean shouldSwap(Task a, Task b) {
       if (a.priority == null && b.priority != null) return true;
       if (a.priority != null && b.priority == null) return false;
       if (a.priority == null && b.priority == null) return a.createdAt > b.createdAt;

       int pCmp = Integer.compare(b.priority, a.priority);
       if (pCmp != 0) return pCmp > 0;
       return a.createdAt > b.createdAt;
   }
   ```
   This is clean.

5.  **Check Constraints & Edge Cases**:
   - "Do not modify the original input list — return a new list": `new ArrayList<>(tasks)` does this.
   - "Return a `SortResult` with the sorted list and total swap count": Handled.
   - "Null handling: tasks where `priority` is `null` always sort to the end... ordered by `createdAt` ascending among themselves": Handled.
   - Bubble sort implementation: Handled.
   - Records: `Task` and `SortResult` are static inner records. Handled.
   - Javadoc: Will add where appropriate.
   - Imports: `java.util.List`, `java.util.ArrayList`, `java.util.Collections` (maybe not needed), `java.util.Objects` (maybe not needed). I'll add necessary imports.

   One thing: `List.of()` in the example creates an immutable list. `new ArrayList<>(tasks)` will create a mutable copy, which is fine for bubble sort. The method signature takes `List<Task> tasks`, so it's fine.

   Let's consider if `tasks` is null. The problem doesn't specify, but it's good practice to handle it or assume non-null. I'll add a null check or just assume valid input per typical coding challenge standards. I'll handle null gracefully by returning empty result.

   Wait, the example uses `List.of(...)`, which returns an immutable list. `new ArrayList<>(tasks)` works fine.

   Let's structure the code:

   ```java
   import java.util.ArrayList;
   import java.util.List;

   public class BubbleSortTasks {

       /**
        * Represents a task with a name, optional priority, and creation timestamp.
        */
       public static record Task(String name, Integer priority, long createdAt) {}

       /**
        * Represents the result of a bubble sort operation on tasks.
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
               return new SortResult(List.of(), 0);
           }

           List<Task> sortedTasks = new ArrayList<>(tasks);
           int swapCount = 0;
           boolean swapped;

           for (int i = 0; i < sortedTasks.size() - 1; i++) {
               swapped = false;
               for (int j = 0; j < sortedTasks.size() - 1 - i; j++) {
                   Task current = sortedTasks.get(j);
                   Task next = sortedTasks.get(j + 1);

                   if (shouldSwap(current, next)) {
                       // Swap adjacent elements
                       sortedTasks.set(j, next);
                       sortedTasks.set(j + 1, current);
                       swapCount++;
                       swapped = true;
                   }
               }
               if (!swapped) {
                   break;
               }
           }

           return new SortResult(sortedTasks, swapCount);
       }

       /**
        * Determines if the first task should be swapped with the second task
        * based on the sorting rules.
        */
       private static boolean shouldSwap(Task a, Task b) {
           boolean aNull = a.priority == null;
           boolean bNull = b.priority == null;

           if (aNull && bNull) {
               // Both null: ascending createdAt
               return a.createdAt > b.createdAt;
           }
           if (aNull) {
               // a is null, b is not: a should come after b
               return true;
           }
           if (bNull) {
               // b is null, a is not: a should come before b
               return false;
           }

           // Both non-null: descending priority
           int priorityCmp = Integer.compare(b.priority, a.priority);
           if (priorityCmp != 0) {
               return priorityCmp > 0; // a has lower priority, so swap
           }

           // Equal priority: ascending createdAt
           return a.createdAt > b.createdAt;
       }
   }
   ```

6.  **Verify against Requirements**:
   - Single file `BubbleSortTasks.java`? Yes.
   - Public class `BubbleSortTasks`? Yes.
   - Static inner `Task` record with `String name`, `Integer priority`, `long createdAt`? Yes.
   - Static inner `SortResult` record with `List<Task> tasks`, `int swapCount`? Yes.
   - Static method `bubbleSortTasks(List<Task> tasks)`? Yes.
   - Sorting rules: priority desc, createdAt asc, null priority to end? Yes.
   - Constraints: bubble sort only, return SortResult, don't modify original? Yes.
   - Example matches? Yes.
   - Clean, documented, idiomatic? Yes. Added Javadoc. Used `List.of()` for empty return. Used `ArrayList` copy. Used standard bubble sort with early exit.

   One minor point: `List.of()` returns an immutable list. The `SortResult` record expects a `List<Task>`. That's fine. But if the caller expects to modify it later, they might get an `UnsupportedOperationException`. The requirement says "return a new list", so `new ArrayList<>(tasks)` is mutable. For the empty case, `List.of()` is fine, or I can use `new ArrayList<>()` for consistency. I'll stick with `List.of()` or `Collections.emptyList()`, but `new ArrayList<>()` is safer if mutability is expected. I'll use `new ArrayList<>()` for consistency.

   Actually, `List.of()` is fine. I'll keep it.

   Let's double check the bubble sort loop bounds. `i` from 0 to `size-2`, `j` from 0 to `size-2-i`. Correct.
   Swap logic: `sortedTasks.set(j, next); sortedTasks.set(j+1, current);` Correct.
   `swapCount` increments correctly.
   Early exit on `!swapped` is standard optimization.

   One thing: The problem says "tasks where `priority` is `null` always sort to the end of the list, ordered by `createdAt` ascending among themselves". My logic handles this correctly.

   Let's test mentally with nulls:
   Tasks: A(1, 100), B(null, 50), C(null, 200)
   Initial: [A, B, C]
   Pass 1:
   - A vs B: A not null, B null -> shouldSwap(A, B) = false. No swap.
   - B vs C: both null, 50 < 200 -> shouldSwap(B, C) = false. No swap.
   Wait, B is before C, and B.createdAt=50, C.createdAt=200. Ascending order means B should come before C. So no swap. Correct.
   What if initial: [B, A, C] -> B(null,50), A(1,100), C(null,200)
   - B vs A: B null, A not -> shouldSwap = true. Swap -> [A, B, C]
   - B vs C: both null, 50 < 200 -> false. No swap.
   Result: [A, B, C]. Correct.

   What if initial: [C, B, A] -> C(null,200), B(null,50), A(1,100)
   - C vs B: both null, 200 > 50 -> true. Swap -> [B, C, A]
   - C vs A: C null, A not -> true. Swap -> [B, A, C]
   Pass 2:
   - B vs A: B null, A not -> true. Swap -> [A, B, C]
   - B vs C: both null, 50 < 200 -> false.
   Result: [A, B, C]. Correct.

   All good.

   One detail: `Integer.compare(b.priority, a.priority)` works correctly. `priorityCmp > 0` means `b.priority > a.priority`, so `a` should be after `b`, so swap. Correct.

   I'll add imports and ensure formatting is clean.
   I'll also make sure the class name matches exactly `BubbleSortTasks`.
   The records are static inner, which matches `public static record Task(...) {}`.
   I'll add a brief comment explaining the sorting rules in the method Javadoc.

   Final check of the code structure:
   ```java
   import java.util.ArrayList;
   import java.util.List;

   public class BubbleSortTasks {

       public static record Task(String name, Integer priority, long createdAt) {}

       public static record SortResult(List<Task> tasks, int swapCount) {}

       public static SortResult bubbleSortTasks(List<Task> tasks) {
           // ...
       }

       private static boolean shouldSwap(Task a, Task b) {
           // ...
       }
   }
   ```
   This matches all requirements. I'll produce the final answer.
   One minor improvement: I'll use `List.copyOf(tasks)`? No, that's Java 10+, but `new ArrayList<>(tasks)` is fine and mutable, which is better for sorting. The requirement says "return a new list", so `ArrayList` is perfect.
   I'll stick with `new ArrayList<>(tasks)`.

   All set. Output matches the request.
   I will generate the code block now. 
   Self-Correction/Refinement during thought:
   - Should I handle `tasks` being null? The problem doesn't specify, but it's safe to return an empty result or throw `IllegalArgumentException`. I'll add a null check returning empty result for robustness, or just assume non-null as per typical CP. I'll keep the null check.
   - The example uses `List.of(...)`, which is immutable. `new ArrayList<>(tasks)` handles it fine.
   - I'll make sure the Javadoc is comprehensive.
   - I'll verify the swap count logic matches the example exactly. Example: 2 swaps. My trace gave 2. Good.
   - I'll ensure the code is idiomatic Java 14+ (records are Java 14+). The prompt uses records, so Java 14+ is assumed.

   Code looks solid. Proceed. 
   Output generation. 
   [Done] 
   Output matches the response. 
   Structure:
   ```java
   import java.util.ArrayList;
   import java.util.List;

   public class BubbleSortTasks {
       // records
       // method
       // helper
   }
   ```
   All constraints met. Javadoc added. Clean code. Ready. 
   Output generation. 
   *(Self-Correction/Verification during drafting)*
   Wait, `List.of()` in Java returns an immutable list. If I return `List.of()` for empty input, it's fine. But for consistency, I'll use `new ArrayList<>()` or just `List.of()`. It doesn't matter much. I'll stick with `List.of()` for empty, or `Collections.emptyList()`. Actually, `new ArrayList<>()` is safer if the caller expects mutability. I'll use `new ArrayList<>()` for both cases to be consistent.

   Also, I should ensure the `shouldSwap` method is `private static` as it's an implementation detail.

   One thing: `Integer.compare(b.priority, a.priority)` is correct. But `priorityCmp > 0` means `b > a`, so `a` should be after `b`, so swap. Correct.

   All good.
   Final code:
   ```java
   import java.util.ArrayList;
   import java.util.List;

   public class BubbleSortTasks {

       /**
        * Represents a task with a name, optional priority, and creation timestamp.
        */
       public static record Task(String name, Integer priority, long createdAt) {}

       /**
        * Represents the result of a bubble sort operation on tasks.
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
               return new SortResult(new ArrayList<>(), 0);
           }

           // Create a mutable copy to avoid modifying the original list
           List<Task> sortedTasks = new ArrayList<>(tasks);
           int swapCount = 0;
           boolean swapped;

           for (int i = 0; i < sortedTasks.size() - 1; i++) {
               swapped = false;
               for (int j = 0; j < sortedTasks.size() - 1 - i; j++) {
                   Task current = sortedTasks.get(j);
                   Task next = sortedTasks.get(j + 1);

                   if (shouldSwap(current, next)) {
                       // Swap adjacent elements
                       sortedTasks.set(j, next);
                       sortedTasks.set(j + 1, current);
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
        * Determines if the first task should be swapped with the second task
        * based on the specified sorting rules.
        *
        * @param a the first task
        * @param b the second task
        * @return true if a should come after b (triggering a swap), false otherwise
        */
       private static boolean shouldSwap(Task a, Task b) {
           boolean aNull = a.priority == null;
           boolean bNull = b.priority == null;

           if (aNull && bNull) {
               // Both null: ascending createdAt
               return a.createdAt > b.createdAt;
           }
           if (aNull) {
               // a is null, b is not: a should come after b
               return true;
           }
           if (bNull) {
               // b is null, a is not: a should come before b
               return false;
           }

           // Both non-null: descending priority
           int priorityCmp = Integer.compare(b.priority, a.priority);
           if (priorityCmp != 0) {
               return priorityCmp > 0; // a has lower priority, so swap
           }

           // Equal priority: ascending createdAt
           return a.createdAt > b.createdAt;
       }
   }
   ```
   This matches all requirements perfectly. I'll output it. 
   One minor point: `List.of()` vs `new ArrayList<>()` for empty. I'll keep `new ArrayList<>()` for consistency. It's fine.
   All good.✅
   Output matches response. 
   Proceeds. 
   [Output Generation] -> *See response.* 
   *(Self-Correction/Note during thought)*: I should verify that `Integer.compare` works correctly with `Integer` objects. Yes, it handles unboxing automatically. Since we already checked for nulls, unboxing is safe.
   The code is ready.✅
   Output matches the final code block.✅
   Done. 
   [Output Generation] -> *Proceeds.*


## Response

Here is the complete, well-documented implementation meeting all your requirements:

```java
import java.util.ArrayList;
import java.util.List;

public class BubbleSortTasks {

    /**
     * Represents a task with a name, optional priority, and creation timestamp.
     */
    public static record Task(String name, Integer priority, long createdAt) {}

    /**
     * Represents the result of a bubble sort operation on tasks.
     */
    public static record SortResult(List<Task> tasks, int swapCount) {}

    /**
     * Sorts a list of tasks using the bubble sort algorithm.
     *
     * <p>Sorting rules:
     * <ol>
     *   <li>Primary: {@code priority} descending (higher priority first)</li>
     *   <li>Tiebreaker: {@code createdAt} ascending (earlier timestamp first)</li>
     *   <li>Null handling: tasks with {@code null} priority sort to the end, 
     *       ordered by {@code createdAt} ascending among themselves</li>
     * </ol>
     *
     * @param tasks the list of tasks to sort
     * @return a {@link SortResult} containing the sorted list and the total number of swaps performed
     */
    public static SortResult bubbleSortTasks(List<Task> tasks) {
        if (tasks == null || tasks.isEmpty()) {
            return new SortResult(new ArrayList<>(), 0);
        }

        // Create a mutable copy to strictly avoid modifying the original input list
        List<Task> sortedTasks = new ArrayList<>(tasks);
        int swapCount = 0;
        boolean swapped;

        for (int i = 0; i < sortedTasks.size() - 1; i++) {
            swapped = false;
            for (int j = 0; j < sortedTasks.size() - 1 - i; j++) {
                Task current = sortedTasks.get(j);
                Task next = sortedTasks.get(j + 1);

                if (shouldSwap(current, next)) {
                    // Swap adjacent elements
                    sortedTasks.set(j, next);
                    sortedTasks.set(j + 1, current);
                    swapCount++;
                    swapped = true;
                }
            }
            // Optimization: if no swaps occurred in a pass, the list is already sorted
            if (!swapped) {
                break;
            }
        }

        return new SortResult(sortedTasks, swapCount);
    }

    /**
     * Determines if the first task should be swapped with the second task
     * based on the specified sorting rules.
     *
     * @param a the first task
     * @param b the second task
     * @return true if {@code a} should come after {@code b} (triggering a swap), false otherwise
     */
    private static boolean shouldSwap(Task a, Task b) {
        boolean aNull = a.priority == null;
        boolean bNull = b.priority == null;

        if (aNull && bNull) {
            // Both null: ascending createdAt
            return a.createdAt > b.createdAt;
        }
        if (aNull) {
            // a is null, b is not: a should come after b
            return true;
        }
        if (bNull) {
            // b is null, a is not: a should come before b
            return false;
        }

        // Both non-null: descending priority
        int priorityCmp = Integer.compare(b.priority, a.priority);
        if (priorityCmp != 0) {
            return priorityCmp > 0; // a has lower priority, so swap
        }

        // Equal priority: ascending createdAt
        return a.createdAt > b.createdAt;
    }
}
```

### Key Implementation Details:
1. **Immutability Preservation**: `new ArrayList<>(tasks)` creates a shallow copy, ensuring the original list passed by the caller remains untouched.
2. **Bubble Sort Optimization**: Uses the standard `swapped` flag to exit early if the list becomes sorted before completing all passes, improving best-case time complexity to `O(n)`.
3. **Null-Safe Comparison**: Explicitly handles `null` priorities before unboxing `Integer` values to prevent `NullPointerException`.
4. **Correct Swap Logic**: `shouldSwap` returns `true` only when the left element should appear *after* the right element according to the rules, which correctly triggers the adjacent swap in bubble sort.
5. **Idiomatic Java**: Uses modern records, `Integer.compare()` for safe numeric comparison, and clear Javadoc documenting the sorting contract.

## Timings

- Time to first token: 0.75s
- Total generation: 112.10s
- Reasoning tokens: 5549
- Answer tokens: 1099
- Total tokens: 6648
