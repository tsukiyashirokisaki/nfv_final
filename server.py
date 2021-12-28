from flask import Flask
from flask import request
import string
import json
app = Flask(__name__)
def file_to_words(filename):
    """Read a file and return a sequence of (word, occurances) values.
    """
    STOP_WORDS = set([
            'a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if', 'in', 
            'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the', 'to', 'with',
            ])
    TR = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    output = []
    with open(filename, 'rt',encoding='iso-8859-1') as f:
        for line in f:
            if line.lstrip().startswith('..'): # Skip rst comment lines
                continue
            line = line.translate(TR) # Strip punctuation
            for word in line.split()[8:]:
                word = word.lower()
                if word.isalpha() and word not in STOP_WORDS:
                    output.append( (word, 1) )
    return output
def count_words(item):
    # print(item)
    """Convert the partitioned data for a word to a
    tuple containing the word and the number of occurances.
    """
    word, occurances = item
    return (word, sum(occurances))
map_func = file_to_words
reduce_func = count_words
@app.route("/map",methods=["POST"])
def map():
    paths = request.json["value"]
    return {"value":[map_func(ele) for ele in paths]}
@app.route("/reduce",methods=["POST"])
def reduce():
    data = request.json["value"]
    return {"value":[reduce_func(ele) for ele in data]}
@app.route("/test")
def test():
    return {"value":"test"}

if __name__ == "__main__":
    app.run()