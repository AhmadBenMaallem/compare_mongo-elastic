from pymongo import MongoClient
from dotenv import load_dotenv
import os

# === CHARGER LES VARIABLES D'ENV ===
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

# === RÉCUPÉRATION DES ECM:UUID DE MONGO ===
def get_mongo_uuids():
    client = MongoClient(MONGO_URI)
    collection = client[MONGO_DB][MONGO_COLLECTION]
    uuids = set()
    for doc in collection.find({}, {"ecm:id": 1}):
        uuid = doc.get("ecm:id")
        if uuid:
            uuids.add(uuid)
    print(f"✔️ Mongo: {len(uuids)} UUIDs récupérés")
    return uuids


# === MAIN ===
if __name__ == "__main__":
    mongo_uuids = get_mongo_uuids()
