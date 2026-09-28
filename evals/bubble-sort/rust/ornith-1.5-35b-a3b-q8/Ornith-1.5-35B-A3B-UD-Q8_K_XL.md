# Code Eval: Ornith-1.5-35B-A3B-UD-Q8_K_XL

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

Let me analyze this task carefully.

I need to implement a bubble sort function for task records in Rust.

Let me understand the requirements:

1. A `Task` struct with `name: String`, `priority: Option<i32>`, `created_at: i64`.

2. A public function `bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize)`.

Sorting Rules:
1. Primary: sort by `priority` descending (higher priority comes first)
2. Tiebreaker: when priorities are equal, sort by `created_at` ascending (earlier timestamp comes first)
3. None handling: tasks where `priority` is `None` always sort to the end of the list, ordered by `created_at` ascending among themselves

Constraints:
- Must implement bubble sort — no `.sort()`, `.sort_by()`, etc.
- Return `(sorted_vec, swap_count)` where `swap_count` is total number of element swaps.
- Do not modify input slice — return a new `Vec<Task>`.

Let me think about the comparison logic.

I need a comparison function that determines the ordering. Let me define a function `is_before(a: &Task, b: &Task) -> bool` that returns true if `a` should come before `b`.

For bubble sort, we swap adjacent elements if they are out of order. So I need to determine when two adjacent elements are in the wrong order.

Let me think about the ordering:
- If both have priorities (Some), compare by priority descending, then created_at ascending.
- If one has priority and other doesn't, the one with priority comes first.
- If both don't have priority, compare by created_at ascending.

Let me write a comparison function:

```rust
fn task_before(a: &Task, b: &Task) -> bool {
    match (a.priority, b.priority) {
        (Some(pa), Some(pb)) => {
            if pa != pb {
                pa > pb  // higher priority first
            } else {
                a.created_at < b.created_at  // earlier first
            }
        }
        (Some(_), None) => true,   // a has priority, b doesn't, a comes first
        (None, Some(_)) => false,  // a doesn't have priority, b does, b comes first
        (None, None) => a.created_at < b.created_at,  // earlier first
    }
}
```

Wait, but there's a subtlety with bubble sort stability. Bubble sort is stable if we only swap when strictly out of order (i.e., when `a` should come strictly before `b`, we swap). If two elements are "equal" (neither comes before the other), we don't swap, preserving their relative order.

Let me think about the example:
```
tasks = [
    Task("bug", Some(3), 1000),
    Task("feature", Some(5), 2000),
    Task("docs", Some(3), 500),
]
```

Expected sorted: `[Task("feature",5,2000), Task("docs",3,500), Task("bug",3,1000)]`
Expected swaps: 2

Let me trace through bubble sort.

Initial: [bug(3,1000), feature(5,2000), docs(3,500)]

Pass 1:
- Compare bug(3,1000) and feature(5,2000): should bug come before feature? pa=3, pb=5, 3 != 5, 3 > 5? No. So bug should NOT come before feature. They're out of order, swap.
  - [feature(5,2000), bug(3,1000), docs(3,500)], swaps = 1
- Compare bug(3,1000) and docs(3,500): should bug come before docs? pa=3, pb=3, equal, 1000 < 500? No. So bug should NOT come before docs. Out of order, swap.
  - [feature(5,2000), docs(3,500), bug(3,1000)], swaps = 2

Pass 2:
- Compare feature(5,2000) and docs(3,500): should feature come before docs? pa=5, pb=3, 5 != 3, 5 > 3? Yes. So feature comes before docs. In order, no swap.
- Compare docs(3,500) and bug(3,1000): should docs come before bug? pa=3, pb=3, equal, 500 < 1000? Yes. So docs comes before bug. In order, no swap.

No swaps in pass 2, so we can stop.

Final: [feature(5,2000), docs(3,500), bug(3,1000)], swaps = 2. ✓

Great, my comparison logic works.

Now let me implement bubble sort:

```rust
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    let mut sorted = tasks.to_vec();
    let n = sorted.len();
    let mut swap_count = 0usize;
    
    for i in 0..n {
        let mut swapped = false;
        for j in 0..n - i - 1 {
            if !task_before(&sorted[j], &sorted[j + 1]) {
                sorted.swap(j, j + 1);
                swap_count += 1;
                swapped = true;
            }
        }
        if !swapped {
            break;
        }
    }
    
    (sorted, swap_count)
}
```

Wait, there's an edge case. If `n - i - 1` underflows when `i = n - 1`... Let me check. When `i = n - 1`, `n - i - 1 = n - (n-1) - 1 = 0`. So the inner loop `0..0` doesn't execute. Good. But wait, if `n = 0`, then `0..0` for the outer loop, no iterations. Good.

Actually, let me reconsider. `n - i - 1` where `i` ranges from `0` to `n-1`. When `i = n-1`, `n - i - 1 = 0`. Since these are usize, `n - i` when `i = n` would underflow, but `i` only goes up to `n-1`, so `n - i` is at least 1, and `n - i - 1` is at least 0. Good, no underflow.

Actually wait, let me double check the loop bounds. `for i in 0..n` means `i` goes from 0 to n-1. For each i, the inner loop is `for j in 0..(n - i - 1)`. When i = n-1, n - i - 1 = 0, so inner loop doesn't run. That's fine.

Hmm, but actually there's a subtle issue. The standard bubble sort optimization: after pass i, the last i elements are in their final position. So we compare up to n - i - 1. Let me re-examine.

