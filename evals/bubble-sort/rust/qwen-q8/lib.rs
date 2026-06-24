/// A task record containing a name, optional priority, and creation timestamp.
#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    pub name: String,
    pub priority: Option<i32>,
    pub created_at: i64,
}

/// Sorts a slice of tasks using the bubble sort algorithm.
///
/// # Sorting Rules
/// 1. **Primary:** Sort by `priority` in descending order (higher priority first).
/// 2. **Tiebreaker:** When priorities are equal, sort by `created_at` in ascending order (earlier timestamp first).
/// 3. **None Handling:** Tasks with `priority == None` are always placed at the end,
///    sorted by `created_at` in ascending order among themselves.
///
/// # Returns
/// A tuple containing:
/// - The newly sorted `Vec<Task>`
/// - The total number of element swaps performed during sorting
///
/// # Constraints
/// - Uses a manual bubble sort implementation (no built-in sorting methods).
/// - Does not modify the input slice.
pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    let mut sorted = tasks.to_vec();
    let mut swap_count = 0;
    let n = sorted.len();

    for i in 0..n {
        let mut swapped = false;
        // After each pass, the largest unsorted element bubbles to its correct position.
        // We can safely skip the last `i` elements.
        for j in 0..n - i - 1 {
            if should_swap(&sorted[j], &sorted[j + 1]) {
                sorted.swap(j, j + 1);
                swap_count += 1;
                swapped = true;
            }
        }
        // Optimization: If no swaps occurred in a pass, the list is already sorted.
        if !swapped {
            break;
        }
    }

    (sorted, swap_count)
}

/// Determines if `a` should be placed after `b` according to the sorting rules.
/// Returns `true` if a swap is needed between adjacent elements `a` and `b`.
fn should_swap(a: &Task, b: &Task) -> bool {
    match (a.priority, b.priority) {
        (Some(p1), Some(p2)) => {
            // Higher priority comes first
            if p1 != p2 {
                p1 < p2
            } else {
                // Earlier timestamp comes first
                a.created_at > b.created_at
            }
        }
        (Some(_), None) => false, // `Some` always comes before `None`
        (None, Some(_)) => true,  // `None` always comes after `Some`
        (None, None) => a.created_at > b.created_at, // Sort `None` tasks by `created_at` ascending
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let tasks = vec![
            Task { name: "bug".into(),     priority: Some(3), created_at: 1000 },
            Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
            Task { name: "docs".into(),    priority: Some(3), created_at: 500 },
        ];

        let (sorted, swaps) = bubble_sort_tasks(&tasks);
        
        assert_eq!(
            sorted,
            vec![
                Task { name: "feature".into(), priority: Some(5), created_at: 2000 },
                Task { name: "docs".into(),    priority: Some(3), created_at: 500 },
                Task { name: "bug".into(),     priority: Some(3), created_at: 1000 },
            ]
        );
        assert_eq!(swaps, 2);
    }

    #[test]
    fn test_none_priorities() {
        let tasks = vec![
            Task { name: "a".into(), priority: None, created_at: 300 },
            Task { name: "b".into(), priority: Some(1), created_at: 100 },
            Task { name: "c".into(), priority: None, created_at: 100 },
        ];

        let (sorted, _) = bubble_sort_tasks(&tasks);
        assert_eq!(
            sorted,
            vec![
                Task { name: "b".into(), priority: Some(1), created_at: 100 },
                Task { name: "c".into(), priority: None, created_at: 100 },
                Task { name: "a".into(), priority: None, created_at: 300 },
            ]
        );
    }

    #[test]
    fn test_already_sorted() {
        let tasks = vec![
            Task { name: "high".into(), priority: Some(10), created_at: 100 },
            Task { name: "low".into(),  priority: Some(1),  created_at: 200 },
        ];
        let (_, swaps) = bubble_sort_tasks(&tasks);
        assert_eq!(swaps, 0);
    }
}
