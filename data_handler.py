
import csv
import os
import random

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(PROJECT_DIR, "hostel_complaints.csv")

# Tuple (Immutable allowed categories & priorities)
CATEGORIES = ("Electrical", "Plumbing", "Wi-Fi/Network", "Housekeeping", "Furniture", "Mess/Food")
PRIORITIES = ("Low", "Medium", "High", "Critical")
STATUSES = ("Pending", "In Progress", "Resolved")
BLOCKS = ("Block A", "Block B", "Block C", "Block D")

def generate_initial_dataset(filename=CSV_FILE, num_records=55):
    """Generates a CSV dataset with at least 55 records."""
    if os.path.exists(filename):
        return

    first_names = ["Aarav", "Rohan", "Priya", "Sneha", "Vikram", "Ananya", "Kabir", "Meera", "Arjun", "Diya"]
    last_names = ["Sharma", "Verma", "Patel", "Gupta", "Singh", "Kumar", "Nair", "Reddy", "Joshi", "Das"]
    
    # List of Dictionaries to store records
    records = []
    
    for i in range(1, num_records + 1):
        comp_id = f"CMP{1000 + i}"
        student = f"{random.choice(first_names)} {random.choice(last_names)}"
        block = random.choice(BLOCKS)
        room_no = random.randint(101, 420)
        category = random.choice(CATEGORIES)
        priority = random.choice(PRIORITIES)
        status = random.choice(STATUSES)
        
        # Intentionally inject a few missing values (None/empty) for Pandas handling
        res_hours = "" if i % 12 == 0 else random.randint(2, 72)
        est_cost = "" if i % 15 == 0 else round(random.uniform(150.0, 2500.0), 2)

        record = {
            "Complaint_ID": comp_id,
            "Student_Name": student,
            "Block": block,
            "Room_No": room_no,
            "Category": category,
            "Priority": priority,
            "Status": status,
            "Resolution_Hours": res_hours,
            "Repair_Cost": est_cost
        }
        records.append(record)  # List method: append()

    fieldnames = list(records[0].keys())  # Dictionary method: keys()
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

def load_records_from_csv(filename=CSV_FILE):
    """Reads CSV using standard Python file handling and returns a list of dictionaries."""
    generate_initial_dataset(filename)
    records = []
    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(dict(row))
    return records

def save_records_to_csv(records, filename=CSV_FILE):
    """Writes updated list of dictionaries back to the CSV file."""
    if not records:
        return
    fieldnames = list(records[0].keys())
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

def get_unique_metadata(records):
    """Demonstrates Set operations and Dictionary methods to inspect unique values."""
    unique_blocks = {rec.get("Block") for rec in records}       # Set comprehension & dict.get()
    unique_categories = {rec.get("Category") for rec in records}
    return unique_blocks, unique_categories
print("Data handler module loaded successfully.")
print("Available Categories:", CATEGORIES)
print("Available Priorities:", PRIORITIES)
print("Available Statuses:", STATUSES)
print("Available Blocks:", BLOCKS)