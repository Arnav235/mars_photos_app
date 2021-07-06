import os

from flask import Flask, request

app = Flask(__name__)

import json
import requests
from google.cloud import storage, firestore
firestore_db = firestore.Client()

from datetime import datetime, timedelta
import ast
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

import torch
import torchvision.models
import torchvision.transforms as transforms
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# downloading the nasa_api_key
blob = storage.Client().bucket("mars_images_scoring_model").blob("nasa_api_key.txt")
nasa_api_key = blob.download_as_text()

def download_model_from_gcloud(bucket_name, object_path, local_download_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_path)
    blob.download_to_filename(local_download_path)
    log.info("Downloaded model")

def load_model(local_model_path):
    download_model_from_gcloud("mars_images_scoring_model","model-resnet50.pth", local_model_path)
    model = torchvision.models.resnet50()
    model.fc = torch.nn.Linear(in_features=2048, out_features=1)
    model.load_state_dict(torch.load(local_model_path, map_location=device)) 
    model.eval().to(device)
    return model

# Returns as a python dictionary the URLs of the most recent photos organized by camera {"Camera_name": [url1, url2...]}
def get_images_by_camera(earth_date):

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

def make_predictions(earth_date=None, model=None):
    if model==None:
        model = load_model("model.pth")

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
        photos_dict = get_camera_predictions("MAST", photos_dict, urls_by_camera, model)
        del urls_by_camera["MAST"]
        log.info("Finished getting predictions on the MAST images")

    if "NAVCAM" in urls_by_camera:
        log.info("NAVCAM is in the URLs dictionary")
        photos_dict = get_camera_predictions("NAVCAM", photos_dict, urls_by_camera, model)
        del urls_by_camera["NAVCAM"]
        log.info("Finished getting predictions on the NAVCAM images")

    for camera in urls_by_camera:
        photos_dict[camera] = urls_by_camera[camera]
    
    firestore_db.collection("mars_img_url_scores").document(earth_date).set(photos_dict)
    return ("Success")

# this function takes the model, the name of a camera, a firestore object and an object with urls from 
# the API. It returns an instance of the firestore_obj with the predictions for the camera.
def get_camera_predictions(camera_name, firestore_obj, api_obj, model):
    firestore_obj[camera_name] = []
    for url in api_obj[camera_name]:
        image = Image.open(requests.get(url, stream=True).raw)
        if image.size[0] > 200 and image.size[1] > 200:
            firestore_obj[camera_name].append( {"url":url, "score":predict_image_score(image, model)} )
    firestore_obj[camera_name] = sorted(firestore_obj[camera_name], key = lambda x: x["score"], reverse=True)
    return firestore_obj

# function returns the firestore object with an updated array for the camera_name key
def update_camera_predictions(camera_name, firestore_obj, api_obj, model):
    firestore_camera_urls_arr = []
    for obj in firestore_obj[camera_name]:
        firestore_camera_urls_arr.append(obj["url"])
    
    for url in api_obj[camera_name]:
        if url not in firestore_camera_urls_arr:
            image = Image.open(requests.get(url, stream=True).raw)
            if image.size[0] > 200 and image.size[1] > 200:
                firestore_obj[camera_name].append( {"url":url, "score":predict_image_score(image, model)} )
    
    firestore_obj[camera_name] = sorted(firestore_obj[camera_name], key = lambda x: x["score"], reverse=True)
    return firestore_obj

def update_firestore_db():
    response = requests.get("https://api.nasa.gov/mars-photos/api/v1/manifests/curiosity?&api_key=DEMO_KEY")
    earth_date = ast.literal_eval( response.content.decode("UTF-8") )['photo_manifest']['max_date']
    earth_date_obj = datetime.strptime(earth_date, "%Y-%m-%d")
    log.info("Latest date with images data: " + earth_date)
    log.info("Loading model")
    model = load_model("model.pth")
    log.info("Finished loading model")

    log.info("Making new prediction on date: " + earth_date)
    #make_predictions(earth_date, model)
    log.info("Finished making prediction and writing to db")

    for i in range(5):
        earth_date_obj = earth_date_obj - timedelta(days=1)
        earth_date = earth_date_obj.strftime("%Y-%m-%d")

        log.info("Updating predictions for date: " + earth_date)
        api_photos = get_images_by_camera(earth_date)
        firestore_photos = firestore_db.collection("mars_img_url_scores").document(earth_date).get().to_dict()
        log.info("Got API photos and firestore photos")

        for key in api_photos:
            if key not in firestore_photos:
                if key=="MAST" or key=="NAVCAM":
                    log.info("Key is MAST or NAVCAM and NOT in firestore_photos")
                    firestore_photos = get_camera_predictions(key, firestore_photos, api_photos, model)
                else :
                    firestore_photos[key] = api_photos[key]
            else:
                if key=="MAST" or key=="NAVCAM":
                    log.info("Key is MAST or NAVCAM and IS in firestore_photos")
                    update_camera_predictions(key, firestore_photos, api_photos, model)
                else:
                    for url in api_photos[key]:
                        if url not in firestore_photos[key]:
                            firestore_photos[key].append(url)


    """
    - make predictions on today's date
    
    - loop through the last 5 days
        - get the firestore database's document for that day
        - run get_images_by_camera() for that date
        - get the cameras both on firestore and API, and those only on the API
        - If MAST or NAVCAM doesn't exist in firestore, but does from the API call, get predictions
          for those images and add them to the firestore db
        - If any other camera doesn't exist in firestore, add that to firestore

        - If either MAST or NAVCAM exist on both firestore and the API
            - Go through the firestore directory and put all of the URLs in an array
            - Find the URLs that exist on the API but not on firestore
            - For those URLs, get the predicted scores and append them to the existing firestore database
            - Resort the array of objects 
        - For other camera names on both API and firestore
            - Make the firestore DB's value equal to the APIs array
    """

@app.route("/")
def fetch_handler():
    if request.args.get("api_key") != nasa_api_key:
        return "Invalid api_key!"
    
    earth_date = request.args.get("earth_date")
    if earth_date is not None:
        make_predictions(earth_date)
        return "Got new predictions for date {} and wrote them to the firestore db".format(earth_date) 
    
    update_firestore_db()
    return "Successfully updated the firestore db"

if __name__ == "__main__":
    update_firestore_db()
    #app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

"""
Things to do
    Setup a key in the get request that authenticates the user
    Allow a post request to be sent to the endpoint with a specific date
    Setup automatic updating of photos from the previous five days
    Setup a top 20 photos of all time and top 20 photos of each month
"""