class Task:
    def __init__(self, task_name):
        self.task_name = task_name
        self.next = None

class ToDoList:
    def __init__(self):
        self.head = None

    def add_task(self, task_name):
        new_task = Task(task_name)

        if self.head is None:
            self.head = new_task
            return

        current_task = self.head

        while current_task.next is not None:
            current_task = current_task.next
        current_task.next = new_task

    def show_todo_list(self):
        if self.head is None:
            print("We don't have pending tasks")

        current_task = self.head

        while current_task is not None:
            print(current_task.task_name)
            current_task = current_task.next

    def add_urgent_task(self, task_name):
        new_task = Task(task_name)
        if self.head is None:
            self.head = new_task

        first_task = self.head
        self.head = new_task
        new_task.next = first_task

    def search_task(self, task_name):
        if self.head is None:
            return False

        current_task = self.head
        while current_task is not None:
            if current_task.task_name == task_name:
                return True
            current_task = current_task.next
        return False

    def complete_task(self, task_name):
        if self.head is None:
            print("The task is already completed")

        if self.head.task_name == task_name:
            self.head = self.head.next
            return

        current_task = self.head
        while current_task.next is not None:
            if current_task.next.task_name == task_name:
                current_task.next = current_task.next.next
                return
            current_task = current_task.next

    def add_after(self, task_name, existing_task):
        new_task = Task(task_name)

        if self.head.task_name == existing_task:
            next_existing_task = self.head.next
            new_task.next = next_existing_task
            self.head.next = new_task
            return

        current_task = self.head
        while current_task.next is not None:
            if current_task.task_name == existing_task:
                next_existing_task = current_task.next
                new_task.next = next_existing_task
                current_task.next = new_task
                return
            current_task = current_task.next


todo_list = ToDoList()
todo_list.add_task("Task 1")
todo_list.add_task("Task 2")
todo_list.add_task("Task 3")
todo_list.add_task("Task 4")
todo_list.add_urgent_task("Task 5 Urgent")
todo_list.complete_task("Task 4")
todo_list.add_after("Task 6", "Task 2")

todo_list.show_todo_list()
print(todo_list.search_task("Task 4"))