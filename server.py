from flask import Flask
from flask import request
import string
import json
from mapreduce import file_to_words,count_words

app = Flask(__name__)
map_func = file_to_words
reduce_func = count_words
@app.route("/map",methods=["POST"])
def map():
    paths = request.json["value"]
    return {"value":[map_func(ele) for ele in paths]}
@app.route("/reduce",methods=["POST"])
def reduce():
    data = request.json["value"]
    return {"value":reduce_func(data)}
@app.route("/test")
def test():
    return {"value":"test"}

if __name__ == "__main__":
    app.run()