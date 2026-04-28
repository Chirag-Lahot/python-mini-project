import json
import os
from datetime import datetime

# File to store our data
DATA_FILE = "hospital_data.json"

# ==========================================
# Domain Classes (OOP Concepts)
# ==========================================

class User:
    def __init__(self, user_id, username, password, role="patient"):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {"id": self.user_id, "username": self.username, "password": self.password, "role": self.role}

class Doctor:
    def __init__(self, doc_id, name, specialization, timing, fees):
        self.doc_id = doc_id
        self.name = name
        self.specialization = specialization
        self.timing = timing
        self.fees = fees

    def to_dict(self):
        return {"id": self.doc_id, "name": self.name, "specialization": self.specialization, 
                "timing": self.timing, "fees": self.fees}

class Appointment:
    def __init__(self, app_id, patient_id, doc_id, date, time):
        self.app_id = app_id
        self.patient_id = patient_id
        self.doc_id = doc_id
        self.date = date
        self.time = time
        self.status = "Scheduled"

    def to_dict(self):
        return {"id": self.app_id, "patient_id": self.patient_id, "doc_id": self.doc_id, 
                "date": self.date, "time": self.time, "status": self.status}

# ==========================================
# Data Management Class (File Handling)
# ==========================================

class DataManager:
    def __init__(self):
        self.data = {"users": [], "doctors": [], "appointments": []}
        self.load_data()

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            # Seed default admin and some default doctors if file doesn't exist
            admin = User(1, "admin", "admin123", "admin")
            doc1 = Doctor(1, "Dr. Smith", "Cardiologist", "10:00-14:00", 500)
            doc2 = Doctor(2, "Dr. Jane", "Dermatologist", "14:00-18:00", 400)
            self.data["users"].append(admin.to_dict())
            self.data["doctors"].extend([doc1.to_dict(), doc2.to_dict()])
            self.save_data()
        else:
            with open(DATA_FILE, "r") as f:
                self.data = json.load(f)

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

# ==========================================
# Main System logic
# ==========================================

