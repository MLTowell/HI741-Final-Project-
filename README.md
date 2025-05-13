# HI741-Final-Project-

Hospital Management System

Overview

This project is a Hospital Management System built using Python's Tkinter library for GUI functionality. It includes several roles with different access levels (e.g., management, admin, clinician, nurse) and provides features like patient visit management, patient removal, retrieval of patient records, viewing notes, counting visits, and generating graphs for hospital statistics. User authentication and tracking of actions are integrated into the application.

Features

User Authentication: Login functionality with username and password. Role-based access to different functionalities based on the user's role.

Role-Based Functionality:

  Management: View hospital and user statistics, generate graphs.
  Admin: Count patient visits.
  Clinician/Nurse: Retrieve patient records, add visits, remove patients, view notes, and count visits.
  Data Tracking: User actions (e.g., login, viewing statistics, etc.) are logged for audit and monitoring purposes.
  Data Handling: The system handles data from CSV files for patient visits, user credentials, and notes.

Dependencies

    Tkinter: GUI library for creating the desktop application.
    csv: For loading and handling CSV files for patient data, credentials, and notes.
    os: For file path handling.

Installation

To run this system, ensure you have Python 3.x installed along with Tkinter. You can install the required dependencies with:

    pip install tk

Usage

Running the Application: 

To start the application, run the following command:

    python hospital_interface.py

The application will open a login screen. Enter your username and password to proceed.


Logging and Tracking:
  All user actions (logins, button clicks, etc.) are logged and displayed in the user activity table for tracking and         auditing.


CSV Files
The system relies on the following CSV files for storing data:

    Credentials.csv: Contains user credentials (username, password, role).
    Patient_data.csv: Stores records of patient visits.
    Notes.csv: Contains patient notes for each visit.

  Ensure that these CSV files are populated correctly for the system to function properly.

Future Improvements
Integrate a more robust database system for better data management and scalability.
Add more detailed permissions for each role, allowing for finer control over the features each user can access.
Provide better error handling and user feedback for invalid actions or data inputs.


Contact
For questions or contributions, feel free to reach out to MLTowell@UWM.edu.
