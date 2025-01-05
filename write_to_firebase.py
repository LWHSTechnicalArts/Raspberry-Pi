import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore with service account
cred = credentials.Certificate("firestore-key.json")
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Data to write
data = {
    "device": "Raspberry Pi",
    "temperature": 25.6,
    "humidity": 60,
    "status": "active"
}

# Write data to Firestore
collection_name = "sensor-data"  # Replace with your collection name
document_name = "example-doc"  # Replace with your document name
db.collection(collection_name).document(document_name).set(data)

print("Data written to Firestore successfully!")
