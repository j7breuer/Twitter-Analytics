
import json
import pandas as pd
import emoji
import re
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

# Create string of emoji faces for regex pattern
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
    '''
    desc: function to remove emojis
    inpt:
        text [str]: string to clean
    oupt:
        [str]: cleaned string 
    '''
    return emoji.get_emoji_regexp().sub(r'', text)

def clean_tweet(text):
    '''
    desc: given text from tweet, clean and convert to format that can be analyzed
    inpt:
        text [str]: string from tweet to be cleaned
    oupt:
        text [str]: cleaned string
    
    '''
    text = give_emoji_free_text(text)
    text = re.sub(emoticon_string, '', text)
    text = re.sub(r"(http\S+)|(www\S+)", "", text)
    text = ''.join(x for x in text if x not in emoji.UNICODE_EMOJI)
    text = text.replace("#", "").replace("_", " ").strip()
    return text

# Run
if __name__ in "__main__":

    # Load in CSV from args
    df = pd.read_csv(f"../data/inpt/{args.inpt}", encoding = "utf-8")
    oupt_list = []

    # Loop through text field, remove RTs, clean tweet, append to list
    for i in df['text']:
        # Bypass retweets
        if not i.startswith("RT"):
            # Clean tweet up
            i = clean_tweet(i)
            # If tweet still exists, add to dict
            if i:
                oupt_dict = {'text': i}
                oupt_list.append(oupt_dict)
                
    # Save as JSONL file
    with open(f"../data/oupt/{args.oupt}.jsonl", 'w', encoding='utf-8') as f:
        # Loop through list and dump to jsonl file
        for item in oupt_list:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")