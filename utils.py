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
    data_store = f"data/storico/dataMatte_{now}.csv"
    
    data_or = pd.read_csv(data_orig, sep=";")

    data_f = pd.concat([data_or, df])
    
    assert data_or.shape[0] + df.shape[0] == data_f.shape[0], "Data leakage"

    if not test:
        os.rename(data_orig, data_store)
        data_f.to_csv(data_orig, index=False)
    
    print(f"\n>>>>>>File {data_orig} moved to {data_store}")
    
    return


def process_file_matte(test=True):
    
    columns = ['Data', 'Operazione', 'Dettagli', 'Conto o carta', 'Contabilizzazione',
       'Categoria ', 'Valuta', 'Importo', 'Spesa Comune']
    
    source = "data/new_data/matte"
    destination = "data/storico/matte"
    
    filename = os.listdir(source)[0]
    
    df = pd.read_excel(f"{source}/{filename}", header=19)
    
    df.columns = columns
    df["Tipologia"] = df["Importo"].apply(tipologia_matte)
    df["Agente"] = "M"
    
    append_data_to_original_matte(df, test)

    if not test:
        os.rename(f"{source}/{filename}", f"{destination}/{filename}")

    print(f"\n>>>>>>File {filename} moved from {source} to {destination}")
    return


def append_data_to_original_andre(df):
    
    data_orig = "data/dataAndre.csv"
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    data_store = f"data/storico/dataAndre_{now}.csv"
    
    data_or = pd.read_csv(data_orig)

    data_f = pd.concat([data_or, df])
    
    assert data_or.shape[0] + df.shape[0] == data_f.shape[0], "Data leakage"
    
    os.rename(data_orig, data_store)
    
    data_f.to_csv(data_orig, index=False)
    
    print(f"File {data_orig} moved to {data_store}")
    
    return


def process_file_andre():
    
    columns = ['Data Contabile', 'Data', 'Addebiti', 'Accrediti', 'Dettagli',
       'Spesa Comune', 'Categoria']
    source = "data/new_data/andre"
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    destination = "data/storico/andre"

    filename = os.listdir(source)[0]

    df = pd.read_excel(f"{source}/{filename}", header=11)
    df.columns = columns
    df["Addebiti"] = pd.to_numeric(df["Addebiti"].fillna("0").apply(lambda x: x.replace(".", "").replace(",", ".")))
    df["Accrediti"] = pd.to_numeric(df["Accrediti"].fillna("0").apply(lambda x: x.replace(".", "").replace(",", ".")))
    df["Importo"] = df["Accrediti"] - df["Addebiti"]
    df.drop(columns=["Addebiti", "Accrediti", "Data Contabile"], inplace=True)
    df["Data"] = pd.to_datetime(df["Data"])
    df["Tipologia"] = df["Importo"].apply(tipologia_andre)
    
    append_data_to_original_andre(df)
    
    os.rename(f"{source}/{filename}", f"{destination}/{now}_{filename}")
    print(f"File {filename} moved from {source} to {destination}")
    
    return


if __name__ == "__main__":
    process_file_matte(test=True)
    process_file_andre()
