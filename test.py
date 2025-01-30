class Task:
    def __init__(self, task_id, description, deadline=None, status='pending'):
        self.id = task_id
        self.description = description
        self.deadline = deadline
        self.status = status

    def __str__(self):
        return f'Task(id={self.id}, description="{self.description}", deadline={self.deadline}, status={self.status})'
    
    
#implementing Crud operations
import json

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.load_tasks()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)
                self.next_id = max(task['id'] for task in self.tasks) + 1
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file)

    def add_task(self, description, deadline=None):
        task = Task(self.next_id, description, deadline)
        self.tasks.append(task.__dict__)
        self.next_id += 1
        self.save_tasks()

    def view_tasks(self, status=None):
        for task in self.tasks:
            if status is None or task['status'] == status:
                print(Task(**task))

    def update_task(self, task_id, description=None, status=None):
        for task in self.tasks:
            if task['id'] == task_id:
                if description:
                    task['description'] = description
                if status:
                    task['status'] = status
                self.save_tasks()
                return
        print('Task not found')

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.save_tasks()
        
        
#User Information

def main():
    manager = TaskManager()

    while True:
        print("\nTask Management Application")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View completed tasks")
        print("5. Update a task")
        print("6. Delete a task")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter task description: ")
            deadline = input("Enter task deadline (optional): ")
            manager.add_task(description, deadline)
        elif choice == '2':
            manager.view_tasks()
        elif choice == '3':
            manager.view_tasks(status='pending')
        elif choice == '4':
            manager.view_tasks(status='completed')
        elif choice == '5':
            task_id = int(input("Enter task ID to update: "))
            description = input("Enter new description (or press Enter to skip): ")
            status = input("Enter new status (pending/completed) (or press Enter to skip): ")
            manager.update_task(task_id, description if description else None, status if status else None)
        elif choice == '6':
            task_id = int(input("Enter task ID to delete: "))
            manager.delete_task(task_id)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
