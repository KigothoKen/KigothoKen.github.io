# Animal Classifier Web Application

A web application that accepts images of animals as input and identifies the animal in the image.

## Features

- Upload images via drag-and-drop or file selection
- Real-time image preview
- Animal classification with confidence scores
- Modern, responsive UI
- Supports various animal types

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: TensorFlow (MobileNetV2 pre-trained model)
- **UI Framework**: Bootstrap 5

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure you have activated the virtual environment
2. Run the Flask application:
   ```
   python animal_classifier.py
   ```
3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## How It Works

1. The web application uses a pre-trained MobileNetV2 model from TensorFlow
2. When you upload an image, it's sent to the server for processing
3. The image is resized to 224x224 pixels (required by MobileNetV2)
4. The model predicts the most likely objects in the image
5. The application filters the results to show only animal-related predictions
6. Results are displayed with labels and confidence scores

## Project Structure

```
animal_classifier/
│
├── animal_classifier.py    # Main Flask application
├── templates/              # HTML templates
│   └── index.html          # Main page template
├── uploads/                # Directory for uploaded images (created automatically)
├── venv/                   # Virtual environment
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Known Limitations

- The model is trained on ImageNet, which has a limited set of animal classes
- Works best with clear, well-lit images of common animals
- May not accurately identify obscure animal species

## Future Improvements

- Implement a specialized animal classification model for better accuracy
- Add detailed information about identified animals
- Add support for uploading multiple images
- Add an image gallery of previous classifications 