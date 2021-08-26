
import json
import pandas as pd
import argparse

#------------#
# Parse Args #
#------------#
arg_parser = argparse.ArgumentParser(description="Data arguments")
arg_parser.add_argument(
    "--inpt",
    help = "Filename of input csv located in inpt folder with extension"
)
arg_parser.add_argument(
    "--oupt",
    help = "Name of output JSONL file located in the oupt folder"
)
args = arg_parser.parse_args()

# Run
if __name__ in "__main__":

    # Load in CSV of tweet classification patterns for prodigy's text classification learning recipe
    df = pd.read_csv(f"../data/inpt/{args.inpt}", encoding = "utf-8")
    oupt_list = []

    # Loop through df
    for index, row in df.iterrows():

        # Create dict to add to list
        oupt_list.append({"label": row['label'], "pattern":[{"lower": row['text']}]})

    # Save as JSONL file
    with open(f"../data/oupt/{args.oupt}", 'w', encoding='utf-8') as f:
        for item in oupt_list:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")