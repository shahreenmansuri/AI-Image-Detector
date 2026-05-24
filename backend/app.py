from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from model import detect_ai_image
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/detect', methods=['POST'])
def detect():

    # 1. check file exists
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']

    if image.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # 2. secure filename
    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    # 3. save file
    image.save(image_path)

    try:
        # 4. model prediction
        result = detect_ai_image(image_path)

        if not result or len(result) == 0:
            return jsonify({"error": "No prediction from model"}), 500

        top_result = result[0]

        response = {
            "label": top_result.get("label", "unknown"),
            "confidence": round(top_result.get("score", 0) * 100, 2)
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # 5. cleanup file (important)
        if os.path.exists(image_path):
            os.remove(image_path)

if __name__ == '__main__':
    app.run(debug=True)