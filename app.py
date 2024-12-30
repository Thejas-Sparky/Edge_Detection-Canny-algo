# from flask import Flask, request, jsonify
# from flask_cors import CORS  # Import CORS
# import cv2
# import numpy as np
# import os
# from werkzeug.utils import secure_filename

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Define upload and output folders
# UPLOAD_FOLDER = 'static/uploads/'
# OUTPUT_FOLDER = 'static/output/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# # Allowed file extensions
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# # Check if file extension is allowed
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # Route to handle image upload and Canny edge detection
# @app.route('/upload', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
#     file = request.files['file']
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(upload_path)

#         # Read the image using OpenCV
#         image = cv2.imread(upload_path)

#         # Convert to grayscale
#         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#         # Apply Canny edge detection
#         edges = cv2.Canny(gray_image, 100, 200)

#         # Save the edge-detected image
#         output_filename = f"edges_{filename}"
#         output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
#         cv2.imwrite(output_path, edges)

#         # Return the URL of the processed image
#         return jsonify({"edge_image": f"/static/output/{output_filename}"}), 200
#     else:
#         return jsonify({"error": "Invalid file format"}), 400

# if __name__ == '__main__':
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#     os.makedirs(OUTPUT_FOLDER, exist_ok=True)
#     app.run(debug=True)


import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Define upload and output folders
UPLOAD_FOLDER = 'static/uploads/'
OUTPUT_FOLDER = 'static/output/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to handle image upload and Canny edge detection
@app.route('/upload', methods=['POST'])
def upload_image():
    print("Received request to upload image.")  # Debugging log
    if 'file' not in request.files:
        print("No file found in request.")  # Debugging log
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Saving file to {upload_path}")  # Debugging log
        file.save(upload_path)

        # Read the image using OpenCV
        image = cv2.imread(upload_path)
        if image is None:
            print("Failed to load image.")  # Debugging log
            return jsonify({"error": "Failed to load image"}), 500

        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(gray_image, 100, 200)

        # Save the edge-detected image
        output_filename = f"edges_{filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        print(f"Saving edge-detected image to {output_path}")  # Debugging log
        cv2.imwrite(output_path, edges)

        # Return the URL of the processed image
        return jsonify({"edge_image": f"/static/output/{output_filename}"}), 200
    else:
        print("Invalid file format or no file uploaded.")  # Debugging log
        return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)
