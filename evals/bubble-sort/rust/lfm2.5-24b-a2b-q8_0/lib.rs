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
