# Code Eval: Mellum2-12B-A2.5B-Thinking-Q8_0

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

We need to implement bubble_sort_tasks in Rust. The function takes a slice of Task and returns a tuple of Vec<Task> and usize (swap count). We must implement bubble sort manually, not using any built-in sort.

We need to define the Task struct as given.

Sorting rules:

- Primary: priority descending. So higher priority first.
- Tiebreaker: when priorities are equal, created_at ascending.
- None handling: tasks where priority is None always sort to the end, ordered by created_at ascending among themselves.

Thus we need a comparator function that returns true if a should come before b.

Define a helper function compare(a, b) -> bool:

- If a.priority is None and b.priority is None: compare created_at ascending (a.created_at < b.created_at).
- If a.priority is None and b.priority is Some: a should come after b, so return false.
- If a.priority is Some and b.priority is None: a should come before b, so return true.
- If both are Some: compare priority descending (a.priority > b.priority). If equal, compare created_at ascending (a.created_at < b.created_at).

Thus we can implement bubble sort: iterate n times, for i from 0 to n-1, for j from 0 to n-i-2, compare tasks[j] and tasks[j+1]. If compare(tasks[j+1], tasks[j]) is true (i.e., the later element should come before the current), then swap them and increment swap_count.

We need to copy the input slice into a Vec<Task> to sort.

Edge cases: empty slice, single element.

We need to document the function.

Let's write the code.

We'll include doc comments.

We'll also include a test module to demonstrate usage.

But the user only asked to write the library crate. We can include tests.

We'll write:

```rust
/// Represents a task with a name, optional priority, and creation timestamp.
#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    pub name: String,
    pub priority: Option<i32>,
    pub created_at: i64,
}

/// Sorts a slice of tasks using bubble sort.
///
/// The sorting order is:
/// 1. Higher priority first (`priority` descending).
/// 2. For equal priorities, earlier creation time first (`created_at` ascending).
/// 3. Tasks with `priority` = `None` are placed at the end, sorted by `created_at` ascending.
///
/// # Arguments
///
/// * `tasks` - A slice of `Task` to be sorted.
///
/// # Returns
///
/// A tuple containing:
/// * The sorted vector of tasks.
/// * The total number of swaps performed during sorting.
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
/// assert_eq!(sorted, vec![
///     Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
///     Task { name: "docs".into(),    priority: Some(3), created_at: 500 },
///     Task { name: "bug".into(),     priority: Some(3), created_at: 1000 },
/// ]);
/// assert_eq!(swaps, 2);
/// ```
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    let mut arr: Vec<Task> = tasks.to_vec();
    let n = arr.len();
    let mut swap_count = 0;

    // Helper closure to compare two tasks: returns true if a should come before b.
    let should_come_before = |a: &Task, b: &Task| -> bool {
        match (a.priority, b.priority) {
            (None, None) => a.created_at < b.created_at,
            (None, Some(_)) => false, // a (None) should come after b (Some)
            (Some(_), None) => true,  // a (Some) should come before b (None)
            (Some(p_a), Some(p_b)) => {
                if p_a != p_b {
                    p_a > p_b // higher priority first
                } else {
                    a.created_at < b.created_at // earlier created first
                }
            }
        }
    };

    // Bubble sort
    for i in 0..n {
        // Last i elements are already in place
        for j in 0..n - 1 - i {
            // If the next element should come before the current, swap them
            if should_come_before(&arr[j + 1], &arr[j]) {
                arr.swap_at(j, j + 1);
                swap_count += 1;
            }
        }
    }

    (arr, swap_count)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bubble_sort_tasks() {
        let tasks = vec![
            Task { name: "bug".into(),     priority: Some(3), created_at: 1000 },
            Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
            Task { name: "docs".into(),    priority: Some(3), created_at: 500 },
        ];

        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, vec![
            Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
            Task { name: "docs".into(),    priority: Some(3), created_at: 500 },
            Task { name: "bug".into(),     priority: Some(3), created_at: 1000 },
        ]);
        assert_eq!(swaps, 2);
    }

    #[test]
    fn test_none_priority() {
        let tasks = vec![
            Task { name: "a".into(), priority: Some(2), created_at: 100 },
            Task { name: "b".into(), priority: None,    created_at: 200 },
            Task { name: "c".into(), priority: Some(1), created_at: 300 },
            Task { name: "d".into(), priority: None,    created_at: 400 },
        ];

        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, vec![
            Task { name: "a".into(), priority: Some(2), created_at: 100 },
            Task { name: "c".into(), priority: Some(1), created_at: 300 },
            Task { name: "b".into(), priority: None,    created_at: 200 },
            Task { name: "d".into(), priority: None,    created_at: 400 },
        ]);
        // Let's compute swaps manually:
        // Initial: [a(2,100), b(None,200), c(1,300), d(None,400)]
        // Pass 1:
        //   compare a and b: a before b -> no swap
        //   compare b and c: b (None) after c (Some) -> swap => [a, c, b, d], swaps=1
        //   compare b and d: b (None) before d (None) -> compare created_at: 200 < 400 -> no swap
        // Pass 2:
        //   compare a and c: a before c -> no swap
        //   compare c and b: c (Some) before b (None) -> no swap
        // Pass 3:
        //   compare a and c: no swap
        //   compare c and b: no swap
        // Total swaps = 1
        assert_eq!(swaps, 1);
    }

    #[test]
    fn test_empty() {
        let tasks: Vec<Task> = vec![];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, vec![]);
        assert_eq!(swaps, 0);
    }

    #[test]
    fn test_single() {
        let tasks = vec![Task { name: "only".into(), priority: Some(1), created_at: 123 }];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, tasks);
        assert_eq!(swaps, 0);
    }
}
```

This should satisfy the requirements.

We need to ensure that we don't use any sorting methods. We are using bubble sort manually.

The swap_count is incremented each time we swap.

The code is idiomatic Rust.

We'll output the code as requested.


## Response

Here's the implementation of the bubble sort function for task records in Rust:

```rust
/// Represents a task with a name, optional priority, and creation timestamp.
#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    pub name: String,
    pub priority: Option<i32>,
    pub created_at: i64,
}

