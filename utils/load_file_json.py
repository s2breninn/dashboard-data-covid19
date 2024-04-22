import json

def load_file_json(patth_file):
    data = json.load(open(patth_file, 'r'))
    return data