Actually, let me reconsider the standard bubble sort. In each pass, we bubble the largest element to the end. After pass 1, the largest is at position n-1. After pass 2, the second largest is at position n-2. Etc.

In pass i (0-indexed), we compare adjacent pairs from index 0 to n-2-i. So the inner loop goes from j=0 to j=n-2-i, i.e., `0..(n-1-i)`. That's what I have: `0..n - i - 1`. Good.

Let me verify with the example again. n=3.
- i=0: j in 0..2, so j=0,1. Compare (0,1) and (1,2).
- i=1: j in 0..1, so j=0. Compare (0,1).
- i=2: j in 0..0, no iterations.

That matches my trace. Good.

Now, let me think about the `task_before` function more carefully. Actually, I realize I should think about whether to use a comparison approach or the "before" approach.

For bubble sort, the key insight is: we swap `sorted[j]` and `sorted[j+1]` if they are in the wrong order, i.e., if `sorted[j+1]` should come before `sorted[j]`. Equivalently, if NOT (`sorted[j]` should come before `sorted[j+1]`).

But we need to be careful about the "equal" case. If neither comes before the other (they're "equal" in ordering), we should NOT swap, to maintain stability.

My `task_before` returns true only when `a` strictly comes before `b`. If they're equal (same priority, same created_at), it returns false, and we don't swap. Good, that maintains stability.

Wait, let me reconsider. If `task_before(a, b)` is false, we swap. But if `a` and `b` are equal (task_before false both ways), we'd swap them, which would break stability!

Let me reconsider. In bubble sort, the condition to swap is: `a` should come after `b`, i.e., `b` should come before `a`. So the swap condition should be `task_before(&sorted[j+1], &sorted[j])`.

Let me redo this. We want to swap `sorted[j]` and `sorted[j+1]` if `sorted[j+1]` should come before `sorted[j]`.

```rust
if task_before(&sorted[j + 1], &sorted[j]) {
    sorted.swap(j, j + 1);
    swap_count += 1;
    swapped = true;
}
```

This is cleaner and handles the equal case correctly: if `a` and `b` are equal, `task_before(b, a)` is false, so we don't swap. 

Let me re-verify with the example.

Initial: [bug(3,1000), feature(5,2000), docs(3,500)]

Pass 1 (i=0):
- j=0: compare sorted[1]=feature(5,2000) and sorted[0]=bug(3,1000). task_before(feature, bug)? pa=5, pb=3, 5>3? Yes. So feature comes before bug. Swap.
  - [feature(5,2000), bug(3,1000), docs(3,500)], swaps=1
- j=1: compare sorted[2]=docs(3,500) and sorted[1]=bug(3,1000). task_before(docs, bug)? pa=3, pb=3, equal, 500<1000? Yes. So docs comes before bug. Swap.
  - [feature(5,2000), docs(3,500), bug(3,1000)], swaps=2

Pass 2 (i=1):
- j=0: compare sorted[1]=docs(3,500) and sorted[0]=feature(5,2000). task_before(docs, feature)? pa=3, pb=5, 3>5? No. So docs does not come before feature. No swap.

No swaps in pass 2, break.

Final: [feature(5,2000), docs(3,500), bug(3,1000)], swaps=2. ✓

Both approaches give the same result for this example, but the second approach (checking `task_before(b, a)`) is more correct for stability. Let me use that.

Actually, let me reconsider. The two approaches:
1. Swap if `!task_before(a, b)` — this swaps when a doesn't come before b, including when they're equal. This is NOT stable.
2. Swap if `task_before(b, a)` — this swaps only when b strictly comes before a. This IS stable.

For a correct, stable bubble sort, approach 2 is correct. Let me use approach 2.

Hmm wait, but actually let me reconsider whether the problem wants stability. The problem says "Tiebreaker: when priorities are equal, sort by created_at ascending". So if two tasks have the same priority AND the same created_at, their relative order is unspecified. In that case, stability doesn't matter for correctness. But it's still good practice to be stable.

Actually, let me reconsider. If two tasks have the same priority and same created_at, then `task_before(a, b)` is false and `task_before(b, a)` is false. With approach 1, we'd swap them (since `!task_before(a,b)` is true). With approach 2, we wouldn't swap (since `task_before(b,a)` is false). Both give a valid result since their order doesn't matter. But approach 2 is more stable/correct.

Let me go with approach 2.

Now let me also think about the `swap_count`. The problem says "the total number of element swaps performed during sorting". So each `sorted.swap()` call counts as one swap. My implementation increments `swap_count` by 1 for each swap. Good.

Let me now write the full code with doc comments.

```rust
//! Bubble sort implementation for task records.
//!
//! This crate provides a [`Task`] type and a [`bubble_sort_tasks`] function
//! that sorts tasks according to a well-defined ordering using the bubble
//! sort algorithm.

/// A single task to be sorted.
///
/// * [`Task::priority`] — optional priority; `None` tasks are always sorted to
///   the end of the list.
/// * [`Task::created_at`] — Unix timestamp (seconds) used as a tiebreaker.
#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    /// Human-readable name of the task.
    pub name: String,
    /// Optional priority. Higher values mean higher priority.
    ///
    /// When `None`, the task is always sorted to the end of the list.
    pub priority: Option<i32>,
    /// Creation timestamp, in seconds since the Unix epoch.
    pub created_at: i64,
}

/// Returns `true` if `a` should be placed strictly before `b` in the sorted
/// order.
///
/// Ordering rules:
/// 1. Higher [`Task::priority`] comes first.
/// 2. When priorities are equal, the earlier [`Task::created_at`] comes first.
/// 3. Tasks with `priority == None` always come after tasks with a priority,
///    and among themselves are ordered by `created_at` ascending.
///
/// Returns `false` when `a` should come after `b` or when the two tasks are
/// equivalent for ordering purposes (same priority and same `created_at`).
fn task_comes_before(a: &Task, b: &Task) -> bool {
    match (a.priority, b.priority) {
        (Some(pa), Some(pb)) => {
            if pa != pb {
                pa > pb
            } else {
                a.created_at < b.created_at
            }
        }
        (Some(_), None) => true,
        (None, Some(_)) => false,
        (None, None) => a.created_at < b.created_at,
    }
}

/// Sorts `tasks` using bubble sort and returns the sorted vector together with
/// the number of element swaps performed.
///
/// The input slice is not mutated; a new [`Vec`] is allocated and returned.
///
/// See [`task_comes_before`] for the exact ordering rules.
///
/// # Examples
///
/// ```
/// use bubble_sort_tasks::Task;
/// use bubble_sort_tasks::bubble_sort_tasks;
///
/// let tasks = vec![
///     Task { name: "bug".into(), priority: Some(3), created_at: 1000 },
///     Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
///     Task { name: "docs".into(), priority: Some(3), created_at: 500 },
/// ];
///
/// let (sorted, swaps) = bubble_sort_tasks(&tasks);
/// assert_eq!(
///     sorted,
///     vec![
///         Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
///         Task { name: "docs".into(), priority: Some(3), created_at: 500 },
///         Task { name: "bug".into(), priority: Some(3), created_at: 1000 },
///     ]
/// );
/// assert_eq!(swaps, 2);
/// ```
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    // Work on a clone so the input slice is never mutated.
    let mut sorted = tasks.to_vec();
    let n = sorted.len();
    let mut swap_count = 0usize;

    for end in (0..n).rev() {
        // `end` is the index of the last unsorted element.
        let mut swapped = false;
        for j in 0..end {
            // Swap when the next element should come before the current one.
            if task_comes_before(&sorted[j + 1], &sorted[j]) {
                sorted.swap(j, j + 1);
                swap_count += 1;
                swapped = true;
            }
        }
        // If nothing was swapped in this pass, the list is already sorted.
        if !swapped {
            break;
        }
    }

    (sorted, swap_count)
}
```

Wait, I changed the loop structure. Let me reconsider. I used `for end in (0..n).rev()`. This iterates from n-1 down to 0. In each iteration, `end` is the index of the last element to compare against. So the inner loop is `for j in 0..end`, comparing `sorted[j]` and `sorted[j+1]` for j from 0 to end-1.

Let me verify with the example. n=3.
- end=2: j in 0..2, j=0,1. Compare (0,1) and (1,2).
- end=1: j in 0..1, j=0. Compare (0,1).
- end=0: j in 0..0, no iterations.

That matches. Good.

Actually, both loop structures are equivalent. Let me use the more standard one for clarity. Actually, the `(0..n).rev()` with `end` is a common way to write bubble sort. But let me reconsider which is clearer.

Standard version:
```rust
for i in 0..n {
    let mut swapped = false;
    for j in 0..(n - i - 1) {
        if task_comes_before(&sorted[j + 1], &sorted[j]) {
            sorted.swap(j, j + 1);
            swap_count += 1;
            swapped = true;
        }
    }
    if !swapped {
        break;
    }
}
```

The `(0..n).rev()` version:
```rust
for end in (0..n).rev() {
    let mut swapped = false;
    for j in 0..end {
        if task_comes_before(&sorted[j + 1], &sorted[j]) {
            sorted.swap(j, j + 1);
            swap_count += 1;
            swapped = true;
        }
    }
    if !swapped {
        break;
    }
}
```

Both are fine. The `(0..n).rev()` version avoids the `n - i - 1` computation and is arguably clearer. But there's a subtle issue: when `n = 0`, `(0..0).rev()` is empty, so no iterations. Good. When `n = 1`, `(0..1).rev()` gives `[0]`, and inner loop `0..0` doesn't run. So no swaps, which is correct for a single element. Good.

Hmm, actually let me reconsider. For `n = 1`, the list is trivially sorted, and we should return `(vec![task], 0)`. With my code, `end = 0`, inner loop `0..0` doesn't run, `swapped` stays false, break. Returns `(sorted, 0)`. Good.

Let me go with the `(0..n).rev()` version as it's cleaner.

Actually, I realize I should double-check: does `(0..n).rev()` work correctly? In Rust, `(0..n)` is a `Range<usize>`, and `.rev()` gives a `RangeRev<usize>`. Iterating gives n-1, n-2, ..., 1, 0. Yes. Good.

Now, let me reconsider the crate name. The problem says "Write a library crate (`src/lib.rs`)". So I need a `Cargo.toml` too. Let me provide that.

For the example in the doc comment, I use `use bubble_sort_tasks::Task;`. The crate name would be `bubble_sort_tasks` if the Cargo.toml has `name = "bubble_sort_tasks"`. Let me set that.

Actually, crate names with underscores... Rust crate names can have underscores. The package name `bubble_sort_tasks` would produce a crate that's imported as `bubble_sort_tasks`. Good.

Let me write the Cargo.toml:

```toml
[package]
name = "bubble_sort_tasks"
version = "0.1.0"
edition = "2021"

