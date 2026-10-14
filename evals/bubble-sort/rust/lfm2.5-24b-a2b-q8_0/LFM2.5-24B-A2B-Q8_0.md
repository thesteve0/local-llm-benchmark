# Code Eval: LFM2.5-24B-A2B-Q8_0

## Prompt

# Bubble Sort Tasks — Rust

in Rust, implement a bubble sort function for task records.

## Requirements

Write a library crate (`src/lib.rs`) containing:

1. A `Task` struct:
   ```rust
   #[derive(Clone, Debug, PartialEq)]
   pub struct Task {
       pub name: String,
       pub priority: Option<i32>,
       pub created_at: i64,
   }
   ```

2. A public function:
   ```rust
   pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize)
   ```

### Sorting Rules

1. **Primary:** sort by `priority` descending (higher priority comes first)
2. **Tiebreaker:** when priorities are equal, sort by `created_at` ascending (earlier timestamp comes first)
3. **None handling:** tasks where `priority` is `None` always sort to the end of the list, ordered by `created_at` ascending among themselves

### Constraints

- You must implement the bubble sort algorithm — do not use `.sort()`, `.sort_by()`, `.sort_unstable_by()`, or any other sorting method
- Return a tuple of `(sorted_vec, swap_count)` where `swap_count` is the total number of element swaps performed during sorting
- Do not modify the input slice — return a new `Vec<Task>`

### Example

```rust
let tasks = vec![
    Task { name: "bug".into(),     priority: Some(3), created_at: 1000 },
    Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
    Task { name: "docs".into(),    priority: Some(3), created_at: 500 },
];

let (sorted, swaps) = bubble_sort_tasks(&tasks);
// sorted = [Task("feature",5,2000), Task("docs",3,500), Task("bug",3,1000)]
// swaps = 2
```

Write clean, well-documented, idiomatic Rust code. Include doc comments (`///`) on public items.


## Reasoning

We need to produce a Rust library crate with src/lib.rs containing the Task struct and bubble_sort_tasks function.

Requirements:

- Implement bubble sort manually (no built-in sorting functions).
- Sorting rules:
  - Primary: priority descending (higher priority first). Since priority is Option<i32>, tasks with Some(p) have priority; tasks with None go to end.
  - Tiebreaker: when priorities equal, sort by created_at ascending (earlier timestamp first).
  - None handling: tasks where priority is None always sort to the end of list, ordered by created_at ascending among themselves.

- Return tuple (Vec<Task>, usize) where Vec is sorted copy (not modifying input). swap_count is total number of swaps performed during bubble sort.

- Must not modify input slice; return a new Vec.

Implementation details:

We need to implement bubble sort algorithm: repeatedly iterate over the list, swapping adjacent elements if they are out of order according to sorting rules. Count each swap.

We need to define ordering comparator: For two tasks a and b:

- If both have Some(priority) vs Some(other_priority):
  - Compare priority descending: higher priority first.
  - If priorities equal:
    - Compare created_at ascending: earlier first.
- If one has None priority:
  - The task with None should be placed after all tasks with Some priority. Among the None tasks, sort by created_at ascending.

Thus bubble sort must treat None as lowest priority (i.e., they go to end). In bubble sort comparisons, we need to decide if a should come before b (i.e., a is "less" than b in sorted order). Since we want descending priority, we can define a function `is_before(a: &Task, b: &Task) -> bool` that returns true if a should appear before b in final sorted list.

Alternatively, bubble sort typical algorithm: for i from 0..n-1, for j from 0..n-2-i (or n-1?), compare adjacent elements at positions j and j+1; if they are out of order (i.e., a > b according to sorting criteria), swap them and increment swap count.

We need to define ordering: For bubble sort ascending order typical: if a > b then swap. But here we have custom comparator.

Define:

