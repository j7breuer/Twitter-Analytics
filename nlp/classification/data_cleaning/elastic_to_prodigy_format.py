
import json
from csv import DictReader

json_obj = {}
with open('input.csv', 'r') as read_csv:
    csv_reader = DictReader(read_csv)
    for row in csv_reader:
        oupt_dict = {"text": row["text"]}
        with open('oupt.json', 'w') as oupt_json:
            json.dump(oupt_dict, oupt_json, indent = 4, ensure_ascii = False)
