import pandas as pd
import json
from pathlib import Path
from find_duplicate import find_duplicate

def dict_to_csv():
    path_to_open = Path.cwd() / "data" / "properties_data.json"

    with open(path_to_open, "r", encoding="utf-8") as file:
        data = json.load(file)

    df = pd.DataFrame.from_dict(data, orient='index')
    print(df.head())

    path_to_save = Path.cwd() / "data" / "properties_data.csv"

    #data frame with duplicate data
    df_duplicate = find_duplicate(df)
    
    df.to_csv(path_to_save, index_label="id", encoding="utf-8")
