import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import re
from datetime import datetime
import csv

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("📇 Contact Book Manager")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2C3E50')
        
        # Data file
        self.filename = "contacts.json"
        self.contacts = self.load_contacts()
        
        # Search variable
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_contacts)
        
        # Create GUI
        self.create_widgets()
        self.refresh_contact_list()
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#34495E', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📇 CONTACT BOOK MANAGER",
            font=('Arial', 24, 'bold'),
            bg='#34495E',
            fg='#F1C40F'
        )
        title_label.pack(expand=True)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#2C3E50')
        main_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Left Panel - Contact List
        left_panel = tk.Frame(main_container, bg='#34495E', width=400)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Search Frame
        search_frame = tk.Frame(left_panel, bg='#34495E')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=('Arial', 11),
            bg='#34495E',
            fg='#ECF0F1'
        ).pack(side='left', padx=(0, 5))
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', 11),
            bg='#ECF0F1',
            fg='#2C3E50',
            bd=2,
            relief='sunken'
        )
        search_entry.pack(side='left', fill='x', expand=True)
        
        # Contact List with Scrollbar
        list_frame = tk.Frame(left_panel, bg='#34495E')
        list_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Listbox
        self.contact_listbox = tk.Listbox(
            list_frame,
            font=('Arial', 11),
            bg='#ECF0F1',
            fg='#2C3E50',
            selectbackground='#3498DB',
            selectforeground='white',
            yscrollcommand=scrollbar.set,
            bd=2,
            relief='sunken'
        )
        self.contact_listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=self.contact_listbox.yview)
        
        # Bind selection event
        self.contact_listbox.bind('<<ListboxSelect>>', self.on_contact_select)
        
        # Contact Count Label
        self.count_label = tk.Label(
            left_panel,
            text="Total Contacts: 0",
            font=('Arial', 10, 'italic'),
            bg='#34495E',
            fg='#ECF0F1'
        )
        self.count_label.pack(pady=(0, 10))
        
        # Right Panel - Contact Details & Actions
        right_panel = tk.Frame(main_container, bg='#34495E')
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Contact Details Frame
        details_frame = tk.LabelFrame(
            right_panel,
            text="📋 Contact Details",
            font=('Arial', 12, 'bold'),
            bg='#34495E',
            fg='#F1C40F',
            bd=2,
            relief='groove'
        )
        details_frame.pack(fill='both', expand=True, padx=10, pady=(10, 10))
        
        # Details content
        details_content = tk.Frame(details_frame, bg='#34495E')
        details_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Contact fields
        fields = [
            ("👤 Name:", "name"),
            ("📞 Phone:", "phone"),
            ("✉️ Email:", "email"),
            ("🏠 Address:", "address"),
            ("🏢 Company:", "company"),
            ("🎂 Birthday:", "birthday"),
            ("📝 Notes:", "notes")
        ]
        
        self.detail_vars = {}
        for i, (label, field) in enumerate(fields):
            # Label
            tk.Label(
                details_content,
                text=label,
                font=('Arial', 11, 'bold'),
                bg='#34495E',
                fg='#ECF0F1'
            ).grid(row=i, column=0, sticky='w', pady=5, padx=(0, 10))
            
            # Value
            var = tk.StringVar(value="—")
            self.detail_vars[field] = var
            
            value_label = tk.Label(
                details_content,
                textvariable=var,
                font=('Arial', 11),
                bg='#34495E',
                fg='#BDC3C7',
                wraplength=300,
                justify='left'
            )
            value_label.grid(row=i, column=1, sticky='w', pady=5)
        
        # Action Buttons Frame
        action_frame = tk.Frame(right_panel, bg='#34495E')
        action_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Buttons with colors
        buttons = [
            ("➕ Add Contact", self.add_contact, '#27AE60'),
            ("✏️ Edit Contact", self.edit_contact, '#F39C12'),
            ("❌ Delete Contact", self.delete_contact, '#E74C3C'),
            ("📞 Call", self.call_contact, '#3498DB'),
            ("📧 Email", self.email_contact, '#9B59B6'),
            ("📊 Export", self.export_contacts, '#1ABC9C'),
            ("📥 Import", self.import_contacts, '#E67E22'),
            ("🔄 Refresh", self.refresh_contact_list, '#95A5A6')
        ]
        
        # Create button grid (2 rows, 4 columns)
        for i, (text, command, color) in enumerate(buttons):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                action_frame,
                text=text,
                font=('Arial', 10, 'bold'),
                bg=color,
                fg='white',
                bd=0,
                padx=10,
                pady=8,
                cursor='hand2',
                command=command
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky='ew')
            
            # Hover effect
            btn.bind('<Enter>', lambda e, b=btn, c=color: b.configure(bg=self.darken_color(c)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.configure(bg=c))
        
        # Configure grid weights
        for i in range(4):
            action_frame.columnconfigure(i, weight=1)
        
        # Status Bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=('Arial', 9),
            bg='#34495E',
            fg='#ECF0F1',
            anchor='w',
            padx=10
        )
        self.status_bar.pack(side='bottom', fill='x')
        
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
    
    def load_contacts(self):
        """Load contacts from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Contact file is corrupted. Starting with empty contact book.")
                return []
        return []
    
    def save_contacts(self):
        """Save contacts to file"""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.contacts, file, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save contacts: {str(e)}")
            return False
    
    def refresh_contact_list(self):
        """Refresh the contact listbox"""
        self.contact_listbox.delete(0, tk.END)
        
        # Sort contacts by name
        sorted_contacts = sorted(self.contacts, key=lambda x: x['name'].lower())
        
        for contact in sorted_contacts:
            display_text = f"{contact['name']} - {contact.get('phone', 'No phone')}"
            self.contact_listbox.insert(tk.END, display_text)
        
        # Update count
        count = len(self.contacts)
        self.count_label.config(text=f"Total Contacts: {count}")
        self.status_bar.config(text=f"Loaded {count} contacts")
    
    def on_contact_select(self, event):
        """Handle contact selection from listbox"""
        selection = self.contact_listbox.curselection()
        if selection:
            index = selection[0]
            # Get the actual contact data (sorted)
            sorted_contacts = sorted(self.contacts, key=lambda x: x['name'].lower())
            if index < len(sorted_contacts):
                contact = sorted_contacts[index]
                self.display_contact_details(contact)
    
    def display_contact_details(self, contact):
        """Display contact details in the right panel"""
        fields = ['name', 'phone', 'email', 'address', 'company', 'birthday', 'notes']
        
        for field in fields:
            value = contact.get(field, '—')
            if not value or value == '':
                value = '—'
            self.detail_vars[field].set(value)
    
    def search_contacts(self, *args):
        """Search contacts based on search text"""
        search_term = self.search_var.get().lower()
        
        self.contact_listbox.delete(0, tk.END)
        
        # Filter contacts
        filtered_contacts = []
        for contact in self.contacts:
            if (search_term in contact['name'].lower() or 
                search_term in contact.get('phone', '').lower() or
                search_term in contact.get('email', '').lower()):
                filtered_contacts.append(contact)
        
        # Sort and display filtered contacts
        sorted_contacts = sorted(filtered_contacts, key=lambda x: x['name'].lower())
        
        for contact in sorted_contacts:
            display_text = f"{contact['name']} - {contact.get('phone', 'No phone')}"
            self.contact_listbox.insert(tk.END, display_text)
        
        # Update count
        self.count_label.config(text=f"Showing {len(filtered_contacts)} of {len(self.contacts)} contacts")
    
    def add_contact(self):
        """Add a new contact"""
        dialog = ContactDialog(self.root, "Add New Contact")
        if dialog.result:
            # Check for duplicate phone numbers
            phone = dialog.result.get('phone', '')
            if phone and any(c.get('phone') == phone for c in self.contacts):
                if not messagebox.askyesno("Duplicate Phone", 
                                          "A contact with this phone number already exists. Add anyway?"):
                    return
            
            self.contacts.append(dialog.result)
            if self.save_contacts():
                self.refresh_contact_list()
                self.status_bar.config(text=f"Added contact: {dialog.result['name']}")
                messagebox.showinfo("Success", f"Contact '{dialog.result['name']}' added successfully!")
    
    def edit_contact(self):
        """Edit selected contact"""
        selection = self.contact_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a contact to edit!")
            return
        
        # Get selected contact
        index = selection[0]
        sorted_contacts = sorted(self.contacts, key=lambda x: x['name'].lower())
        if index >= len(sorted_contacts):
            return
        
        contact = sorted_contacts[index]
        
        # Find original contact in unsorted list
        original_contact = next(c for c in self.contacts if c['name'] == contact['name'] 
                               and c.get('phone') == contact.get('phone'))
        
        dialog = ContactDialog(self.root, "Edit Contact", original_contact)
        if dialog.result:
            # Update contact
            original_contact.update(dialog.result)
            if self.save_contacts():
                self.refresh_contact_list()
                self.status_bar.config(text=f"Updated contact: {dialog.result['name']}")
                messagebox.showinfo("Success", "Contact updated successfully!")
    
    def delete_contact(self):
        """Delete selected contact"""
        selection = self.contact_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a contact to delete!")
            return
        
        # Get selected contact
        index = selection[0]
        sorted_contacts = sorted(self.contacts, key=lambda x: x['name'].lower())
        if index >= len(sorted_contacts):
            return
        
        contact = sorted_contacts[index]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{contact['name']}'?"):
            # Remove contact
            self.contacts = [c for c in self.contacts if not 
                           (c['name'] == contact['name'] and c.get('phone') == contact.get('phone'))]
            
            if self.save_contacts():
                self.refresh_contact_list()
                self.clear_details()
                self.status_bar.config(text=f"Deleted contact: {contact['name']}")
                messagebox.showinfo("Success", "Contact deleted successfully!")
    
    def call_contact(self):
        """Simulate calling a contact"""
        selection = self.contact_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a contact to call!")
            return
        
        index = selection[0]
        sorted_contacts = sorted(self.contacts, key=lambda x: x['name'].lower())
        if index >= len(sorted_contacts):
            return
        
        contact = sorted_contacts[index]
        phone = contact.get('phone', '')
        
        if phone and phone != '—':
            messagebox.showinfo("Call", f"📞 Calling {contact['name']} at {phone}...\n(This is a simulation)")
            self.status_bar.config(text=f"Calling {contact['name']}...")
        else:
            messagebox.showwarning("No Phone", "This contact has no phone number!")
    
    def email_contact(self):
        """Simulate emailing a contact"""
        selection = self.contact_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a contact to email!")
            return
        
        index = selection[0]
        sorted_contacts = sorted(self.contacts, key=lambda x: x['name'].lower())
        if index >= len(sorted_contacts):
            return
        
        contact = sorted_contacts[index]
        email = contact.get('email', '')
        
        if email and email != '—':
            messagebox.showinfo("Email", f"📧 Opening email to {contact['name']} at {email}...\n(This is a simulation)")
            self.status_bar.config(text=f"Emailing {contact['name']}...")
        else:
            messagebox.showwarning("No Email", "This contact has no email address!")
    
    def export_contacts(self):
        """Export contacts to CSV file"""
        if not self.contacts:
            messagebox.showwarning("No Contacts", "No contacts to export!")
            return
        
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"contacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    fieldnames = ['name', 'phone', 'email', 'address', 'company', 'birthday', 'notes']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.contacts)
                
                self.status_bar.config(text=f"Exported {len(self.contacts)} contacts to {filename}")
                messagebox.showinfo("Success", f"Contacts exported successfully!\nFile: {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export contacts: {str(e)}")
    
    def import_contacts(self):
        """Import contacts from CSV file"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                imported = 0
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Clean up the data
                        contact = {k: v.strip() if v else '' for k, v in row.items()}
                        
                        # Check for duplicates (by name and phone)
                        if not any(c['name'] == contact.get('name') and 
                                  c.get('phone') == contact.get('phone') 
                                  for c in self.contacts):
                            self.contacts.append(contact)
                            imported += 1
                
                if imported > 0:
                    self.save_contacts()
                    self.refresh_contact_list()
                    self.status_bar.config(text=f"Imported {imported} contacts")
                    messagebox.showinfo("Success", f"Imported {imported} contacts successfully!")
                else:
                    messagebox.showinfo("No New Contacts", "No new contacts were imported (duplicates ignored).")
                    
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import contacts: {str(e)}")
    
    def clear_details(self):
        """Clear contact details display"""
        for var in self.detail_vars.values():
            var.set('—')


