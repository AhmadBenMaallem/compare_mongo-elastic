from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from dotenv import load_dotenv
import os

# === CHARGER LES VARIABLES D'ENV ===
load_dotenv()

# === CONFIGURATION ===

ES_HOST = os.getenv("ES_HOST")
#ES_AUTH# ES_USER = os.getenv("ES_USER")
#ES_AUTH# ES_PASSWORD = os.getenv("ES_PASSWORD")
ES_INDEX = os.getenv("ES_INDEX")



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

# === MAIN ===
if __name__ == "__main__":
    es_uuids = get_es_uuids()

