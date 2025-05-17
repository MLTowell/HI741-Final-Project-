import csv

class HospitalDatabase:
    def __init__(self, csv_file=None, preloaded_data=None):
        if preloaded_data:
            self.data = preloaded_data
        elif csv_file:
            self.data = self.load_csv(csv_file)
        else:
            self.data = []
    
    def load_data(self):
        """Load hospital data from CSV file."""
        try:
            with open(self.csv_file, mode='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # Convert the rows into a list of dictionaries
                return list(reader)
        except FileNotFoundError:
            print(f"Error: The file '{self.csv_file}' was not found.")
            return {}

    def save_data(self):
        """Save hospital data to CSV file."""
        try:
            with open(self.csv_file, mode='w', encoding='utf-8', newline='') as file:
                # Assuming the data is a dictionary, write the data as CSV
                fieldnames = self.data[next(iter(self.data))].keys()  # Get the field names from the first record
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                for row in self.data.values():
                    writer.writerow(row)
        except Exception as e:
            print(f"Error saving file: {e}")

    def get_patient(self, patient_id):
        """Retrieve all visit records for a given patient_id."""
        return [row for row in self.data if row.get("Patient_ID") == str(patient_id)]

    def add_visit_record(self, visit_record):
        """Add a new visit record."""
        self.data.append(visit_record)
        self.save_data()

    def get_all_visits(self):
        return self.data