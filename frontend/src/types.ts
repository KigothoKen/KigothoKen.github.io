export interface Disease {
  name: string;
  symptoms: string[];
  treatments: string[];
  medicines: string[];
}

export interface AnalysisResult {
  name: string;
  symptoms: string[];
  treatments: string[];
  medicines: string[];
}

export interface SymptomAnalysisResponse {
  message: string;
  diseases: Disease[];
} 