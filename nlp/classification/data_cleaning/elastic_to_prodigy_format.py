
import json
import pandas as pd
import emoji
import re

emoticon_string = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth      
      |
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
    )"""

def give_emoji_free_text(text): 
    return emoji.get_emoji_regexp().sub(r'', text)

def clean_tweet(text):
    #text = " ".join(re.sub(r"((https?://)?\w+(\.\w+)+(/\w+)*(/\w+\.\w+)?(\?[\w%&=.]*)*(?=[^\w.?&%=]))|((?<!\w)@[\w+]{1,15}\b)", "", text).split())
    #text = " ".join(re.sub(r"((https?://)?\w+(\.\w+)+(/\w+)*(/\w+\.\w+)?(\?[\w%&=.]*)*(?=[^\w.?&%=]))", "", text).split())
    text = give_emoji_free_text(text)
    text = re.sub(emoticon_string, '', text)
    text = re.sub(r"(http\S+)|(www\S+)", "", text)
    text = ''.join(x for x in text if x not in emoji.UNICODE_EMOJI)
    text = text.replace("#", "").replace("_", " ").replace("@", "").strip()
    return text

if __name__ in "__main__":
    df = pd.read_csv("../data/inpt/tweets_filtered.csv", encoding = "utf-8")
    oupt_list = []
    for i in df['text']:
        if not i.startswith("RT"):
            i = clean_tweet(i)
            if i:
                oupt_dict = {'text': i}
                oupt_list.append(oupt_dict)
    with open("../data/oupt/oupt_tweets_filtered.jsonl", 'w', encoding='utf-8') as f:
        for item in oupt_list:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")