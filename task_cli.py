class Task:
    def __init__(self, id, title, description, due_date):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"ID:{self.id}\nTitle: {self.title}\nDescription: {self.description}\nDue Date: {self.due_date}\nStatus: {status}"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, title, description, due_date):
        task = Task(self.next_id, title, description, due_date)
        self.tasks.append(task)
        self.next_id += 1
        print(f"Task '{title}' added successfully.")
    
    def list_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
        for task in self.tasks:
            print(task)

    def mark_task_completed(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.mark_completed()
                print(f"Task '{task.title}' marked as completed.")
                return
        print(f"No task found with ID {task_id}.")

    def delete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                print(f"Task '{task.title}' deleted successfully.")
                return
        print(f"No task found with ID {task_id}.")