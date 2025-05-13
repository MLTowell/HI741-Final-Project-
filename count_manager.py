import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import csv

class DB:
    def __init__(self, data_path):
        self.data = []
        self.load_data(data_path)

    def load_data(self, data_path):
        try:
            with open(data_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.data = [row for row in reader]
        except FileNotFoundError:
            print(f"Error: File {data_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

class CountManager:
    def __init__(self, db):
        self.db = db

    def count_visits_by_date_gui(self, parent):
        # Ask user for date input in YYYY-MM-DD format
        date_str = simpledialog.askstring("Count Visits", "Enter date (YYYY-MM-DD):", parent=parent)
        if not date_str:
            return

        # Enforce strict format for user input
        try:
            user_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format.")
            return

        # Count matching visits
        count = 0
        if isinstance(self.db.data, list):  # Check if data is a list
            for record in self.db.data:
                if isinstance(record, dict):  # Ensure each record is a dictionary
                    visit_time_str = record.get("Visit_time", "").strip()

                    # Try to parse the visit date (M-D-YYYY format without leading zeros)
                    try:
                        visit_date = datetime.strptime(visit_time_str, "%m-%d-%Y").date()
                    except ValueError:
                        try:
                            # If the visit has a time, we can still extract the date part
                            visit_date = datetime.strptime(visit_time_str, "%m-%d-%Y %H:%M:%S").date()
                        except ValueError:
                            continue  # Skip if the visit_time format is unexpected

                    # Compare the dates
                    if visit_date == user_date:
                        count += 1
                else:
                    messagebox.showerror("Invalid Data", "Database contains invalid record format.")
                    return

            messagebox.showinfo("Visit Count", f"Number of visits on {user_date.isoformat()}: {count}")
        else:
            messagebox.showerror("Invalid Data", "Database 'data' is not in the expected list format.")