fn should_swap(a: &Task, b: &Task) -> bool {
    // returns true if a is currently before b but should be after (i.e., they are out of order)
    // Actually bubble sort typical: if a > b then swap. So we need to define "a > b" according to sorting criteria.
    // Let's define a comparator that returns an ordering: -1 if a < b, 0 if equal, 1 if a > b (i.e., a should come after b).
    // Then bubble sort swaps when comparator says a > b.

    // Determine positions:
    // Cases:
    // - If both have Some(priority):
    //   - Compare priority: higher first. So if a.priority < b.priority => a should be after b => swap needed.
    //   - If priorities equal: compare created_at ascending: earlier first. So if a.created_at > b.created_at => a after b => swap.
    // - If a has Some(priority) and b has None: a should come before b (since None goes to end). So no swap needed.
    // - If a has None and b has Some(priority): then a should be after b => swap needed.
    // - If both have None: compare created_at ascending: earlier first. So if a.created_at > b.created_at => swap.

    // Implementation:
    let a_prio = a.priority;
    let b_prio = b.priority;

    match (a_prio, b_prio) {
        (Some(p_a), Some(p_b)) => {
            if p_a < p_b {
                // a has lower priority than b -> a should be after b -> swap
                true
            } else if p_a > p_b {
                false // a is higher priority, stays before
            } else {
                // equal priority: compare created_at ascending
                if a.created_at > b.created_at {
                    true // a later timestamp => should be after b
                } else {
                    false
                }
            }
        }
        (Some(p_a), None) => {
            // a has priority, b doesn't -> a before b -> no swap
            false
        }
        (None, Some(_)) => {
            // a is None, b has priority -> a should be after b -> swap needed
            true
        }
        (None, None) => {
            // both have no priority: sort by created_at ascending
            if a.created_at > b.created_at {
                true
            } else {
                false
            }
        }
    }
}

But careful: bubble sort algorithm typical: for i in 0..n-1 { for j in 0..n-1-i { if should_swap(&tasks[j], &tasks[j+1]) { swap; swaps++; } } }

We need to count each swap.

Implementation steps:

- In bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize):
    - Create a new Vec<Task> from the slice: let mut sorted = tasks.to_vec(); // clones tasks.
    - let n = sorted.len();
    - let mut swaps = 0usize;
    - Perform bubble sort:
        for i in 0..n {
            // After each pass, the largest element (according to ordering) is at the end? But with custom comparator, we can still use typical bubble sort: iterate j from 0..n-1-i-1? Actually typical bubble sort: for i in 0..n-1 { for j in 0..n-1-i { if a[j] > a[j+1] { swap } } }
            // Since we need to count swaps, we can implement nested loops.
        }

But careful: The typical bubble sort optimization: after each outer iteration i, the last i elements are sorted. So inner loop goes up to n - 1 - i.

Thus:

for i in 0..n {
    for j in 0..(n - 1 - i) {
        if should_swap(&sorted[j], &sorted[j+1]) {
            // swap
            sorted.swap(j, j+1);
            swaps += 1;
        }
    }
}

But note: bubble sort with this pattern will produce correct sorting for any comparator that defines a strict weak ordering. However, we need to ensure that the algorithm terminates and sorts correctly.

Alternatively, we could implement a simple while loop with swapped flag; but given constraints, it's okay.

Now about returning sorted_vec: The sorted vector after bubble sort is the sorted copy.

Edge Cases:

- Empty slice: n=0 => loops not executed; swaps=0; return empty vec.
- Single element: no swaps.

Now about None handling: tasks with priority None go to end. Among themselves, sorted by created_at ascending.

Our comparator handles that: if a is None and b is Some -> swap needed (a after b). If both None -> compare created_at.

Thus bubble sort will push all None tasks to the end.

Now test with example:

tasks = [
    Task { name: "bug", priority: Some(3), created_at: 1000 },
    Task { name: "feature", priority: Some(5), created_at: 2000 },
    Task { name: "docs", priority: Some(3), created_at: 500 },
]

Sorted expected: [feature (prio5), docs (prio3, created_at500), bug (prio3, created_at1000)], swaps=2.

Let's simulate bubble sort:

sorted = copy of tasks.

Indices: 0: bug (3,1000), 1: feature (5,2000), 2: docs (3,500)

We need to see if algorithm yields swaps=2.

Let's manually compute bubble sort passes:

n=3.

i=0: inner loop j from 0..(3-1-0)=2? Actually n-1-i = 2. So j=0,1.

- Compare sorted[0] (bug) and sorted[1] (feature). Should_swap(bug, feature)? Let's compute:

a=bug: Some(3), created_at1000; b=feature: Some(5), created_at2000.

Both have Some. Compare priority: 3 < 5 => a lower priority than b => should_swap returns true (a should be after b). So swap needed. After swap, sorted becomes [feature, bug, docs]; swaps=1.

