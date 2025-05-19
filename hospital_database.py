import csv

class HospitalDatabase:
    def __init__(self, csv_file=None, preloaded_data=None):
        self.csv_file = csv_file  # ✅ Store the file path
        if preloaded_data:
            self.data = preloaded_data
        elif csv_file:
            self.data = self.load_csv(csv_file)
        else:
            self.data = []

    def load_csv(self, path):
        """Read CSV and return list of dicts."""
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            print(f"Error: The file '{path}' was not found.")
            return []

    def reload_data(self):
        """Reload data from CSV to ensure freshness."""
        if self.csv_file:
            self.data = self.load_csv(self.csv_file)

    def save_data(self):
        try:
            with open(self.csv_file, mode='w', encoding='utf-8', newline='') as file:
                if not self.data:
                    return
                fieldnames = self.data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in self.data:
                    writer.writerow(row)
        except Exception as e:
            print(f"Error saving file: {e}")

    def get_patient(self, patient_id):
        return [row for row in self.data if row.get("Patient_ID") == str(patient_id)]

    def add_visit_record(self, visit_record):
        self.data.append(visit_record)
        self.save_data()

    def get_all_visits(self):
        return self.data