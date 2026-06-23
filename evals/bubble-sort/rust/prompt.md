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