- Next j=1: compare sorted[1] (bug) and sorted[2] (docs). Now a=bug (Some3), b=docs (Some3). Both have Some priority equal. Compare created_at: 1000 > 500 => a later than b => should_swap true. So swap: sorted becomes [feature, docs, bug]; swaps=2.

End of i=0 pass.

i=1: inner loop j from 0..(3-1-1)=1? Actually n-1-i = 1. So j=0 only.

Compare sorted[0] (feature) and sorted[1] (docs). a=feature (prio5), b=docs (prio3). Since priority descending: higher first => feature > docs, so no swap needed (should_swap false). So final sorted = [feature, docs, bug]; swaps=2.

Matches expected.

Thus algorithm works.

Now we need to implement bubble_sort_tasks with doc comments.

We also need to ensure that the function signature matches: pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize)

Return tuple of sorted Vec and swap count.

Implementation details:

- Use #[derive(Clone, Debug, PartialEq)] on Task.
- Provide doc comment for struct and function.

Potential pitfalls:

- The bubble sort algorithm must not use built-in sorting functions. We'll implement manually.

- Ensure we don't modify input slice: we clone tasks into a new Vec.

- Count swaps correctly: each time we swap two elements, increment swaps.

- Edge Cases: tasks with same priority and created_at? If both equal, order doesn't matter; but comparator will treat them as not needing swap (since a.created_at > b.created_at false). If equal, no swap.

Now about the crate: The problem says "Write a library crate (`src/lib.rs`) containing...". So we need to produce code for src/lib.rs. Possibly also Cargo.toml? Not required but could include minimal crate definition. Usually they'd ask for just lib.rs. But we can provide both.

We'll produce:

```
[package]
name = "bubble_sort_tasks"
version = "0.1.0"
edition = "2021"

[lib]
```

But not necessary. However, to be safe, include Cargo.toml with lib name.

Thus final answer: Provide code for src/lib.rs and optionally Cargo.toml.

We'll also add doc comments:

/// A task record representing a unit of work.
///
/// # Fields
///
/// - `name`: Human-readable name of the task.
/// - `priority`: Optional priority level; tasks with a higher priority are sorted first.
/// - `created_at`: Unix timestamp indicating when the task was created.
#[derive(Clone, Debug, PartialEq)]
pub struct Task { ... }

/// Sorts a slice of tasks using bubble sort according to the specified ordering rules.
///
/// The function returns a tuple containing a new vector with the tasks sorted and the total number of swaps performed during sorting.
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) { ... }

We'll also include private helper function `is_out_of_order(a: &Task, b: &Task) -> bool` maybe.

Implementation details:

```
fn is_out_of_order(a: &Task, b: &Task) -> bool {
    // Returns true if a should come after b (i.e., they are in wrong order for the desired sort)
    let (a_prio, b_prio) = (a.priority, b.priority);
    match (a_prio, b_prio) {
        (Some(p_a), Some(p_b)) => {
            if p_a < p_b {
                true // a has lower priority than b -> should be after
            } else if p_a > p_b {
                false // a higher priority -> stays before
            } else {
                // equal priority: earlier created_at first
                if a.created_at > b.created_at {
                    true
                } else {
                    false
                }
            }
        }
        (Some(p_a), None) => false, // a has priority, b doesn't -> a before b
        (None, Some(_)) => true, // a is None -> should be after b
        (None, None) => {
            if a.created_at > b.created_at {
                true
            } else {
                false
            }
        }
    }
}
```

Then bubble sort:

```
let mut sorted = tasks.to_vec();
let n = sorted.len();
let mut swaps = 0;

for i in 0..n {
    for j in 0..(n - 1 - i) {
        if is_out_of_order(&sorted[j], &sorted[j+1]) {
            sorted.swap(j, j+1);
            swaps += 1;
        }
    }
}
```

Return (sorted, swaps).

Now test with example.

Potential issues: The bubble sort algorithm as written will produce correct ordering? Let's think about correctness for custom comparator. Since bubble sort is stable? Not required. But we need to ensure that after sorting, tasks with None are at end sorted by created_at ascending. Our comparator ensures that when comparing a None vs Some, we treat None as larger (i.e., out-of-order if None appears before Some). In bubble sort, if a is None and b is Some, is_out_of_order returns true => swap needed, moving None to the right. This will push all None tasks to the end. However, does it guarantee that among None tasks they are sorted by created_at ascending? Let's see: When both are None, comparator uses created_at ascending: if a.created_at > b.created_at => out-of-order => swap. That ensures that earlier timestamps move leftwards relative to later ones. Since bubble sort moves elements gradually, it should produce ascending order among None tasks.

