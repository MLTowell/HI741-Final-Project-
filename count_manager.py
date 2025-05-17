
from tkinter import simpledialog, messagebox
from datetime import datetime


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
       
        for record in self.db.get_all_visits():
            if isinstance(record, dict):  # Ensure each record is a dictionary
                visit_time_str = record.get("Visit_time", "").strip()

                # Try to parse the visit date (M-D-YYYY format without leading zeros)
                try:
                    visit_date = datetime.strptime(visit_time_str, "%m/%d/%Y").date()
                except ValueError:
                    try:
                        # If the visit has a time, we can still extract the date part
                        visit_date = datetime.strptime(visit_time_str, "%m/%d/%Y %H:%M:%S").date()
                    except ValueError:
                        continue  # Skip if the visit_time format is unexpected

                # Compare the dates
                if visit_date == user_date:
                    count += 1
            else:
                messagebox.showerror("Invalid Data", "Database contains invalid record format.")
                return

        messagebox.showinfo("Visit Count", f"Number of visits on {user_date.isoformat()}: {count}")
        