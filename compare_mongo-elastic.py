from pymongo import MongoClient
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from dotenv import load_dotenv
from get_mongo import get_mongo_uuids
from get_es import get_es_uuids
import os

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