Similarly for Some tasks with equal priority: tiebreaker by created_at ascending is handled.

Thus final sorted order matches spec.

Now about swap count: Each swap increments swaps. That's correct.

Potential nuance: In bubble sort, after each pass i, the largest element (according to comparator) is placed at position n-1-i. But our comparator defines "largest" as highest priority then earliest timestamp. However, we don't need to rely on that; just performing full passes will eventually sort.

Now about not modifying input: We clone tasks into new Vec. Good.

Now about returning tuple: (Vec<Task>, usize). That's fine.

Now let's think about edge cases:

- All tasks have None priority: Then comparator treats them as equal priority case with created_at ordering. Bubble sort will sort them by created_at ascending. Swaps count will be number of swaps needed to sort by created_at ascending (like bubble sort on that key). That's okay.

- Mixed priorities: Works.

- Duplicate tasks: If two tasks have same name, priority, created_at? Not relevant.

Now about documentation: Provide doc comments for public items.

Implementation details:

We'll put the helper function `is_out_of_order` as private (no pub). Or we could make it pub(crate) but not needed.

Now produce final code.

We also need to include Cargo.toml? The problem says "Write a library crate (`src/lib.rs`)". Usually they'd expect just lib.rs. But I'll include minimal Cargo.toml for completeness.

Thus final answer: Provide:

```
[package]
name = "bubble_sort_tasks"
version = "0.1.0"
edition = "2021"

[lib]
```

Then src/lib.rs with code.

Let's write the code.

We'll start with:

```rust
//! # Bubble Sort Tasks
//!
//! A small library that implements a bubble sort for task records.
//! The sorting rules are:
//! - Primary: priority descending (higher priority first)
//! - Tiebreaker: created_at ascending when priorities equal
//! - Tasks with `priority` set to `None` are placed at the end, ordered by `created_at` ascending.

use std::fmt::Debug;

/// Represents a task record.
///
/// # Fields
///
/// * `name` - A human-readable name for the task.
/// * `priority` - An optional priority level. Tasks with a higher priority are sorted before those with lower priority.
/// * `created_at` - Unix timestamp indicating when the task was created.
#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    pub name: String,
    pub priority: Option<i32>,
    pub created_at: i64,
}

/// Sorts a slice of tasks using the bubble sort algorithm according to the library's ordering rules.
///
/// The function returns a tuple containing:
/// - A new `Vec<Task>` with the tasks sorted as described below.
/// - The total number of swaps performed while sorting.
///
/// # Sorting Rules
///
/// 1. **Primary:** Tasks are ordered by `priority` in descending order (higher values first).
/// 2. **Tiebreaker:** When two tasks have the same priority, they are ordered by `created_at` in ascending order (earlier timestamps first).
/// 3. **None handling:** Tasks whose `priority` is `None` always appear after all tasks with a defined priority. Among themselves they are sorted by `created_at` ascending.
///
/// # Example
///
/// ```
/// use bubble_sort_tasks::bubble_sort_tasks;
///
/// let tasks = vec![
///     Task { name: "bug".into(), priority: Some(3), created_at: 1000 },
///     Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
///     Task { name: "docs".into(), priority: Some(3), created_at: 500 },
/// ];
///
/// let (sorted, swaps) = bubble_sort_tasks(&tasks);
/// assert_eq!(sorted.len(), 3);
/// // The first element should be the feature task (priority 5)
/// assert_eq!(sorted[0].name, "feature");
/// // The remaining two are ordered by created_at ascending
/// assert_eq!(sorted[1].name, "docs");
/// assert_eq!(sorted[2].name, "bug");
/// assert_eq!(swaps, 2);
/// ```
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    // Create a mutable copy of the input slice.
    let mut sorted = tasks.to_vec();
    let n = sorted.len();
    let mut swap_count = 0usize;

    // Helper closure that determines whether `a` should come after `b`
    // (i.e., they are in the wrong order for the desired sorting).
    fn is_out_of_order(a: &Task, b: &Task) -> bool {
        let a_prio = a.priority;
        let b_prio = b.priority;

        match (a_prio, b_prio) {
            (Some(p_a), Some(p_b)) => {
                // Both have priorities: higher priority first.
                if p_a < p_b {
                    true // a has lower priority -> should be after b
                } else if p_a > p_b {
                    false // a has higher priority -> stays before b
                } else {
                    // Same priority: earlier created_at first.
                    if a.created_at > b.created_at {
                        true
                    } else {
                        false
                    }
                }
            }
            (Some(p_a), None) => {
                // a has a defined priority, b does not -> a should be before b.
                false
            }
            (None, Some(_)) => {
                // a is None, b has a priority -> a must go after b.
                true
            }
            (None, None) => {
                // Both have no priority: order by created_at ascending.
                if a.created_at > b.created_at {
                    true
                } else {
                    false
                }
            }
        }
    }

    // Bubble sort implementation.
    for i in 0..n {
        // After each outer iteration, the last `i` elements are already in their final position.
        for j in 0..(n - 1 - i) {
            if is_out_of_order(&sorted[j], &sorted[j + 1]) {
                sorted.swap(j, j + 1);
                swap_count += 1;
            }
        }
    }

    (sorted, swap_count)
}
```

That's the core.

Now we need to ensure that we didn't use any prohibited sorting functions. We used only .to_vec() and .swap() which are allowed.

Potential improvements: Use `std::mem::replace`? Not needed.

Now test with example manually.

We'll also add a small test in lib.rs? Not required but could include #[cfg(test)] mod tests. But not necessary.

But we might want to show usage.

Given the problem statement, they likely expect just the implementation.

Thus final answer: Provide Cargo.toml and src/lib.rs.

Let's craft final output accordingly.

We'll include comments explaining each part.

Potential issues:

- The comparator uses Option<i32> pattern matching; ensure that we treat None correctly.

- In bubble sort loops, we used n - 1 - i. For n=0 or 1, loops won't execute.

Now about swap count: Should be number of swaps performed. Our algorithm increments each time we swap. That's correct.

Now about returning tuple: (Vec<Task>, usize). Good.

Now about not modifying input: We used to_vec() which clones each Task (since Task contains String and i64, Clone is derived). So input remains unchanged.

Thus final code ready.

We'll produce final answer with both files.

Potential extra: Provide documentation for the crate.

Will include:

```
[package]
name = "bubble_sort_tasks"
version = "0.1.0"
edition = "2021"