[lib]
name = "bubble_sort_tasks"
path = "src/lib.rs"
```

Actually, the default lib path is `src/lib.rs`, so I don't strictly need the `[lib]` section. But it doesn't hurt. Let me keep it minimal.

```toml
[package]
name = "bubble_sort_tasks"
version = "0.1.0"
edition = "2021"
```

Now let me also add some unit tests to demonstrate correctness. The problem doesn't explicitly ask for tests, but it's good practice. Let me add a `#[cfg(test)]` module.

Actually, the problem says "Write clean, well-documented, idiomatic Rust code. Include doc comments (`///`) on public items." It doesn't require tests, but including them is good. Let me add tests to verify the behavior, including the example and edge cases (None handling, empty list, single element, stability).

Let me write tests:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    fn task(name: &str, priority: Option<i32>, created_at: i64) -> Task {
        Task {
            name: name.to_string(),
            priority,
            created_at,
        }
    }

    #[test]
    fn example_from_spec() {
        let tasks = vec![
            task("bug", Some(3), 1000),
            task("feature", Some(5), 2000),
            task("docs", Some(3), 500),
        ];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(
            sorted,
            vec![
                task("feature", Some(5), 2000),
                task("docs", Some(3), 500),
                task("bug", Some(3), 1000),
            ]
        );
        assert_eq!(swaps, 2);
    }

    #[test]
    fn none_tasks_go_to_end() {
        let tasks = vec![
            task("a", None, 100),
            task("b", Some(1), 100),
            task("c", None, 50),
            task("d", Some(2), 10),
        ];
        let (sorted, _) = bubble_sort_tasks(&tasks);
        assert_eq!(
            sorted,
            vec![
                task("d", Some(2), 10),
                task("b", Some(1), 100),
                task("c", None, 50),
                task("a", None, 100),
            ]
        );
    }

    #[test]
    fn empty_list() {
        let tasks: Vec<Task> = vec![];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert!(sorted.is_empty());
        assert_eq!(swaps, 0);
    }

    #[test]
    fn single_element() {
        let tasks = vec![task("only", Some(1), 1)];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, tasks);
        assert_eq!(swaps, 0);
    }

    #[test]
    fn already_sorted_no_swaps() {
        let tasks = vec![
            task("a", Some(3), 1),
            task("b", Some(3), 2),
            task("c", Some(2), 1),
        ];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, tasks);
        assert_eq!(swaps, 0);
    }

    #[test]
    fn input_not_mutated() {
        let tasks = vec![
            task("a", Some(1), 1),
            task("b", Some(2), 2),
        ];
        let original = tasks.clone();
        let (sorted, _) = bubble_sort_tasks(&tasks);
        assert_eq!(tasks, original);
        assert_ne!(sorted, tasks);
    }

    #[test]
    fn all_none() {
        let tasks = vec![
            task("a", None, 30),
            task("b", None, 10),
            task("c", None, 20),
        ];
        let (sorted, _) = bubble_sort_tasks(&tasks);
        assert_eq!(
            sorted,
            vec![
                task("b", None, 10),
                task("c", None, 20),
                task("a", None, 30),
            ]
        );
    }
}
```

Let me verify the `none_tasks_go_to_end` test.
tasks = [a(None,100), b(Some(1),100), c(None,50), d(Some(2),10)]
Expected: [d(Some(2),10), b(Some(1),100), c(None,50), a(None,100)]

Let me trace:
- d has priority 2, b has priority 1, so d before b. ✓
- b has priority 1, c and a have None, so b before c and a. ✓
- c(None,50) and a(None,100): both None, c has earlier created_at (50 < 100), so c before a. ✓

Good.

Let me verify `already_sorted_no_swaps`:
tasks = [a(Some(3),1), b(Some(3),2), c(Some(2),1)]
- a and b: same priority 3, a created_at 1 < b created_at 2, so a before b. In order.
- b and c: b priority 3 > c priority 2, so b before c. In order.
So already sorted, 0 swaps. ✓

Now let me trace through the bubble sort for `none_tasks_go_to_end` to make sure the swap count is reasonable (though I don't assert it).

tasks = [a(None,100), b(Some(1),100), c(None,50), d(Some(2),10)], n=4.

Pass end=3:
- j=0: compare sorted[1]=b(Some(1),100) and sorted[0]=a(None,100). task_comes_before(b, a)? b has Some(1), a has None. Match (Some, None) => true. So b comes before a. Swap.
  - [b(Some(1),100), a(None,100), c(None,50), d(Some(2),10)], swaps=1
- j=1: compare sorted[2]=c(None,50) and sorted[1]=a(None,100). task_comes_before(c, a)? Both None, c.created_at 50 < a.created_at 100? Yes. So c comes before a. Swap.
  - [b(Some(1),100), c(None,50), a(None,100), d(Some(2),10)], swaps=2
- j=2: compare sorted[3]=d(Some(2),10) and sorted[2]=a(None,100). task_comes_before(d, a)? d has Some(2), a has None. (Some, None) => true. So d comes before a. Swap.
  - [b(Some(1),100), c(None,50), d(Some(2),10), a(None,100)], swaps=3

Pass end=2:
- j=0: compare sorted[1]=c(None,50) and sorted[0]=b(Some(1),100). task_comes_before(c, b)? c has None, b has Some(1). (None, Some) => false. So c does not come before b. No swap.
- j=1: compare sorted[2]=d(Some(2),10) and sorted[1]=c(None,50). task_comes_before(d, c)? d has Some(2), c has None. (Some, None) => true. So d comes before c. Swap.
  - [b(Some(1),100), d(Some(2),10), c(None,50), a(None,100)], swaps=4

Pass end=1:
- j=0: compare sorted[1]=d(Some(2),10) and sorted[0]=b(Some(1),100). task_comes_before(d, b)? d has Some(2), b has Some(1). (Some, Some), 2 != 1, 2 > 1? Yes. So d comes before b. Swap.
  - [d(Some(2),10), b(Some(1),100), c(None,50), a(None,100)], swaps=5

Pass end=0:
- j in 0..0, no iterations.

Final: [d(Some(2),10), b(Some(1),100), c(None,50), a(None,100)], swaps=5.

That matches the expected order. 

Now, let me reconsider the doc comment example. I want to make sure it compiles. The `into()` for String... `"bug".into()` — the type needs to be inferred. In the context of `Task { name: "bug".into(), ... }`, the `name` field is `String`, so `"bug".into()` should infer to `String`. Actually, `into()` requires a target type. Since `name: String`, the compiler should infer `"bug".into()` as `String::from("bug")`. This works because `&str: Into<String>`. Good.

Actually, let me double check. In the example in the problem statement, they use `"bug".into()`. This works because the field type is known to be `String`. Good.

Let me also reconsider: should I use `String::from` or `.to_string()` in tests? Both work. I used `.to_string()` in the helper. Good.

Now, let me reconsider the overall structure. The problem asks for `src/lib.rs`. I'll provide the lib.rs content and mention the Cargo.toml.

Let me also think about whether there are any clippy warnings. The `task_comes_before` function is private, so it doesn't need doc comments, but I added one anyway. Actually, clippy might warn about the private function... no, clippy doesn't require docs on private functions. But it's fine to have them.

Wait, actually, there might be a clippy lint about the match. Let me think. The match on `(a.priority, b.priority)` where both are `Option<i32>`. This is fine.

Hmm, one thing: clippy might suggest using `partial_cmp` or something, but since we're doing custom logic, it's fine.

Let me reconsider the naming. `task_comes_before` is a good name. Alternatively `is_before`. Let me keep `task_comes_before`.

Actually, let me reconsider whether I should make the comparison function public or keep it private. The problem only requires the `Task` struct and `bubble_sort_tasks` function to be public. The comparison helper can be private. I'll keep it private.

Let me also reconsider the return type. `(Vec<Task>, usize)`. Good.

Now, let me reconsider the edge case where the input is empty. `tasks.to_vec()` gives an empty vec. `n = 0`. `(0..0).rev()` is empty. Returns `(empty_vec, 0)`. Good.

Let me also think about performance. Bubble sort is O(n²), which is expected for this task. The problem explicitly requires bubble sort, so that's fine.

Let me finalize the code.

Actually, let me reconsider the doc comment for the crate. I'll add a crate-level doc comment.

Let me also reconsider: the problem says "Include doc comments (`///`) on public items." So I need `///` on `Task`, its fields, and `bubble_sort_tasks`. I have those. The `task_comes_before` is private, so `///` is optional but I'll keep it for clarity (or use `//` — actually doc comments on private items are fine and can be useful). Let me keep the doc comment but maybe note it's an internal helper.

