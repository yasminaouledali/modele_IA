import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import joblib


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

#df_encoded.to_csv("test.csv")

print(print(df_encoded.values))
X = np.array(df_encoded.values)

# Number of neighbors to find
k = 3
# Initialize the NearestNeighbors model with the desired number of neighbors
nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(X)

# Save the model to a file
model_filename = 'models/nearest_neighbors_model.pkl'
joblib.dump(nbrs, model_filename)
print(f"Model saved to {model_filename}")
experience = 6
location = "tunisie"
languages = ['français']
skills = ['django']
input_json['experience'] = experience

if location in input_json:
    input_json[location] = 1

for l in languages:
    if l in input_json:
        input_json[l] = 1
for skill in skills:
    if skill in input_json:
        input_json[skill] = 3

input_list = list(input_json.values())
input_list = np.array([input_list])

# Find the k nearest neighbors to the given cv
distances, indices = nbrs.kneighbors(input_list)

# Get ids of cv
ids_cv = [ids_cv_json[i] for i in list(indices[0])]

# Retrieve JSON data from the file
with open("resume_data.json", "r") as file:
    data = json.load(file)

# Display all similar cv
for item in data:
    if item.get('user').get('id') in ids_cv:
        print(item)

similar_data_points = X[indices][0]
print("Similar data cvs:")
print(similar_data_points)

# Get the similar data cvs
similar_data_cvs = X[indices][0]

# Plot the data points and the query point
plt.scatter(X[:, 0], X[:, 1], color='blue', label='Data cvs')
plt.scatter(input_list[:, 0], input_list[:, 1], color='red', label='Query cvs')
plt.scatter(similar_data_cvs[:, 0], similar_data_cvs[:, 1], color='green', label='Nearest neighbors')

# Plot lines between the query point and its nearest neighbors
for similar_point in similar_data_cvs:
    plt.plot([input_list[0, 0], similar_point[0]], [input_list[0, 1], similar_point[1]], 'k--')

plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('Nearest Neighbors')
plt.legend()
plt.show()

# Evaluation
print("Distances to nearest neighbors:")
print(distances)




