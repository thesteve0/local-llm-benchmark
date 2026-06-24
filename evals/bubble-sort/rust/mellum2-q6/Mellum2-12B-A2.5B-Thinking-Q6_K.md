# Code Eval: Mellum2-12B-A2.5B-Thinking-Q6_K

## Prompt

# Bubble Sort Tasks — Rust

Implement a bubble sort function for task records.

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

We need to implement bubble sort for Task according to rules. We'll write a function that takes a slice and returns a tuple of sorted Vec and swap count.

We need to compare two tasks:

- If both have Some(priority): compare priority descending. If equal, compare created_at ascending.
- If one has Some and the other None: the Some comes first.
- If both None: compare created_at ascending.

We'll implement bubble sort: iterate n times, for i in 0..n-1, for j in 0..n-i-2, compare tasks[j] and tasks[j+1]. If out of order, swap them and increment swap_count.

We need to copy tasks into a Vec to sort.

We'll write doc comments.

Let's produce the code.


## Response

```rust
//! Bubble sort implementation for task records.
//!
//! This module provides a `Task` struct and a `bubble_sort_tasks` function that
//! sorts a slice of `Task` using the bubble sort algorithm according to the
//! specified rules.

/// A task record with a name, optional priority, and creation timestamp.
#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    /// The name of the task.
    pub name: String,
    /// The priority of the task, if any.
    pub priority: Option<i32>,
    /// The creation timestamp (Unix time in seconds).
    pub created_at: i64,
}

/// Compares two tasks according to the sorting rules.
///
/// Returns `true` if `a` should come before `b` in the sorted order.
fn task_less(a: &Task, b: &Task) -> bool {
    match (a.priority, b.priority) {
        // Both have priorities: higher priority comes first.
        (Some(pa), Some(pb)) => {
            if pa != pb {
                pa > pb // descending
            } else {
                a.created_at < b.created_at // ascending
            }
        }
        // Only `a` has a priority: `a` comes before `b`.
        (Some(_), None) => true,
        // Only `b` has a priority: `a` comes after `b`.
        (None, Some(_)) => false,
        // Both have no priority: sort by created_at ascending.
        (None, None) => a.created_at < b.created_at,
    }
}

/// Sorts a slice of tasks using bubble sort.
///
/// # Sorting Rules
///
/// 1. **Primary:** sort by `priority` descending (higher priority comes first).
/// 2. **Tiebreaker:** when priorities are equal, sort by `created_at` ascending
///    (earlier timestamp comes first).
/// 3. **None handling:** tasks where `priority` is `None` always sort to the end
///    of the list, ordered by `created_at` ascending among themselves.
///
/// # Parameters
///
/// * `tasks` - A slice of `Task` to sort.
///
/// # Returns
///
/// A tuple containing:
///
/// * `sorted_vec` - A new `Vec<Task>` with the tasks sorted according to the
///   rules.
/// * `swap_count` - The total number of element swaps performed during sorting.
///
/// # Example
///
/// ```
/// let tasks = vec![
///     Task { name: "bug".into(),     priority: Some(3), created_at: 1000 },
///     Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
///     Task { name: "docs".into(),    priority: Some(3), created_at: 500 },
/// ];
///
/// let (sorted, swaps) = bubble_sort_tasks(&tasks);
/// assert_eq!(sorted[0].name, "feature");
/// assert_eq!(sorted[1].name, "docs");
/// assert_eq!(sorted[2].name, "bug");
/// assert_eq!(swaps, 2);
/// ```
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    let mut sorted = tasks.to_vec();
    let n = sorted.len();
    let mut swap_count = 0;

    // Perform bubble sort.
    for i in 0..n {
        // Last i elements are already in place.
        for j in 0..n - i - 1 {
            if task_less(&sorted[j + 1], &sorted[j]) {
                // Swap elements.
                sorted.swap(j, j + 1);
                swap_count += 1;
            }
        }
    }

    (sorted, swap_count)
}
```

## Timings

- Time to first token: 0.34s
- Total generation: 12.62s
- Reasoning tokens: 201
- Answer tokens: 947
- Total tokens: 1148