Actually, let me reconsider. Having a `///` doc comment on a private function is fine. But some might argue it's unnecessary. I'll keep a brief one.

Let me write the final version.

One more consideration: the `#[derive(Clone, Debug, PartialEq)]` must be exactly as specified. I have it. Good.

Let me also make sure the struct fields are exactly as specified:
```rust
pub struct Task {
    pub name: String,
    pub priority: Option<i32>,
    pub created_at: i64,
}
```
Good.

Let me write the final lib.rs.

Actually, I want to reconsider the loop one more time for correctness and clarity. Let me use the classic nested loop with a clear comment.

I'll go with:
```rust
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    // Clone the input so the caller's slice is never mutated.
    let mut sorted = tasks.to_vec();
    let n = sorted.len();
    let mut swap_count = 0usize;

    // `last` is the index of the last element that is still unsorted.
    // After each full pass the largest remaining element settles at `last`.
    for last in (0..n).rev() {
        let mut swapped = false;

        // Compare each adjacent pair within the unsorted region.
        for j in 0..last {
            // Swap when the right element should come before the left one.
            if task_comes_before(&sorted[j + 1], &sorted[j]) {
                sorted.swap(j, j + 1);
                swap_count += 1;
                swapped = true;
            }
        }

        // No swaps means the list is fully sorted; stop early.
        if !swapped {
            break;
        }
    }

    (sorted, swap_count)
}
```

