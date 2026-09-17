from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline


app = FastAPI(
    title="API Analyse de Sentiment",
    description="API en temps reel pour analyser des textes",
    version="1.0.0"
)

sentiment_analyzer = pipeline(
    "sentiment-analysis", 
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)
print("Modele charge avec succes !")

class TextRequest(BaseModel):
    text: str

@app.post("/predict")
async def predict_sentiment(request: TextRequest):
    # L'IA analyse le texte
    result = sentiment_analyzer(request.text)[0]
    
    stars = int(result['label'][0])
    
    if stars >= 4:
        sentiment = "Positif"
    elif stars == 3:
        sentiment = "Neutre"
    else:
        sentiment = "Négatif"
        
    return {
        "texte_original": request.text,
        "sentiment": sentiment,
        "score_confiance": round(result['score'], 4),
        "etoiles": stars
    }

# test
@app.get("/")
async def root():
    return {"message": "L'API NLP est en ligne"}