/// A task record to be sorted.
#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    /// The name of the task.
    pub name: String,
    /// The priority of the task. `None` indicates lowest priority.
    pub priority: Option<i32>,
    /// The Unix timestamp when the task was created.
    pub created_at: i64,
}

/// Sorts a slice of tasks using the bubble sort algorithm.
///
/// Sorting rules:
/// 1. Primary: `priority` descending (higher priority comes first)
/// 2. Tiebreaker: when priorities are equal, `created_at` ascending (earlier timestamp comes first)
/// 3. `None` priorities always sort to the end, ordered by `created_at` ascending among themselves
///
/// # Returns
/// A tuple containing the sorted `Vec<Task>` and the total number of element swaps performed.
///
/// # Constraints
/// - Uses the bubble sort algorithm (no built-in sorting methods)
/// - Does not modify the input slice
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    let mut sorted = tasks.to_vec();
    let mut swap_count = 0;
    let n = sorted.len();

    for i in 0..n {
        let mut swapped = false;
        // Last `i` elements are already in their final positions
        for j in 0..n - 1 - i {
            if should_swap(&sorted[j], &sorted[j + 1]) {
                sorted.swap(j, j + 1);
                swap_count += 1;
                swapped = true;
            }
        }
        // Optimization: if no swaps occurred in a pass, the list is already sorted
        if !swapped {
            break;
        }
    }

    (sorted, swap_count)
}

/// Determines if two adjacent tasks are in the wrong order for the specified sorting rules.
/// Returns `true` if `a` should come after `b` (triggering a swap).
fn should_swap(a: &Task, b: &Task) -> bool {
    match (a.priority, b.priority) {
        // `None` priorities always go to the end
        (None, Some(_)) => true,
        (Some(_), None) => false,
        
        // Both have priorities: higher priority comes first
        (Some(p1), Some(p2)) => {
            if p1 != p2 {
                p1 < p2 // Lower priority should be placed later
            } else {
                // Tiebreaker: earlier created_at comes first
                a.created_at > b.created_at
            }
        }
        
        // Both are `None`: sort by created_at ascending
        (None, None) => a.created_at > b.created_at,
    }
}
