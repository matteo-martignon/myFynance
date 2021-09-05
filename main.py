import os
import pandas as pd
from datetime import datetime

now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
directory = "C:/Users/matte/Projects/myFynance/"

def tipologia_matte(x):

    if x in (250, -250, 500, -500, 250.6, -250.6, 500.6, -500.6):
        return "M"
    elif x == -100:
        return "A"
    elif x < 0:
        return "C"
    else:
        return "R"


def tipologia_andre(x):

    if x in (-100, -50):
        return "A"
    elif x < 0:
        return "C"
    else:
        return "R"


def append_data_to_original_matte(df, apply=True,
                                  source="data/dataMatte.csv",
                                  backup=f"data/storico/full/matte/dataMatte_{now}.csv"):

    data_or = pd.read_csv(directory + source, sep=";")
    print(f"\n''append_data_to_original_matte'':\t\tloaded {source}")

    data_f = pd.concat([data_or, df])
    assert data_or.shape[0] + df.shape[0] == data_f.shape[0], "Data leakage"
    print(f"''append_data_to_original_matte'':\t\tappended data to {source}")

    if apply:
        os.rename(directory + source, directory + backup)
        print(f"\n''append_data_to_original_matte'':\t\t>>>>>>File {source} moved to {backup}")
        data_f.to_csv(directory + source, index=False, sep=";")
        print(f"\n''append_data_to_original_matte'':\t\t>>>>>>NEW data written in new file {source}")
    else:
        print(f"\n''append_data_to_original_matte'':\t\tTEST>>>>>>File {source} moved to {backup}")
        print(f"\n''append_data_to_original_matte'':\t\tTEST>>>>>>NEW data written in new file {source}")

    return


def append_data_to_original_andre(df, apply=True,
                                  source="data/dataAndre.csv",
                                  backup=f"data/storico/full/andre/dataAndre_{now}.csv"):

    data_or = pd.read_csv(directory + source, sep=";")
    print(f"\n''append_data_to_original_andre'':\t\tloaded {source}")

    data_f = pd.concat([data_or, df])
    assert data_or.shape[0] + df.shape[0] == data_f.shape[0], "Data leakage"
    print(f"''append_data_to_original_andre'':\t\tappended data to {source}")

    if apply:
        os.rename(directory + source, directory + backup)
        print(f"\n''append_data_to_original_andre'':\t\t>>>>>>File {source} moved to {backup}")
        data_f.to_csv(directory + source, index=False, sep=";")
        print(f"\n''append_data_to_original_andre'':\t\t>>>>>>NEW data written in new file {source}")
    else:
        print(f"\n''append_data_to_original_andre'':\t\tTEST>>>>>>File {source} moved to {backup}")
        print(f"\n''append_data_to_original_andre'':\t\tTEST>>>>>>NEW data written in new file {source}")

    return


def process_file_matte(apply=True, move_new_files=True,
                       source="data/new_data/matte", backup="data/storico/new/matte"):

    columns = ['Data', 'Operazione', 'Dettagli', 'Conto o carta', 'Contabilizzazione',
       'Categoria ', 'Valuta', 'Importo', 'Spesa Comune']

    try:
        filename = os.listdir(directory + source)[0]
        print(f"\n''process_file_matte'':\t\tfounded {filename} in {source}")
    except IndexError:
        raise Exception(f"Nessun file in {directory + source}")

    df = pd.read_excel(f"{directory + source}/{filename}", header=19)
    print(f"\t\t{df.shape[0]} rows, {df.shape[1]} columns")

    df.columns = columns
    df["Tipologia"] = df["Importo"].apply(tipologia_matte)
    df["Agente"] = "M"

    print("''process_file_matte'':\t\tsomma ricavi: %.2f" % df[df['Tipologia'] == 'R']['Importo'].sum())
    print("''process_file_matte'':\t\tsomma costi: %.2f" % df[df['Tipologia'] == 'C']['Importo'].sum())
    print("''process_file_matte'':\t\tsomma accantonamenti: %.2f" % df[df['Tipologia'] == 'A']['Importo'].sum())
    print(f"''process_file_matte'':\t\trecord di spesa comune: {df['Spesa Comune'].value_counts()[0]}")
    print("''process_file_matte'':\t\tsomma importo spesa comune: %.2f" % df[df['Spesa Comune'] == 'Y']['Importo'].sum())

    append_data_to_original_matte(df, apply)

    if move_new_files:
        os.rename(f"{directory + source}/{filename}", f"{directory + backup}/{now}_{filename}")
        print(f"\n''process_file_matte'':\t\t>>>>>>file {filename} moved from {source} to {backup}")
    else:
        print(f"\n''process_file_matte'':\t\tTEST>>>>>>file {filename} moved from {source} to {backup}")

    print("''process_file_matte'':\t\tEND")

    return


