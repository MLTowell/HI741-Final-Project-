import csv

class UserAuth:
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path
        self.credentials = self.load_credentials()

    def load_credentials(self):
        """Load credentials from a CSV file."""
        try:
            with open(self.credentials_path, mode='r', encoding='utf-8') as file:
                return list(csv.DictReader(file))  # Parse CSV into list of dictionaries
        except FileNotFoundError:
            print(f"Error: The credentials file '{self.credentials_path}' was not found.")
            return []

    def login(self, username, password):
        """Authenticate user and return their role if credentials are valid."""
        for user in self.credentials:
            if user["username"] == username and user["password"] == password:
                print(f"Login successful. Role: {user['role']}")
                return user["role"]
        return None

    def check_permission(self, role, mode):
        """Check if the given role can perform the requested mode."""
        ROLE_PERMISSIONS = {
            "admin": ["count"],
            "clinician": ["add", "remove", "retrieve", "view", "count"],
            "nurse": ["add", "remove", "retrieve", "view", "count"]
        }
        return mode in ROLE_PERMISSIONS.get(role, [])