import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from task_cli import Task, TaskManager


class TaskTests(unittest.TestCase):
    def test_string_includes_task_details_and_pending_status(self):
        task = Task(1, "Write tests", "Cover task behavior", "2026-10-21")

        self.assertEqual(
            str(task),
            "ID:1\n"
            "Title: Write tests\n"
            "Description: Cover task behavior\n"
            "Due Date: 2026-10-21\n"
            "Status: Pending",
        )

    def test_mark_completed_changes_status(self):
        task = Task(1, "Write tests", "Cover task behavior", "2026-10-21")

        task.mark_completed()

        self.assertTrue(task.completed)
        self.assertIn("Status: Completed", str(task))


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.file_path = Path(self.temp_dir.name) / "tasks.json"
        file_name_patch = patch.object(TaskManager, "FILE_NAME", str(self.file_path))
        file_name_patch.start()
        self.addCleanup(file_name_patch.stop)
        self.manager = TaskManager()

    def capture_output(self, function, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            function(*args)
        return output.getvalue()

    def test_add_task_saves_task_and_advances_id(self):
        output = self.capture_output(
            self.manager.add_task, "Write tests", "Cover task behavior", "2026-10-21"
        )

        self.assertEqual(output, "Task 'Write tests' added successfully.\n")
        self.assertEqual(self.manager.next_id, 2)
        self.assertEqual(
            json.loads(self.file_path.read_text()),
            [
                {
                    "id": 1,
                    "title": "Write tests",
                    "description": "Cover task behavior",
                    "completed": False,
                    "due_date": "2026-10-21",
                }
            ],
        )

    def test_list_tasks_prints_empty_message_and_task_details(self):
        self.assertEqual(
            self.capture_output(self.manager.list_tasks), "No tasks available.\n"
        )
        self.capture_output(
            self.manager.add_task, "Write tests", "Cover task behavior", "2026-10-21"
        )

        output = self.capture_output(self.manager.list_tasks)

        self.assertIn("Title: Write tests", output)
        self.assertIn("Status: Pending", output)

    def test_mark_task_completed_saves_status(self):
        self.capture_output(
            self.manager.add_task, "Write tests", "Cover task behavior", "2026-10-21"
        )

        output = self.capture_output(self.manager.mark_task_completed, 1)

        self.assertEqual(output, "Task 'Write tests' marked as completed.\n")
        self.assertTrue(json.loads(self.file_path.read_text())[0]["completed"])

    def test_mark_missing_task_reports_not_found(self):
        output = self.capture_output(self.manager.mark_task_completed, 99)

        self.assertEqual(output, "No task found with ID 99.\n")
        self.assertFalse(self.file_path.exists())

    def test_delete_task_removes_and_saves_task(self):
        self.capture_output(
            self.manager.add_task, "Write tests", "Cover task behavior", "2026-10-21"
        )

        output = self.capture_output(self.manager.delete_task, 1)

        self.assertEqual(output, "Task 'Write tests' deleted successfully.\n")
        self.assertEqual(json.loads(self.file_path.read_text()), [])

    def test_load_tasks_restores_tasks_and_next_id(self):
        self.capture_output(
            self.manager.add_task, "Write tests", "Cover task behavior", "2026-10-21"
        )
        loaded_manager = TaskManager()

        output = self.capture_output(loaded_manager.load_tasks)

        self.assertEqual(output, "Tasks loaded successfully.\n")
        self.assertEqual(loaded_manager.next_id, 2)
        self.assertEqual(len(loaded_manager._tasks), 1)
        self.assertEqual(loaded_manager._tasks[0].title, "Write tests")

    def test_load_missing_file_reports_empty_list(self):
        output = self.capture_output(self.manager.load_tasks)

        self.assertEqual(
            output, "No saved tasks found. Starting with an empty task list.\n"
        )
        self.assertEqual(self.manager._tasks, [])

    def test_load_invalid_json_reports_error(self):
        self.file_path.write_text("{invalid json")

        output = self.capture_output(self.manager.load_tasks)

        self.assertEqual(
            output, "Error decoding tasks from the file. Starting with an empty task list.\n"
        )
        self.assertEqual(self.manager._tasks, [])


if __name__ == "__main__":
    unittest.main()
