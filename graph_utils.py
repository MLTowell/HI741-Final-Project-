
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from dateutil import parser

class GraphGenerator:
    def __init__(self, hospital_db):
        today_str = datetime.today().strftime("%m-%d-%Y")
        self.output_dir = f"Management Statistics {today_str}"
        os.makedirs(self.output_dir, exist_ok=True)

        # Store list of visit records internally (dict values)
        self.db = hospital_db.data

    def count_chief_complaints(self):
        complaint_count = {}

        for visit_data in self.db:
            chief_complaint = visit_data.get("Chief_complaint")
            if chief_complaint:
                complaint_count[chief_complaint] = complaint_count.get(chief_complaint, 0) + 1

        self.show_complaint_graph(complaint_count)

    def show_complaint_graph(self, complaint_count):
        complaints = list(complaint_count.keys())
        counts = list(complaint_count.values())

        plt.figure(figsize=(10, 5))
        plt.bar(complaints, counts)
        plt.xlabel('Chief Complaint')
        plt.ylabel('Number of Occurrences')
        plt.title('Occurrences of Chief Complaints')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "chief_complaints.png"))
        plt.show()

    def generate_department_graph(self):
        departments = defaultdict(int)

        for visit in self.db:
            dept = visit.get("Visit_department", "Unknown")
            departments[dept] += 1

        plt.figure(figsize=(10, 5))
        plt.bar(departments.keys(), departments.values(), color="skyblue")
        plt.title("Department Visit Counts")
        plt.xlabel("Department")
        plt.ylabel("Number of Visits")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "department_visits.png"))
        plt.show()

    def generate_visits_per_year_graph(self):
        visits_by_year = defaultdict(int)

        for visit in self.db:
            date_str = visit.get("Visit_time", "")
            if not date_str:
                continue

            try:
                date_obj = parser.parse(date_str)  # Flexible date parsing
                visits_by_year[date_obj.year] += 1
            except (ValueError, TypeError):
                print(f"Skipping invalid date: {date_str}")
                continue

        if not visits_by_year:
            print("No valid visit data available.")
            return

        years = sorted(visits_by_year.keys())
        counts = [visits_by_year[year] for year in years]

        plt.figure(figsize=(10, 5))
        plt.plot(years, counts, marker="o", color="green")
        plt.title("Visits per Year")
        plt.xlabel("Year")
        plt.ylabel("Number of Visits")
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(os.path.join(self.output_dir, "visits_per_year.png"))
        plt.show()

    def generate_all(self):
        self.count_chief_complaints()
        self.generate_department_graph()
        self.generate_visits_per_year_graph()
        print("All graphs generated and saved.")