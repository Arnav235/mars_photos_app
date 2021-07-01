from google.cloud import firestore

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

add_data("users", "Arnav", {"name":"Arnav", "sport":"badminton"})
# get_document_with_condition("users", "sport", "==", "Tennis")