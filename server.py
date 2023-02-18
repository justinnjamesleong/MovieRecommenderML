import pickle
from flask import Flask, request, jsonify
from waitress import serve
from movierecmodel import recommend
from flask_cors import CORS
import boto3

# create an S3 resource
s3 = boto3.resource('s3')

# specify the S3 bucket and file to download
bucket_name = 'cosinesimilarityformovies'
file_name = 'cosine_sim.pickle'

# download the file
s3.Bucket(bucket_name).download_file(file_name, file_name)

# Load the cosine similarity matrix using pickle
with open('cosine_sim.pickle', 'rb') as f:
    cosine_sim = pickle.load(f)

app = Flask(__name__)
CORS(app)


@app.route('/recommend', methods=['POST'])
def make_recommendation():
    # Get the request data
    data = request.get_json()
    title = data['title']

    # Make the recommendation
    results = recommend(title, cosine_sim)

    # Return the result as a JSON response
    response = {'resultsRec': results}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
