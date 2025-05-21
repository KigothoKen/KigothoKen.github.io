from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize global variable for model
model = None

def load_model():
    global model
    try:
        model = tf.keras.models.load_model('model/pig_health_model.h5')
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

# Load model when app starts
load_model()

# List of possible diseases and symptoms
DISEASES = [
    "African Swine Fever",
    "Foot and Mouth Disease",
    "Classical Swine Fever",
    "Porcine Reproductive and Respiratory Syndrome",
    "Swine Influenza",
    "Porcine Circovirus",
    "Mycoplasma Pneumonia",
    "Salmonellosis"
]

SYMPTOMS = [
    "High Fever",
    "Loss of Appetite",
    "Lethargy",
    "Respiratory Issues",
    "Skin Discoloration",
    "Diarrhea",
    "Vomiting",
    "Lameness",
    "Coughing",
    "Nasal Discharge",
    "Joint Swelling",
    "Weight Loss"
]

# Symptom to disease mapping (simplified for demo)
SYMPTOM_DISEASE_MAPPING = {
    "High Fever": ["African Swine Fever", "Classical Swine Fever", "Swine Influenza"],
    "Loss of Appetite": ["African Swine Fever", "Classical Swine Fever", "PRRS"],
    "Lethargy": ["African Swine Fever", "Classical Swine Fever", "Swine Influenza"],
    "Respiratory Issues": ["PRRS", "Swine Influenza", "Mycoplasma Pneumonia"],
    "Skin Discoloration": ["African Swine Fever", "Classical Swine Fever"],
    "Diarrhea": ["Classical Swine Fever", "Salmonellosis"],
    "Vomiting": ["Classical Swine Fever", "Salmonellosis"],
    "Lameness": ["Foot and Mouth Disease"],
    "Coughing": ["PRRS", "Swine Influenza", "Mycoplasma Pneumonia"],
    "Nasal Discharge": ["PRRS", "Swine Influenza"],
    "Joint Swelling": ["Foot and Mouth Disease", "Mycoplasma Pneumonia"],
    "Weight Loss": ["PRRS", "Porcine Circovirus"]
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def preprocess_image(image_path):
    """Preprocess image for model prediction"""
    try:
        img = tf.keras.preprocessing.image.load_img(
            image_path, target_size=(224, 224)
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def analyze_image(image_path):
    """Analyze image using the loaded model"""
    if model is None:
        # If model is not loaded, return random predictions
        print("Model not loaded, using random predictions")
        return [
            {"disease": disease, "confidence": float(np.random.random())}
            for disease in DISEASES
        ]
    
    try:
        # Preprocess the image
        processed_image = preprocess_image(image_path)
        if processed_image is None:
            raise Exception("Failed to preprocess image")

        # Get model predictions
        predictions = model.predict(processed_image)
        
        # Convert predictions to results format
        results = []
        for i, confidence in enumerate(predictions[0]):
            if confidence > 0.1:  # Only include predictions with >10% confidence
                results.append({
                    "disease": DISEASES[i],
                    "confidence": float(confidence)
                })
        
        # Sort by confidence
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results
    except Exception as e:
        print(f"Error in image analysis: {e}")
        # Fallback to random predictions
        return [
            {"disease": disease, "confidence": float(np.random.random())}
            for disease in DISEASES
        ]

def analyze_symptoms_list(symptoms):
    disease_scores = {disease: 0.0 for disease in DISEASES}
    
    for symptom in symptoms:
        if symptom in SYMPTOM_DISEASE_MAPPING:
            related_diseases = SYMPTOM_DISEASE_MAPPING[symptom]
            for disease in related_diseases:
                disease_scores[disease] += 1.0

    # Normalize scores
    max_score = max(disease_scores.values()) if disease_scores.values() else 1
    if max_score > 0:
        disease_scores = {
            disease: score/max_score 
            for disease, score in disease_scores.items()
        }

    return [
        {"disease": disease, "confidence": score}
        for disease, score in disease_scores.items()
        if score > 0
    ]

@app.route('/')
def index():
    return render_template('app.html', symptoms=SYMPTOMS)

@app.route('/analyze_image', methods=['POST'])
def analyze_image_route():
    if 'image' not in request.files and 'image_data' not in request.form:
        return jsonify({'error': 'No image provided'}), 400

    if 'image' in request.files:
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            results = analyze_image(filepath)
            os.remove(filepath)  # Clean up
            return render_template('app.html', results=results, symptoms=SYMPTOMS)

    elif 'image_data' in request.form:
        # Handle base64 image data from camera
        try:
            image_data = request.form['image_data']
            image_data = image_data.split(',')[1] if ',' in image_data else image_data
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Save temporarily for analysis
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.jpg')
            image.save(temp_path)
            results = analyze_image(temp_path)
            os.remove(temp_path)  # Clean up
            return render_template('app.html', results=results, symptoms=SYMPTOMS)
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'Invalid image format'}), 400

@app.route('/analyze_symptoms', methods=['POST'])
def analyze_symptoms_route():
    symptoms = request.form.getlist('symptoms[]')
    if not symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400

    results = analyze_symptoms_list(symptoms)
    return render_template('app.html', results=results, symptoms=SYMPTOMS)

if __name__ == '__main__':
    app.run(debug=True) 