from flask import escape, Flask
from datetime import datetime, timedelta
from google.cloud import firestore
from flask_cors import cross_origin
firestore_db = firestore.Client()

# This function loops through documents in the cloud firestore db and returns 
# the name of the most recent document
def most_recent_date_in_firestore():
    collection = firestore_db.collection("mars_img_url_scores")
    date_obj = datetime.today()
    date_str = date_obj.strftime("%Y-%m-%d")

    while not (collection.document(date_str).get().exists): # while the document does not exist, do ...
        date_obj = date_obj - timedelta(days=1)
        date_str = date_obj.strftime("%Y-%m-%d")
    return date_str

# This is the main function that handles incoming POST and GET requests
@cross_origin() # flask_cors header used to handle cross origin requests
def get_images(request):
    if request.method == "GET":
        return most_recent_date_in_firestore() # returns the most recent date for which firestore has data

    # If a POST request is recieved, the function returns a dictionary with the photos from the date earth_date
    # and the top all time photos and top photos of the month for NAVCAM and MAST cameras
    if request.method == "POST":
        request_json = request.get_json()

        if "earth_date" not in request_json:
            return "earth_date parameter not specified"

        earth_date = request_json["earth_date"]

        # Ensuring that earth_date is formatted correctly
        try:
            datetime.strptime(earth_date, "%Y-%m-%d")
        except:
            return "The earth_date string is not formatted accuratly"

        return_dict = {} 
        firebase_doc = firestore_db.collection("mars_img_url_scores").document(earth_date).get()
        if firebase_doc.exists:
            return_dict = firebase_doc.to_dict()
        else:
            return "This document does not exist", 400
        
        # getting the top documents
        return_dict["MAST_top20_overall"] = firestore_db.collection("top_20").document("MAST_all_time").get().to_dict()["images"]
        return_dict["NAVCAM_top20_overall"] = firestore_db.collection("top_20").document("NAVCAM_all_time").get().to_dict()["images"]
        return_dict["MAST_top20_month"] = firestore_db.collection("top_20").document("MAST_" + earth_date[:-3]).get().to_dict()["images"]
        return_dict["NAVCAM_top20_month"] = firestore_db.collection("top_20").document("NAVCAM_" + earth_date[:-3]).get().to_dict()["images"]

        return return_dict


    return "invalid HTTPS method"