import os
import csv
import random
from data_handler import generate_initial_dataset
from crud_operations import (
    add_complaint,
    display_all_complaints,
    search_complaint,
    update_complaint,
    delete_complaint,
    generate_summary_report
)
from analytics_engine import run_numpy_analysis

def main():
    # Ensure a dataset containing at least 55 records is initialized on startup.
    generate_initial_dataset()
    
    while True:
        print("\n==================================================")
        print("      HOSTEL COMPLAINT MANAGEMENT SYSTEM")
        print("==================================================")
        print("1. Display All Complaints")
        print("2. Add a New Complaint")
        print("3. Search for a Complaint")
        print("4. Update an Existing Complaint")
        print("5. Delete a Complaint")
        print("6. Generate Quick Summary Report")
        print("7. Run Full Data Analysis (Pandas & NumPy)")
        print("8. Exit")
        print("==================================================")
        
        choice = input("Select an option (1-8): ").strip()
        
        if choice == "1":
            display_all_complaints(limit=55)
        elif choice == "2":
            add_complaint()
        elif choice == "3":
            search_complaint()
        elif choice == "4":
            update_complaint()
        elif choice == "5":
            delete_complaint()
        elif choice == "6":
            generate_summary_report()
        elif choice == "7":
            run_numpy_analysis()
        elif choice == "8":
            print("Exiting Hostel Complaint Management System. Goodbye!")
            break
        else:
            print("[WARNING] Invalid selection. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