[lib]
```

Then src/lib.rs as above.

Now let's double-check everything.

Edge Cases:

Case: tasks = [Task { name: "a", priority: None, created_at: 100 }, Task { name: "b", priority: Some(1), created_at: 200 }].

Our comparator: For a (None) vs b (Some): is_out_of_order(a,b)? Let's compute: a_prio=None, b_prio=Some(1). In match arms: (None, Some(_)) => true. So swap needed. After swap, sorted becomes [b, a]. Then bubble sort will finish. Swaps=1. Sorted order: b first (priority 1), then a (None). Among None tasks only one, fine.

If there are multiple None tasks: e.g., tasks: None at 300, None at 100, None at 200. Our comparator for both None: if a.created_at > b.created_at => out-of-order. This will cause bubble sort to reorder them ascending by created_at. Let's test quickly: initial order: [c(300), a(100), b(200)]? Actually let's simulate: Suppose tasks = [c(300), a(100), b(200)], all None. Bubble sort passes:

n=3.

i=0: j=0 compare c vs a: a.created_at 300 > 100 => out-of-order => swap -> [a,c,b]; swaps=1.
j=1 compare c vs b: c.created_at 300 > 200 => swap -> [a,b,c]; swaps=2.

i=1: j=0 compare a vs b: a.created_at 100 < 200 => no swap. End. Sorted = [a(100), b(200), c(300)] ascending. Good.

Thus works.

Now about priority descending: Suppose tasks have Some priorities: Some(5) and Some(3). Our comparator: p_a < p_b => true (swap needed). That ensures higher priority moves forward. In bubble sort, we compare adjacent pairs; if lower priority is before higher, swap. This will eventually bring higher priority to front.

Now about tiebreaker: If priorities equal, compare created_at ascending: if a.created_at > b.created_at => swap. That ensures earlier timestamp moves leftwards (i.e., appears earlier). In bubble sort, when we have two tasks with same priority but reversed timestamps, they will be swapped.

Thus overall correct.

Now about performance: Not needed.

Now about code style: Use idiomatic Rust, doc comments.

Potential improvements: Use `#[allow(dead_code)]`? Not needed.

Now final answer: Provide Cargo.toml and src/lib.rs.

