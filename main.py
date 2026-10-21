from task_cli import TaskManager

def print_menu():
    print("\nWelcome to the Task Manager CLI!\n")
    print("Available commands:")
    print("1. add - Add a new task")
    print("2. list - List all tasks")
    print("3. complete - Mark a task as completed")
    print("4. delete - Delete a task")
    print("5. exit - Exit the application")

def main():
    manager = TaskManager();
    while True:

        print_menu()
        choice = input("\nEnter your choice (add/list/complete/delete): ").strip().lower()

        match choice:
            case "1":
                description = input("Enter task description: ")
                title = input("Enter task title: ")
                due_date = input("Enter task due date (YYYY-MM-DD): ")
                manager.add_task(title, description, due_date)
                pass
            case "2":
                manager.list_tasks()
                pass
            case "3":
                id_task = int(input("Enter the ID of the task to mark as completed: "))
                manager.mark_task_completed(id_task)
                pass
            case "4":
                pass
            case "5":
                print("Exiting the application. Goodbye!")
                break
            case _:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()