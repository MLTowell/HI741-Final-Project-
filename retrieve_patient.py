import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Listbox, MULTIPLE

class RetrievePatient:
    def __init__(self, master, db):
        """Initialize with the parent window and visit records."""
        self.master = master
        if not isinstance(db, list) or not all(isinstance(entry, dict) for entry in db):
            raise TypeError("Expected 'db' to be a list of dictionaries.")
        self.db = db  # List of patient visit dictionaries

    def execute(self):
        patient_id = simpledialog.askstring("Patient Lookup", "Enter Patient ID:", parent=self.master)
        if not patient_id:
            return

        visits = [entry for entry in self.db if entry.get("Patient_ID") == patient_id]
        if not visits:
            messagebox.showinfo("Not Found", f"Patient ID {patient_id} not found.")
            return

        # Ask user to choose a visit
        visit_selection = Toplevel(self.master)
        visit_selection.title("Select Visit")
        visit_selection.geometry("400x300")
        tk.Label(visit_selection, text=f"Visits for Patient {patient_id}:").pack()

        visit_listbox = Listbox(visit_selection)
        visit_listbox.pack(expand=True, fill=tk.BOTH)

        for i, visit in enumerate(visits):
            summary = f"{i+1}. ID: {visit.get('Visit_ID')}, Time: {visit.get('Visit_time')}, Dept: {visit.get('Visit_department')}"
            visit_listbox.insert(tk.END, summary)

        def on_select_visit():
            selected_index = visit_listbox.curselection()
            if not selected_index:
                messagebox.showwarning("No Selection", "Please select a visit.")
                return
            visit_selection.destroy()
            self.show_fields(visits[selected_index[0]])

        tk.Button(visit_selection, text="Select", command=on_select_visit).pack(pady=10)

    def show_fields(self, visit):
        fields = [
            "Gender", "Race", "Age", "Ethnicity", "Insurance", "Zip_code",
            "Chief_complaint", "Note_ID", "Note_type"
        ]

        field_window = Toplevel(self.master)
        field_window.title("Select Fields to View")
        field_window.geometry("350x300")

        tk.Label(field_window, text="Select fields to view:").pack()

        field_listbox = Listbox(field_window, selectmode=MULTIPLE)
        field_listbox.pack(expand=True, fill=tk.BOTH)

        for field in fields:
            field_listbox.insert(tk.END, field.replace("_", " "))

        def display_selected_fields():
            selected_indices = field_listbox.curselection()
            if not selected_indices:
                messagebox.showinfo("No Fields Selected", "Please select at least one field.")
                return

            result = "\n".join(
                f"{fields[i].replace('_', ' ')}: {visit.get(fields[i], 'N/A')}"
                for i in selected_indices
            )

            messagebox.showinfo("Visit Details", result)

        tk.Button(field_window, text="Show Info", command=display_selected_fields).pack(pady=10)