from pymongo import MongoClient
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from dotenv import load_dotenv
from get_mongo import get_mongo_uuids
from get_os import get_os_uuids
import os


# === COMPARAISON ===
def compare_uuids(mongo_uuids, os_uuids):
    missing_in_os = mongo_uuids - os_uuids
    missing_in_mongo = os_uuids - mongo_uuids

    print("\n📊 Résultat de la comparaison :")
    print(f"➡️ Manquants dans Opensearch : {len(missing_in_os)}")
    print(f"➡️ Manquants dans MongoDB : {len(missing_in_mongo)}")

    with open("missing_in_os.txt", "w") as f1:
        for uuid in sorted(missing_in_os):
            f1.write(uuid + "\n")

    with open("missing_in_mongo.txt", "w") as f2:
        for uuid in sorted(missing_in_mongo):
            f2.write(uuid + "\n")

    print("📄 Fichiers générés : missing_in_os.txt / missing_in_mongo.txt")

# === MAIN ===
if __name__ == "__main__":
    mongo_uuids = get_mongo_uuids()
    os_uuids = get_os_uuids()
    compare_uuids(mongo_uuids, os_uuids)