This is clean and well-documented.

Let me reconsider: is there any issue with `for last in (0..n).rev()` when n=0? `(0..0).rev()` yields nothing. Good. When n=1, yields [0], inner loop `0..0` empty. Good.

Alright, I'm confident in the implementation. Let me also add a brief explanation in the response.

Let me reconsider whether I should include the Cargo.toml. The problem says "Write a library crate (`src/lib.rs`)". So the main deliverable is `src/lib.rs`. But to make it a complete crate, I should mention Cargo.toml. I'll include it for completeness.

Let me also double-check the doc test. The doc test uses `use bubble_sort_tasks::Task;` and `use bubble_sort_tasks::bubble_sort_tasks;`. For this to work, the crate must be named `bubble_sort_tasks`. With edition 2021, the crate name in `use` statements is the package name. Good.

Actually, wait. In Rust, when you write `use bubble_sort_tasks::Task;`, the `bubble_sort_tasks` refers to the crate name. The crate name is derived from the package name in Cargo.toml (with hyphens converted to underscores, but here it's already underscores). So `bubble_sort_tasks` is correct. Good.

Let me finalize.

Actually, I realize I should double check: does the doc example compile with `into()`? Let me think again.

```rust
let tasks = vec![
    Task { name: "bug".into(), priority: Some(3), created_at: 1000 },
    ...
];
```

Here, `Task { name: ..., ... }` — the `name` field is `String`. So `"bug".into()` needs to produce a `String`. Since `&str: Into<String>`, and the expected type is `String`, this works. The compiler infers the target type of `into()` from the field type. Good.

But wait, in a doc test, is the inference the same? Yes, doc tests are compiled as separate crates but with the same type inference rules. Good.

Let me also verify the assertions in the doc test. The expected sorted vec and swaps=2. Matches the example. Good.

Alright, let me write the final response.

Let me reconsider the structure of my answer:
1. Brief intro.
2. Cargo.toml (for completeness).
3. src/lib.rs (main deliverable).
4. Brief explanation of key points.
5. How to run tests.

Let me write it concisely but completely.

Actually, I want to reconsider one thing about the swap counting and stability once more. The problem says "swap_count is the total number of element swaps performed during sorting". My implementation counts each `sorted.swap()` as one swap. This is the natural interpretation. Good.

Also, "Do not modify the input slice — return a new `Vec<Task>`". My implementation clones the input via `tasks.to_vec()`. Good.

Let me also make sure I handle the case where tasks might have duplicate entries correctly. The bubble sort with `task_comes_before` (strict) is stable, so duplicates retain their original order. Good.

Let me finalize.

I think the code is solid. Let me write the response.

Let me reconsider whether to include the helper function's doc comment. Since it's private, I could use a regular comment. But doc comments on private items are allowed and don't cause warnings. I'll keep it as a doc comment for clarity, but I could also just note it's internal. Let me keep `///` but mention it's an internal helper.

Actually, to be safe and clean, let me keep the doc comment on the private helper since it documents the ordering rules which are important. It's good practice.

Final code:

```rust
//! Bubble sort for ordered task records.
//!
//! This crate exposes a [`Task`] type together with [`bubble_sort_tasks`],
//! which sorts tasks by priority (descending) and creation time (ascending)
//! using the classic bubble sort algorithm.

/// A single unit of work to be sorted.
///
/// * [`Task::priority`] — optional priority; `None` tasks are always sorted to
///   the end of the list.
/// * [`Task::created_at`] — Unix timestamp (seconds) used as a tiebreaker.
#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    /// Human-readable name of the task.
    pub name: String,
    /// Optional priority. Higher values mean higher priority.
    ///
    /// When `None`, the task is always sorted to the end of the list.
    pub priority: Option<i32>,
    /// Creation timestamp, in seconds since the Unix epoch.
    pub created_at: i64,
}

/// Returns `true` when `a` must be placed strictly before `b` in the sorted
/// order.
///
/// This is the single source of truth for the ordering rules used by
/// [`bubble_sort_tasks`]:
///
/// 1. Higher [`Task::priority`] comes first.
/// 2. When priorities are equal, the earlier [`Task::created_at`] comes first.
/// 3. Tasks with `priority == None` always come after tasks that have a
///    priority; among themselves they are ordered by `created_at` ascending.
///
/// Returns `false` when `a` should come after `b`, or when the two tasks are
/// equivalent for ordering purposes (identical priority and `created_at`).
/// Returning `false` for equivalent elements keeps the sort stable.
fn task_comes_before(a: &Task, b: &Task) -> bool {
    match (a.priority, b.priority) {
        (Some(pa), Some(pb)) => {
            if pa != pb {
                pa > pb
            } else {
                a.created_at < b.created_at
            }
        }
        (Some(_), None) => true,
        (None, Some(_)) => false,
        (None, None) => a.created_at < b.created_at,
    }
}

/// Sorts `tasks` with bubble sort and returns the sorted vector along with the
/// number of element swaps performed.
///
/// The ordering rules are documented in [`task_comes_before`].
///
/// The input slice is never mutated: a new [`Vec`] is allocated and returned,
/// so the caller's original data is left untouched.
///
/// # Examples
///
/// ```
/// use bubble_sort_tasks::{bubble_sort_tasks, Task};
///
/// let tasks = vec![
///     Task { name: "bug".into(), priority: Some(3), created_at: 1000 },
///     Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
///     Task { name: "docs".into(), priority: Some(3), created_at: 500 },
/// ];
///
/// let (sorted, swaps) = bubble_sort_tasks(&tasks);
/// assert_eq!(
///     sorted,
///     vec![
///         Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
///         Task { name: "docs".into(), priority: Some(3), created_at: 500 },
///         Task { name: "bug".into(), priority: Some(3), created_at: 1000 },
///     ]
/// );
/// assert_eq!(swaps, 2);
/// ```
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    // Work on a clone so the caller's slice is never mutated.
    let mut sorted = tasks.to_vec();
    let n = sorted.len();
    let mut swap_count = 0usize;

    // `last` is the index of the last element still awaiting its final place.
    // After each pass the largest remaining element bubbles up to `last`.
    for last in (0..n).rev() {
        let mut swapped = false;

        // Walk the unsorted region, comparing each adjacent pair.
        for j in 0..last {
            // Swap only when the right element should come strictly before the
            // left one; equivalent elements are left in place (stable sort).
            if task_comes_before(&sorted[j + 1], &sorted[j]) {
                sorted.swap(j, j + 1);
                swap_count += 1;
                swapped = true;
            }
        }

        // If a full pass makes no swaps, the list is already sorted.
        if !swapped {
            break;
        }
    }

    (sorted, swap_count)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn task(name: &str, priority: Option<i32>, created_at: i64) -> Task {
        Task {
            name: name.to_string(),
            priority,
            created_at,
        }
    }

    #[test]
    fn example_from_spec() {
        let tasks = vec![
            task("bug", Some(3), 1000),
            task("feature", Some(5), 2000),
            task("docs", Some(3), 500),
        ];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(
            sorted,
            vec![
                task("feature", Some(5), 2000),
                task("docs", Some(3), 500),
                task("bug", Some(3), 1000),
            ]
        );
        assert_eq!(swaps, 2);
    }

    #[test]
    fn none_tasks_go_to_end_ordered_by_created_at() {
        let tasks = vec![
            task("a", None, 100),
            task("b", Some(1), 100),
            task("c", None, 50),
            task("d", Some(2), 10),
        ];
        let (sorted, _) = bubble_sort_tasks(&tasks);
        assert_eq!(
            sorted,
            vec![
                task("d", Some(2), 10),
                task("b", Some(1), 100),
                task("c", None, 50),
                task("a", None, 100),
            ]
        );
    }

    #[test]
    fn empty_input() {
        let tasks: Vec<Task> = vec![];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert!(sorted.is_empty());
        assert_eq!(swaps, 0);
    }

    #[test]
    fn single_element() {
        let tasks = vec![task("only", Some(1), 1)];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, tasks);
        assert_eq!(swaps, 0);
    }

    #[test]
    fn already_sorted_makes_no_swaps() {
        let tasks = vec![
            task("a", Some(3), 1),
            task("b", Some(3), 2),
            task("c", Some(2), 1),
        ];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, tasks);
        assert_eq!(swaps, 0);
    }

    #[test]
    fn input_slice_is_not_mutated() {
        let tasks = vec![task("a", Some(1), 1), task("b", Some(2), 2)];
        let original = tasks.clone();
        let (sorted, _) = bubble_sort_tasks(&tasks);
        assert_eq!(tasks, original);
        assert_ne!(sorted, tasks);
    }

    #[test]
    fn all_none_tasks() {
        let tasks = vec![
            task("a", None, 30),
            task("b", None, 10),
            task("c", None, 20),
        ];
        let (sorted, _) = bubble_sort_tasks(&tasks);
        assert_eq!(
            sorted,
            vec![
                task("b", None, 10),
                task("c", None, 20),
                task("a", None, 30),
            ]
        );
    }
}
```

This looks complete and correct. Let me write the response with the Cargo.toml and explanation.

I'll keep the explanation concise but informative.


## Response

## Solution

Here's a complete library crate. I've included `Cargo.toml` for completeness, with the main deliverable being `src/lib.rs`.

### `Cargo.toml`

```toml
[package]
name = "bubble_sort_tasks"
version = "0.1.0"
edition = "2021"
```

### `src/lib.rs`

```rust
//! Bubble sort for ordered task records.
//!
//! This crate exposes a [`Task`] type together with [`bubble_sort_tasks`],
//! which sorts tasks by priority (descending) and creation time (ascending)
//! using the classic bubble sort algorithm.

