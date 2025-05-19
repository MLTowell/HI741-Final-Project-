import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime
import csv
import os

def center_toplevel(window):
    window.update_idletasks()
    w = window.winfo_width()
    h = window.winfo_height()
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    window.geometry(f"{w}x{h}+{x}+{y}")

class PatientAdd:
    def __init__(self, database, notes_db, data_path, notes_path, parent):
        self.db = database
        self.notes_db = notes_db
        self.data_path = data_path
        self.notes_path = notes_path
        self.parent = parent
        self.latest_visit_data = {}

        self.add_window = tk.Toplevel(parent)
        self.add_window.title("Add Patient Visit")
        self.ask_patient_id()

    def ask_patient_id(self):
        self.clear_window()

        ttk.Label(self.add_window, text="Enter Patient ID:").grid(row=0, column=0, padx=5, pady=5)
        self.patient_id_entry = ttk.Entry(self.add_window)
        self.patient_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.patient_id_entry.focus()

        ttk.Button(self.add_window, text="Submit", command=self.handle_patient_id).grid(row=1, column=0, columnspan=2, pady=10)

    def clear_window(self):
        for widget in self.add_window.winfo_children():
            widget.destroy()

    def handle_patient_id(self):
        pid = self.patient_id_entry.get().strip()
        if not pid:
            messagebox.showerror("Input Error", "Patient ID cannot be empty.")
            return

        self.patient_id_str = pid
        existing_ids = {record["Patient_ID"] for record in self.db}

        if pid in existing_ids:
            patient_visits = [rec for rec in self.db if rec["Patient_ID"] == pid]
            patient_visits.sort(key=lambda x: datetime.strptime(x["Visit_time"], "%m/%d/%Y"), reverse=True)
            self.latest_visit_data = patient_visits[0] if patient_visits else {}
            self.create_visit_form()
        else:
            proceed = messagebox.askyesno("New Patient", f"Patient ID '{pid}' does not exist. Create new patient?")
            if proceed:
                self.latest_visit_data = {}
                self.create_visit_form()
            else:
                self.add_window.destroy()

    def create_visit_form(self):
        self.clear_window()

        def get_prefill(field):
            return self.latest_visit_data.get(field, "")

        fields = [
            ("Department:", "department_entry", ""),
            ("Visit Date (YYYY-MM-DD):", "visit_date_entry", datetime.today().strftime("%Y-%m-%d")),
            ("Race:", "race_entry", get_prefill("Race")),
            ("Gender:", "gender_entry", get_prefill("Gender")),
            ("Ethnicity:", "ethnicity_entry", get_prefill("Ethnicity")),
            ("Age:", "age_entry", get_prefill("Age")),
            ("Zip Code:", "zip_code_entry", get_prefill("Zip_code")),
            ("Insurance:", "insurance_entry", get_prefill("Insurance")),
            ("Chief Complaint:", "chief_complaint_entry", ""),
            ("Note Type:", "note_type_entry", ""),
            ("Clinical Notes:", "note_text_entry", "")
        ]

        for idx, (label, attr, default) in enumerate(fields):
            ttk.Label(self.add_window, text=label).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(self.add_window)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="we")
            entry.insert(0, default)
            setattr(self, attr, entry)

        ttk.Button(self.add_window, text="Add Visit", command=self.add_visit).grid(row=len(fields), column=0, columnspan=2, pady=10)
        self.add_window.grid_columnconfigure(1, weight=1)

        center_toplevel(self.add_window)
   
    def generate_unique_id(self, existing_ids_set):
        while True:
            new_id = str(random.randint(100000, 999999))
            if new_id not in existing_ids_set:
                return new_id

    def add_visit(self):
        pid = self.patient_id_str
        if not pid:
            messagebox.showerror("Error", "Patient ID is not set.")
            return

        try:
            visit_date = datetime.strptime(self.visit_date_entry.get().strip(), "%Y-%m-%d")
            formatted_date = f"{visit_date.month}/{visit_date.day}/{visit_date.year}"
        except ValueError:
            messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD format.")
            return

        if not messagebox.askyesno("Confirm", f"Add visit for Patient ID '{pid}'?"):
            return

        visit_ids = {rec["Visit_ID"] for rec in self.db}
        note_ids = {note["Note_ID"] for note in self.notes_db}
        visit_id = self.generate_unique_id(visit_ids)
        note_id = self.generate_unique_id(note_ids)

        visit_record = {
            "Patient_ID": pid,
            "Visit_ID": visit_id,
            "Visit_time": formatted_date,
            "Visit_department": self.department_entry.get().strip(),
            "Race": self.race_entry.get().strip(),
            "Gender": self.gender_entry.get().strip(),
            "Ethnicity": self.ethnicity_entry.get().strip(),
            "Age": self.age_entry.get().strip(),
            "Zip_code": self.zip_code_entry.get().strip(),
            "Insurance": self.insurance_entry.get().strip(),
            "Chief_complaint": self.chief_complaint_entry.get().strip(),
            "Note_ID": note_id,
            "Note_type": self.note_type_entry.get().strip(),
        }

        note_text = self.note_text_entry.get().strip()

        try:
            self.db.append(visit_record)
            self.notes_db.append({
                "": str(len(self.notes_db) + 1),  # Index column
                "Patient_ID": pid,
                "Visit_ID": visit_id,
                "Note_ID": note_id,
                "Note_text": note_text
            })
            self.save_visit()
            self.save_notes()
            messagebox.showinfo("Success", "Visit and note added.")
            self.add_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not save visit or note: {e}")

    def save_visit(self):
        if not self.db:
            return
        fieldnames = self.db[0].keys()
        with open(self.data_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.db)

    def save_notes(self):
        if not self.notes_db:
            return

        # Reindex all notes sequentially
        for idx, note in enumerate(self.notes_db, start=1):
            note[""] = str(idx)  # Set the placeholder index

        fieldnames = ["", "Patient_ID", "Visit_ID", "Note_ID", "Note_text"]

        with open(self.notes_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.notes_db)