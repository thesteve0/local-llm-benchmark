//! # Bubble Sort for Task Records
//!
//! This crate provides a `Task` struct and a `bubble_sort_tasks` function that sorts
//! tasks according to the rules described in the module documentation.

/// A task record containing a name, an optional priority, and a creation timestamp.
#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    pub name: String,
    pub priority: Option<i32>,
    pub created_at: i64,
}

/// Sorts a slice of tasks using the bubble‑sort algorithm.

//!
//! # Sorting Rules
//!
//! 1. **Primary:** tasks are ordered by `priority` in descending order (higher
//!    priority comes first).
//! 2. **Tiebreaker:** when priorities are equal, tasks are ordered by
//!    `created_at` ascending (earlier timestamps come first).
//! 3. **None handling:** tasks with `priority: None` always sort to the end of
//!    the list, ordered by `created_at` ascending among themselves.

/// Sorts `tasks` using bubble sort and returns the sorted vector together with
/// the number of swaps performed.
///
/// # Arguments
/// * `tasks` - A slice of `Task` values to be sorted. The original slice is not
///   modified.
///
/// # Returns
/// A tuple `(sorted_vec, swap_count)` where `sorted_vec` is a new `Vec<Task>`
/// containing the tasks in the required order and `swap_count` is the total
/// number of element swaps executed during the sort.
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    // Clone the input into a mutable vector – we must not alter the original.
    let mut sorted = tasks.to_vec();
    let n = sorted.len();
    let mut swap_count: usize = 0;

    // Classic bubble sort: after each outer iteration the largest element is
    // placed at the end, so the inner loop can shrink.
    for i in 0..n {
        for j in 0..(n - i - 1) {
            if should_swap(&sorted[j], &sorted[j + 1]) {
                sorted.swap(j, j + 1);
                swap_count += 1;
            }
        }
    }

    (sorted, swap_count)
}

/// Determines whether two tasks are out of order and need to be swapped.
///
/// Returns `true` if the first task (`a`) should appear *after* the second
/// task (`b`) in the final sorted list.
fn should_swap(a: &Task, b: &Task) -> bool {
    let a_none = a.priority.is_none();
    let b_none = b.priority.is_none();

    // Tasks without a priority go to the end of the list.
    if a_none && !b_none {
        return true; // a is None, b has a priority → swap
    }
    if !a_none && b_none {
        return false; // a has a priority, b is None → keep order
    }

    // Both have a priority or both are None.
    if a_none && b_none {
        // Sort by creation time ascending.
        return a.created_at > b.created_at;
    }

    // Both have a concrete priority.
    let a_pri = a.priority.unwrap();
    let b_pri = b.priority.unwrap();

    if a_pri != b_pri {
        // Higher priority first (descending order).
        return a_pri < b_pri;
    } else {
        // Same priority: earlier creation time first.
        return a.created_at > b.created_at;
    }
}
