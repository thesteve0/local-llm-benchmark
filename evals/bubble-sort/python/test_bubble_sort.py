import copy
import unittest
from bubble_sort import bubble_sort_tasks


def task(name, priority, created_at):
    return {"name": name, "priority": priority, "created_at": created_at}


class TestBubbleSortTasks(unittest.TestCase):
    def test_empty_list(self):
        result, swaps = bubble_sort_tasks([])
        self.assertEqual(result, [])
        self.assertEqual(swaps, 0)

    def test_single_element(self):
        tasks = [task("only", 5, 100)]
        result, swaps = bubble_sort_tasks(tasks)
        self.assertEqual(result, [task("only", 5, 100)])
        self.assertEqual(swaps, 0)

    def test_already_sorted(self):
        tasks = [
            task("high", 5, 100),
            task("mid", 3, 200),
            task("low", 1, 300),
        ]
        result, swaps = bubble_sort_tasks(tasks)
        self.assertEqual([t["name"] for t in result], ["high", "mid", "low"])
        self.assertEqual(swaps, 0)

    def test_reverse_sorted(self):
        tasks = [
            task("low", 1, 300),
            task("mid", 3, 200),
            task("high", 5, 100),
        ]
        result, swaps = bubble_sort_tasks(tasks)
        self.assertEqual([t["name"] for t in result], ["high", "mid", "low"])
        self.assertEqual(swaps, 3)

    def test_tiebreaker_by_created_at(self):
        tasks = [
            task("later", 5, 200),
            task("earlier", 5, 100),
        ]
        result, swaps = bubble_sort_tasks(tasks)
        self.assertEqual([t["name"] for t in result], ["earlier", "later"])
        self.assertEqual(swaps, 1)

    def test_null_priority_sorts_to_end(self):
        tasks = [
            task("none", None, 100),
            task("high", 5, 200),
            task("mid", 3, 300),
        ]
        result, swaps = bubble_sort_tasks(tasks)
        self.assertEqual([t["name"] for t in result], ["high", "mid", "none"])
        self.assertEqual(swaps, 2)

    def test_multiple_null_priorities(self):
        tasks = [
            task("later_null", None, 400),
            task("earlier_null", None, 50),
        ]
        result, swaps = bubble_sort_tasks(tasks)
        self.assertEqual([t["name"] for t in result], ["earlier_null", "later_null"])
        self.assertEqual(swaps, 1)

    def test_mixed_comprehensive(self):
        tasks = [
            task("d", None, 400),
            task("a", 5, 100),
            task("c", 3, 300),
            task("b", 5, 200),
            task("e", None, 50),
        ]
        result, swaps = bubble_sort_tasks(tasks)
        self.assertEqual([t["name"] for t in result], ["a", "b", "c", "e", "d"])
        self.assertEqual([t["priority"] for t in result], [5, 5, 3, None, None])
        self.assertEqual([t["created_at"] for t in result], [100, 200, 300, 50, 400])
        self.assertEqual(swaps, 5)

    def test_all_same_priority(self):
        tasks = [
            task("c", 3, 300),
            task("a", 3, 100),
            task("b", 3, 200),
        ]
        result, swaps = bubble_sort_tasks(tasks)
        self.assertEqual([t["name"] for t in result], ["a", "b", "c"])
        self.assertEqual(swaps, 2)

    def test_null_sorts_after_lowest_priority(self):
        tasks = [
            task("none", None, 100),
            task("lowest", 1, 200),
        ]
        result, swaps = bubble_sort_tasks(tasks)
        self.assertEqual([t["name"] for t in result], ["lowest", "none"])
        self.assertEqual(swaps, 1)

    def test_input_not_modified(self):
        tasks = [
            task("low", 1, 300),
            task("high", 5, 100),
        ]
        original = copy.deepcopy(tasks)
        bubble_sort_tasks(tasks)
        self.assertEqual(tasks, original)


if __name__ == "__main__":
    unittest.main()
