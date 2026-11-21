import numpy as np
import pandas as pd
from data_handler import CSV_FILE, generate_initial_dataset

def run_pandas_analysis():
    """Performs comprehensive Pandas data cleaning, filtering, GroupBy, and stats."""
    generate_initial_dataset(CSV_FILE)
    
    # 1. Read data from CSV into a Pandas DataFrame
    df = pd.read_csv(CSV_FILE)
    print("\n================ PANDAS DATA ANALYSIS ================")
    print(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 2. Handle Missing Values
    missing_before = df.isnull().sum()
    print("\n[1] Missing Values Before Cleaning:")
    print(missing_before[missing_before > 0])
    
    # Fill missing Resolution_Hours with median and Repair_Cost with category mean
    df["Resolution_Hours"] = df["Resolution_Hours"].fillna(df["Resolution_Hours"].median())
    df["Repair_Cost"] = df["Repair_Cost"].fillna(df["Repair_Cost"].mean().round(2))
    print(f"Total Missing Values After Cleaning: {df.isnull().sum().sum()}")
    
    # 3. Display Selected Rows and Columns (using loc & iloc)
    print("\n[2] Selected Rows (0 to 4) & Specific Columns:")
    selected_df = df.loc[0:4, ["Complaint_ID", "Block", "Category", "Priority", "Repair_Cost"]]
    print(selected_df.to_string(index=False))
    
    # 4. Data Filtering and Sorting (High/Critical unresolved complaints sorted by Cost)
    print("\n[3] Filtered & Sorted: Pending/In-Progress High/Critical Complaints (Top 5 by Cost):")
    filtered_df = df[
        (df["Priority"].isin(["High", "Critical"])) & 
        (df["Status"] != "Resolved")
    ].sort_values(by="Repair_Cost", ascending=False)
    print(filtered_df[["Complaint_ID", "Block", "Category", "Priority", "Status", "Repair_Cost"]].head(5).to_string(index=False))
    
    # 5. GroupBy Operations
    print("\n[4] GroupBy Category (Total Cost, Average Resolution Hours, Complaint Count):")
    category_summary = df.groupby("Category").agg(
        Total_Complaints=("Complaint_ID", "count"),
        Avg_Resolution_Hrs=("Resolution_Hours", "mean"),
        Total_Repair_Cost=("Repair_Cost", "sum")
    ).round(2)
    print(category_summary)
    
    print("\n[5] GroupBy Hostel Block (Average Repair Cost):")
    block_summary = df.groupby("Block")["Repair_Cost"].mean().round(2)
    print(block_summary)
    
    # 6. Statistical Analysis (describe)
    print("\n[6] Statistical Summary of Numerical Columns:")
    print(df[["Room_No", "Resolution_Hours", "Repair_Cost"]].describe().round(2))
    print("======================================================")
    
    return df

def run_numpy_analysis():
    """Performs 1D & 2D NumPy array operations, indexing, slicing, and statistical metrics."""
    df = run_pandas_analysis()
    
    print("\n================ NUMPY NUMERICAL INSIGHTS ================")
    # 1. Create 1D NumPy Arrays
    costs_1d = df["Repair_Cost"].to_numpy()
    hours_1d = df["Resolution_Hours"].to_numpy()
    
    # 2. Array Indexing and Slicing on 1D Array
    print(f"[1] 1D Array Indexing -> First Complaint Cost: ₹{costs_1d[0]:.2f}, Last Complaint Cost: ₹{costs_1d[-1]:.2f}")
    print(f"[2] 1D Array Slicing  -> First 5 Resolution Hours: {hours_1d[:5]}")
    
    # 3. Sum, Mean, Max, Min, and Standard Deviation
    print("\n[3] Repair Cost Metrics (NumPy):")
    print(f"    - Total Expenditure (Sum) : ₹{np.sum(costs_1d):.2f}")
    print(f"    - Average Cost (Mean)     : ₹{np.mean(costs_1d):.2f}")
    print(f"    - Highest Cost (Max)      : ₹{np.max(costs_1d):.2f}")
    print(f"    - Lowest Cost (Min)       : ₹{np.min(costs_1d):.2f}")
    print(f"    - Cost Volatility (Std)   : ₹{np.std(costs_1d):.2f}")
    
    print("\n[4] Resolution Time Metrics (NumPy):")
    print(f"    - Mean Resolution Time    : {np.mean(hours_1d):.2f} hrs")
    print(f"    - Std Dev Resolution Time : {np.std(hours_1d):.2f} hrs")
    
    # 4. Create 2D NumPy Array (Pairing Resolution Hours and Repair Cost)
    matrix_2d = np.column_stack((hours_1d, costs_1d))
    print(f"\n[5] 2D Array Shape: {matrix_2d.shape} (Rows: Records, Col 0: Hours, Col 1: Cost)")
    print(f"    - 2D Indexing [Row 2, Col 1] (3rd record's cost): ₹{matrix_2d[2, 1]:.2f}")
    print(f"    - 2D Slicing [Rows 0:3, Both Cols]:\n{matrix_2d[0:3, :]}")
    
    # 5. Meaningful Insight: Cost per Hour Efficiency
    cost_per_hour = costs_1d / hours_1d
    high_cost_count = np.sum(costs_1d > np.mean(costs_1d))
    print("\n[6] Key Derived Insights:")
    print(f"    - {high_cost_count} out of {len(costs_1d)} complaints exceeded the average repair cost.")
    print(f"    - Average Maintenance Burn Rate: ₹{np.mean(cost_per_hour):.2f} per resolution hour.")
    print("==========================================================")