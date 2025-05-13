import tkinter as tk
from tkinter import ttk, messagebox
import csv

class PatientRemoval:
    def __init__(self, patient_data, notes_data, data_path, notes_path, parent):
        self.patient_data = patient_data
        self.notes_data = notes_data
        self.data_path = data_path
        self.notes_path = notes_path
        self.parent = parent

        # Create a new window or frame for patient removal
        self.remove_window = tk.Toplevel(parent)
        self.remove_window.title("Patient Removal")

        # GUI Elements for removing patient
        self.patient_id_label = ttk.Label(self.remove_window, text="Enter Patient ID to remove:")
        self.patient_id_entry = ttk.Entry(self.remove_window)

        self.remove_button = ttk.Button(self.remove_window, text="Remove Patient", command=self.remove_patient)

        # Layout
        self.patient_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.patient_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.remove_button.grid(row=1, column=0, columnspan=2, pady=10)

    def remove_patient(self):
        patient_id = self.patient_id_entry.get().strip()

        # Check if input is empty
        if not patient_id:
            messagebox.showerror("Input Error", "Please enter a Patient ID.")
            return

        # Check if the patient ID exists in the visit records
        patient_found = any(record['Patient_ID'] == patient_id for record in self.patient_data)

        if not patient_found:
            messagebox.showerror("Error", f"No patient found with ID {patient_id}.")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Patient ID {patient_id} and all related records?")
        if not confirm:
            messagebox.showinfo("Cancelled", "Deletion cancelled. Goodbye.")
            self.remove_window.destroy()  # Close the window after cancellation
            return

        # Remove patient visit records (only those related to this patient)
        self.patient_data = [record for record in self.patient_data if record['Patient_ID'] != patient_id]
    
        # Remove notes related to the patient (only those related to this patient)
        self.notes_data = [note for note in self.notes_data if note['Patient_ID'] != patient_id]

        # Save changes
        self.save_to_file(self.patient_data, self.data_path)
        self.save_to_file(self.notes_data, self.notes_path)

        messagebox.showinfo("Success", f"Patient ID {patient_id} and related visits/notes successfully removed.")
        self.remove_window.destroy()  # Close the window after successful removal

    def save_to_file(self, data, file_name):
        """Helper function to save data back to a CSV file."""
        try:
            with open(file_name, 'w', encoding='utf-8', errors='replace', newline='') as file:
                if not data:
                    # Handle empty file with no data rows
                    file.truncate()
                    print(f"'{file_name}' emptied successfully (no remaining records).")
                    return

                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                print(f"Database '{file_name}' updated successfully.")
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' was not found.")
        except IOError as e:
            print(f"An error occurred while saving '{file_name}': {e}")