from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your Roblox API endpoint (if hosting externally)
DATASTORE_URL = "https://your-roblox-server.com/updateRank"

@app.route('/updateRank', methods=['POST'])
def update_rank():
    data = request.json
    user_id = data.get("user_id")
    new_rank = data.get("new_rank")

    if not user_id or not new_rank:
        return jsonify({"status": "error", "message": "Missing user ID or rank"}), 400

    # Forward request to Roblox DataStore API
    response = requests.post(DATASTORE_URL, json=data)

    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Rank updated!"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to update rank"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
