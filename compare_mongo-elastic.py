from pymongo import MongoClient
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from dotenv import load_dotenv
import os


# === CHARGER LES VARIABLES D'ENV ===
load_dotenv()

# === CONFIGURATION ===
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")


ES_HOST = os.getenv("ES_HOST")
ES_INDEX = os.getenv("ES_INDEX")
#ES_AUTH# ES_USER = os.getenv("ES_USER")
#ES_AUTH# ES_PASSWORD = os.getenv("ES_PASSWORD")

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

# === RÉCUPÉRATION DES ECM:UUID D'ELASTICSEARCH ===
def get_es_uuids():
    es = Elasticsearch(
        ES_HOST,
    #ES_AUTH#   basic_auth=(ES_USER, ES_PASSWORD),
        headers={"Content-Type": "application/json"}
    )
    uuids = set()
    results = scan(
        es,
        index=ES_INDEX,
        query={"_source": ["ecm:uuid"], "query": {"match_all": {}}},
        size=1000,
        scroll='5m'
    )
    for doc in results:
        source = doc.get('_source', {})
        uuid = source.get("ecm:uuid")
        if uuid:
            uuids.add(uuid)
    print(f"✔️ Elasticsearch: {len(uuids)} UUIDs récupérés")
    return uuids

# === COMPARAISON ===
def compare_uuids(mongo_uuids, es_uuids):
    missing_in_es = mongo_uuids - es_uuids
    missing_in_mongo = es_uuids - mongo_uuids

    print("\n📊 Résultat de la comparaison :")
    print(f"➡️ Manquants dans Elasticsearch : {len(missing_in_es)}")
    print(f"➡️ Manquants dans MongoDB : {len(missing_in_mongo)}")

    with open("missing_in_es.txt", "w") as f1:
        for uuid in sorted(missing_in_es):
            f1.write(uuid + "\n")

    with open("missing_in_mongo.txt", "w") as f2:
        for uuid in sorted(missing_in_mongo):
            f2.write(uuid + "\n")

    print("📄 Fichiers générés : missing_in_es.txt / missing_in_mongo.txt")

# === MAIN ===
if __name__ == "__main__":
    mongo_uuids = get_mongo_uuids()
    es_uuids = get_es_uuids()
    compare_uuids(mongo_uuids, es_uuids)