class AppointmentSystem:
    def __init__(self):
        self.db = DataManager()
        self.current_user = None

    def register(self):
        print("\n--- Register New Patient ---")
        username = input("Enter username: ").strip()
        
        # Check if username exists
        if any(u['username'] == username for u in self.db.data['users']):
            print("Error: Username already exists!")
            return

        password = input("Enter password: ").strip()
        if len(password) < 4:
            print("Error: Password must be at least 4 characters.")
            return

        new_id = len(self.db.data['users']) + 1
        new_user = User(new_id, username, password)
        self.db.data['users'].append(new_user.to_dict())
        self.db.save_data()
        print("Registration successful! You can now log in.")

    def login(self):
        print("\n--- Login ---")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        for u in self.db.data['users']:
            if u['username'] == username and u['password'] == password:
                self.current_user = u
                print(f"Login successful! Welcome, {username}.")
                return True
        
        print("Error: Invalid credentials.")
        return False

    def view_doctors(self):
        print("\n--- Available Doctors ---")
        if not self.db.data['doctors']:
            print("No doctors available.")
            return

        print(f"{'ID':<5} | {'Name':<15} | {'Specialization':<15} | {'Timing':<15} | {'Fees':<5}")
        print("-" * 65)
        for d in self.db.data['doctors']:
            print(f"{d['id']:<5} | {d['name']:<15} | {d['specialization']:<15} | {d['timing']:<15} | ${d['fees']:<5}")

    def book_appointment(self):
        self.view_doctors()
        try:
            doc_id = int(input("\nEnter Doctor ID to book: "))
            doctor = next((d for d in self.db.data['doctors'] if d['id'] == doc_id), None)
            
            if not doctor:
                print("Error: Doctor not found.")
                return

            date_str = input("Enter Date (YYYY-MM-DD): ")
            # Validate Date Format
            datetime.strptime(date_str, "%Y-%m-%d")
            
            time_str = input("Enter Time (HH:MM): ")
            
            # Simple availability check bonus
            for appt in self.db.data['appointments']:
                if appt['doc_id'] == doc_id and appt['date'] == date_str and appt['time'] == time_str and appt['status'] == "Scheduled":
                    print("Error: Doctor is already booked at this specific date and time.")
                    return

            new_id = len(self.db.data['appointments']) + 1
            new_appt = Appointment(new_id, self.current_user['id'], doc_id, date_str, time_str)
            self.db.data['appointments'].append(new_appt.to_dict())
            self.db.save_data()
            print("Success: Appointment booked successfully!")

        except ValueError:
            print("Error: Invalid Input. Please check your IDs and Date formats.")

    def view_my_appointments(self):
        print("\n--- My Appointments ---")
        my_appts = [a for a in self.db.data['appointments'] if a['patient_id'] == self.current_user['id']]
        
        if not my_appts:
            print("You have no appointments.")
            return

        print(f"{'Appt ID':<8} | {'Doctor Name':<15} | {'Date':<12} | {'Time':<8} | {'Status'}")
        print("-" * 65)
        for a in my_appts:
            doc = next((d for d in self.db.data['doctors'] if d['id'] == a['doc_id']), None)
            doc_name = doc['name'] if doc else "Unknown"
            print(f"{a['id']:<8} | {doc_name:<15} | {a['date']:<12} | {a['time']:<8} | {a['status']}")

    def cancel_appointment(self):
        self.view_my_appointments()
        try:
            appt_id = int(input("\nEnter Appointment ID to cancel (or 0 to exit): "))
            if appt_id == 0: return

            for a in self.db.data['appointments']:
                if a['id'] == appt_id and a['patient_id'] == self.current_user['id']:
                    if a['status'] == "Cancelled":
                        print("Appointment is already cancelled.")
                    else:
                        a['status'] = "Cancelled"
                        self.db.save_data()
                        print("Success: Appointment cancelled successfully.")
                    return
            print("Error: Appointment not found.")
        except ValueError:
            print("Error: Invalid ID.")

    # ------ ADMIN FEATURES BONUS ------
    def admin_add_doctor(self):
        print("\n--- Add New Doctor ---")
        name = input("Enter Name: ")
        spec = input("Enter Specialization: ")
        timing = input("Enter Timing (e.g., 09:00-17:00): ")
        try:
            fees = float(input("Enter Fees: "))
            new_id = len(self.db.data['doctors']) + 1
            new_doc = Doctor(new_id, name, spec, timing, fees)
            self.db.data['doctors'].append(new_doc.to_dict())
            self.db.save_data()
            print("Doctor added successfully!")
        except ValueError:
            print("Error: Fees must be a number.")

    def admin_remove_doctor(self):
        self.view_doctors()
        try:
            doc_id = int(input("Enter Doctor ID to remove: "))
            self.db.data['doctors'] = [d for d in self.db.data['doctors'] if d['id'] != doc_id]
            self.db.save_data()
            print("Success: Doctor removed (if existed).")
        except ValueError:
            print("Error: Invalid ID.")

    # ------ MENUS ------
    def patient_menu(self):
        while True:
            print("\n=== Patient Menu ===")
            print("1. View Doctors")
            print("2. Book Appointment")
            print("3. View My Appointments")
            print("4. Cancel Appointment")
            print("5. Logout")
            choice = input("Enter choice: ")

            if choice == '1': self.view_doctors()
            elif choice == '2': self.book_appointment()
            elif choice == '3': self.view_my_appointments()
            elif choice == '4': self.cancel_appointment()
            elif choice == '5': break
            else: print("Invalid choice.")

    def admin_menu(self):
        while True:
            print("\n=== Admin Menu ===")
            print("1. View All Doctors")
            print("2. Add Doctor")
            print("3. Remove Doctor")
            print("4. Logout")
            choice = input("Enter choice: ")

            if choice == '1': self.view_doctors()
            elif choice == '2': self.admin_add_doctor()
            elif choice == '3': self.admin_remove_doctor()
            elif choice == '4': break
            else: print("Invalid choice.")

    def run(self):
        while True:
            print("\n=== DOCTOR APPOINTMENT SYSTEM ===")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                if self.login():
                    if self.current_user['role'] == 'admin':
                        self.admin_menu()
                    else:
                        self.patient_menu()
                    self.current_user = None # Clear session on logout
            elif choice == '2':
                self.register()
            elif choice == '3':
                print("Exiting system. Goodbye!")
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    app = AppointmentSystem()
    app.run()