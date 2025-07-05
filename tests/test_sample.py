import unittest
import os
import sys

# Make sure Python can find your task_manager.py file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from task_manager import Task_Manager

class TestTaskManager(unittest.TestCase):
    
    def setUp(self):
        # Use a separate test file so main data.txt is not affected
        self.test_file = "test_data.txt"
        self.tm = Task_Manager(self.test_file)

    def tearDown(self):
        # Clean up after test: delete test file if it exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task_function_exists(self):
        self.assertTrue(hasattr(self.tm, "add_task"))

    def test_add_task_file_created(self):
        # We'll simulate task writing by mocking input()
        import builtins
        input_values = [
            "Test Task",               # title
            "This is a test task",     # description
            "2025-12-31",              # deadline
            "High",                    # priority
            "Testing"                  # category
        ]
        def mock_input(prompt):
            return input_values.pop(0)

        original_input = builtins.input
        builtins.input = mock_input
        try:
            self.tm.add_task()
            self.assertTrue(os.path.exists(self.test_file))
        finally:
            builtins.input = original_input

if __name__ == '__main__':
    unittest.main()
