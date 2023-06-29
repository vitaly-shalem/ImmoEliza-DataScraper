import pandas as pd
import json
from pathlib import Path

path_to_open = Path.cwd() / "data" / "properties_ids_data.json"

with open(path_to_open, "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame.from_dict(data, orient='index')
print(df)

path_to_save = Path.cwd() / "data" / "data.csv"

df.to_csv(path_to_save)


