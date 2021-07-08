import json
import requests
from flask import escape, Flask
from datetime import datetime, timedelta
from google.cloud import storage, firestore
from flask_cors import cross_origin
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
@cross_origin()
def get_images(request):
    if request.method == "GET":
        return most_recent_date_in_firestore()

    if request.method == "POST":
        request_json = request.get_json()

        if "earth_date" in request_json and "top_20" in request_json:
            return "Both earth_date and top_20 are in your POST request. You can only have one of the two variables. Choose one!"

        if "earth_date" in request_json:
            earth_date = request_json["earth_date"]
            if type(earth_date) is str:
                firebase_doc = firestore_db.collection("mars_img_url_scores").document(earth_date).get()
                if firebase_doc.exists:
                    return firebase_doc.to_dict()
                else:
                    return "This document does not exist"
            else:
                return "The earth_date object must be a string" 
        
        if "top_20" in request_json:
            top_20_doc = request_json["top_20"]

            if type(top_20_doc) is str:
                firebase_doc = firestore_db.collection("top_20").document(top_20_doc).get()

                if firebase_doc.exists:
                    return firebase_doc.to_dict()
                else:
                    return "This document does not exist in top_20"
            else:
                return "The top_20 object must be a string" 