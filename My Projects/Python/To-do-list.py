import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#2C3E50')
        
        # Data file
        self.filename = "tasks.json"
        self.tasks = self.load_tasks()
        
        # Create GUI
        self.create_widgets()
        self.refresh_task_list()
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#34495E', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📋 To-Do List Manager",
            font=('Arial', 24, 'bold'),
            bg='#34495E',
            fg='white'
        )
        title_label.pack(expand=True)
        
        # Stats Frame
        stats_frame = tk.Frame(main_frame, bg='#34495E')
        stats_frame.pack(fill='x', pady=(0, 20))
        
        self.stats_label = tk.Label(
            stats_frame,
            text="",
            font=('Arial', 12),
            bg='#34495E',
            fg='#ECF0F1'
        )
        self.stats_label.pack(pady=10)
        
        # Main Content - Treeview for tasks
        self.create_treeview(main_frame)
        
        # Buttons Frame
        button_frame = tk.Frame(main_frame, bg='#2C3E50')
        button_frame.pack(fill='x', pady=(20, 0))
        
        # Configure button grid
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)
        
        # Buttons with colors
        buttons = [
            ("➕ Add Task", self.add_task, '#27AE60', 0),
            ("✅ Complete", self.complete_task, '#2980B9', 1),
            ("✏️ Edit Task", self.edit_task, '#F39C12', 2),
            ("❌ Delete Task", self.delete_task, '#E74C3C', 3),
            ("🔍 Search", self.search_tasks, '#8E44AD', 0),
            ("📊 Statistics", self.show_statistics, '#16A085', 1),
            ("📥 Export", self.export_tasks, '#7F8C8D', 2),
            ("🔄 Refresh", self.refresh_task_list, '#95A5A6', 3)
        ]
        
        for text, command, color, col in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=('Arial', 11, 'bold'),
                bg=color,
                fg='white',
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2',
                command=command
            )
            btn.grid(row=0 if buttons.index((text, command, color, col)) < 4 else 1, 
                    column=col, padx=5, pady=5, sticky='ew')
            
            # Hover effect
            btn.bind('<Enter>', lambda e, b=btn, c=color: b.configure(bg=self.darken_color(c)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.configure(bg=c))
        
        # Search Frame (hidden by default)
        self.search_frame = tk.Frame(main_frame, bg='#34495E')
        self.search_entry = tk.Entry(
            self.search_frame,
            font=('Arial', 12),
            bg='white',
            fg='#2C3E50'
        )
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        search_btn = tk.Button(
            self.search_frame,
            text="Search",
            font=('Arial', 11, 'bold'),
            bg='#8E44AD',
            fg='white',
            bd=0,
            padx=20,
            command=self.perform_search
        )
        search_btn.pack(side='right')
        
        close_search_btn = tk.Button(
            self.search_frame,
            text="✕",
            font=('Arial', 11, 'bold'),
            bg='#E74C3C',
            fg='white',
            bd=0,
            padx=10,
            command=self.hide_search
        )
        close_search_btn.pack(side='right', padx=(0, 10))
        
    def create_treeview(self, parent):
        # Treeview Frame
        tree_frame = tk.Frame(parent, bg='#34495E')
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(tree_frame)
        v_scrollbar.pack(side='right', fill='y')
        
        h_scrollbar = tk.Scrollbar(tree_frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Status', 'Priority', 'Due Date', 'Created'),
            show='tree headings',
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Configure scrollbars
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.column('#0', width=300, minwidth=200)
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Status', width=80, anchor='center')
        self.tree.column('Priority', width=80, anchor='center')
        self.tree.column('Due Date', width=100, anchor='center')
        self.tree.column('Created', width=150, anchor='center')
        
        # Configure headings
        self.tree.heading('#0', text='Task Description')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Priority', text='Priority')
        self.tree.heading('Due Date', text='Due Date')
        self.tree.heading('Created', text='Created')
        
        # Tag configurations for colors
        self.tree.tag_configure('completed', background='#27AE60', foreground='white')
        self.tree.tag_configure('high', background='#E74C3C', foreground='white')
        self.tree.tag_configure('medium', background='#F39C12', foreground='white')
        self.tree.tag_configure('low', background='#3498DB', foreground='white')
        
        self.tree.pack(fill='both', expand=True)
        
        # Bind double-click to edit
        self.tree.bind('<Double-Button-1>', lambda e: self.edit_task())
        
    def darken_color(self, color):
        """Darken a color for hover effect"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            r = max(0, r - 20)
            g = max(0, g - 20)
            b = max(0, b - 20)
            
            return f'#{r:02x}{g:02x}{b:02x}'
        return color
    
    def load_tasks(self):
        """Load tasks from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except:
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to file"""
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=2)
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add tasks to treeview
        for task in self.tasks:
            status = "✅" if task['completed'] else "⭕"
            priority = task.get('priority', 'medium').upper()
            due_date = task.get('due_date', 'N/A')
            created = task.get('created_at', 'N/A')
            
            # Determine tag based on status and priority
            if task['completed']:
                tag = 'completed'
            else:
                tag = task.get('priority', 'medium')
            
            self.tree.insert(
                '',
                'end',
                text=task['description'],
                values=(task['id'], status, priority, due_date, created),
                tags=(tag,)
            )
        
        # Update stats
        self.update_stats()
        self.hide_search()
    
    def update_stats(self):
        """Update statistics display"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['completed'])
        pending = total - completed
        
        if total > 0:
            stats = f"📊 Total: {total} | ✅ Completed: {completed} ({completed/total*100:.1f}%) | ⭕ Pending: {pending}"
        else:
            stats = "📊 No tasks yet. Click 'Add Task' to get started!"
        
        self.stats_label.config(text=stats)
    
    def add_task(self):
        """Add a new task"""
        dialog = TaskDialog(self.root, "Add New Task")
        if dialog.result:
            description, priority, due_date = dialog.result
            
            task = {
                'id': len(self.tasks) + 1,
                'description': description,
                'priority': priority,
                'due_date': due_date,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'completed': False
            }
            
            self.tasks.append(task)
            self.save_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Success", "Task added successfully!")
    
    def complete_task(self):
        """Mark selected task as completed"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to complete!")
            return
        
        task_id = int(self.tree.item(selected[0])['values'][0])
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                break
        
        self.save_tasks()
        self.refresh_task_list()
        messagebox.showinfo("Success", "Task marked as completed!")
    
    def edit_task(self):
        """Edit selected task"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to edit!")
            return
        
        task_id = int(self.tree.item(selected[0])['values'][0])
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        
        if task:
            dialog = TaskDialog(
                self.root,
                "Edit Task",
                task['description'],
                task['priority'],
                task.get('due_date', '')
            )
            
            if dialog.result:
                description, priority, due_date = dialog.result
                task['description'] = description
                task['priority'] = priority
                task['due_date'] = due_date
                
                self.save_tasks()
                self.refresh_task_list()
                messagebox.showinfo("Success", "Task updated successfully!")
    
    def delete_task(self):
        """Delete selected task"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            task_id = int(self.tree.item(selected[0])['values'][0])
            
            # Remove task
            self.tasks = [t for t in self.tasks if t['id'] != task_id]
            
            # Reorder IDs
            for i, task in enumerate(self.tasks, 1):
                task['id'] = i
            
            self.save_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Success", "Task deleted successfully!")
    
    def search_tasks(self):
        """Show search frame"""
        self.search_frame.pack(fill='x', pady=(20, 0))
        self.search_entry.delete(0, tk.END)
        self.search_entry.focus()
    
    def hide_search(self):
        """Hide search frame"""
        self.search_frame.pack_forget()
    
    def perform_search(self):
        """Perform search"""
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            messagebox.showwarning("Empty Search", "Please enter a search keyword!")
            return
        
        # Clear current display
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add matching tasks
        for task in self.tasks:
            if keyword in task['description'].lower():
                status = "✅" if task['completed'] else "⭕"
                priority = task.get('priority', 'medium').upper()
                due_date = task.get('due_date', 'N/A')
                created = task.get('created_at', 'N/A')
                
                if task['completed']:
                    tag = 'completed'
                else:
                    tag = task.get('priority', 'medium')
                
                self.tree.insert(
                    '',
                    'end',
                    text=task['description'],
                    values=(task['id'], status, priority, due_date, created),
                    tags=(tag,)
                )
    
    def show_statistics(self):
        """Show detailed statistics"""
        total = len(self.tasks)
        if total == 0:
            messagebox.showinfo("Statistics", "No tasks to analyze.")
            return
        
        completed = sum(1 for t in self.tasks if t['completed'])
        pending = total - completed
        
        priority_counts = {
            'high': sum(1 for t in self.tasks if t.get('priority') == 'high'),
            'medium': sum(1 for t in self.tasks if t.get('priority') == 'medium'),
            'low': sum(1 for t in self.tasks if t.get('priority') == 'low')
        }
        
        stats_text = f"""
📊 TASK STATISTICS
{'='*30}

Total Tasks: {total}
Completed: {completed} ({completed/total*100:.1f}%)
Pending: {pending} ({pending/total*100:.1f}%)

📈 By Priority:
  High: {priority_counts['high']}
  Medium: {priority_counts['medium']}
  Low: {priority_counts['low']}

📅 Tasks with due dates: {sum(1 for t in self.tasks if t.get('due_date'))}
        """
        
        messagebox.showinfo("Statistics", stats_text)
    
    def export_tasks(self):
        """Export tasks to a text file"""
        if not self.tasks:
            messagebox.showwarning("No Tasks", "No tasks to export!")
            return
        
        filename = f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as file:
            file.write("TO-DO LIST EXPORT\n")
            file.write("="*50 + "\n\n")
            
            for task in self.tasks:
                status = "✓" if task['completed'] else "○"
                priority = task.get('priority', 'medium').upper()
                due = f" (Due: {task['due_date']})" if task.get('due_date') else ""
                created = task.get('created_at', 'N/A')
                
                file.write(f"[{status}] {task['description']}\n")
                file.write(f"   Priority: {priority}{due}\n")
                file.write(f"   Created: {created}\n\n")
        
        messagebox.showinfo("Export Successful", f"Tasks exported to {filename}")

class TaskDialog:
    def __init__(self, parent, title, description="", priority="medium", due_date=""):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.configure(bg='#2C3E50')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (300 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Create form
        self.create_form(description, priority, due_date)
        
        # Wait for dialog to close
        parent.wait_window(self.dialog)
    
    def create_form(self, description, priority, due_date):
        # Description
        tk.Label(
            self.dialog,
            text="Task Description:",
            font=('Arial', 11),
            bg='#2C3E50',
            fg='white'
        ).pack(pady=(20, 5))
        
        self.desc_entry = tk.Entry(
            self.dialog,
            font=('Arial', 12),
            width=40
        )
        self.desc_entry.insert(0, description)
        self.desc_entry.pack(pady=(0, 10))
        self.desc_entry.focus()
        
        # Priority
        tk.Label(
            self.dialog,
            text="Priority:",
            font=('Arial', 11),
            bg='#2C3E50',
            fg='white'
        ).pack()
        
        self.priority_var = tk.StringVar(value=priority)
        priority_frame = tk.Frame(self.dialog, bg='#2C3E50')
        priority_frame.pack(pady=5)
        
        priorities = [('High', 'high'), ('Medium', 'medium'), ('Low', 'low')]
        for text, value in priorities:
            tk.Radiobutton(
                priority_frame,
                text=text,
                value=value,
                variable=self.priority_var,
                bg='#2C3E50',
                fg='white',
                selectcolor='#2C3E50',
                activebackground='#2C3E50'
            ).pack(side='left', padx=10)
        
        # Due Date
        tk.Label(
            self.dialog,
            text="Due Date (YYYY-MM-DD):",
            font=('Arial', 11),
            bg='#2C3E50',
            fg='white'
        ).pack(pady=(10, 5))
        
        self.date_entry = tk.Entry(
            self.dialog,
            font=('Arial', 12),
            width=20
        )
        self.date_entry.insert(0, due_date)
        self.date_entry.pack(pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg='#2C3E50')
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="OK",
            font=('Arial', 11, 'bold'),
            bg='#27AE60',
            fg='white',
            bd=0,
            padx=30,
            command=self.ok_clicked
        ).pack(side='left', padx=10)
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 11, 'bold'),
            bg='#E74C3C',
            fg='white',
            bd=0,
            padx=30,
            command=self.cancel_clicked
        ).pack(side='left', padx=10)
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self.cancel_clicked())
    
    def ok_clicked(self):
        description = self.desc_entry.get().strip()
        if not description:
            messagebox.showwarning("Invalid Input", "Task description cannot be empty!")
            return
        
        priority = self.priority_var.get()
        due_date = self.date_entry.get().strip()
        
        # Validate due date if provided
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Invalid Date", "Please use YYYY-MM-DD format for due date!")
                return
        
        self.result = (description, priority, due_date if due_date else None)
        self.dialog.destroy()
    
    def cancel_clicked(self):
        self.dialog.destroy()

def main():
    root = tk.Tk()
    
    # Set style for treeview
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview", 
                    background="#ECF0F1",
                    foreground="#2C3E50",
                    rowheight=30,
                    fieldbackground="#ECF0F1")
    style.map('Treeview', background=[('selected', '#3498DB')])
    
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()