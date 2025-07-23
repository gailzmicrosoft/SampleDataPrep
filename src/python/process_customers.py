import pandas as pd
import os

def process_customer_names():
    """
    Process customer_names.csv to remove duplicates by Last_Name,
    keeping only the first occurrence of each unique Last_Name,
    and sort alphabetically by Last_Name.
    """
    
    # Define file paths
    input_file = 'customer_names_raw.csv'
    output_file = 'customer_names_unique.csv'
    
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: {input_file} not found in current directory")
            return
        
        print(f"Reading {input_file}...")
        
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        print(f"Original data: {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        
        # Remove duplicates based on Last_Name, keeping the first occurrence
        df_unique = df.drop_duplicates(subset=['Last_Name'], keep='first')
        
        # Sort alphabetically by Last_Name
        df_unique = df_unique.sort_values('Last_Name')
        
        # Reset index
        df_unique = df_unique.reset_index(drop=True)
        
        # Write to new CSV file
        df_unique.to_csv(output_file, index=False)
        
        print(f"\nProcessing complete!")
        print(f"Unique data: {len(df_unique)} rows")
        print(f"Removed {len(df) - len(df_unique)} duplicate last names")
        print(f"Output saved to: {output_file}")
        
        # Show first few rows of the result
        print(f"\nFirst 5 rows of {output_file}:")
        print(df_unique.head().to_string(index=False))
        
        # Show some statistics
        print(f"\nGender distribution in unique data:")
        print(df_unique['Gender'].value_counts())
        
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    process_customer_names()