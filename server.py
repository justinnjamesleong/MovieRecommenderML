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

access_key = "AKIAUUQTHWBQZO7K4DXL"
secret_key = "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"


# download the file
s3 = boto3.resource('s3', aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key)

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
    serve(app, host='0.0.0.0', port=5000)
