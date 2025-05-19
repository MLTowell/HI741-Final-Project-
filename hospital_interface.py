import tkinter as tk
from tkinter import messagebox
from user_auth import UserAuth
from patient_add import PatientAdd
from count_manager import CountManager
from retrieve_patient import RetrievePatient
from view_notes import ViewNotes
from graph_utils import GraphGenerator
from patient_removal import PatientRemoval
from hospital_database import HospitalDatabase
from user_tracker import UserActionTracker
import os
import csv
from datetime import datetime

class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
       
        # Paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(base_dir, "data", "Patient_data.csv")
        self.credentials_path = os.path.join(base_dir, "data", "Credentials.csv")
        self.notes_path = os.path.join(base_dir, "data", "Notes.csv")

        self.user_auth = UserAuth(self.credentials_path)
        self.user_role = None
        self.username = None

        # Shared data
        self.data = self.load_csv(self.data_path)
        self.notes = self.load_csv(self.notes_path)
        
        self.login_screen()


    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("400x200+600+300")  # Set window size and position
        self.root.resizable(True, True)      # Make the window fixed-size

        # System name/title
        tk.Label(self.root, text="Hospital Management System", font=("Arial", 16, "bold")).pack(pady=(20, 10))

        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.handle_login).pack(pady=10)


    def center_window(self):
        """Centers the window on the screen based on current size."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.user_auth.login(username, password)

        action_tracker = UserActionTracker(self.root)
        self.username = username  # Save for tracking

        if role:
            self.user_role = role
            action_tracker.track_action(username, role, "Logged In")
            self.show_role_actions()
        else:
            action_tracker.track_action(username, "Unknown", "Failed Login")
            messagebox.showerror("Login Failed", "Invalid credentials")


    def logout(self, tracker):
        tracker.track_action(self.username, self.user_role, "Logged Out")
        self.username = None
        self.user_role = None
        self.login_screen() 
    

    def show_role_actions(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Welcome, {self.user_role.title()}", font=("Helvetica", 14, "bold")).pack(pady=10)

        self.center_window()  # ✅ Center after layout is complete

        db = HospitalDatabase(csv_file=self.data_path, preloaded_data=self.data)
        action_tracker = UserActionTracker(self.root)

        # Display buttons based on role
        if self.user_role == "management":
            tk.Label(self.root, text="Management actions available:").pack(pady=5)
            tk.Button(self.root, text="Hospital Statistics", command=lambda: self.generate_graphs(db, action_tracker)).pack(pady=5)
            tk.Button(self.root, text="User Actions Log", command=lambda: self.display_user_statistics(action_tracker)).pack(pady=5)

        if self.user_role == "admin":
            tk.Label(self.root, text="Admin actions available:").pack(pady=5)
            tk.Button(self.root, text="Count Visits", command=lambda: self.count_visits(db, action_tracker)).pack(pady=5)

        if self.user_role in ["clinician", "nurse"]:
            tk.Label(self.root, text=f"{self.user_role.title()} actions available:").pack(pady=5)
            tk.Button(self.root, text="Retrieve Patient", command=lambda: self.retrieve_patient(action_tracker)).pack(pady=5)
            tk.Button(self.root, text="Add Visit", command=lambda: self.add_visit(action_tracker)).pack(pady=5)
            tk.Button(self.root, text="Remove Patient", command=lambda: self.remove_patient(action_tracker)).pack(pady=5)
            tk.Button(self.root, text="View Notes", command=lambda: self.view_notes(action_tracker)).pack(pady=5)
            tk.Button(self.root, text="Count Visits", command=lambda: self.count_visits(db, action_tracker)).pack(pady=5)

        tk.Button(self.root, text="Logout", command=lambda: self.logout(action_tracker)).pack(pady=20)

        # Resize and center the window dynamically
        self.root.geometry("")  # Let Tkinter auto-size
        self.center_window()    # Then center it
    

    # Action-wrapped functional methods
    def generate_graphs(self, db, tracker):
        tracker.track_action(self.username, self.user_role, "Generated Graphs")

              # Inform the user with the actual folder path
        today_str = datetime.today().strftime("%m-%d-%Y")
        folder_name = f"Hospital Statistics {today_str}"

        messagebox.showinfo(
            "Graphs Generated",
            f"All graphs have been generated and saved in the folder:\n\n{folder_name}"
        )
      
        # Create the graphs and save to the output folder
        graph_generator = GraphGenerator(db.get_all_visits())
        graph_generator.generate_all()

     
    def display_user_statistics(self, tracker):
        tracker.track_action(self.username, self.user_role, "Viewed User Statistics")
        tracker.display_action_table()

    def count_visits(self, db, tracker):
        tracker.track_action(self.username, self.user_role, "Counted Visits")
        CountManager(db).count_visits_by_date_gui(self.root)

    def add_visit(self, tracker):
        tracker.track_action(self.username, self.user_role, "Initiated Add Visit")
        self.data = self.load_csv(self.data_path)
        self.notes = self.load_csv(self.notes_path)
        PatientAdd(self.data, self.notes, self.data_path, self.notes_path, self.root)
   
    def remove_patient(self, tracker):
        tracker.track_action(self.username, self.user_role, "Opened Patient Removal")
        self.data = self.load_csv(self.data_path)
        self.notes = self.load_csv(self.notes_path)
        PatientRemoval(self.data, self.notes, self.data_path, self.notes_path, self.root)

    def retrieve_patient(self, tracker):
        tracker.track_action(self.username, self.user_role, "Retrieved Patient")
        RetrievePatient(self.root, self.data_path).execute()

    def view_notes(self, tracker):
        tracker.track_action(self.username, self.user_role, "Viewed Notes")
        ViewNotes(self.root, self.data_path, self.notes_path).execute()

    def load_csv(self, path):
        with open(path, newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()