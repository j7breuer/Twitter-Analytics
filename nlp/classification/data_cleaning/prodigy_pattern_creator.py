
import json
import pandas as pd

if __name__ in "__main__":
    df = pd.read_csv("../data/inpt/tweet_classification_patterns.csv", encoding = "utf-8")
    oupt_list = []
    for index, row in df.iterrows():
        oupt_list.append({"label": row['label'], "pattern":[{"lower": row['text']}]})
    with open("../data/oupt/tweet_classification_patterns.jsonl", 'w', encoding='utf-8') as f:
        for item in oupt_list:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")