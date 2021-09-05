import os
import pandas as pd
from datetime import datetime


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


def append_data_to_original_matte(df, test=True):

    data_orig = "data/dataMatte.csv"
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    data_store = f"data/storico/full/matte/dataMatte_{now}.csv"

    data_or = pd.read_csv(data_orig, sep=";")
    print(f"\n''append_data_to_original_matte'':\t\tloaded {data_orig}")

    data_f = pd.concat([data_or, df])
    assert data_or.shape[0] + df.shape[0] == data_f.shape[0], "Data leakage"
    print(f"''append_data_to_original_matte'':\t\tappended data to {data_orig}")

    if not test:
        os.rename(data_orig, data_store)
        print(f"\n''append_data_to_original_matte'':\t\t>>>>>>File {data_orig} moved to {data_store}")
        data_f.to_csv(data_orig, index=False, sep=";")
        print(f"\n''append_data_to_original_matte'':\t\t>>>>>>NEW data written in new file {data_orig}")
    else:
        print(f"\n''append_data_to_original_matte'':\t\tTEST>>>>>>File {data_orig} moved to {data_store}")
        print(f"\n''append_data_to_original_matte'':\t\tTEST>>>>>>NEW data written in new file {data_orig}")

    return


def append_data_to_original_andre(df, test=True):

    data_orig = "data/dataAndre.csv"
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    data_store = f"data/storico/full/andre/dataAndre_{now}.csv"

    data_or = pd.read_csv(data_orig, sep=";")
    print(f"\n''append_data_to_original_andre'':\t\tloaded {data_orig}")

    data_f = pd.concat([data_or, df])
    assert data_or.shape[0] + df.shape[0] == data_f.shape[0], "Data leakage"
    print(f"''append_data_to_original_andre'':\t\tappended data to {data_orig}")

    if not test:
        os.rename(data_orig, data_store)
        print(f"\n''append_data_to_original_andre'':\t\t>>>>>>File {data_orig} moved to {data_store}")
        data_f.to_csv(data_orig, index=False, sep=";")
        print(f"\n''append_data_to_original_andre'':\t\t>>>>>>NEW data written in new file {data_orig}")
    else:
        print(f"\n''append_data_to_original_andre'':\t\tTEST>>>>>>File {data_orig} moved to {data_store}")
        print(f"\n''append_data_to_original_andre'':\t\tTEST>>>>>>NEW data written in new file {data_orig}")

    return


def process_file_matte(test=True):

    columns = ['Data', 'Operazione', 'Dettagli', 'Conto o carta', 'Contabilizzazione',
       'Categoria ', 'Valuta', 'Importo', 'Spesa Comune']

    source = "data/new_data/matte"
    destination = "data/storico/new/matte"
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    filename = os.listdir(source)[0]
    print(f"\n''process_file_matte'':\t\tfounded {filename} in {source}")

    df = pd.read_excel(f"{source}/{filename}", header=19)
    print(f"\t\t{df.shape[0]} rows, {df.shape[1]} columns")

    df.columns = columns
    df["Tipologia"] = df["Importo"].apply(tipologia_matte)
    df["Agente"] = "M"

    print("''process_file_matte'':\t\tsomma ricavi: %.2f" % df[df['Tipologia'] == 'R']['Importo'].sum())
    print("''process_file_matte'':\t\tsomma costi: %.2f" % df[df['Tipologia'] == 'C']['Importo'].sum())
    print("''process_file_matte'':\t\tsomma accantonamenti: %.2f" % df[df['Tipologia'] == 'A']['Importo'].sum())
    print(f"''process_file_matte'':\t\trecord di spesa comune: {df['Spesa Comune'].value_counts()[0]}")
    print("''process_file_matte'':\t\tsomma importo spesa comune: %.2f" % df[df['Spesa Comune'] == 'Y']['Importo'].sum())

    append_data_to_original_matte(df, test)

    if not test:
        os.rename(f"{source}/{filename}", f"{destination}/{now}_{filename}")
        print(f"\n''process_file_matte'':\t\t>>>>>>file {filename} moved from {source} to {destination}")
    else:
        print(f"\n''process_file_matte'':\t\tTEST>>>>>>file {filename} moved from {source} to {destination}")

    print("''process_file_matte'':\t\tEND")

    return


def process_file_andre(test=True):

    columns = ['Data Contabile', 'Data', 'Addebiti', 'Accrediti', 'Dettagli',
       'Spesa Comune', 'Categoria']
    source = "data/new_data/andre"
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    destination = "data/storico/new/andre"

    filename = os.listdir(source)[0]
    print(f"\n''process_file_andre'':\t\tfounded {filename} in {source}")

    df = pd.read_excel(f"{source}/{filename}", header=11)
    print(f"\t\t{df.shape[0]} rows, {df.shape[1]} columns")

    df.columns = columns
    df["Addebiti"] = pd.to_numeric(df["Addebiti"].fillna("0").apply(lambda x: x.replace(".", "").replace(",", ".")))
    df["Accrediti"] = pd.to_numeric(df["Accrediti"].fillna("0").apply(lambda x: x.replace(".", "").replace(",", ".")))
    df["Importo"] = df["Accrediti"] - df["Addebiti"]
    df.drop(columns=["Addebiti", "Accrediti", "Data Contabile"], inplace=True)
    df["Data"] = pd.to_datetime(df["Data"])
    df["Tipologia"] = df["Importo"].apply(tipologia_andre)

    print("''process_file_andre'':\t\tsomma ricavi: %.2f" % df[df['Tipologia'] == 'R']['Importo'].sum())
    print("''process_file_andre'':\t\tsomma costi: %.2f" % df[df['Tipologia'] == 'C']['Importo'].sum())
    print("''process_file_andre'':\t\tsomma accantonamenti: %.2f" % df[df['Tipologia'] == 'A']['Importo'].sum())
    print(f"''process_file_andre'':\t\trecord di spesa comune: {df['Spesa Comune'].value_counts()[0]}")
    print("''process_file_andre'':\t\tsomma importo spesa comune: %.2f" % df[df['Spesa Comune'] == 'Y']['Importo'].sum())

    append_data_to_original_andre(df, test)

    if not test:
        os.rename(f"{source}/{filename}", f"{destination}/{now}_{filename}")
        print(f"\n''process_file_andre'':\t\t>>>>>>file {filename} moved from {source} to {destination}")
    else:
        print(f"\n''process_file_andre'':\t\tTEST>>>>>>file {filename} moved from {source} to {destination}")

    print("''process_file_andre'':\t\tEND")

    return


if __name__ == "__main__":
    process_file_matte(test=True)
    process_file_andre(test=True)
    # process_file_matte(test=False)
    # process_file_andre(test=False)
