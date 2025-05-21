# Pig Health Diagnostic Tool 🐷

An AI-powered application for diagnosing pig health conditions through image analysis and symptom recognition. This tool helps farmers and veterinarians quickly identify common pig diseases and receive treatment recommendations.

## Features 🌟

- **Image-based Disease Detection**: Upload images of pigs for AI-powered disease detection
- **Symptom Analysis**: Input observed symptoms to receive accurate diagnoses
- **8 Disease Coverage**: Detects and provides information about common pig diseases:
  - Swine Flu
  - PRRS (Porcine Reproductive and Respiratory Syndrome)
  - Foot and Mouth Disease
  - Pneumonia
  - Swine Dysentery
  - Sarcoptic Mange
  - Swine Erysipelas
  - Porcine Parvovirus
- **Treatment Recommendations**: Get detailed treatment suggestions and preventive measures
- **User-friendly Interface**: Modern, responsive design for easy use on any device

## Technology Stack 💻

- **Backend**: Python, Flask
- **AI/ML**: TensorFlow, MobileNetV2 (Transfer Learning)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Processing**: NumPy, Pandas
- **Image Processing**: OpenCV, Pillow

## Installation 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/KigothoKen/pig-health-diagnostic.git
   cd pig-health-diagnostic
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Model Architecture 🧠

The disease detection model is built using MobileNetV2 architecture with transfer learning:

- Base Model: MobileNetV2 (pre-trained on ImageNet)
- Additional Layers:
  - Global Average Pooling
  - Dense Layer (1024 units, ReLU)
  - Dropout (0.5)
  - Dense Layer (512 units, ReLU)
  - Output Layer (8 units, Softmax)

## API Endpoints 🔌

### Image Analysis
```
POST /api/analyze-image
Content-Type: multipart/form-data
```
Parameters:
- `image`: Image file (jpg, png, jpeg)

### Symptom Analysis
```
POST /api/analyze-symptoms
Content-Type: application/json
```
Parameters:
- `symptoms`: Array of observed symptoms

## Contributing 🤝

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a Pull Request

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author ✨

**Kenneth Kigotho**
- GitHub: [@KigothoKen](https://github.com/KigothoKen)
- LinkedIn: [Kenneth Kigotho](https://linkedin.com/in/kenneth-kigotho-0a1744323)
- Twitter: [@ken_kigotho](https://twitter.com/ken_kigotho)

## Acknowledgments 🙏

- TensorFlow team for the excellent deep learning framework
- The open-source community for various tools and libraries
- All contributors who help improve this project

---

For more information or support, please open an issue or contact the author. 