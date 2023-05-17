import pandas as pd
from utils import *
import os


def main():
    all_files = os.listdir("data")
    li = []
    all_files.sort(key=sort_lower_case)
    for file in all_files:
        if not file.endswith(".csv"):
            continue
        df = pd.read_csv("data/" + file)
        df.Name = file.replace(".csv", "")
        li.append(df)

    new_df = pd.DataFrame()
    species = []

    for i, df in enumerate(li):
        if i > 99:
            break
        species_ = get_species(df)
        for specie in species_:
            if species.count(specie) == 0:
                species.append(specie)

    new_df["Species"] = species
    for i, df in enumerate(li):
        if i > 0:
            break

        data = get_data(species, df, new_df)

    print(new_df)
    # print(df.Name, start_tables_index)
    # print(df.Name, end_tables_index)
    # print(df.Name, last_species_index)
    # new_df.to_excel('output.xlsx', index=False)


main()
