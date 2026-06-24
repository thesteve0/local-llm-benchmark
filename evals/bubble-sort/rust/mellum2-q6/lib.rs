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
///
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
