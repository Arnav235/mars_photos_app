import json
import requests
from flask import escape, Flask
from datetime import datetime, timedelta
from google.cloud import storage, firestore
firestore_db = firestore.Client()

# This function loops through documents in the cloud firestore db and returns 
# the name of the most recent document
def most_recent_date_in_firestore():
    collection = firestore_db.collection("mars_img_url_scores")
    date_obj = datetime.today()
    date_str = date_obj.strftime("%Y-%m-%d")

    while not (collection.document(date_str).get().exists):
        date_obj = date_obj - timedelta(days=1)
        date_str = date_obj.strftime("%Y-%m-%d")
    return date_str

# This is the main function that handles incoming POST and GET requests
def get_images(request):
    if request.method == "GET":
        return most_recent_date_in_firestore()

    if request.method == "POST":
        request_json = request.get_json()
        if "earth_date" in request_json:
            earth_date = request_json["earth_date"]
            firebase_doc = firestore_db.collection("mars_img_url_scores").document(earth_date).get()

            if firebase_doc.exists:
                return firebase_doc.to_dict()
            else:
                return "This document does not exist"
        
        if "top_20" in request_json:
            top_20_doc = request_json["top_20"]
            firebase_doc = firestore_db.collection("top_20").document(top_20_doc).get()

            if firebase_doc.exists:
                return firebase_doc.to_dict()
            else:
                return "This document does not exist in top_20"