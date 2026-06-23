use bubble_sort_tasks::{Task, bubble_sort_tasks};

fn task(name: &str, priority: Option<i32>, created_at: i64) -> Task {
    Task {
        name: name.to_string(),
        priority,
        created_at,
    }
}

fn names(tasks: &[Task]) -> Vec<&str> {
    tasks.iter().map(|t| t.name.as_str()).collect()
}

fn priorities(tasks: &[Task]) -> Vec<Option<i32>> {
    tasks.iter().map(|t| t.priority).collect()
}

#[test]
fn test_empty_list() {
    let (result, swaps) = bubble_sort_tasks(&[]);
    assert!(result.is_empty());
    assert_eq!(swaps, 0);
}

#[test]
fn test_single_element() {
    let tasks = vec![task("only", Some(5), 100)];
    let (result, swaps) = bubble_sort_tasks(&tasks);
    assert_eq!(result.len(), 1);
    assert_eq!(result[0].name, "only");
    assert_eq!(swaps, 0);
}

#[test]
fn test_already_sorted() {
    let tasks = vec![
        task("high", Some(5), 100),
        task("mid", Some(3), 200),
        task("low", Some(1), 300),
    ];
    let (result, swaps) = bubble_sort_tasks(&tasks);
    assert_eq!(names(&result), vec!["high", "mid", "low"]);
    assert_eq!(swaps, 0);
}

#[test]
fn test_reverse_sorted() {
    let tasks = vec![
        task("low", Some(1), 300),
        task("mid", Some(3), 200),
        task("high", Some(5), 100),
    ];
    let (result, swaps) = bubble_sort_tasks(&tasks);
    assert_eq!(names(&result), vec!["high", "mid", "low"]);
    assert_eq!(swaps, 3);
}

#[test]
fn test_tiebreaker_by_created_at() {
    let tasks = vec![
        task("later", Some(5), 200),
        task("earlier", Some(5), 100),
    ];
    let (result, swaps) = bubble_sort_tasks(&tasks);
    assert_eq!(names(&result), vec!["earlier", "later"]);
    assert_eq!(swaps, 1);
}

#[test]
fn test_null_priority_sorts_to_end() {
    let tasks = vec![
        task("none", None, 100),
        task("high", Some(5), 200),
        task("mid", Some(3), 300),
    ];
    let (result, swaps) = bubble_sort_tasks(&tasks);
    assert_eq!(names(&result), vec!["high", "mid", "none"]);
    assert_eq!(swaps, 2);
}

#[test]
fn test_multiple_null_priorities() {
    let tasks = vec![
        task("later_null", None, 400),
        task("earlier_null", None, 50),
    ];
    let (result, swaps) = bubble_sort_tasks(&tasks);
    assert_eq!(names(&result), vec!["earlier_null", "later_null"]);
    assert_eq!(swaps, 1);
}

#[test]
fn test_mixed_comprehensive() {
    let tasks = vec![
        task("d", None, 400),
        task("a", Some(5), 100),
        task("c", Some(3), 300),
        task("b", Some(5), 200),
        task("e", None, 50),
    ];
    let (result, swaps) = bubble_sort_tasks(&tasks);
    assert_eq!(names(&result), vec!["a", "b", "c", "e", "d"]);
    assert_eq!(priorities(&result), vec![Some(5), Some(5), Some(3), None, None]);
    assert_eq!(swaps, 5);
}

#[test]
fn test_all_same_priority() {
    let tasks = vec![
        task("c", Some(3), 300),
        task("a", Some(3), 100),
        task("b", Some(3), 200),
    ];
    let (result, swaps) = bubble_sort_tasks(&tasks);
    assert_eq!(names(&result), vec!["a", "b", "c"]);
    assert_eq!(swaps, 2);
}

#[test]
fn test_null_sorts_after_lowest_priority() {
    let tasks = vec![
        task("none", None, 100),
        task("lowest", Some(1), 200),
    ];
    let (result, swaps) = bubble_sort_tasks(&tasks);
    assert_eq!(names(&result), vec!["lowest", "none"]);
    assert_eq!(swaps, 1);
}

#[test]
fn test_input_not_modified() {
    let tasks = vec![
        task("low", Some(1), 300),
        task("high", Some(5), 100),
    ];
    let original = tasks.clone();
    let _ = bubble_sort_tasks(&tasks);
    assert_eq!(tasks, original);
}
