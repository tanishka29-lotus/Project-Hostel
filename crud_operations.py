from data_handler import (
    load_records_from_csv,
    save_records_to_csv,
    get_unique_metadata,
    CATEGORIES,
    PRIORITIES,
    STATUSES
)

def add_complaint():
    """UDF 1: Adds a new complaint record to the dataset."""
    records = load_records_from_csv()
    print("\n--- ADD NEW COMPLAINT ---")

    if not records:
        print("[ERROR] The dataset is empty.")
        return

    # Generate next sequential ID
    last_id_num = max(int(r["Complaint_ID"].replace("CMP", "")) for r in records)
    new_id = f"CMP{last_id_num + 1}"
    
    name = input("Enter Student Name: ").strip()
    block = input("Enter Hostel Block (Block A/B/C/D): ").strip()
    room = input("Enter Room Number: ").strip()
    
    print(f"Available Categories: {CATEGORIES}")
    category = input("Enter Category: ").strip()
    if category not in CATEGORIES:
        category = "Housekeeping"
        
    print(f"Available Priorities: {PRIORITIES}")
    priority = input("Enter Priority: ").strip()
    if priority not in PRIORITIES:
        priority = "Medium"
        
    res_hours = input("Estimated Resolution Hours (or press Enter to skip): ").strip()
    cost = input("Estimated Repair Cost in INR (or press Enter to skip): ").strip()

    new_record = {
        "Complaint_ID": new_id,
        "Student_Name": name,
        "Block": block,
        "Room_No": room,
        "Category": category,
        "Priority": priority,
        "Status": "Pending",
        "Resolution_Hours": res_hours,
        "Repair_Cost": cost
    }
    
    records.append(new_record)
    save_records_to_csv(records)
    print(f"[SUCCESS] Complaint {new_id} added successfully!")

def display_all_complaints(limit=15):
    """UDF 2: Displays records in a formatted VS Code terminal table."""
    records = load_records_from_csv()
    print(f"\n--- HOSTEL COMPLAINTS (Showing top {min(limit, len(records))} of {len(records)} records) ---")
    header = f"{'ID':<8} | {'Student':<16} | {'Block':<8} | {'Room':<5} | {'Category':<14} | {'Priority':<9} | {'Status':<12} | {'Hours':<6} | {'Cost(₹)':<8}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    
    for rec in records[:limit]:  # List slicing
        print(
            f"{rec['Complaint_ID']:<8} | {rec['Student_Name']:<16} | {rec['Block']:<8} | "
            f"{rec['Room_No']:<5} | {rec['Category']:<14} | {rec['Priority']:<9} | "
            f"{rec['Status']:<12} | {str(rec['Resolution_Hours']):<6} | {str(rec['Repair_Cost']):<8}"
        )
    print("-" * len(header))

def search_complaint():
    """UDF 3: Searches for a complaint by Complaint ID or Student Name."""
    records = load_records_from_csv()
    query = input("\nEnter Complaint ID (e.g., CMP1005) or Student Name to search: ").strip().lower()
    
    matches = [
        r for r in records 
        if query in r["Complaint_ID"].lower() or query in r["Student_Name"].lower()
    ]
    
    if not matches:
        print("[INFO] No matching records found.")
        return
        
    print(f"\nFound {len(matches)} matching record(s):")
    for r in matches:
        for k, v in r.items():  # Dictionary method: items()
            print(f"  {k}: {v}")
        print("-" * 30)

def update_complaint():
    """UDF 4: Updates the status, resolution hours, or cost of an existing record."""
    records = load_records_from_csv()
    comp_id = input("\nEnter Complaint ID to update (e.g., CMP1002): ").strip().upper()
    
    for rec in records:
        if rec["Complaint_ID"] == comp_id:
            print(f"Current Record: {rec}")
            print(f"Valid Statuses: {STATUSES}")
            new_status = input("Enter new Status (leave blank to keep current): ").strip()
            new_hours = input("Enter Resolution Hours (leave blank to keep current): ").strip()
            new_cost = input("Enter Repair Cost (leave blank to keep current): ").strip()
            
            updates = {}
            if new_status in STATUSES:
                updates["Status"] = new_status
            if new_hours:
                updates["Resolution_Hours"] = new_hours
            if new_cost:
                updates["Repair_Cost"] = new_cost
                
            rec.update(updates)  # Dictionary method: update()
            save_records_to_csv(records)
            print(f"[SUCCESS] Record {comp_id} updated!")
            return
            
    print(f"[ERROR] Complaint ID {comp_id} not found.")

def delete_complaint():
    """UDF 5: Deletes a complaint record by Complaint ID."""
    records = load_records_from_csv()
    comp_id = input("\nEnter Complaint ID to delete (e.g., CMP1010): ").strip().upper()
    
    for idx, rec in enumerate(records):
        if rec["Complaint_ID"] == comp_id:
            removed = records.pop(idx)  # List method: pop()
            save_records_to_csv(records)
            print(f"[SUCCESS] Deleted complaint {removed['Complaint_ID']} ({removed['Student_Name']}).")
            return
            
    print(f"[ERROR] Complaint ID {comp_id} not found.")

def generate_summary_report():
    """UDF 6: Generates a quick operational summary using Python data structures."""
    records = load_records_from_csv()
    blocks, categories = get_unique_metadata(records)
    
    status_counts = {}
    for r in records:
        st = r["Status"]
        status_counts[st] = status_counts.get(st, 0) + 1
        
    print("\n================ SUMMARY REPORT ================")
    print(f"Total Complaints Logged : {len(records)}")
    print(f"Active Hostel Blocks    : {sorted(list(blocks))}")
    print(f"Categories Tracked      : {len(categories)} -> {', '.join(sorted(categories))}")
    print("\nStatus Breakdown:")
    for status, count in status_counts.items():
        print(f"  - {status:<15}: {count}")
    print("================================================")