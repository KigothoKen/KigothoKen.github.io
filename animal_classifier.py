import os
import numpy as np
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load pre-trained MobileNetV2 model
model = MobileNetV2(weights='imagenet')

def predict_animal(file_stream):
    """Process the uploaded image and return animal prediction"""
    # Open image from file stream
    img = Image.open(file_stream)
    
    # Resize to required input size for MobileNetV2
    img = img.resize((224, 224))
    
    # Convert to array and preprocess
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    
    # Make prediction
    predictions = model.predict(img_array)
    decoded = decode_predictions(predictions, top=3)[0]
    
    results = []
    for i, (imagenet_id, label, score) in enumerate(decoded):
        # Filter for animal classes only
        animal_keywords = ['animal', 'bird', 'cat', 'dog', 'fish', 'insect', 
                          'reptile', 'amphibian', 'mammal', 'beast', 'creature']
                          
        is_animal = any(keyword in label.lower() for keyword in animal_keywords) or i == 0
        
        if is_animal:
            results.append({
                'label': label.replace('_', ' ').capitalize(),
                'confidence': float(score) * 100
            })
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        try:
            # Process the image
            results = predict_animal(file.stream)
            return jsonify({
                'success': True,
                'predictions': results
            })
        except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 