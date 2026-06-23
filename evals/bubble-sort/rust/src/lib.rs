// Model replaces this file with its implementation.

#[derive(Clone, Debug, PartialEq)]
pub struct Task {
    pub name: String,
    pub priority: Option<i32>,
    pub created_at: i64,
}

pub fn bubble_sort_tasks(_tasks: &[Task]) -> (Vec<Task>, usize) {
    todo!("Model implements this")
}
