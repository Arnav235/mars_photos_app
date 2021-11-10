# This file contains functions to add, delete and access documents in the cloud firestore database

from google.cloud import firestore
import requests

db = firestore.Client()

def add_data(collection, document, data, merge=True):
    doc_ref = db.collection(collection).document(document)
    doc_ref.set(data, merge=merge)

def delete_document(collection, document):
    db.collection(collection).document(document).delete()

def get_document(collection, document):
    doc = db.collection(collection).document(document).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return "The document {} does not exist".format(document)

def get_document_with_condition(collection, field, operator, value):
    collection_ref = db.collection(collection)
    query_ref = collection_ref.where(field, operator, value)
    query_result = query_ref.stream()
    for doc in query_result:
        print (doc.to_dict())

# This function invokes the script on Cloud Run with a specific set of dates
def make_cloud_run_predict():
    api_key = open("../nasa_api_key.txt", mode="r").read()
    for i in range(30, 0, -1):
        date = "2021-06-" + "{0:0=2d}".format(i)
        print("Making prediction on date: " + date)
        requests.get("https://marspredictions-b6q4ckctha-uc.a.run.app?api_key={}&earth_date={}".format(api_key, date))
        print("Finished making prediction on date: " + date)

make_cloud_run_predict()