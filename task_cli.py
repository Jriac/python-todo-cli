import json
class Task:
    def __init__(self, id, title, description, due_date, completed = False):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"ID:{self.id}\nTitle: {self.title}\nDescription: {self.description}\nDue Date: {self.due_date}\nStatus: {status}"

class TaskManager:
    FILE_NAME = "tasks.json"
    def __init__(self):
        self._tasks = []
        self.next_id = 1

    def add_task(self, title, description, due_date):
        task = Task(self.next_id, title, description, due_date)
        self._tasks.append(task)
        self.next_id += 1
        print(f"Task '{title}' added successfully.")
        self.save_tasks()
    
    def list_tasks(self):
        if not self._tasks:
            print("No tasks available.")
            return
        for task in self._tasks:
            print(task)

    def mark_task_completed(self, task_id):
        for task in self._tasks:
            if task.id == task_id:
                task.mark_completed()
                print(f"Task '{task.title}' marked as completed.")
                self.save_tasks()
                return
        print(f"No task found with ID {task_id}.")

    def delete_task(self, task_id):
        for task in self._tasks:
            if task.id == task_id:
                self._tasks.remove(task)
                print(f"Task '{task.title}' deleted successfully.")
                self.save_tasks()
                return
        print(f"No task found with ID {task_id}.")

    def load_tasks(self):
        try:
            with open(self.FILE_NAME, 'r') as file:
                tasks_data = json.load(file)
                self._tasks = [Task(item["id"], item["title"], item["description"], item["due_date"], item["completed"]) for item in tasks_data]
                if self._tasks:
                    self.next_id = max(task.id for task in self._tasks) + 1
                else:
                    self.next_id = 1
                
            print("Tasks loaded successfully.")
        except FileNotFoundError:
            print("No saved tasks found. Starting with an empty task list.")
        except json.JSONDecodeError:
            print("Error decoding tasks from the file. Starting with an empty task list.")

    def save_tasks(self):
        with open(self.FILE_NAME, "w") as file:
            json.dump([{"id":task.id, "title":task.title, "description":task.description, "completed":task.completed, "due_date":task.due_date } for task in self._tasks], file, indent=4)