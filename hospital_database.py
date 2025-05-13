import csv

class HospitalDatabase:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = self.load_data()

    def load_data(self):
        """Load hospital data from CSV file."""
        try:
            with open(self.csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # Convert the rows into a list of dictionaries
                return {row['Patient_ID']: row for row in reader}
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
        """Retrieve patient data by patient_id."""
        return self.data.get(str(patient_id), None)

    def update_patient_data(self, patient_id, patient_data):
        """Update or add patient data and save it."""
        self.data[str(patient_id)] = patient_data
        self.save_data()

    def get_all_visits(self):
        """Return all visit records as a list."""
        return list(self.data.values())  # Convert the dictionary to a list of values