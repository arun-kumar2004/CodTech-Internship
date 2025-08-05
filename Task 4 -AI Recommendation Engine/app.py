from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendation import get_recommendations

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title', '')
    recommendations = get_recommendations(title)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
