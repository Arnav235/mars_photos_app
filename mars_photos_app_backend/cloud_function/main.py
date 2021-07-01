import json
import requests
from flask import escape, Flask
from google.cloud import storage, firestore
firestore_db = firestore.Client()

from datetime import date, timedelta
import ast
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

import argparse
import torch
import torchvision.models
import torchvision.transforms as transforms
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def download_model_from_gcloud(bucket_name, object_path, local_download_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_path)
    blob.download_to_filename(local_download_path)
    log.info("Downloaded model")

# Returns as a python dictionary the URLs of the most recent photos organized by camera {"Camera_name": [url1, url2...]}
def get_images_by_camera(earth_date):
    # downloading the nasa_api_key
    blob = storage.Client().bucket("mars_images_scoring_model").blob("nasa_api_key.txt")
    nasa_api_key = blob.download_as_text()

    log.debug("Getting photos for {}".format(earth_date))
    nasa_api_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={}&api_key={}".format(earth_date, nasa_api_key)

    #getting the response
    response = requests.get(nasa_api_url)
    unprocessed_photos = ast.literal_eval( response.content.decode("UTF-8") )['photos']
    
    processed_photos = {}
    for photo in unprocessed_photos:
        camera_name = photo["camera"]["name"]
        if camera_name in processed_photos:
            processed_photos[camera_name].append(photo["img_src"])
        else:
            processed_photos[camera_name] = [photo["img_src"]]

    return processed_photos

def prepare_image(image):
    if image.mode != 'RGB':
        image = image.convert("RGB")
    Transform = transforms.Compose([
            transforms.Resize([224,224]),      
            transforms.ToTensor(),
            ])
    image = Transform(image)   
    image = image.unsqueeze(0)
    return image.to(device)

def predict_image_score(image, model):
    image = prepare_image(image)
    with torch.no_grad():
        preds = model(image)
    return preds.item()

def make_predictions(earth_date=None):
    download_model_from_gcloud("mars_images_scoring_model","model-resnet50.pth", "./model.pth")
    model = torchvision.models.resnet50()
    model.fc = torch.nn.Linear(in_features=2048, out_features=1)
    model.load_state_dict(torch.load('./model.pth', map_location=device)) 
    model.eval().to(device)

    if earth_date==None:
        response = requests.get("https://api.nasa.gov/mars-photos/api/v1/manifests/curiosity?&api_key=DEMO_KEY")
        earth_date = ast.literal_eval( response.content.decode("UTF-8") )['photo_manifest']['max_date']

    log.info("Getting urls of all images")
    urls_by_camera = get_images_by_camera(earth_date)
    log.info("Got urls of all images")
    photos_dict = {}

    # here we loop through all of the MAST photos and get predictions on them
    if "MAST" in urls_by_camera:
        log.info("MAST is in the urls dictionary")
        photos_dict["MAST"] = []
        for url in urls_by_camera["MAST"]:
            image = Image.open(requests.get(url, stream=True).raw)
            if image.size[0] > 200 and image.size[1] > 200:
                photos_dict["MAST"].append( {"url":url, "score":predict_image_score(image, model)} )
        photos_dict["MAST"] = sorted(photos_dict["MAST"], key = lambda x: x["score"], reverse=True)
        del urls_by_camera["MAST"]
        log.info("Finished getting predictions on the MAST images")

    if "NAVCAM" in urls_by_camera:
        log.info("NAVCAM is in the URLs dictionary")
        photos_dict["NAVCAM"] = []
        for url in urls_by_camera["NAVCAM"]:
            image = Image.open(requests.get(url, stream=True).raw)
            if image.size[0] > 200 and image.size[1] > 200:
                photos_dict["NAVCAM"].append( {"url":url, "score":predict_image_score(image, model)} )
        photos_dict["NAVCAM"] = sorted(photos_dict["NAVCAM"], key = lambda x: x["score"], reverse=True)
        del urls_by_camera["NAVCAM"]
        log.info("Finished getting predictions on the NAVCAM images")

    for camera in urls_by_camera:
        photos_dict[camera] = urls_by_camera[camera]
    
    firestore_db.collection("mars_img_url_scores").document(earth_date).set(photos_dict)
    return photos_dict

def get_images(request):
    earth_date = "2021-06-22"
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    request_json = request.get_json()
    earth_date = request_json["earth_date"]
    firebase_doc = firestore_db.collection("mars_img_url_scores").document(earth_date).get()

    if firebase_doc.exists:
        return firebase_doc.to_dict()
    else:
        return make_predictions(earth_date)


# download_model("mars_images_scoring_model", "model-resnet50.pth", "/Users/Arnav/Desktop/code/HTML/mars_photos_app/model.pth")

"""
Framework for the backend server:

The frontend just calls the API
If the Server doesn't have that day's top 20 images
    the Server fetches all of the images from the NASA API
    the server downloads all of the corresponding images (do this asynchronously) 
    the server runs the pytorch model on each photo (do this asynchronously)
    once the server has the scores for all of the images, it stores the scores somewhere (maybe a JSON)
    the server then returns a JSON with the top 20 images(their URLs) and their corresponding scores

Else if the server has the day's top 20 images
    the server returns the JSON (URLs of the top images + their scores) for the day
"""    