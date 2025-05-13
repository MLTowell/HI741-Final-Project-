import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime
import csv

class PatientAdd:
    def __init__(self, database, notes_db, data_path, notes_path, parent):
        self.db = database
        self.notes_db = notes_db
        self.data_path = data_path
        self.notes_path = notes_path
        self.parent = parent

        # Create a new window or frame for adding a patient visit
        self.add_window = tk.Toplevel(parent)
        self.add_window.title("Add Patient Visit")

        # Start with the Patient ID entry pop-up
        self.ask_patient_id()

    def ask_patient_id(self):
        """ Ask for Patient ID and handle new patient creation. """
        self.patient_id_label = ttk.Label(self.add_window, text="Enter Patient ID:")
        self.patient_id_entry = ttk.Entry(self.add_window)

        self.patient_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.submit_patient_id_button = ttk.Button(self.add_window, text="Submit", command=self.handle_patient_id)
        self.submit_patient_id_button.grid(row=1, column=0, columnspan=2, pady=10)

    def handle_patient_id(self):
        """ Handle the patient ID input and prompt for creating a new patient if necessary. """
        self.patient_id_str = self.patient_id_entry.get().strip()  # Store the Patient ID here

        # Check if the patient exists
        existing_patient_ids = {record["Patient_ID"] for record in self.db}
        if self.patient_id_str in existing_patient_ids:
            # If the patient exists, continue to the visit details
            self.patient_id_label.grid_forget()
            self.patient_id_entry.grid_forget()
            self.submit_patient_id_button.grid_forget()

            # Find the most recent visit for the patient
            patient_visits = [record for record in self.db if record["Patient_ID"] == self.patient_id_str]
            patient_visits.sort(key=lambda x: datetime.strptime(x["Visit_time"], "%m/%d/%Y"), reverse=True)
            latest_visit = patient_visits[0] if patient_visits else {}

            # Store for use in create_ui_elements
            self.latest_visit_data = latest_visit

            # Continue with creating the UI for visit details
            self.create_ui_elements()
        else:
            # If the patient does not exist, ask if they want to create a new patient
            proceed = messagebox.askyesno(
                "New Patient Warning",
                f"Patient ID {self.patient_id_str} does not exist in the database.\n"
                "Do you want to create a new patient with this ID?"
            )
            if proceed:
                # If yes, proceed with the visit details input
                self.patient_id_label.grid_forget()
                self.patient_id_entry.grid_forget()
                self.submit_patient_id_button.grid_forget()

                # Continue with creating the UI for visit details
                self.create_ui_elements()
            else:
                self.add_window.destroy()

    def create_ui_elements(self):
        """ Create all necessary UI elements for adding patient data. """
        self.latest_visit_data = getattr(self, 'latest_visit_data', {})

        def get_prefill(field):  # helper
            return self.latest_visit_data.get(field, "")

        self.department_label = ttk.Label(self.add_window, text="Enter Department:")
        self.department_entry = ttk.Entry(self.add_window)

        self.visit_date_label = ttk.Label(self.add_window, text="Enter Visit Date (YYYY-MM-DD):")
        self.visit_date_entry = ttk.Entry(self.add_window)

        self.race_label = ttk.Label(self.add_window, text="Enter Race:")
        self.race_entry = ttk.Entry(self.add_window)
        self.race_entry.insert(0, get_prefill("Race"))

        self.gender_label = ttk.Label(self.add_window, text="Enter Gender:")
        self.gender_entry = ttk.Entry(self.add_window)
        self.gender_entry.insert(0, get_prefill("Gender"))

        self.ethnicity_label = ttk.Label(self.add_window, text="Enter Ethnicity:")
        self.ethnicity_entry = ttk.Entry(self.add_window)
        self.ethnicity_entry.insert(0, get_prefill("Ethnicity"))

        self.age_label = ttk.Label(self.add_window, text="Enter Age:")
        self.age_entry = ttk.Entry(self.add_window)
        self.age_entry.insert(0, get_prefill("Age"))

        self.zip_code_label = ttk.Label(self.add_window, text="Enter Zip Code:")
        self.zip_code_entry = ttk.Entry(self.add_window)

        self.insurance_label = ttk.Label(self.add_window, text="Enter Insurance:")
        self.insurance_entry = ttk.Entry(self.add_window)

        self.chief_complaint_label = ttk.Label(self.add_window, text="Enter Chief Complaint:")
        self.chief_complaint_entry = ttk.Entry(self.add_window)

        self.note_type_label = ttk.Label(self.add_window, text="Enter Note Type:")
        self.note_type_entry = ttk.Entry(self.add_window)

        self.note_text_label = ttk.Label(self.add_window, text="Enter Clinical Notes:")
        self.note_text_entry = ttk.Entry(self.add_window)

        self.submit_button = ttk.Button(self.add_window, text="Add Visit", command=self.add_visit)

        # Layout the widgets in the window
        self.arrange_ui_elements()

    def arrange_ui_elements(self):
        """ Arrange the UI elements in the window. """
        self.department_label.grid(row=1, column=0, padx=5, pady=5)
        self.department_entry.grid(row=1, column=1, padx=5, pady=5)

        self.visit_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.visit_date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.race_label.grid(row=3, column=0, padx=5, pady=5)
        self.race_entry.grid(row=3, column=1, padx=5, pady=5)

        self.gender_label.grid(row=4, column=0, padx=5, pady=5)
        self.gender_entry.grid(row=4, column=1, padx=5, pady=5)

        self.ethnicity_label.grid(row=5, column=0, padx=5, pady=5)
        self.ethnicity_entry.grid(row=5, column=1, padx=5, pady=5)

        self.age_label.grid(row=6, column=0, padx=5, pady=5)
        self.age_entry.grid(row=6, column=1, padx=5, pady=5)

        self.zip_code_label.grid(row=7, column=0, padx=5, pady=5)
        self.zip_code_entry.grid(row=7, column=1, padx=5, pady=5)

        self.insurance_label.grid(row=8, column=0, padx=5, pady=5)
        self.insurance_entry.grid(row=8, column=1, padx=5, pady=5)

        self.chief_complaint_label.grid(row=9, column=0, padx=5, pady=5)
        self.chief_complaint_entry.grid(row=9, column=1, padx=5, pady=5)

        self.note_type_label.grid(row=10, column=0, padx=5, pady=5)
        self.note_type_entry.grid(row=10, column=1, padx=5, pady=5)

        self.note_text_label.grid(row=11, column=0, padx=5, pady=5)
        self.note_text_entry.grid(row=11, column=1, padx=5, pady=5)

        self.submit_button.grid(row=12, column=0, columnspan=2, pady=10)

    def generate_unique_visit_id(self):
        """Generate a unique Visit_ID."""
        existing_ids = {visit["Visit_ID"] for visit in self.db}
        while True:
            visit_id = random.randint(100000, 999999)
            if visit_id not in existing_ids:
                return visit_id

    def generate_unique_note_id(self):
        """Generate a unique Note_ID."""
        existing_ids = {note["Note_ID"] for note in self.notes_db}
        while True:
            note_id = random.randint(100000, 999999)
            if note_id not in existing_ids:
                return note_id

    def add_visit(self):
        # Collect data
        patient_id_str = self.patient_id_str  # From earlier user input
        department = self.department_entry.get().strip()
        visit_date = self.visit_date_entry.get().strip()
        race = self.race_entry.get().strip()
        gender = self.gender_entry.get().strip()
        ethnicity = self.ethnicity_entry.get().strip()
        age = self.age_entry.get().strip()
        zip_code = self.zip_code_entry.get().strip()
        insurance = self.insurance_entry.get().strip()
        chief_complaint = self.chief_complaint_entry.get().strip()
        note_type = self.note_type_entry.get().strip()
        note_text = self.note_text_entry.get().strip()

        # Confirm addition
        confirm = messagebox.askyesno(
            "Confirm New Visit", 
            f"Are you sure you want to add a new visit for Patient ID {patient_id_str}?"
        )
        if not confirm:
            return

        # Validate date
        try:
            visit_date_obj = datetime.strptime(visit_date, "%Y-%m-%d")
            formatted_visit_date = f"{visit_date_obj.month}/{visit_date_obj.day}/{visit_date_obj.year}"
        except ValueError:
            messagebox.showerror("Invalid Date", "Invalid date format. Please enter date as YYYY-MM-DD.")
            return

        # Check if patient exists
        existing_patient_ids = {record["Patient_ID"] for record in self.db}
        if patient_id_str not in existing_patient_ids:
            messagebox.showerror("Invalid Patient", "The Patient ID does not exist.")
            return

        # Generate unique Visit ID and Note ID
        visit_id = self.generate_unique_visit_id()
        note_id = self.generate_unique_note_id()

        # Create visit and note dictionaries
        visit_data = {
            "Patient_ID": patient_id_str,
            "Visit_ID": visit_id,
            "Visit_time": formatted_visit_date,
            "Visit_department": department,
            "Race": race,
            "Gender": gender,
            "Ethnicity": ethnicity,
            "Age": age,
            "Zip_code": zip_code,
            "Insurance": insurance,
            "Chief_complaint": chief_complaint,
            "Note_ID": note_id,
            "Note_type": note_type,
        }

        # Save to main visit database
        self.db.append(visit_data)
        self.save_note_to_file(patient_id_str, visit_id, note_id, note_text)

        messagebox.showinfo("Visit Added", "The visit has been successfully added.")
        self.add_window.destroy()

    def save_note_to_file(self, patient_id, visit_id, note_id, note_text):
        """Append note to notes file with Entry number."""
        try:
            with open(self.notes_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                existing_notes = list(reader)
                next_entry = len(existing_notes) + 1
        except FileNotFoundError:
            existing_notes = []
            next_entry = 1

        note_entry = {
            "Entry_ID": next_entry,
            "Patient_ID": patient_id,
            "Visit_ID": visit_id,
            "Note_ID": note_id,
            "Note": note_text,
        }

        existing_notes.append(note_entry)

        with open(self.notes_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=note_entry.keys())
            if f.tell() == 0:  # If the file is empty, write the header
                writer.writeheader()
            writer.writerows(existing_notes)
