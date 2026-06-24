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
///
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
