from hmac import new
from numpy import column_stack, nan
import pandas as pd


def treat_string(specie_name):
    if specie_name == "Quercus lusitanica":
        return "Quercus lusitanica Lam."
    specie_name = str(specie_name).replace("\xa0", " ")
    specie_name = str(specie_name).replace(" [sub]", "")
    specie_name = str(specie_name).replace("¿ ", "")
    specie_name = str(specie_name).strip()
    return specie_name


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


def get_data(
    species: list,
    df: pd.DataFrame,
    new_df: pd.DataFrame,
    killers: dict,
    new_taxonomy=pd.DataFrame(),
    _kill=True,
):
    df_zone = get_df_zone(df, killers)
    zone_killers = killers[df_zone]
    start_tables_index = get_species_index(df, 0)
    end_tables_index = get_last_species_index(df)
    last_species_index = find_last_species(df)

    for index, start in enumerate(start_tables_index):
        for i in range(end_tables_index[index] - start):
            data = []
            for _ in range(len(species)):
                data.append(".")
            tmp = df[df.columns[start + 1 + i]]
            flag = False

            for index1, dado in enumerate(tmp):
                specie_name = treat_string(df.iloc[index1, start])
                specie_name = get_new_name(specie_name, new_taxonomy)
                if specie_name == "nan":
                    break
                specie_id = get_unique_index(species, specie_name)
                if specie_name in zone_killers and _kill:
                    if dado == "+" or dado == "x" or dado == "." or dado == "r":
                        flag = True
                        break
                    elif int(dado) < 3:
                        flag = True
                        break
                data[specie_id] = dado
            if not flag or _kill is False:
                new_df[df.Name + str(index + 1) + "." + str(i + 1)] = data
    return new_df


def get_df_zone(df: pd.DataFrame, killers: dict):
    df_name = df.Name
    for name in killers.keys():
        if name in df_name:
            return name
    return "NaN"


def get_unique_index(species, wanted):
    for i, specie in enumerate(species):
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


def get_new_name(specie: str, new_taxonomy: pd.DataFrame) -> str:
    new_specie = specie
    good_names = new_taxonomy[new_taxonomy.columns[0]].tolist()
    new_taxonomy = new_taxonomy.drop(columns=[new_taxonomy.columns[0]])
    if good_names.count(specie) > 0:
        return specie
    for i in range(0, len(good_names)):
        if (
            specie == new_taxonomy[new_taxonomy.columns[0]][i]
            or specie == new_taxonomy[new_taxonomy.columns[1]][i]
            or specie == new_taxonomy[new_taxonomy.columns[2]][i]
        ):
            new_specie = good_names[i]
            break
    return new_specie


def get_species(df: pd.DataFrame, new_taxonomy: pd.DataFrame):
    tables_index = []
    species = []
    tables_index = get_species_index(df, 0)
    for index in tables_index:
        column = df.columns[index]
        for specie in df[column]:
            specie = treat_string(specie)
            specie = get_new_name(specie, new_taxonomy)

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
        added = False
        for index, row in enumerate(df[column]):
            if not (str(row) != "nan" and df[column].size != index):
                last_species_index.append(index)
                added = True
                break
        if not added:
            last_species_index.append(df[column].size)
    return last_species_index


def sort_lower_case(x):
    return x.lower()
