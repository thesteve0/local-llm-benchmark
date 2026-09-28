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

