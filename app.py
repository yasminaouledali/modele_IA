# -*- coding: utf-8 -*
from flask_cors import CORS
from flask import Flask, jsonify, request
import joblib
import json
import pandas as pd
import numpy as np



# Load the model from the file
model_filename = 'models/nearest_neighbors_model.pkl'
loaded_model = joblib.load(model_filename)
print("Model loaded successfully")

# Read the CSV file into a DataFrame
df = pd.read_csv('resume.csv',encoding='ISO-8859-1')
# Apply one-hot encoding on 'location' column
one_hot_encoded = pd.get_dummies(df['location'])
ids_cv_json = {i:value for i,value in enumerate(df['id'].tolist())}
df = df.drop(["id", "location"], axis=1)
# Concatenate the one-hot encoded DataFrame with the original DataFrame
df_encoded = pd.concat([df, one_hot_encoded], axis=1)
# Get head of csv
input_json = { key:0 for key in df_encoded.columns.tolist()}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response



@app.route('/similarity_search_cvs', methods=['GET'])
def similarity_search():
    data = request.data
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON data"}), 400
    experience = data.get("experience")
    location = data.get("location")
    languages = data.get("languages")
    skills = data.get("skills")
    input_json['experience'] = experience
    if location in input_json:
        input_json[location] = 1
    for l in languages:
        if l in input_json:
            input_json[l] = 1
    for item in skills:
        if item.get('skill') in input_json:
            input_json[item.get('skill')] = item.get('rating')
    input_list = list(input_json.values())
    input_list = np.array([input_list])
    # Find the k nearest neighbors to the given input data
    distances, indices = loaded_model.kneighbors(input_list)
    # Get ids of cv
    ids_cv = [ids_cv_json[i] for i in list(indices[0])]

    return jsonify(ids_cv)

if __name__ == '__main__':
     app.run(host="0.0.0.0", debug=True)