/// A single unit of work to be sorted.
///
/// * [`Task::priority`] — optional priority; `None` tasks are always sorted to
///   the end of the list.
/// * [`Task::created_at`] — Unix timestamp (seconds) used as a tiebreaker.
#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    /// Human-readable name of the task.
    pub name: String,
    /// Optional priority. Higher values mean higher priority.
    ///
    /// When `None`, the task is always sorted to the end of the list.
    pub priority: Option<i32>,
    /// Creation timestamp, in seconds since the Unix epoch.
    pub created_at: i64,
}

/// Returns `true` when `a` must be placed strictly before `b` in the sorted
/// order.
///
/// This is the single source of truth for the ordering rules used by
/// [`bubble_sort_tasks`]:
///
/// 1. Higher [`Task::priority`] comes first.
/// 2. When priorities are equal, the earlier [`Task::created_at`] comes first.
/// 3. Tasks with `priority == None` always come after tasks that have a
///    priority; among themselves they are ordered by `created_at` ascending.
///
/// Returns `false` when `a` should come after `b`, or when the two tasks are
/// equivalent for ordering purposes (identical priority and `created_at`).
/// Returning `false` for equivalent elements keeps the sort stable.
fn task_comes_before(a: &Task, b: &Task) -> bool {
    match (a.priority, b.priority) {
        (Some(pa), Some(pb)) => {
            if pa != pb {
                pa > pb
            } else {
                a.created_at < b.created_at
            }
        }
        (Some(_), None) => true,
        (None, Some(_)) => false,
        (None, None) => a.created_at < b.created_at,
    }
}

