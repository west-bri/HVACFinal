import pandas as pd
import os
import glob
from datetime import datetime

def find_common_timestamps(csv_files, ignore_columns=None):
    """
    Read multiple CSV files into dataframes and find rows with common timestamps
    where fields (except ignored ones) are populated.
    
    Args:
        csv_files: List of paths to CSV files
        ignore_columns: List of column names to ignore when checking for completeness
    
    Returns:
        Tuple of (common_data, ignored_columns)
    """
    if ignore_columns is None:
        ignore_columns = []
    
    # Read all CSV files into a list of dataframes
    dataframes = []
    file_names = []
    for file in csv_files:
        df = pd.read_csv(file)
        # Make sure the timestamp column is properly named
        if 'time' not in df.columns:
            print(f"Warning: 'time' column not found in {file}")
            continue
        dataframes.append(df)
        file_names.append(os.path.basename(file))
    
    if not dataframes:
        print("No valid dataframes loaded.")
        return {}, ignore_columns
    
    # Get all columns except those we're ignoring
    all_columns = set(dataframes[0].columns) - set(ignore_columns) - {'time'}
    
    # Find rows where required columns (all except ignored ones) are populated
    timestamps_by_df = []
    for df in dataframes:
        # Check only the required columns for completeness
        columns_to_check = [col for col in df.columns if col in all_columns]
        # Get rows where these columns are not null
        complete_rows = df.dropna(subset=columns_to_check)
        
        # Extract the time column from complete rows
        if not complete_rows.empty:
            timestamps_by_df.append(set(complete_rows['time']))
        else:
            # If any dataframe has no matching rows, there can't be common timestamps
            return {}, ignore_columns
    
    # Find timestamps that exist in all dataframes
    common_timestamps = set.intersection(*timestamps_by_df) if timestamps_by_df else set()
    
    # Create a dictionary to store rows with common timestamps
    common_data = {}
    for timestamp in common_timestamps:
        common_data[timestamp] = []
        for i, df in enumerate(dataframes):
            # Get the row that matches this timestamp
            mask = df['time'] == timestamp
            if not df[mask].empty:
                matching_row = df[mask].iloc[0].to_dict()
                matching_row['_source_file'] = file_names[i]
                common_data[timestamp].append(matching_row)
    
    return common_data, ignore_columns

def progressive_timestamp_search(csv_files):
    """
    Progressively ignore fields until common timestamps are found
    
    Args:
        csv_files: List of paths to CSV files
    
    Returns:
        Tuple of (common_data, ignored_columns)
    """
    # First, try with no ignored columns
    ignored_columns = []
    common_data, _ = find_common_timestamps(csv_files, ignored_columns)
    
    if common_data:
        return common_data, ignored_columns
    
    # Load one dataframe to get column names
    df = pd.read_csv(csv_files[0])
    all_columns = list(df.columns)
    
    # Remove 'time' from the list of columns we can ignore
    if 'time' in all_columns:
        all_columns.remove('time')
    
    # Progressively ignore columns that might have missing values
    for df_sample in [pd.read_csv(f) for f in csv_files]:
        # Calculate the percentage of null values in each column
        null_percentages = df_sample.isnull().mean()
        
        # Sort columns by their null percentage (highest first)
        columns_by_null = null_percentages.sort_values(ascending=False)
        
        # Add high-null columns to our ignore list
        for col, null_pct in columns_by_null.items():
            if col != 'time' and col not in ignored_columns and null_pct > 0:
                ignored_columns.append(col)
                # Try again with the updated ignore list
                common_data, _ = find_common_timestamps(csv_files, ignored_columns)
                print(f"Trying without column: {col} (has {null_pct:.1%} null values)")
                
                if common_data:
                    return common_data, ignored_columns
    
    # If we still don't have common timestamps, try ignoring different combinations
    # This is a more aggressive approach
    print("\nTrying more aggressive combinations of columns to ignore...")
    
    # Get all columns that have any null values across any file
    columns_with_nulls = set()
    for file in csv_files:
        df = pd.read_csv(file)
        null_cols = df.columns[df.isnull().any()].tolist()
        columns_with_nulls.update(null_cols)
    
    # Remove 'time' from this set
    if 'time' in columns_with_nulls:
        columns_with_nulls.remove('time')
    
    ignored_columns = list(columns_with_nulls)
    common_data, _ = find_common_timestamps(csv_files, ignored_columns)
    
    return common_data, ignored_columns

def export_common_rows(common_data, output_file):
    """
    Export rows with common timestamps to a CSV file
    
    Args:
        common_data: Dictionary mapping timestamps to lists of rows
        output_file: Path to the output CSV file
    
    Returns:
        Path to the output file
    """
    if not common_data:
        print("No common data to export.")
        return None
    
    # Create a list to hold all the rows
    all_rows = []
    
    # For each timestamp, add all rows from different files
    for timestamp, rows in common_data.items():
        for row in rows:
            # Make a copy of the row to avoid modifying the original
            row_data = row.copy()
            # Ensure the source file is included
            source_file = row_data.pop('_source_file', 'unknown')
            row_data['source_file'] = source_file
            all_rows.append(row_data)
    
    # Convert to DataFrame
    output_df = pd.DataFrame(all_rows)
    
    # Move 'time' and 'source_file' columns to the front
    cols = list(output_df.columns)
    if 'time' in cols:
        cols.remove('time')
        cols = ['time'] + cols
    if 'source_file' in cols:
        cols.remove('source_file')
        cols = ['source_file'] + cols
    
    output_df = output_df[cols]
    
    # Write to CSV
    output_df.to_csv(output_file, index=False)
    print(f"\nExported {len(output_df)} rows to {output_file}")
    
    return output_file

def main():
    # Example usage
    csv_directory = "data/terminalUnits"  # Update this path
    output_file = os.path.join(csv_directory, "common_timestamps.csv")
    
    csv_files = glob.glob(os.path.join(csv_directory, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {csv_directory}")
        return
    
    print(f"Found {len(csv_files)} CSV files:")
    for file in csv_files:
        print(f"  - {os.path.basename(file)}")
    
    print("\nSearching for common timestamps...")
    common_data, ignored_columns = progressive_timestamp_search(csv_files)
    
    if common_data:
        print(f"\nSuccess! Found {len(common_data)} common timestamps after ignoring {len(ignored_columns)} columns:")
        if ignored_columns:
            print("Ignored columns:")
            for col in ignored_columns:
                print(f"  - {col}")
        
        print(f"\nCommon timestamps found:")
        for i, (timestamp, rows) in enumerate(list(common_data.items())[:5], 1):  # Show just first 5
            print(f"\n{i}. Common timestamp: {timestamp}")
            print(f"   Found in {len(rows)} files")
            # Print a sample of the data
            if rows:
                sample_row = rows[0]
                sample_file = sample_row.get('_source_file', 'unknown file')
                print(f"   Sample data from {sample_file}:")
                for k, v in list([(k, v) for k, v in sample_row.items() if k != '_source_file'][:5]):  # Show just first 5 fields
                    print(f"     {k}: {v}")
                
        if len(common_data) > 5:
            print(f"\n... and {len(common_data) - 5} more timestamps")
        
        # Export the common rows to a CSV file
        export_common_rows(common_data, output_file)
    else:
        print("\nNo common timestamps found even after trying to ignore columns with missing values.")
        print("Columns we tried to ignore:")
        for col in ignored_columns:
            print(f"  - {col}")

if __name__ == "__main__":
    main()