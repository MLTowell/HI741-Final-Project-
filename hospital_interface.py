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

        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.handle_login).pack(pady=10)

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

        tk.Label(self.root, text=f"Welcome, {self.user_role.title()}").pack(pady=10)

        db = HospitalDatabase(self.data_path)
        action_tracker = UserActionTracker(self.root)

        if self.user_role == "management":
            tk.Label(self.root, text="Management actions available.").pack(pady=10)

            tk.Button(self.root, text="Hospital Statistics", command=lambda: self.generate_graphs(db, action_tracker)).pack(pady=5)
            tk.Button(self.root, text="User Actions Log", command=lambda: self.display_user_statistics(action_tracker)).pack(pady=5)

        if self.user_role == "admin":
            tk.Button(self.root, text="Count Visits", command=lambda: self.count_visits(db, action_tracker)).pack(pady=5)

        if self.user_role in ["clinician", "nurse"]:
            tk.Button(self.root, text="Retrieve Patient", command=lambda: self.retrieve_patient(db, action_tracker)).pack(pady=5)
            tk.Button(self.root, text="Add Visit", command=lambda: self.add_visit(action_tracker)).pack(pady=5)
            tk.Button(self.root, text="Remove Patient", command=lambda: self.remove_patient(action_tracker)).pack(pady=5)
            tk.Button(self.root, text="View Notes", command=lambda: self.view_notes(action_tracker)).pack(pady=5)
            tk.Button(self.root, text="Count Visits", command=lambda: self.count_visits(db, action_tracker)).pack(pady=5)
            
        tk.Button(self.root, text="Logout", command=lambda: self.logout(action_tracker)).pack(pady=10)

    # Action-wrapped functional methods
    def generate_graphs(self, db, tracker):
        tracker.track_action(self.username, self.user_role, "Generated Graphs")
        GraphGenerator(db).generate_all()

    def display_user_statistics(self, tracker):
        tracker.track_action(self.username, self.user_role, "Viewed User Statistics")
        tracker.display_action_table()

    def count_visits(self, db, tracker):
        tracker.track_action(self.username, self.user_role, "Counted Visits")
        CountManager(db).count_visits_by_date_gui(self.root)

    def add_visit(self, tracker):
        tracker.track_action(self.username, self.user_role, "Added Patient Visit")
        PatientAdd(self.data, self.notes, self.data_path, self.notes_path, self.root).add_visit()
    
    def remove_patient(self, tracker):
        tracker.track_action(self.username, self.user_role, "Removed Patient")
        PatientRemoval(self.data, self.notes, self.data_path, self.notes_path, self.root).remove_patient()

    def retrieve_patient(self, db, tracker):
        tracker.track_action(self.username, self.user_role, "Retrieved Patient")
        RetrievePatient(self.root, db.get_all_visits()).execute()

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