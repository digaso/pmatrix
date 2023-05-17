import pandas as pd


def find_species_column(df: pd.DataFrame, i: int) -> int:
    unnamed_count = 0
    for index, column in enumerate(df):
        if index >= i:
            if not str(column).find("Unnamed"):
                unnamed_count += 1
                continue
            elif unnamed_count > 1:
                return index - 1
            else:
                continue
    return -1


def get_data(species: list, df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    data = []
    start_tables_index = get_species_index(df, 0)
    end_tables_index = get_last_species_index(df)
    last_species_index = find_last_species(df)

    print(df.Name, start_tables_index)
    print(df.Name, end_tables_index)
    print(df.Name, last_species_index)
    for i, start in enumerate(start_tables_index):
        
        for j in range(last_species_index[i] + 1):
            for end in range(start + 1, end_tables_index[i] + 1):
                for item in df.iloc[j]:
                    pass

    return new_df


def get_unique_index(species, wanted):
    for i, specie in species:
        if specie == wanted:
            return i
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
    species = []
    tables_index = get_species_index(df, 0)
    for index in tables_index:
        column = df.columns[index]
        for specie in df[column]:
            specie = str(specie).replace("\xa0", " ")
            specie = str(specie).replace(" [sub]", "")
            specie = str(specie).replace("¿ ", "")
            specie = str(specie).strip()
            if species.count(specie) == 0 and specie != "nan":
                species.append(specie)
    return species


def find_last_collumn(df: pd.DataFrame, i: int) -> int:
    for index, column in enumerate(df):
        if index >= i + 1:
            if str(column).find("Unnamed") == -1 and index != df.columns.size - 1:
                continue
            elif index == df.columns.size - 1:
                return index
            else:
                return index - 1
    return -1


def get_last_species_index(df: pd.DataFrame):
    tables_index = []
    start_index = get_species_index(df, 0)
    for i in start_index:
        tables_index.append(find_last_collumn(df, i))
    return tables_index


def find_last_species(df: pd.DataFrame):
    li = []
    tables_index = get_species_index(df, 0)
    last_species_index = []
    for i in tables_index:
        column = df.columns[i]
        for index, row in enumerate(df[column]):
            if str(row) != "nan" and df[column].size - 1 != index:
                continue
            else:
                last_species_index.append(index)
                break

    return last_species_index


def sort_lower_case(x):
    return x.lower()
