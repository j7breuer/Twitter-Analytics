
import sys
import argparse
import pandas as pd
import spacy
import emoji
import re
import operator

#------------#
# Parse Args #
#------------#
arg_parser = argparse.ArgumentParser(description="Data arguments")
arg_parser.add_argument(
    "--modelname",
    help = "Subdirectory name in ../data/oupt directory that contains the model output from the train_classification bash script"
)
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
    text = text.replace("#", "").replace("_", " ").replace("@", "").strip()
    return text

# Load spacy model
nlp = spacy.load(f"../data/oupt/{args.modelname}")

# Run
if __name__ in "__main__":
    
    # Load spacy model
    df = pd.read_csv(f"../data/inpt/{args.inpt}", encoding = "utf-8")
    # Create list to append model classifications to
    class_list = []

    # Loop through data frame and classify text and compare to annotations
    for index, row in df.iterrows():
        # Clean tweet
        text = clean_tweet(row["text"])
        # Get classification
        doc = nlp(text)
        doc = doc.cats
        # Extract label with highest score
        cur_class = max(doc.items(), key = operator.itemgetter(1))[0]
        # Assign value for review
        if cur_class == row['annotation']:
            class_list.append("correct")
        else:
            class_list.append("misclassifcation")

    # Append results
    df["results"] = class_list
    # Calculate accuracy rate
    accuracy_rate = len([x for x in class_list if x == "correct"]) / len(class_list)
    # Write to stdout
    sys.stdout.write(f"\nModel: {args.modelname}\nAnnotation Count: {str(len(df))}\nAccuracy Rate: {str(accuracy_rate)}\n")

    # Save CSV
    df.to_csv(f"../data/oupt/{args.oupt}", encoding = "utf-8", index = False)