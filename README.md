# Doctor Appointment Booking System (CLI)

A beginner-friendly, console-based Python application for managing doctor appointments. This project uses Object-Oriented Programming (OOP) principles and stores data persistently using a lightweight JSON file handler.

## Features

- **User Authentication:** Registration and Login system.
- **Role-based Access:** Differentiates between regular Patients and Admin users.
- **Patient Features:**
  - View available doctors and their details (specialization, timing, fees).
  - Book an appointment with date and time validation.
  - View a list of your booked appointments.
  - Cancel existing appointments.
- **Admin Features:**
  - View all registered doctors.
  - Add new doctors to the system.
  - Remove existing doctors.
- **Persistent Storage:** All data (users, doctors, appointments) is saved locally in `hospital_data.json`.

## Prerequisites

- **Python 3.x** installed on your system.
- No external libraries are required (only uses standard built-in modules `json`, `os`, and `datetime`).

## Installation & Setup

1. Clone or download the repository to your local machine.
2. Ensure the main Python script is saved as `main.py`.
3. Open a terminal or command prompt and navigate to the project directory.

## How to Run

Execute the main script using Python:

```bash
python main.py
```

*(Depending on your environment, you might need to use `python3 main.py`)*

## Usage Guide

Upon running the application, you will be greeted with the main menu. 

### Default Credentials
If you are running the application for the first time, a default `json` database will be created. You can use the built-in Admin account:
- **Username:** `admin`
- **Password:** `admin123`

### Workflows

**For Patients:**
1. Select **Register** from the main menu to create a new patient account.
2. Select **Login** and enter your credentials.
3. Choose **View Doctors** to see the list or **Book Appointment** to schedule one. You will need the specific Doctor ID.
4. Manage your bookings using the **View My Appointments** and **Cancel Appointment** options.

**For Admins:**
1. **Login** using the admin credentials.
2. Manage the doctor roster by adding new doctors (requires Name, Specialization, Timings, and Fees) or removing them by ID.

## Project Structure

```text
.
├── main.py                # The main application script
├── hospital_data.json     # Data storage file (auto-generated on first run)
└── README.md              # Project documentation
```

## Future Enhancements
- Replace JSON file storage with an SQLite database.
- Add dynamic time-slot management to prevent double-booking.
- Password hashing for improved security.
- Develop a basic GUI using `tkinter`.
