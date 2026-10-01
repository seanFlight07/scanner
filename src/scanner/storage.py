import json

from datetime import datetime
from pathlib import Path

def file_path():
    data_dir = Path(__file__).resolve().parents[2] / "data"
    return data_dir

def to_json(log, file_name,file_path):
    json_log = json.dumps(log)
    with open(file_path / file_name, "w") as f:
        f.write(json_log)

def date_time_filename():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M")
    str_datetime = str(current_datetime)
    file_name = str_datetime + ".json"
    return file_name

def load_json(file_path):
    now = datetime.now()
    files = list(file_path.glob("*.json"))
    previous_files = [] 
    for file in files:
        file_datetime = datetime.strptime(
            file.stem,
            "%Y-%m-%d %H-%M"
            )

        if file_datetime < now:
            previous_files.append((file_datetime,file))
    latest_time, latest_file = max(previous_files, key=lambda item: item[0])

    with open(latest_file, "r") as f:
        print("completed")
        return json.load(f)
