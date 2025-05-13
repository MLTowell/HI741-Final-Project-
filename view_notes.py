import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from datetime import datetime
import csv

class ViewNotes:
    def __init__(self, master, data_path, notes_path):
        self.master = master
        self.data_path = data_path
        self.notes_path = notes_path
        self.patient_data = self.load_csv(self.data_path)
        self.note_data = self.load_csv(self.notes_path)

    def load_csv(self, path): 
        with open(path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def execute(self):
        patient_id = simpledialog.askstring("Patient ID", "Enter Patient ID:", parent=self.master)
        if not patient_id:
            return

        visit_date_input = simpledialog.askstring("Visit Date", "Enter Visit Date (YYYY-MM-DD):", parent=self.master)
        if not visit_date_input:
            return

        # Convert date
        try:
            dt = datetime.strptime(visit_date_input, "%Y-%m-%d")
            formatted_date = f"{dt.month}/{dt.day}/{dt.year}"
        except ValueError:
            messagebox.showerror("Invalid Date", "Please use the YYYY-MM-DD format.")
            return

        # Find matching Visit_IDs
        visit_ids = [
            visit["Visit_ID"]
            for visit in self.patient_data
            if visit.get("Patient_ID") == patient_id and visit.get("Visit_time") == formatted_date
        ]

        if not visit_ids:
            messagebox.showinfo("No Visits Found", "No visit found for that Patient ID and date.")
            return

        # Find matching notes
        matching_notes = [
            note.get("Note_text", "")
            for note in self.note_data
            if note.get("Patient_ID") == patient_id and note.get("Visit_ID") in visit_ids
        ]

        if not matching_notes:
            messagebox.showinfo("No Notes Found", "No notes found for that visit.")
            return

        # Display notes in a scrollable popup
        notes_window = tk.Toplevel(self.master)
        notes_window.title(f"Notes for Patient {patient_id} on {visit_date_input}")
        notes_window.geometry("500x400")

        text_area = scrolledtext.ScrolledText(notes_window, wrap=tk.WORD, font=("Arial", 11))
        text_area.pack(expand=True, fill=tk.BOTH)

        for i, note in enumerate(matching_notes, 1):
            text_area.insert(tk.END, f"Note {i}:\n{note}\n{'-'*40}\n")

        text_area.config(state=tk.DISABLED)  # Make text read-only