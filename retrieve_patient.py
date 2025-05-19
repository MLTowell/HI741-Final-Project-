import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Listbox, MULTIPLE
from datetime import datetime
from dateutil import parser
import csv

class RetrievePatient:
    def __init__(self, master, data_path):
        """Initialize with the parent window and data file path."""
        self.master = master
        self.data_path = data_path  

    def execute(self):
        try:
            with open(self.data_path, newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                db = list(reader)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read data file: {e}")
            return

        patient_id = simpledialog.askstring("Patient Lookup", "Enter Patient ID:", parent=self.master)
        if not patient_id:
            return

        patient_id = patient_id.strip()
        visits = [entry for entry in db if entry.get("Patient_ID", "").strip() == patient_id]
        if not visits:
            messagebox.showinfo("Not Found", f"Patient ID {patient_id} not found.")
            return

        # Parse visit times safely and store paired with visit
        parsed_visits = []
        for visit in visits:
            date_str = visit.get("Visit_time", "")
            try:
                dt = parser.parse(date_str)
            except Exception:
                dt = datetime.min  # fallback to very old date if parse fails
            parsed_visits.append((dt, visit))

        # Sort visits by datetime ascending (oldest first)
        parsed_visits.sort(key=lambda x: x[0])

        # Get the max datetime
        max_dt = parsed_visits[-1][0]

        # Filter all visits that happened exactly on that max date (date only)
        max_date_visits = [v for dt, v in parsed_visits if dt.date() == max_dt.date()]

        # Pick the last visit on that date (chronological order preserved by sorting)
        most_recent_visit = max_date_visits[-1]

        self.show_fields(most_recent_visit)

    def show_fields(self, visit):
        fields = [
            "Gender", "Race", "Age", "Ethnicity", "Insurance", "Zip_code",
            "Chief_complaint", "Note_ID", "Note_type"
        ]

        field_window = Toplevel(self.master)
        field_window.title("Select Field(s) to View")
        field_window.geometry("350x300")

        tk.Label(field_window, text="Select field(s) to view:").pack()

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