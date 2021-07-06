import json
import requests
from flask import escape, Flask
from datetime import datetime, timedelta
from google.cloud import storage, firestore
firestore_db = firestore.Client()

def most_recent_date_in_firestore():
    collection = firestore_db.collection("mars_img_url_scores")
    date_obj = datetime.today()
    date_str = date_obj.strftime("%Y-%m-%d")

    while not (collection.document(date_str).get().exists):
        date_obj = date_obj - timedelta(days=1)
        date_str = date_obj.strftime("%Y-%m-%d")
    return date_str

def get_images(request):
    if request.method == "GET":
        return most_recent_date_in_firestore()

    if request.method == "POST":
        request_json = request.get_json()
        earth_date = request_json["earth_date"]
        firebase_doc = firestore_db.collection("mars_img_url_scores").document(earth_date).get()

        if firebase_doc.exists:
            return firebase_doc.to_dict()
        else:
            return "This document does not exist"

"""
Things to do
    - remove all of the model imports and functions
    - when the request comes in, if it's a get request, then run a function that returns
       the most recent date for which the firestore database has data
    - If it's a post request, then return the data from that specific date. If data doesn't exist for 
       the specific date, then return an error
"""