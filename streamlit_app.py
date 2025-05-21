import streamlit as st
import numpy as np
import os
from PIL import Image
import cv2
import urllib.request
import zipfile
import io

st.set_page_config(
    page_title="PigDoc - AI-Powered Pig Disease Detection",
    page_icon="🐷",
    layout="centered"
)

# Define disease classes
DISEASE_CLASSES = [
    "Healthy",
    "Respiratory Disease",
    "Skin Disease",
    "Gastrointestinal Disease"
]

@st.cache_resource
def initialize_tensorflow():
    try:
        # Disable GPU
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        import tensorflow as tf
        return tf
    except Exception as e:
        st.error(f"Error initializing TensorFlow: {str(e)}")
        return None

@st.cache_resource
def download_model():
    try:
        model_path = "detect.tflite"
        if not os.path.exists(model_path):
            st.info("Downloading model file... Please wait.")
            # Download the zip file
            zip_url = "https://github.com/KigothoKen/PigDoc/releases/download/v1.0/model.zip"
            response = urllib.request.urlopen(zip_url)
            zip_data = io.BytesIO(response.read())
            
            # Extract the model file
            with zipfile.ZipFile(zip_data) as zip_ref:
                zip_ref.extract("detect.tflite")
            
            st.success("Model downloaded and extracted successfully!")
        return model_path
    except Exception as e:
        st.error(f"Error downloading model: {str(e)}")
        return None

def preprocess_image(image, target_size=(224, 224)):
    # Convert PIL Image to numpy array
    img = np.array(image)
    
    # Resize image
    img = cv2.resize(img, target_size)
    
    # Convert to RGB if needed
    if len(img.shape) == 2:  # If grayscale
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif img.shape[2] == 4:  # If RGBA
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    
    # Normalize pixel values
    img = img.astype(np.float32) / 255.0
    
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    return img

# Initialize TensorFlow
tf = initialize_tensorflow()
if tf is None:
    st.error("Failed to initialize TensorFlow. Please try refreshing the page.")
    st.stop()

# Load the TFLite model
@st.cache_resource
def load_model():
    try:
        model_path = download_model()
        if model_path is None or not os.path.exists(model_path):
            st.error("Model file not available")
            return None
        
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def predict_disease(interpreter, image):
    if interpreter is None:
        raise ValueError("Model not loaded properly")
        
    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Preprocess the image
    processed_image = preprocess_image(image, target_size=(input_details[0]['shape'][1], input_details[0]['shape'][2]))
    
    try:
        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], processed_image)
        
        # Run inference
        interpreter.invoke()
        
        # Get prediction results
        output_data = interpreter.get_tensor(output_details[0]['index'])
        prediction = np.argmax(output_data)
        confidence = float(output_data[0][prediction])
        
        return DISEASE_CLASSES[prediction], confidence
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
        return None, None

# UI Elements
st.title("🐷 PigDoc")
st.subheader("AI-Powered Pig Disease Detection System")

st.markdown("""
This application uses machine learning to detect potential health issues in pigs through image analysis.
Simply upload an image of a pig, and the system will analyze it for possible health conditions.
""")

# Load model
interpreter = load_model()

if interpreter is None:
    st.error("""
    Error: Could not load the model. Please check if:
    1. You have a stable internet connection
    2. The model file is not corrupted
    3. You have sufficient memory
    """)
    st.stop()

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Add a spinner during prediction
        with st.spinner("Analyzing image..."):
            # Get prediction
            disease, confidence = predict_disease(interpreter, image)
            
            if disease is not None and confidence is not None:
                # Display results
                st.success("Analysis Complete!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Detected Condition", disease)
                with col2:
                    st.metric("Confidence", f"{confidence*100:.2f}%")
                
                # Additional information based on condition
                st.subheader("Recommendations")
                if disease == "Healthy":
                    st.info("The pig appears to be in good health. Continue with regular care and monitoring.")
                else:
                    st.warning(f"""
                    Potential {disease} detected. Recommended actions:
                    - Consult with a veterinarian
                    - Isolate the affected animal if necessary
                    - Monitor temperature and eating habits
                    - Document symptoms and changes
                    """)
            
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        
st.markdown("---")
st.markdown("""
### Usage Tips
- Ensure the image is clear and well-lit
- The pig should be clearly visible in the image
- Multiple pigs in one image may affect accuracy
""")

# Add GitHub link
st.sidebar.markdown("### Project Information")
st.sidebar.markdown("[View on GitHub](https://github.com/KigothoKen/PigDoc)") 