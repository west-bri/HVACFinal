import os
import pandas as pd

def remove_columns_from_csvs(directory_path, columns_to_remove, output_directory=None):
    """
    Iterate through CSV files in a directory and remove specified columns.
    
    Args:
        directory_path (str): Path to directory containing CSV files
        columns_to_remove (list): List of column names to remove
        output_directory (str, optional): Path to save modified files. If None, overwrites original files.
    """
    # Create output directory if specified and doesn't exist
    if output_directory and not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in {directory_path}")
        return
    
    for file_name in csv_files:
        file_path = os.path.join(directory_path, file_name)
        
        # Read the CSV file
        try:
            df = pd.read_csv(file_path)
            print(f"Processing {file_name}...")
            
            # Check which columns to remove actually exist in the file
            cols_to_remove = [col for col in columns_to_remove if col in df.columns]
            
            if not cols_to_remove:
                print(f"  None of the specified columns found in {file_name}")
                continue
            
            # Remove the columns
            df = df.drop(columns=cols_to_remove)
            print(f"  Removed columns: {', '.join(cols_to_remove)}")
            
            # Save the modified dataframe
            if output_directory:
                output_path = os.path.join(output_directory, file_name)
            else:
                output_path = file_path
                
            df.to_csv(output_path, index=False)
            print(f"  Saved to {output_path}")
            
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")
    
    print("Processing complete!")

# Example usage
if __name__ == "__main__":
    # Define parameters
    directory_path = "data/terminalUnits_copy"  # Change this to your directory
    columns_to_remove = ["Air_Flow_Diff", "Room_Temperature_Diff", "VAV_Temperature_Diff", "SaTemp", "oppMode"]  # Change to your columns
    output_directory = "data/cleaned_TU"  # Optional, set to None to overwrite original files
    
    # Run the function
    remove_columns_from_csvs(directory_path, columns_to_remove, output_directory)