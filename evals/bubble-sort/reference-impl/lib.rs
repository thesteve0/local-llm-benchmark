#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    pub name: String,
    pub priority: Option<i32>,
    pub created_at: i64,
}

pub fn bubble_sort_tasks(tasks: &[Task]) -> (Vec<Task>, usize) {
    let mut working: Vec<Task> = tasks.to_vec();
    let n = working.len();
    let mut swap_count: usize = 0;

    for i in 0..n.saturating_sub(1) {
        for j in 0..n - 1 - i {
            if should_swap(&working[j], &working[j + 1]) {
                working.swap(j, j + 1);
                swap_count += 1;
            }
        }
    }

    (working, swap_count)
}

fn should_swap(a: &Task, b: &Task) -> bool {
    match (a.priority, b.priority) {
        (None, None) => a.created_at > b.created_at,
        (None, Some(_)) => true,
        (Some(_), None) => false,
        (Some(ap), Some(bp)) => {
            if ap != bp {
                ap < bp
            } else {
                a.created_at > b.created_at
            }
        }
    }
}