class ContactDialog:
    def __init__(self, parent, title, contact=None):
        self.result = None
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.configure(bg='#34495E')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (500 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (600 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Make dialog modal
        self.dialog.focus_set()
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
        
        # Create form
        self.create_form(contact)
        
        # Wait for dialog to close
        parent.wait_window(self.dialog)
    
    def create_form(self, contact):
        # Title
        title_label = tk.Label(
            self.dialog,
            text=("✏️ Edit Contact" if contact else "➕ New Contact"),
            font=('Arial', 16, 'bold'),
            bg='#34495E',
            fg='#F1C40F'
        )
        title_label.pack(pady=(20, 20))
        
        # Form Frame
        form_frame = tk.Frame(self.dialog, bg='#34495E')
        form_frame.pack(fill='both', expand=True, padx=30, pady=(0, 20))
        
        # Form fields
        fields = [
            ("👤 Name *:", "name", True),
            ("📞 Phone *:", "phone", True),
            ("✉️ Email:", "email", False),
            ("🏠 Address:", "address", False),
            ("🏢 Company:", "company", False),
            ("🎂 Birthday (YYYY-MM-DD):", "birthday", False),
            ("📝 Notes:", "notes", False)
        ]
        
        self.entries = {}
        
        for i, (label, field, required) in enumerate(fields):
            # Label
            label_widget = tk.Label(
                form_frame,
                text=label,
                font=('Arial', 11, 'bold' if required else 'normal'),
                bg='#34495E',
                fg='#F1C40F' if required else '#ECF0F1'
            )
            label_widget.grid(row=i, column=0, sticky='w', pady=8, padx=(0, 10))
            
            # Entry
            entry = tk.Entry(
                form_frame,
                font=('Arial', 11),
                bg='#ECF0F1',
                fg='#2C3E50',
                width=30,
                bd=2,
                relief='sunken'
            )
            entry.grid(row=i, column=1, sticky='ew', pady=8)
            
            # If editing, populate with existing data
            if contact and field in contact:
                entry.insert(0, contact[field])
            
            self.entries[field] = entry
        
        # Notes field (multiline)
        self.notes_text = tk.Text(
            form_frame,
            font=('Arial', 11),
            bg='#ECF0F1',
            fg='#2C3E50',
            width=30,
            height=4,
            bd=2,
            relief='sunken'
        )
        self.notes_text.grid(row=len(fields)-1, column=1, sticky='ew', pady=8)
        
        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)
        
        # Required fields note
        note_label = tk.Label(
            self.dialog,
            text="* Required fields",
            font=('Arial', 9, 'italic'),
            bg='#34495E',
            fg='#E74C3C'
        )
        note_label.pack(pady=(0, 10))
        
        # Buttons Frame
        button_frame = tk.Frame(self.dialog, bg='#34495E')
        button_frame.pack(pady=(0, 20))
        
        # Save Button
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Contact",
            font=('Arial', 12, 'bold'),
            bg='#27AE60',
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.save
        )
        save_btn.pack(side='left', padx=5)
        
        # Cancel Button
        cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancel",
            font=('Arial', 12, 'bold'),
            bg='#E74C3C',
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.cancel
        )
        cancel_btn.pack(side='left', padx=5)
        
        # Bind Enter and Escape keys
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        # Set focus to name field
        self.entries['name'].focus()
    
    def validate_phone(self, phone):
        """Validate phone number format"""
        # Remove common separators
        cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
        return cleaned.isdigit() and len(cleaned) >= 7
    
    def validate_email(self, email):
        """Validate email format"""
        if not email:  # Email is optional
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_date(self, date_str):
        """Validate date format"""
        if not date_str:  # Date is optional
            return True
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def save(self):
        """Save contact data"""
        # Get data from entries
        data = {}
        
        # Required fields
        name = self.entries['name'].get().strip()
        phone = self.entries['phone'].get().strip()
        
        if not name:
            messagebox.showwarning("Validation Error", "Name is required!")
            self.entries['name'].focus()
            return
        
        if not phone:
            messagebox.showwarning("Validation Error", "Phone number is required!")
            self.entries['phone'].focus()
            return
        
        # Validate phone
        if not self.validate_phone(phone):
            messagebox.showwarning("Validation Error", 
                                  "Invalid phone number format!\nPlease enter at least 7 digits.")
            self.entries['phone'].focus()
            return
        
        data['name'] = name
        data['phone'] = phone
        
        # Optional fields
        email = self.entries['email'].get().strip()
        if email and not self.validate_email(email):
            messagebox.showwarning("Validation Error", "Invalid email format!")
            self.entries['email'].focus()
            return
        data['email'] = email
        
        address = self.entries['address'].get().strip()
        data['address'] = address
        
        company = self.entries['company'].get().strip()
        data['company'] = company
        
        birthday = self.entries['birthday'].get().strip()
        if birthday and not self.validate_date(birthday):
            messagebox.showwarning("Validation Error", 
                                  "Invalid date format!\nPlease use YYYY-MM-DD")
            self.entries['birthday'].focus()
            return
        data['birthday'] = birthday
        
        # Get notes from Text widget
        notes = self.notes_text.get("1.0", tk.END).strip()
        data['notes'] = notes
        
        # Set result and close
        self.result = data
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel and close dialog"""
        self.dialog.destroy()


def main():
    root = tk.Tk()
    
    # Set style
    style = ttk.Style()
    style.theme_use('clam')
    
    app = ContactBook(root)
    root.mainloop()

if __name__ == "__main__":
    main()