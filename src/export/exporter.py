"""
Export Excel to CSV for delivery.
"""

import pandas as pd

def export_to_csv(input_file, output_file):
    """
    Export the Excel file to CSV.
    Args:
        input_file (str): Path to Excel file.
        output_file (str): Path to save CSV.
    """
    df = pd.read_excel(input_file)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Exported {input_file} to {output_file}")

# Example usage:
# export_to_csv('data/Transformed_Data.xlsx', 'data/Transformed_Data.csv')