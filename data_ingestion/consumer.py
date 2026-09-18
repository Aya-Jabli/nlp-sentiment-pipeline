import json
import requests
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'commentaires_test',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

API_URL = "http://127.0.0.1:8000/predict"

print("En attente de nouveaux messages dans Kafka")

for message in consumer:
    donnees = message.value
    texte = donnees.get('texte', '')
    print(f"\nMessage reçu : {texte[:50]}...")
    
    try:
        reponse = requests.post(API_URL, json={"text": texte})
        
        if reponse.status_code == 200:
            resultat = reponse.json()
            
            sentiment = resultat.get('sentiment', 'INCONNU').upper()
            score = resultat.get('score_confiance', 'N/A')
            print(f"Sentiment : {sentiment} (Score: {score})")
        else:
            print(f"Erreur de l API : Code {reponse.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("API injoignable")