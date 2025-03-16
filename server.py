from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

import chefff

app = Flask(__name__, static_folder="./dist/", static_url_path="/") 

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@app.route('/', methods=['GET'])
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/test', methods=['GET'])
def home1():
    return jsonify({"message": "SUCCESSFUL TEST"}), 200

# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return jsonify({"message": "STOP FAVICON"}), 200

@app.route('/create-file', methods=['POST', 'OPTIONS'])
def create_file():
    print("reached here")
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400


        # print(data)
        filter_option = data.get("filter_option")
        budget = data.get("budget")
        serving = data.get("servings")
        diet_requirements = data.get("diet_requirements", [])
        food_allergies = data.get("food_allergies")


        result = chefff.generateRecipes(
            cuisine=filter_option,
            allergies=food_allergies, 
            numServings=serving, 
            totalBudget=budget, 
            dietaryReqs=diet_requirements, 
            remarks=""
        )

        return jsonify({"message": f"{result}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable or default to 5000
    app.run(host="0.0.0.0", port=port)