/// Sorts `tasks` with bubble sort and returns the sorted vector along with the
/// number of element swaps performed.
///
/// The ordering rules are documented in [`task_comes_before`].
///
/// The input slice is never mutated: a new [`Vec`] is allocated and returned,
/// so the caller's original data is left untouched.
///
/// # Examples
///
/// ```
/// use bubble_sort_tasks::{bubble_sort_tasks, Task};
///
/// let tasks = vec![
///     Task { name: "bug".into(), priority: Some(3), created_at: 1000 },
///     Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
///     Task { name: "docs".into(), priority: Some(3), created_at: 500 },
/// ];
///
/// let (sorted, swaps) = bubble_sort_tasks(&tasks);
/// assert_eq!(
///     sorted,
///     vec![
///         Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
///         Task { name: "docs".into(), priority: Some(3), created_at: 500 },
///         Task { name: "bug".into(), priority: Some(3), created_at: 1000 },
///     ]
/// );
/// assert_eq!(swaps, 2);
/// ```
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    // Work on a clone so the caller's slice is never mutated.
    let mut sorted = tasks.to_vec();
    let n = sorted.len();
    let mut swap_count = 0usize;

    // `last` is the index of the last element still awaiting its final place.
    // After each pass the largest remaining element bubbles up to `last`.
    for last in (0..n).rev() {
        let mut swapped = false;

        // Walk the unsorted region, comparing each adjacent pair.
        for j in 0..last {
            // Swap only when the right element should come strictly before the
            // left one; equivalent elements are left in place (stable sort).
            if task_comes_before(&sorted[j + 1], &sorted[j]) {
                sorted.swap(j, j + 1);
                swap_count += 1;
                swapped = true;
            }
        }

        // If a full pass makes no swaps, the list is already sorted.
        if !swapped {
            break;
        }
    }

    (sorted, swap_count)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn task(name: &str, priority: Option<i32>, created_at: i64) -> Task {
        Task {
            name: name.to_string(),
            priority,
            created_at,
        }
    }

    #[test]
    fn example_from_spec() {
        let tasks = vec![
            task("bug", Some(3), 1000),
            task("feature", Some(5), 2000),
            task("docs", Some(3), 500),
        ];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(
            sorted,
            vec![
                task("feature", Some(5), 2000),
                task("docs", Some(3), 500),
                task("bug", Some(3), 1000),
            ]
        );
        assert_eq!(swaps, 2);
    }

    #[test]
    fn none_tasks_go_to_end_ordered_by_created_at() {
        let tasks = vec![
            task("a", None, 100),
            task("b", Some(1), 100),
            task("c", None, 50),
            task("d", Some(2), 10),
        ];
        let (sorted, _) = bubble_sort_tasks(&tasks);
        assert_eq!(
            sorted,
            vec![
                task("d", Some(2), 10),
                task("b", Some(1), 100),
                task("c", None, 50),
                task("a", None, 100),
            ]
        );
    }

    #[test]
    fn empty_input() {
        let tasks: Vec<Task> = vec![];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert!(sorted.is_empty());
        assert_eq!(swaps, 0);
    }

    #[test]
    fn single_element() {
        let tasks = vec![task("only", Some(1), 1)];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, tasks);
        assert_eq!(swaps, 0);
    }

    #[test]
    fn already_sorted_makes_no_swaps() {
        let tasks = vec![
            task("a", Some(3), 1),
            task("b", Some(3), 2),
            task("c", Some(2), 1),
        ];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, tasks);
        assert_eq!(swaps, 0);
    }

    #[test]
    fn input_slice_is_not_mutated() {
        let tasks = vec![task("a", Some(1), 1), task("b", Some(2), 2)];
        let original = tasks.clone();
        let (sorted, _) = bubble_sort_tasks(&tasks);
        assert_eq!(tasks, original);
        assert_ne!(sorted, tasks);
    }

    #[test]
    fn all_none_tasks() {
        let tasks = vec![
            task("a", None, 30),
            task("b", None, 10),
            task("c", None, 20),
        ];
        let (sorted, _) = bubble_sort_tasks(&tasks);
        assert_eq!(
            sorted,
            vec![
                task("b", None, 10),
                task("c", None, 20),
                task("a", None, 30),
            ]
        );
    }
}
```

## Key design points

- **Single source of truth for ordering** — `task_comes_before` centralizes all three rules (priority desc, `created_at` asc, `None` → end). The sort algorithm itself is agnostic to the rules.

- **Stability via strict comparison** — the swap condition is `task_comes_before(&sorted[j + 1], &sorted[j])`, i.e. swap only when the right element should come *strictly* before the left. Equivalent elements (same priority + same timestamp) return `false` both ways, so they're never swapped and keep their original relative order.

- **No forbidden methods** — only `to_vec()` (copy) and `Vec::swap` are used; no `.sort*` anywhere.

- **Early exit** — the `swapped` flag breaks out of the outer loop as soon as a pass makes no swaps, so already-sorted input costs `0` swaps.

- **Input immutability** — `tasks.to_vec()` clones the data, guaranteeing the caller's slice is untouched.

## Running it

```bash
cargo test          # unit tests
cargo test --doc    # doc-example tests
cargo clippy        # lint check
```

## Timings

- Time to first token: 0.83s
- Temperature: 0.0
- Total generation: 302.04s
- Reasoning tokens: 10931
- Answer tokens: 2405
- Total tokens: 13336

## Server Timings (llama.cpp)

- Prompt tokens: 478
- Prompt eval speed: 594.76 t/s
- Prompt eval time: 803.68 ms
- Generation tokens: 13336
- Generation speed: 44.27 t/s
- Generation time: 301209.06 ms