def process_file_andre(apply=True, move_new_files=True,
                       source="data/new_data/andre", backup="data/storico/new/andre"):

    columns = ['Data Contabile', 'Data', 'Addebiti', 'Accrediti', 'Dettagli',
       'Spesa Comune', 'Categoria']

    try:
        filename = os.listdir(directory + source)[0]
        print(f"\n''process_file_matte'':\t\tfounded {filename} in {source}")
    except IndexError:
        raise Exception(f"Nessun file in {directory + source}")

    df = pd.read_excel(f"{directory + source}/{filename}", header=11)
    print(f"\t\t{df.shape[0]} rows, {df.shape[1]} columns")

    df.columns = columns
    df["Addebiti"] = pd.to_numeric(df["Addebiti"].fillna("0").apply(lambda x:
                                                                    x.replace(".", "").replace(",", ".")))
    df["Accrediti"] = pd.to_numeric(df["Accrediti"].fillna("0").apply(lambda x:
                                                                      x.replace(".", "").replace(",", ".")))
    df["Importo"] = df["Accrediti"] - df["Addebiti"]
    df.drop(columns=["Addebiti", "Accrediti", "Data Contabile"], inplace=True)
    df["Data"] = pd.to_datetime(df["Data"])
    df["Tipologia"] = df["Importo"].apply(tipologia_andre)

    print("''process_file_andre'':\t\tsomma ricavi: %.2f" % df[df['Tipologia'] == 'R']['Importo'].sum())
    print("''process_file_andre'':\t\tsomma costi: %.2f" % df[df['Tipologia'] == 'C']['Importo'].sum())
    print("''process_file_andre'':\t\tsomma accantonamenti: %.2f" % df[df['Tipologia'] == 'A']['Importo'].sum())
    print(f"''process_file_andre'':\t\trecord di spesa comune: {df['Spesa Comune'].value_counts()[0]}")
    print("''process_file_andre'':\t\tsomma importo spesa comune: %.2f" % df[df['Spesa Comune'] == 'Y']['Importo'].sum())

    append_data_to_original_andre(df, apply)

    if move_new_files:
        os.rename(f"{directory + source}/{filename}", f"{directory + backup}/{now}_{filename}")
        print(f"\n''process_file_andre'':\t\t>>>>>>file {filename} moved from {source} to {backup}")
    else:
        print(f"\n''process_file_andre'':\t\tTEST>>>>>>file {filename} moved from {source} to {backup}")

    print("''process_file_andre'':\t\tEND")

    return


def merge_files(apply=True, source_andre="dataAndre.csv",
                source_matte="dataAndre.csv", source_data="data/", file_merge="data.csv",
                backup_data="storico/full/merged/"):

    path_andre = directory + source_data + source_andre
    path_matte = directory + source_data + source_matte
    path_merge = directory + source_data + file_merge

    df_andre = pd.read_csv(path_andre, sep=";")
    print(f"\n''merge_files'':\t\tloaded {path_andre}")

    df_matte = pd.read_csv(path_matte, sep=";")
    print(f"''merge_files'':\t\tloaded {path_matte}")

    merge = pd.concat([df_matte, df_andre.drop(columns="ID_OPERAZIONE")])
    assert df_andre.shape[0] + df_matte.shape[0] == merge.shape[0], "Data leakage"
    print(f"''merge_files'':\t\tmerged {source_matte} and {source_andre}")

    if apply:
        os.rename(f"{path_merge}", f"{directory + source_data + backup_data}/{now}_{file_merge}")
        print(f"\n''merge_files'':\t\t>>>>>>file {path_merge} moved to {source_data + backup_data}")

        merge.to_csv(path_merge, sep=";", index=False)
        print(f"\n''merge_files'':\t\t>>>>>>NEW data written in new file "
              f"{source_data + backup_data}/{now}_{file_merge}")
    else:
        print(f"\n''merge_files'':\t\tTEST>>>>>>file {path_merge} moved to {source_data + backup_data}")
        print(f"\n''merge_files'':\t\tTEST>>>>>>NEW data written in new file "
              f"{source_data + backup_data + now}_{file_merge}")
    print("''merge_files'':\t\tEND")

    return


if __name__ == "__main__":
    # process_file_matte(apply=True, move_new_files=True)
    # process_file_andre(apply=True, move_new_files=True)
    process_file_matte(apply=True, move_new_files=False)
    process_file_andre(apply=True, move_new_files=False)
    merge_files(apply=True)
