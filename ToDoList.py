import tkinter as tk
from tkinter import messagebox, filedialog, Tk
from datetime import datetime
import os
import textwrap

class ToDoListManager:
    def __init__(self, root):
        # Create the main directory for storing tasks if it doesn't exist
        self.tasks_dir = os.path.join(os.path.expanduser('~'), 'ToDoListApp')
        os.makedirs(self.tasks_dir, exist_ok=True)
        
        # Full paths for task files
        self.tasks_file = os.path.join(self.tasks_dir, 'tasks.txt')
        self.completed_tasks_file = os.path.join(self.tasks_dir, 'completed_tasks.txt')
        
        # Create the main window
        self.root = root
        self.root.title("Take Actions Official™")
        self.root.geometry("800x700")
        self.root.configure(bg="#333333")

        # Create menu bar
        self.create_menu_bar()

        # Bind keyboard shortcuts
        self.bind_shortcuts()

        # Load existing tasks
        self.tasks = []
        self.load_tasks()

        # Create UI components
        self.create_ui_components()

        # Update task list and countdown
        self.update_task_list()
        self.update_countdown()

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)



    def save_tasks_and_quit(self):
        """Save tasks and close the application"""
        self.save_tasks()
        self.root.destroy()

    def open_tasks_file(self):
        """Open and potentially import tasks from a file"""
        try:
            # Open file dialog to select a task file
            file_path = filedialog.askopenfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            
            # If a file was selected
            if file_path:
                # Open and read the selected file
                with open(file_path, "r") as f:
                    for line in f:
                        parts = line.strip().split('|||')
                        if len(parts) == 3:
                            title, deadline_str, notes = parts
                            try:
                                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
                                notes = notes.replace('\\n', '\n')
                                self.tasks.append((title, deadline, notes))
                            except ValueError:
                                print(f"Skipping invalid task: {line}")
                
                # Update the task list and save
                self.update_task_list()
                
                # Show success message
                messagebox.showinfo("Tasks Imported", f"Successfully imported tasks from {os.path.basename(file_path)}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not open tasks file: {e}")

    def create_menu_bar(self):
        # Menu bar setup
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open Tasks", command=self.open_tasks_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save Tasks", command=self.save_tasks, accelerator="Ctrl+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.save_tasks_and_quit, accelerator="Alt+F4")

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Add Task", command=self.add_task, accelerator="Ctrl+N")
        self.edit_menu.add_command(label="Delete Task", command=self.delete_task, accelerator="Del")
        self.edit_menu.add_command(label="Complete Task", command=self.complete_task, accelerator="Ctrl+D")

        self.paymelah = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="PREMIUM", menu=self.paymelah)
        self.paymelah.add_command(label="Auto Done", command=self.QR)
        self.paymelah.add_command(label="Increase your productivity", command=self.QR)
        self.paymelah.add_command(label="Focus mode on?", command=self.QR)
        self.paymelah.add_command(label="SCAN FOR FREE MONEY", command=self.QR, accelerator="Ctrl+M")


    
    def QR(self):
        self.Tngqr = tk.PhotoImage(file="C:/Users/user/Pictures/Screenshots/Screenshot 2024-04-04 115401.png")
        self.qr_label = tk.Label(self.root, image=self.Tngqr)
        self.qr_label.pack(pady=20)

    def bind_shortcuts(self):
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda event: self.open_tasks_file())
        self.root.bind('<Control-s>', lambda event: self.save_tasks())
        self.root.bind('<Control-n>', lambda event: self.focus_on_add_task())
        self.root.bind('<Delete>', lambda event: self.delete_task())
        self.root.bind('<Control-d>', lambda event: self.complete_task())

    def create_ui_components(self):
        # Main frames
        self.task_frame = tk.Frame(self.root, bg="black", width=500)
        self.task_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.details_frame = tk.Frame(self.root, bg="black", width=300)
        self.details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=20, pady=20)

        # Task list
        self.task_label = tk.Label(self.task_frame, text="Take Actions", font=("Arial", 16, "bold"), bg="black", fg="gold")
        self.task_label.pack(pady=10)

        self.task_listbox = tk.Listbox(self.task_frame, width=40, height=20, font=("Arial", 12), 
                                       bg="gray", fg="black", selectbackground="#ccc", selectforeground="#333")
        self.task_listbox.pack(fill=tk.BOTH, expand=True)
        self.task_listbox.bind("<<ListboxSelect>>", self.display_task_details)

        # Countdown label
        self.countdown_label = tk.Label(self.task_frame, text="", font=("Arial", 12), fg="red", bg="white")
        self.countdown_label.pack(pady=10)

        # Task details section
        self.details_label = tk.Label(self.details_frame, text="Task Details", font=("Arial", 16, "bold"), bg="black", fg="gold")
        self.details_label.pack(pady=10)

        # Title input
        self.title_label = tk.Label(self.details_frame, text="Title:", font=("Arial", 12), bg="gold", fg="black")
        self.title_label.pack(anchor="w")
        self.title_entry = tk.Entry(self.details_frame, font=("Arial", 12), bg="gray", fg="black", insertbackground="gold")
        self.title_entry.pack(fill=tk.X, pady=5)

        # Deadline input
        self.deadline_label = tk.Label(self.details_frame, text="Deadline (YYYY-MM-DD HH:MM):", font=("Arial", 12), bg="gold", fg="black")
        self.deadline_label.pack(anchor="w")
        self.deadline_entry = tk.Entry(self.details_frame, font=("Arial", 12), bg="gray", fg="black", insertbackground="gold")
        self.deadline_entry.pack(fill=tk.X, pady=5)

        # Notes input
        self.notes_label = tk.Label(self.details_frame, text="Notes:", font=("Arial", 12), bg="gold", fg="black")
        self.notes_label.pack(anchor="w")

        # Notes frame with scrollbar
        self.notes_frame = tk.Frame(self.details_frame)
        self.notes_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.notes_scrollbar = tk.Scrollbar(self.notes_frame)
        self.notes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.notes_text = tk.Text(self.notes_frame, width=40, height=10, font=("Arial", 12),
                                  bg="gray", fg="black", insertbackground="gold",
                                  yscrollcommand=self.notes_scrollbar.set, wrap=tk.WORD)
        self.notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.notes_scrollbar.config(command=self.notes_text.yview)

        # Buttons
        self.add_button = tk.Button(self.details_frame, text="Add Task", command=self.add_task, 
                                    font=("Arial", 12), bg="#333", fg="white")
        self.add_button.pack(side=tk.TOP, pady=10)

        self.delete_button = tk.Button(self.details_frame, text="Delete Task", command=self.delete_task, 
                                       font=("Arial", 12), bg="#333", fg="white")
        self.delete_button.pack(side=tk.TOP, pady=5)

        self.complete_button = tk.Button(self.details_frame, text="Mark as Complete", command=self.complete_task, 
                                         font=("Arial", 12), bg="#333", fg="white")
        self.complete_button.pack(side=tk.TOP, pady=5)

    def on_close(self):
        """Handle the close event for the To-Do List window."""
        self.save_tasks()
        self.root.destroy()

    def focus_on_add_task(self):
        """Set focus on the title entry for quick task addition"""
        self.title_entry.focus_set()

    def load_tasks(self):
        """Load tasks from the tasks file with robust error handling"""
        try:
            if not os.path.exists(self.tasks_file):
                # Create the file if it doesn't exist
                open(self.tasks_file, 'a').close()
                return

            with open(self.tasks_file, "r") as f:
                self.tasks = []
                for line in f:
                    parts = line.strip().split('|||')
                    if len(parts) == 3:
                        title, deadline_str, notes = parts
                        try:
                            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
                            notes = notes.replace('\\n', '\n')
                            self.tasks.append((title, deadline, notes))
                        except ValueError:
                            print(f"Skipping invalid task: {line}")
        except PermissionError:
            messagebox.showerror("Permission Error", 
                f"Cannot read tasks file. Ensure you have permissions to access {self.tasks_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load tasks: {e}")

    def save_tasks(self):
        """Save tasks to the tasks file with robust error handling"""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.tasks_file), exist_ok=True)
            
            with open(self.tasks_file, "w") as f:
                for task in self.tasks:
                    title, deadline, notes = task
                    escaped_notes = notes.replace('\n', '\\n')
                    f.write(f"{title}|||{deadline.strftime('%Y-%m-%d %H:%M')}|||{escaped_notes}\n")
            
            # Optional: Show a subtle notification
            self.root.after(1000, self.show_save_notification)
        except PermissionError:
            messagebox.showerror("Permission Error", 
                f"Cannot save tasks file. Ensure you have permissions to write to {self.tasks_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save tasks: {e}")

    def show_save_notification(self):
        """Show a temporary save notification"""
        notification = tk.Label(self.task_frame, text="Tasks Saved!", fg="green", bg="black")
        notification.pack(side=tk.BOTTOM)
        self.root.after(2000, notification.destroy)

    def save_tasks_and_quit(self):
        """Save tasks and close the application"""
        self.save_tasks()
        self.root.destroy()

    def add_task(self):
        """Add a new task to the list"""
        title = self.title_entry.get().strip()
        deadline_str = self.deadline_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()

        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

            if title:
                self.tasks.append((title, deadline, notes))
                self.update_task_list()
                
                # Clear input fields
                self.title_entry.delete(0, tk.END)
                self.deadline_entry.delete(0, tk.END)
                self.notes_text.delete("1.0", tk.END)
            else:
                messagebox.showwarning("Invalid Task", "Please enter a task title")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter deadline in YYYY-MM-DD HH:MM format")

    def delete_task(self):
        """Delete the selected task"""
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            del self.tasks[index]
            self.update_task_list()

    def complete_task(self):
        """Mark a task as completed and move to completed tasks file"""
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            completed_task = self.tasks[index]
            title, deadline, notes = completed_task

            # Save to completed tasks file
            try:
                with open(self.completed_tasks_file, "a") as f:
                    escaped_notes = notes.replace('\n', '\\n')
                    f.write(f"{title}|||{deadline.strftime('%Y-%m-%d %H:%M')}|||{escaped_notes}\n")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save completed task: {e}")

            # Remove from current tasks
            del self.tasks[index]
            self.update_task_list()

    def display_task_details(self, event):
        """Display details of the selected task"""
        selected = self.task_listbox.curselection()
        if selected:
            title, deadline, notes = self.tasks[selected[0]]
            
            # Clear existing entries
            self.title_entry.delete(0, tk.END)
            self.deadline_entry.delete(0, tk.END)
            self.notes_text.delete("1.0", tk.END)
            
            # Populate with selected task details
            self.title_entry.insert(0, title)
            self.deadline_entry.insert(0, deadline.strftime("%Y-%m-%d %H:%M"))
            self.notes_text.insert("1.0", notes)

    def update_task_list(self):
        """Update the task listbox and save tasks"""
        # Clear existing listbox
        self.task_listbox.delete(0, tk.END)
        
        # Repopulate listbox
        for task in self.tasks:
            title, deadline, notes = task
            display_text = f"{title} (Deadline: {deadline.strftime('%Y-%m-%d %H:%M')}) - {notes}"
            self.task_listbox.insert(tk.END, display_text)
        
        # Save tasks after update
        self.save_tasks()

    def update_countdown(self):
        """Update the countdown to the nearest deadline"""
        now = datetime.now()
        nearest_deadline = None
        nearest_task = None

        for task in self.tasks:
            title, deadline, _ = task
            if deadline > now:
                if nearest_deadline is None or deadline < nearest_deadline:
                    nearest_deadline = deadline
                    nearest_task = title

        # Update countdown label
        if nearest_deadline:
            time_left = nearest_deadline - now
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Format countdown text
            if days > 0:
                countdown_text = f"Next Deadline: {nearest_task} in {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
            elif hours > 0:
                countdown_text = f"Next Deadline: {nearest_task} in {hours} hours, {minutes} minutes, {seconds} seconds"
            else:
                countdown_text = f"Next Deadline: {nearest_task} in {minutes} minutes, {seconds} seconds"

            self.countdown_label.config(text=countdown_text)
        else:
            self.countdown_label.config(text="No upcoming deadlines")

        # Schedule next update

        # Schedule next update in 1 second
        self.root.after(1000, self.update_countdown)  # Use self.root here

if __name__ == "__main__":
    root = Tk()
    app = ToDoListManager(root)
    root.mainloop()
