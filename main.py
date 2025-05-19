from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
from typing import List

app = FastAPI(title="Piggy Doc")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock database of pig diseases and treatments
DISEASE_DATABASE = {
    "swine_flu": {
        "name": "Swine Flu",
        "symptoms": ["fever", "coughing", "nasal discharge", "lethargy"],
        "treatments": [
            "Isolation of infected animals",
            "Antiviral medications",
            "Supportive care with fluids",
        ],
        "medicines": ["Tamiflu (oseltamivir)", "NSAIDs for fever"]
    },
    "foot_and_mouth": {
        "name": "Foot and Mouth Disease",
        "symptoms": ["blisters", "lameness", "reduced appetite", "fever"],
        "treatments": [
            "Isolation",
            "Clean and dry environment",
            "Soft bedding",
        ],
        "medicines": ["Antibiotic treatment for secondary infections", "Pain management medication"]
    }
}

def analyze_image(image: Image.Image) -> dict:
    """
    Simple mock function to analyze the image
    In a production environment, this would use a trained ML model
    """
    # For demo purposes, always return swine flu
    return DISEASE_DATABASE["swine_flu"]

@app.post("/analyze")
async def analyze_pig_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        result = analyze_image(image)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/analyze-symptoms")
async def analyze_symptoms(symptoms: List[str]):
    matched_diseases = []
    for disease_id, disease in DISEASE_DATABASE.items():
        if any(symptom in disease["symptoms"] for symptom in symptoms):
            matched_diseases.append(disease)
    
    if not matched_diseases:
        return {"message": "No matching diseases found", "diseases": []}
    
    return {"message": "Potential matches found", "diseases": matched_diseases}

@app.get("/diseases")
async def get_diseases():
    return {"diseases": list(DISEASE_DATABASE.values())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 