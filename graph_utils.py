import os
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from dateutil import parser

class GraphGenerator:
    def __init__(self, visit_records):  # Expecting a list of dicts
        today_str = datetime.today().strftime("%m-%d-%Y")
        self.output_dir = f"Hospital Statistics {today_str}"
        os.makedirs(self.output_dir, exist_ok=True)

        # Sanitize input
        self.db = [r for r in visit_records if isinstance(r, dict)]

    def get_timestamped_filepath(self, base_filename, ext="png"):
        from datetime import datetime
        timestamp = datetime.now().strftime("%m%d%Y_%H%M%S")
        filename = f"{base_filename}_{timestamp}.{ext}"
        return os.path.join(self.output_dir, filename)

    def count_chief_complaints(self):
        complaint_count = {}

        for visit_data in self.db:
            chief_complaint = visit_data.get("Chief_complaint", "").strip()
            if chief_complaint:
                complaint_count[chief_complaint] = complaint_count.get(chief_complaint, 0) + 1

        if not complaint_count:
            print("No chief complaint data found.")
            return

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

        filepath = self.get_timestamped_filepath("Patient Chief Complaints")
        plt.savefig(filepath)
        plt.show()

    def generate_department_graph(self):
        departments = defaultdict(int)

        for visit in self.db:
            dept = visit.get("Visit_department", "Unknown").strip()
            if dept:
                departments[dept] += 1

        if not departments:
            print("No department data found.")
            return

        plt.figure(figsize=(10, 5))
        plt.bar(departments.keys(), departments.values(), color="skyblue")
        plt.title("Department Visit Counts")
        plt.xlabel("Department")
        plt.ylabel("Number of Visits")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        filepath = self.get_timestamped_filepath("Hospital Department Visits")
        plt.savefig(filepath)
        plt.show()

    def generate_visits_per_year_graph(self):
        visits_by_year = defaultdict(int)

        for visit in self.db:
            date_str = visit.get("Visit_time", "").strip()
            if not date_str:
                continue

            try:
                date_obj = parser.parse(date_str)
                visits_by_year[date_obj.year] += 1
            except Exception as e:
                print(f"Skipping invalid date: {date_str} ({e})")

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

        filepath = self.get_timestamped_filepath("Yearly Hosptial Visits")
        plt.savefig(filepath)
        plt.show()

    def generate_all(self):
        self.count_chief_complaints()
        self.generate_department_graph()
        self.generate_visits_per_year_graph()
        print("All graphs generated and saved.")