/// Sorts a slice of tasks using bubble sort.
///
/// The sorting order is:
/// 1. Higher priority first (`priority` descending).
/// 2. For equal priorities, earlier creation time first (`created_at` ascending).
/// 3. Tasks with `priority` = `None` are placed at the end, sorted by `created_at` ascending.
///
/// # Arguments
///
/// `tasks` - A slice of `Task` to be sorted.
///
/// # Returns
///
/// A tuple containing:
/// * The sorted vector of tasks.
/// * The total number of swaps performed during sorting.
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
/// assert_eq!(sorted, vec![
///     Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
///     Task { name: "docs".into(),    priority: Some(3), created_at: 500 },
///     Task { name: "bug".into(),     priority: Some(3), created_at: 1000 },
/// ]);
/// assert_eq!(swaps, 2);
/// ```
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    let mut arr: Vec<Task> = tasks.to_vec();
    let n = arr.len();
    let mut swap_count = 0;

    // Helper closure to compare two tasks: returns true if a should come before b.
    let should_come_before = |a: &Task, b: &Task| -> bool {
        match (a.priority, b.priority) {
            (None, None) => a.created_at < b.created_at,
            (None, Some(_)) => false, // a (None) should come after b (Some)
            (Some(_), None) => true,  // a (Some) should come before b (None)
            (Some(p_a), Some(p_b)) => {
                if p_a != p_b {
                    p_a > p_b // higher priority first
                } else {
                    a.created_at < b.created_at // earlier created first
                }
            }
        }
    };

    // Bubble sort
    for i in 0..n {
        // Last i elements are already in place
        for j in 0..n - 1 - i {
            // If the next element should come before the current, swap them
            if should_come_before(&arr[j + 1], &arr[j]) {
                arr.swap_at(j, j + 1);
                swap_count += 1;
            }
        }
    }

    (arr, swap_count)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bubble_sort_tasks() {
        let tasks = vec![
            Task { name: "bug".into(),     priority: Some(3), created_at: 1000 },
            Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
            Task { name: "docs".into(),    priority: Some(3), created_at: 500 },
        ];

        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, vec![
            Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
            Task { name: "docs".into(),    priority: Some(3), created_at: 500 },
            Task { name: "bug".into(),     priority: Some(3), created_at: 1000 },
        ]);
        assert_eq!(swaps, 2);
    }

    #[test]
    fn test_none_priority() {
        let tasks = vec![
            Task { name: "a".into(), priority: Some(2), created_at: 100 },
            Task { name: "b".into(), priority: None,    created_at: 200 },
            Task { name: "c".into(), priority: Some(1), created_at: 300 },
            Task { name: "d".into(), priority: None,    created_at: 400 },
        ];

        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, vec![
            Task { name: "a".into(), priority: Some(2), created_at: 100 },
            Task { name: "c".into(), priority: Some(1), created_at: 300 },
            Task { name: "b".into(), priority: None,    created_at: 200 },
            Task { name: "d".into(), priority: None,    created_at: 400 },
        ]);
        // Let's compute swaps manually:
        // Initial: [a(2,100), b(None,200), c(1,300), d(None,400)]
        // Pass 1:
        //   compare a and b: a before b -> no swap
        //   compare b and c: b (None) after c (Some) -> swap => [a, c, b, d], swaps=1
        //   compare b and d: b (None) before d (None) -> compare created_at: 200 < 400 -> no swap
        // Pass 2:
        //   compare a and c: a before c -> no swap
        //   compare c and b: c (Some) before b (None) -> no swap
        // Pass 3:
        //   compare a and c: no swap
        //   compare c and b: no swap
        // Total swaps = 1
        assert_eq!(swaps, 1);
    }

    #[test]
    fn test_empty() {
        let tasks: Vec<Task> = vec![];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, vec![]);
        assert_eq!(swaps, 0);
    }

    #[test]
    fn test_single() {
        let tasks = vec![Task { name: "only".into(), priority: Some(1), created_at: 123 }];
        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(sorted, tasks);
        assert_eq!(swaps, 0);
    }
}
```

This implementation:
1. Defines the `Task` struct as specified
2. Implements bubble sort manually without using any built-in sorting methods
3. Handles all the sorting rules including None priority cases
4. Returns both the sorted vector and the total number of swaps
5. Includes comprehensive tests to verify correctness
6. Uses idiomatic Rust with proper documentation and helper closures

## Timings

- Time to first token: 0.41s
- Total generation: 52.66s
- Reasoning tokens: 2308
- Answer tokens: 1842
- Total tokens: 4150