We'll embed the code in markdown fences.

Thus final output:

```
# Cargo.toml
[package]
name = "bubble_sort_tasks"
version = "0.1.0"
edition = "2021"

[lib]
```

Then src/lib.rs with code.

Make sure to include `use std::fmt::Debug;`? Actually we don't need import for Debug because derive provides it. But we can keep.

Better to not import anything unnecessary.

Alright.

Now produce final answer.


## Response



**Cargo.toml**

```toml
[package]
name = "bubble_sort_tasks"
version = "0.1.0"
edition = "2021"

[lib]
```

**src/lib.rs**

```rust
//! # Bubble Sort Tasks
//!
//! A tiny library that implements a bubble‑sort for task records.
//!
//! # Sorting rules
//!
//! 1. **Primary:** tasks are ordered by `priority` in *descending* order (higher values first).
//! 2. **Tiebreaker:** when two tasks have the same priority, they are ordered by
//!    `created_at` in *ascending* order (earlier timestamps first).
//! 3. **None handling:** tasks whose `priority` is `None` always appear after all
//!    tasks with a defined priority. Among themselves they are sorted by
//!    `created_at` ascending.
//!
//! The function returns the sorted vector together with the total number of swaps
//! performed while sorting.

/// A task record representing a unit of work.
///
/// # Fields
///
/// * `name` – Human‑readable name of the task.
/// * `priority` – Optional priority level. Higher values are sorted first.
/// * `created_at` – Unix timestamp indicating when the task was created.
#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    pub name: String,
    pub priority: Option<i32>,
    pub created_at: i64,
}

/// Sorts a slice of tasks using the bubble‑sort algorithm according to the
/// library's ordering rules.
///
/// # Returns
///
/// A tuple `(sorted_vec, swap_count)` where:
/// * `sorted_vec` – a new `Vec<Task>` containing the tasks in the correct order.
/// * `swap_count` – the total number of element swaps performed during sorting.
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    // Work on a copy so the original slice is never modified.
    let mut sorted = tasks.to_vec();
    let n = sorted.len();
    let mut swap_count = 0usize;

    /// Determines whether `a` should come *after* `b` in the final ordering.
    fn is_out_of_order(a: &Task, b: &Task) -> bool {
        let a_prio = a.priority;
        let b_prio = b.priority;

        match (a_prio, b_prio) {
            // Both tasks have explicit priorities → higher priority first.
            (Some(p_a), Some(p_b)) => {
                if p_a < p_b {
                    true // a has lower priority → needs to move right
                } else if p_a > p_b {
                    false // a has higher priority → stays left
                } else {
                    // Same priority: earlier created_at first.
                    if a.created_at > b.created_at {
                        true
                    } else {
                        false
                    }
                }
            }
            // Task with a priority vs. a task without a priority.
            (Some(_), None) => false, // defined priority comes before None
            (None, Some(_)) => true,  // None must be placed after any defined priority
            // Both have no priority → order by created_at ascending.
            (None, None) => {
                if a.created_at > b.created_at {
                    true
                } else {
                    false
                }
            }
        }
    }

    // Classic bubble‑sort implementation.
    for i in 0..n {
        // After each outer pass the last `i` elements are already settled.
        for j in 0..(n - 1 - i) {
            if is_out_of_order(&sorted[j], &sorted[j + 1]) {
                sorted.swap(j, j + 1);
                swap_count += 1;
            }
        }
    }

    (sorted, swap_count)
}
```

The implementation follows all the requirements:

* `Task` is defined with the required fields and derives `Clone`, `Debug`, and `PartialEq`.
* `bubble_sort_tasks` returns a new `Vec<Task>` (the input slice is never mutated) together with the total number of swaps.
* The sorting follows the three rules: descending priority, ascending `created_at` as tiebreaker, and `None` priorities placed at the end ordered by `created_at`.
* Only manual bubble‑sort logic is used; no built‑in sorting methods are employed.

## Timings

- Time to first token: 0.27s
- Temperature: 0.0
- Total generation: 91.96s
- Reasoning tokens: 5547
- Answer tokens: 999
- Total tokens: 6546

## Server Timings (llama.cpp)

- Prompt tokens: 460
- Prompt eval speed: 1707.50 t/s
- Prompt eval time: 269.40 ms
- Generation tokens: 6546
- Generation speed: 71.38 t/s
- Generation time: 91687.02 ms
