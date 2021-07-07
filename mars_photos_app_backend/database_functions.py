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

# add_data("users", "Mihir", {"name":"Mihir", "sport":"basketball"})
# add_data("users", "Roger", {"name":"Roger", "sport":"Tennis"})
# add_data("users", "Allison", {"name":"Allison", "sport":"Soccer"})
# add_data("users", "Kara", {"name":"Kara", "sport":"Hockey"})
# get_document_with_condition("users", "sport", "==", "Tennis")

def make_cloud_run_predict():
    for i in range(14, 1, -1):
        date = "2021-06-" + "{0:0=2d}".format(i)
        print("Making prediction on date: " + date)
        requests.get("https://marspredictions-b6q4ckctha-uc.a.run.app?api_key=n8zqHczABgNKMwlvNmFInOXUa3IILc3jvevTYriF&earth_date={}".format(date))
        print("Finished making prediction on date: " + date)

