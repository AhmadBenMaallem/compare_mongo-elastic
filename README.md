# 🔍 Comparateur de UUID entre MongoDB et Elasticsearch/Opensearch

Ce script Python compare les documents présents dans une collection MongoDB avec ceux présents dans un index Elasticsearch, en se basant sur le champ `ecm:uuid` (ou `ecm:id` côté Mongo).

## 📌 Objectif

Identifier :
- Les documents présents dans **MongoDB** mais **absents d'Elasticsearch**
- Les documents présents dans **Elasticsearch** mais **absents de MongoDB**

Les résultats sont exportés dans deux fichiers :
- `missing_in_es.txt` : UUIDs présents dans Mongo mais absents dans ES
- `missing_in_mongo.txt` : UUIDs présents dans ES mais absents dans Mongo

---

## ⚙️ Étape 1 : Vérification de Python 3

> **Remarque :** Si tu utilises encore Python 2.7, il est fortement recommandé de passer à Python 3, car Python 2 n’est plus maintenu.

### 1. Vérifier si Python 3 est installé

```bash
python3 --version
```

Tu dois obtenir une sortie du type :

```bash
Python 3.x.x
```

---

## ⚙️ Étape 2 : Création d’un environnement virtuel Python 3

```bash
python3 -m venv myenv
```

Cela va créer un dossier `myenv` contenant ton environnement virtuel.

---

## ⚙️ Étape 3 : Activation de l’environnement virtuel

- Sur **MacOS/Linux** :

```bash
source myenv/bin/activate
```

- Sur **Windows** :

```bash
myenv\Scripts\activate
```

Tu devrais voir un préfixe `(myenv)` au début de ta ligne de commande.

---

## ⚙️ Étape 4 : Installation des dépendances

```bash
pip install pymongo elasticsearch==7.9.1 python-dotenv opensearch-py
```

---

## 📁 Étape 5 : Configuration via fichier `.env`

Crée un fichier `.env` à la racine du projet avec les informations de connexion :

```dotenv
# Connexion MongoDB
MONGO_URI=mongodb://user:password@localhost:27017
MONGO_DB=nuxeo
MONGO_COLLECTION=default

# Connexion Elasticsearch
ES_HOST=http://localhost:9200
ES_INDEX=nuxeo
ES_USER=elastic
ES_PASSWORD=changeme
```

---

## 🚀 Étape 6 : Lancer le script

### Mongodb / Elasticsearch

```bash
python compare_mongo-elastic.py
```

### Mongodb / Opensearch

```bash
python compare_mongo-opensearch.py
```

Cela va :
1. Se connecter à MongoDB et récupérer tous les `ecm:id`
2. Se connecter à Elasticsearch et récupérer tous les `ecm:uuid`
3. Comparer les deux ensembles d’UUID
4. Générer deux fichiers texte avec les UUID manquants

---

## 📄 Exemple de sortie

```
✔️ Mongo: 3,982,145 UUIDs récupérés
✔️ Elasticsearch: 3,975,312 UUIDs récupérés

📊 Résultat de la comparaison :
➡️ Manquants dans Elasticsearch : 6,833
➡️ Manquants dans MongoDB : 0

📄 Fichiers générés : missing_in_es.txt / missing_in_mongo.txt
```

---

## ✅ Astuce

Si tu relances le script plusieurs fois, pense à supprimer les anciens fichiers `missing_in_*.txt` pour éviter toute confusion.

---

## 🧠 Remarques

- Ce script utilise le champ `ecm:id` côté MongoDB et `ecm:uuid` côté Elasticsearch. Assure-toi qu'ils correspondent bien.
- Le `scan()` d'Elasticsearch est utilisé pour gérer les gros volumes de documents efficacement.

---

## 🧪 Scripts complémentaires

Deux scripts sont également inclus pour vérifier rapidement le nombre total de documents dans MongoDB et Elasticsearch :

### 🔹 `get-mongo.py`
Ce script se connecte à la base MongoDB (définie dans le fichier `.env`) et affiche le nombre total de documents présents dans la collection.

### 🔹 `get-es.py`
Ce script se connecte à l'index Elasticsearch (défini dans le fichier `.env`) et affiche le nombre total de documents indexés.

Ces scripts sont utiles pour vérifier la volumétrie globale avant ou après une synchronisation.

### 🔹 `get-os.py`
Ce script se connecte à l'index Opensearch (défini dans le fichier `.env`) et affiche le nombre total de documents indexés.

Ces scripts sont utiles pour vérifier la volumétrie globale avant ou après une synchronisation.

---

## 🛠️ Auteur

Script conçu pour les développeurs et administrateurs de systèmes utilisant MongoDB + Elasticsearch (ex: Nuxeo) pour la vérification de synchronisation.

---

