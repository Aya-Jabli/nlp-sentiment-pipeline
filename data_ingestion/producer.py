import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

donnees_test = [
    "L'application est super fluide, je la recommande vivement !",
    "L'interface est correcte, mais il manque quelques fonctionnalités de base.",
    "Crash total au démarrage, impossible de l'utiliser. Très décevant.",
    "Service client réactif et problème résolu rapidement. Merci !",
    "Je n'ai pas d'avis particulier, le logiciel fait simplement ce qu'on lui demande.",
    "La dernière mise à jour a tout cassé, mon écran reste noir."
]

print("Demarrage de lenvoi des donnees de test vers Kafka")

try:
    while True:
        texte_choisi = random.choice(donnees_test)
        message = {"source": "plateforme_test", "texte": texte_choisi}
        
        producer.send('commentaires_test', value=message)
        print(f"Envoye : {texte_choisi[:50]}...")
        
        time.sleep(random.randint(2, 5))
        
except KeyboardInterrupt:
    print("\nArret du script.")