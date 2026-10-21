from task_cli import TaskManager
from ai_service import create_simple_tasks

def print_menu():
    print("\nWelcome to the Task Manager CLI!\n")
    print("Available commands:")
    print("1. add - Add a new task")
    print("2. add - Add a new task(with AI assistance)")
    print("3. list - List all tasks")
    print("4. complete - Mark a task as completed")
    print("5. delete - Delete a task")
    print("6. exit - Exit the application")

def main():
    manager = TaskManager();
    manager.load_tasks()  # Load tasks from file if available
    while True:

        print_menu()
        try:
            choice = int(input("\nEnter your choice (add/list/complete/delete): ").strip().lower())
            match choice:
                case 1:
                    description = input("Enter task description: ")
                    title = input("Enter task title: ")
                    due_date = input("Enter task due date (YYYY-MM-DD): ")
                    manager.add_task(title, description, due_date)
                    pass
                case 2:
                    description = input("Enter a complex task description: ")
                    subtasks = create_simple_tasks(description)
                    counter = 0
                    for subtask in subtasks:
                        counter = 1+counter
                        if not subtask.startswith("Error:"):
                            title = input(f"subtask {counter} - {subtask}': ")
                            due_date = time.now().strftime("%Y-%m-%d")  # Set due date to today for simplicity
                            manager.add_task(title, subtask, due_date)
                        else:
                            print(subtask)  # Print the error message
                            break
                    pass
                case 3:
                    manager.list_tasks()
                    pass
                case 4:
                    id_task = int(input("Enter the ID of the task to mark as completed: "))
                    manager.mark_task_completed(id_task)
                    pass
                case 5:
                    id_task = int(input("Enter the ID of the task to delete: "))
                    manager.delete_task(id_task)
                    pass
                case 6:
                    print("Exiting the application. Goodbye!")
                    break
                case _:
                    print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()