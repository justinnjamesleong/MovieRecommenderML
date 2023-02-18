import pickle
import requests
from flask import Flask, request, jsonify
from waitress import serve
from movierecmodel import recommend
from flask_cors import CORS


# Download the cosine similarity matrix using requests
export_file_url = 'https://drive.google.com/uc?id=1qNYXLL7jlrMx8AFv2CD71G89l7CqNTnl'
response = requests.get(export_file_url)
cosine_sim = pickle.loads(response.content)

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
