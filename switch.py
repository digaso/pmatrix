import pandas as pd
import sys

def main(new_names, excel_file):
    # Read the files into pandas DataFrames
    new_names_df = pd.read_excel(new_names)
    excel_df = pd.read_excel(excel_file)
    
    # Create a dictionary from new_names_df for quick lookup
    name_mapping = pd.Series(new_names_df.new_name.values, index=new_names_df.names).to_dict()
    count = 0
    # Iterate over the rows of the excel_df DataFrame
    for index, row in excel_df.iterrows():
        species = row['Species']
        if species in name_mapping:
            count += 1
            excel_df.at[index, 'Species'] = name_mapping[species]
    
    # make an excel file with the new data
    print(f"Updated {count} species")
    excel_df.to_excel("updatedQL.xlsx", index=False)
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python switch.py <file1> <file2>")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    main(file1, file2)