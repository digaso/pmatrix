import pandas as pd
import os


def find_species_column(df: pd.DataFrame, i: int) -> int:
    unnamed_count = 0
    for index, column in enumerate(df):
        if index >= i:
            if not str(column).find("Unnamed"):
                unnamed_count += 1
                continue
            elif unnamed_count > 1:
                return index-1
            else:
                continue

    return -1


def get_species_index(df, i):
    tables_index = []
    while True:
        i = find_species_column(df, i)
        if i == -1:
            break
        tables_index.append(i)
        i += 1
    return tables_index


def get_species(df: pd.DataFrame):
    tables_index = []
    i = 0
    species = []
    tables_index = get_species_index(df, i)

    for index in tables_index:
        column = df.columns[index]
        for specie in df[column]:
            if species.count(specie) == 0:
                species.append(specie)
    return species


def find_last_species(df: pd.DataFrame):
    li = []
    tables_index = get_species_index(df, 0)
    print(tables_index)
    last_species_index = []
    for i in tables_index:
        column = df.columns[i]
        for index, row in enumerate(df[column]):
            if str(row) != 'nan':
                continue
            else:
                last_species_index.append(index)
                break

    return last_species_index


def main():
    all_files = os.listdir('data')
    li = []
    all_files.sort()
    for file in all_files:
        if not file.endswith('.csv'):
            continue
        df = pd.read_csv('data/' + file)
        li.append(df)

    new_df = pd.DataFrame()

    for i, df in enumerate(li):
        if i > 0:
            break
        get_species(df)
        print(find_last_species(df))

    # new_df.to_excel('output.xlsx', index=False)


main()
