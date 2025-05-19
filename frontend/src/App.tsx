import React, { useState, useRef } from 'react';
import axios from 'axios';
import Camera from './components/Camera';
import { AnalysisResult } from './types';

const API_URL = 'http://localhost:8000';

function App() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [symptoms, setSymptoms] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result as string);
      };
      reader.readAsDataURL(file);
      analyzeImage(file);
    }
  };

  const handleCameraCapture = (blob: Blob) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setSelectedImage(reader.result as string);
    };
    reader.readAsDataURL(blob);
    analyzeImage(blob);
  };

  const analyzeImage = async (file: Blob) => {
    setIsAnalyzing(true);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error analyzing image:', error);
      alert('Error analyzing image. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const analyzeSymptoms = async () => {
    if (!symptoms.trim()) {
      alert('Please enter symptoms');
      return;
    }

    setIsAnalyzing(true);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/analyze-symptoms`, {
        symptoms: symptoms.split(',').map(s => s.trim()),
      });
      if (response.data.diseases.length > 0) {
        setResult(response.data.diseases[0]);
      }
    } catch (error) {
      console.error('Error analyzing symptoms:', error);
      alert('Error analyzing symptoms. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="relative px-4 py-10 bg-white mx-8 md:mx-0 shadow rounded-3xl sm:p-10">
          <div className="max-w-md mx-auto">
            <div className="divide-y divide-gray-200">
              <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <h1 className="text-3xl font-bold text-center text-primary-600 mb-8">
                  Piggy Doc
                </h1>

                <div className="space-y-4">
                  <div>
                    <input
                      type="file"
                      accept="image/*"
                      className="hidden"
                      ref={fileInputRef}
                      onChange={handleImageUpload}
                    />
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className="btn-primary w-full mb-4"
                    >
                      Upload Image
                    </button>
                  </div>

                  <div className="mb-4">
                    <Camera onCapture={handleCameraCapture} />
                  </div>

                  <div className="mt-4">
                    <label className="block text-sm font-medium text-gray-700">
                      Or enter symptoms (comma-separated)
                    </label>
                    <input
                      type="text"
                      value={symptoms}
                      onChange={(e) => setSymptoms(e.target.value)}
                      className="input-field"
                      placeholder="fever, coughing, etc."
                    />
                    <button
                      onClick={analyzeSymptoms}
                      className="btn-primary w-full mt-2"
                      disabled={isAnalyzing}
                    >
                      Analyze Symptoms
                    </button>
                  </div>

                  {selectedImage && (
                    <div className="mt-4">
                      <img
                        src={selectedImage}
                        alt="Selected"
                        className="w-full rounded-lg shadow-lg"
                      />
                    </div>
                  )}

                  {isAnalyzing && (
                    <div className="text-center text-primary-600">
                      Analyzing...
                    </div>
                  )}

                  {result && (
                    <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                      <h2 className="text-xl font-semibold text-primary-600 mb-4">
                        Analysis Results
                      </h2>
                      <div className="space-y-2">
                        <p><strong>Disease:</strong> {result.name}</p>
                        <div>
                          <strong>Symptoms:</strong>
                          <ul className="list-disc pl-5">
                            {result.symptoms.map((symptom, index) => (
                              <li key={index}>{symptom}</li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <strong>Recommended Treatments:</strong>
                          <ul className="list-disc pl-5">
                            {result.treatments.map((treatment, index) => (
                              <li key={index}>{treatment}</li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <strong>Recommended Medicines:</strong>
                          <ul className="list-disc pl-5">
                            {result.medicines.map((medicine, index) => (
                              <li key={index}>{medicine}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 