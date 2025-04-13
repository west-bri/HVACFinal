import pandas as pd
import datetime as dt

def merge_csv_datasets(rtu_file_path, tu_file_path, output_file_path):
    """
    Merge RTU and TU datasets based on timestamp
    
    Parameters:
    -----------
    rtu_file_path : str
        Path to the RTU CSV file
    tu_file_path : str
        Path to the TU CSV file
    output_file_path : str
        Path where the merged CSV will be saved
    """
    # Read the CSV files
    print(f"Reading RTU data from {rtu_file_path}")
    rtu_df = pd.read_csv(rtu_file_path)
    
    print(f"Reading TU data from {tu_file_path}")
    tu_df = pd.read_csv(tu_file_path)
    
    # Display basic info
    print(f"\nRTU Dataset: {rtu_df.shape[0]} rows, {rtu_df.shape[1]} columns")
    print(f"TU Dataset: {tu_df.shape[0]} rows, {tu_df.shape[1]} columns")
    
    # Process timestamps - ensure they are in a standard format
    print("\nProcessing timestamps...")
    
    # Create a copy of the original time column for reference
    rtu_df['original_time'] = rtu_df['time']
    tu_df['original_time'] = tu_df['time']
    
    # Convert time strings to datetime objects for proper merging
    try:
        # Try using automatic parsing first
        rtu_df['datetime'] = pd.to_datetime(rtu_df['time'])
        tu_df['datetime'] = pd.to_datetime(tu_df['time'])
    except:
        # If automatic parsing fails, explicitly parse the format
        # The format appears to be 'M/D/YY H:M' based on sample data
        rtu_df['datetime'] = pd.to_datetime(rtu_df['time'], format='%m/%d/%y %H:%M')
        tu_df['datetime'] = pd.to_datetime(tu_df['time'], format='%m/%d/%y %H:%M')
    
    # Set datetime as index for merging
    rtu_df.set_index('datetime', inplace=True)
    tu_df.set_index('datetime', inplace=True)
    
    # Check for common timestamps
    rtu_timestamps = set(rtu_df.index)
    tu_timestamps = set(tu_df.index)
    common_timestamps = rtu_timestamps.intersection(tu_timestamps)
    
    print(f"RTU unique timestamps: {len(rtu_timestamps)}")
    print(f"TU unique timestamps: {len(tu_timestamps)}")
    print(f"Common timestamps: {len(common_timestamps)}")
    
    # Rename columns to avoid conflicts
    rtu_df = rtu_df.add_prefix('RTU_')
    tu_df = tu_df.add_prefix('TU_')
    
    # Fix the renamed original time columns
    rtu_df.rename(columns={'RTU_original_time': 'original_time'}, inplace=True)
    tu_df.rename(columns={'TU_original_time': 'original_time'}, inplace=True)
    
    # Merge the datasets on the datetime index
    print("\nMerging datasets...")
    
    # Different merge options:
    
    # 1. Inner join - only keep rows where timestamp exists in both datasets
    merged_df_inner = pd.merge(rtu_df, tu_df, left_index=True, right_index=True, how='inner')
    
    # 2. Outer join - keep all rows, fill missing values with NaN
    merged_df_outer = pd.merge(rtu_df, tu_df, left_index=True, right_index=True, how='outer')
    
    # 3. Left join - keep all RTU rows, only matching TU rows
    merged_df_left = pd.merge(rtu_df, tu_df, left_index=True, right_index=True, how='left')
    
    # 4. Right join - keep all TU rows, only matching RTU rows
    merged_df_right = pd.merge(rtu_df, tu_df, left_index=True, right_index=True, how='right')
    
    # Print merge results
    print(f"Inner join result: {merged_df_inner.shape[0]} rows, {merged_df_inner.shape[1]} columns")
    print(f"Outer join result: {merged_df_outer.shape[0]} rows, {merged_df_outer.shape[1]} columns")
    print(f"Left join result: {merged_df_left.shape[0]} rows, {merged_df_left.shape[1]} columns")
    print(f"Right join result: {merged_df_right.shape[0]} rows, {merged_df_right.shape[1]} columns")
    
    # Save merged dataset - using inner join by default (only timestamps common to both)
    # But you can change to one of the other merge results if preferred
    merged_df = merged_df_inner  # Change this to merged_df_outer, merged_df_left, or merged_df_right if needed
    
    # Reset index to make datetime a regular column
    merged_df.reset_index(inplace=True)
    
    # Save to CSV
    print(f"\nSaving merged dataset to {output_file_path}")
    merged_df.to_csv(output_file_path, index=False)
    
    print(f"Merge complete! Merged dataset has {merged_df.shape[0]} rows and {merged_df.shape[1]} columns.")
    
    return merged_df

if __name__ == "__main__":
    # Specify file paths
    rtu_file_path = "data/cleaned_RTU/Combined_RTU.csv"
    tu_file_path = "data/cleaned_RTU/Combined_TU.csv"
    output_file_path = "Merged_RTU_TU.csv"
    
    # Run the merge function
    merged_data = merge_csv_datasets(rtu_file_path, tu_file_path, output_file_path)
    
    # Print a sample of the merged data
    print("\nSample of merged data:")
    print(merged_data.head())