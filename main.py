import warnings
import pandas as pd
from utils import *
import os

warnings.filterwarnings("ignore")


def output_all(
    li, species, new_taxonomy: pd.DataFrame, killers, sort=False, _kill=True
):
    new_df = pd.DataFrame()
    new_df["Species"] = species
    for i, df in enumerate(li):
        if i > 50:
            break
        new_df = get_data(species, df, new_df, killers, new_taxonomy, _kill)
    if sort:
        new_df = new_df.sort_values(by=["Species"])
    kill_str = ""
    if _kill:
        kill_str = "_kill"
    new_df.to_excel("output" + kill_str + ".xlsx", index=False)


def output_by_zone(li, new_taxonomy: pd.DataFrame, killers, sort=False, _kill=False):
    species = []
    df_by_zones = dict()
    for i, df in enumerate(li):
        zone = get_df_zone(df, killers)
        if not df_by_zones.keys().__contains__(zone):
            df_by_zones[zone] = []
        df_by_zones[zone].append(df)
    for zone in df_by_zones.keys():
        new_df = pd.DataFrame()
        species = []
        for df in df_by_zones[zone]:
            species_ = get_species(df, new_taxonomy)
            for specie in species_:
                if species.count(specie) == 0:
                    species.append(specie)
        new_df["Species"] = species

        for i, df in enumerate(df_by_zones[zone]):
            new_df = get_data(species, df, new_df, killers, new_taxonomy, _kill)
        if sort:
            new_df = new_df.sort_values(by=["Species"])
        new_df.to_excel("output_" + zone + ".xlsx", index=False)
        print("output_" + zone + ".xlsx done")

    pass


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
    killers_df = pd.read_csv("killer_species.csv")
    killers = dict()
    new_taxonomy = pd.read_csv("new_taxonomy.csv")

    for index, row in killers_df.iterrows():
        if not killers.keys().__contains__(row["zone"]):
            killers[row["zone"]] = []
        killers[row["zone"]].append(row["specie"])
    species = []

    # for i, df in enumerate(li):
    #     if i > 99:
    #         break
    #     species_ = get_species(df, new_taxonomy)
    #     for specie in species_:
    #         if species.count(specie) == 0:
    #             species.append(specie)

    # output_all(li, species, new_taxonomy, killers, True)
    # print("output_all done with killers")
    # output_all(li, species, new_taxonomy, killers, False)
    # print("output_all done without killers")
    output_by_zone(li, new_taxonomy, killers, False)
    print("output_by_zone done ")


main()
