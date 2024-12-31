import tkinter as tk
from tkinter import simpledialog
from tkinter.dnd import dnd_start◘

class DraggableListbox(tk.Listbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.bind("<ButtonPress-1>", self.start_drag)
        self.dnd_source = None

    def start_drag(self, event):
        if self.curselection():
            self.dnd_source = self.get(self.curselection()[0])
            dnd_start(self, event)

    def dnd_accept(self, source, event):
        return self

    def dnd_enter(self, source, event):
        self.config(bg="lightblue")

    def dnd_leave(self, source, event):
        self.config(bg="white")

    def dnd_commit(self, source, event):
        if source.dnd_source:
            self.insert(tk.END, source.dnd_source)
            index = source.get(0, tk.END).index(source.dnd_source)
            source.delete(index)
            source.dnd_source = None

    def dnd_end(self, target, event):
        self.dnd_source = None

# Helper functions
def get_selected_listbox():
    for listbox in [todo_listbox, in_progress_listbox, completed_listbox]:
        if listbox.curselection():
            return listbox, listbox.curselection()
    return None, None

def add_task():
    task = task_entry.get()
    due_date = date_entry.get()
    if task and due_date:
        todo_listbox.insert(tk.END, f"{task} (Due: {due_date})")
        task_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)

def edit_task():
    selected_listbox, selected_item = get_selected_listbox()
    if selected_listbox and selected_item:
        task = selected_listbox.get(selected_item)
        new_task = simpledialog.askstring("Edit Task", "Edit the task:", initialvalue=task)
        if new_task:
            selected_listbox.delete(selected_item)
            selected_listbox.insert(tk.END, new_task)

def delete_task():
    selected_listbox, selected_item = get_selected_listbox()
    if selected_listbox and selected_item:
        selected_listbox.delete(selected_item)

# Main application window
root = tk.Tk()
root.title("To-Do List with Drag and Drop")

# Input fields for tasks
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Task:").grid(row=0, column=0, padx=5)
task_entry = tk.Entry(input_frame)
task_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Due Date:").grid(row=0, column=2, padx=5)
date_entry = tk.Entry(input_frame)
date_entry.grid(row=0, column=3, padx=5)

add_task_button = tk.Button(input_frame, text="Add Task", command=add_task)
add_task_button.grid(row=0, column=4, padx=5)

# Drag-and-Drop Listboxes
listboxes_frame = tk.Frame(root)
listboxes_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# To-Do Section
todo_frame = tk.Frame(listboxes_frame)
todo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

tk.Label(todo_frame, text="To-Do").pack()
todo_listbox = DraggableListbox(todo_frame, selectmode=tk.SINGLE, height=10)
todo_listbox.pack(fill=tk.BOTH, expand=True)

edit_delete_frame = tk.Frame(todo_frame)
edit_delete_frame.pack(pady=5)

edit_button = tk.Button(edit_delete_frame, text="Edit Task", command=edit_task)
edit_button.pack(side=tk.LEFT, padx=5)
delete_button = tk.Button(edit_delete_frame, text="Delete Task", command=delete_task)
delete_button.pack(side=tk.LEFT, padx=5)

# In-Progress Section
in_progress_frame = tk.Frame(listboxes_frame)
in_progress_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

tk.Label(in_progress_frame, text="In-Progress").pack()
in_progress_listbox = DraggableListbox(in_progress_frame, selectmode=tk.SINGLE, height=10)
in_progress_listbox.pack(fill=tk.BOTH, expand=True)

# Completed Section
completed_frame = tk.Frame(listboxes_frame)
completed_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

tk.Label(completed_frame, text="Completed").pack()
completed_listbox = DraggableListbox(completed_frame, selectmode=tk.SINGLE, height=10)
completed_listbox.pack(fill=tk.BOTH, expand=True)

# Run the application
root.mainloop()
