from opensearchpy import OpenSearch
from dotenv import load_dotenv
import os
 
# Charger les variables d'environnement
load_dotenv()
 
ES_HOST = os.getenv("ES_HOST")  # ex: https://your-domain.com
ES_INDEX = os.getenv("ES_INDEX")
ES_USER = os.getenv("ES_USER")
ES_PASSWORD = os.getenv("ES_PASSWORD")
 
def get_os_uuids():
    client = OpenSearch(
        hosts=[{'host': ES_HOST.replace("https://", ""), 'port': 443}],
        http_auth=(ES_USER, ES_PASSWORD),
        use_ssl=True,
        verify_certs=False,  # à activer en prod avec un certificat valide
        ssl_show_warn=False
    )
 
    uuids = set()
 
    query = {
        "_source": ["ecm:uuid"],
        "query": {"match_all": {}}
    }
 
    # Pagination manuelle car opensearch-py n'a pas de `scan` comme elasticsearch-py
    result = client.search(index=ES_INDEX, body=query, scroll='5m', size=1000)
    scroll_id = result['_scroll_id']
 
    while True:
        hits = result['hits']['hits']
        if not hits:
            break
        for doc in hits:
            uuid = doc.get('_source', {}).get("ecm:uuid")
            if uuid:
                uuids.add(uuid)
 
        result = client.scroll(scroll_id=scroll_id, scroll='5m')
 
    print(f"✔️ OpenSearch: {len(uuids)} UUIDs récupérés")
    return uuids
 
if __name__ == "__main__":
    get_os_uuids()