import os

from flask import Flask, request

app = Flask(__name__)

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

# This function downloads an object located on gcloud storage in bucket_name, 
# at the path object_path, to the local directory local_download_path
def download_model_from_gcloud(bucket_name, object_path, local_download_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_path)
    blob.download_to_filename(local_download_path)
    log.info("Downloaded model")

# This function loads the Pytorch model stored at local_model_path. It returns a pytorch model object
def load_model(local_model_path):
    download_model_from_gcloud("mars_images_scoring_model","model-resnet50.pth", local_model_path)
    model = torchvision.models.resnet50()
    model.fc = torch.nn.Linear(in_features=2048, out_features=1)
    model.load_state_dict(torch.load(local_model_path, map_location=device)) 
    model.eval().to(device)
    log.info("Finished loading model")
    return model

# This function fetches the Mars photos taken on the date earth_date. It then extracts all of the image URLs
# and copies them to a JSON where they're organized by camera name --> {"Camera_name": [url1, url2...]}. 
# This JSON is returned
def get_images_by_camera(earth_date):

    nasa_api_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={}&api_key={}".format(earth_date, nasa_api_key)

    #getting the response
    response = requests.get(nasa_api_url)
    unprocessed_photos = ast.literal_eval( response.content.decode("UTF-8") )['photos']
    
    # here we loop through all of the photos, get their urls and put that in processed_photos
    processed_photos = {}
    for photo in unprocessed_photos:
        camera_name = photo["camera"]["name"]
        # if the camera name is a key in processed_photos, then we add it, and make it's value equal to an array of urls.
        # Otherwise we append the url to the array of urls
        if camera_name in processed_photos:
            processed_photos[camera_name].append(photo["img_src"]) 
        else:
            processed_photos[camera_name] = [photo["img_src"]]

    return processed_photos

# function taken from the paper. It prepares images before the pytorch model makes predictions on them
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

# function taken from paper. This function takes an image and pytorch model object, and returns the score of the image
def predict_image_score(image, model):
    image = prepare_image(image)
    with torch.no_grad():
        preds = model(image)
    return preds.item()

# function makes new predictions on photos from a specific date, and updates the firestore db with those predictions 
def make_predictions(earth_date=None, model=None):
    log.info("Running make_predictions() function")
    if model==None:
        model = load_model("model.pth")

    # if the earth_date is not specified, we get the most recent date for which photos are available from the NASA API
    if earth_date==None:
        response = requests.get("https://api.nasa.gov/mars-photos/api/v1/manifests/curiosity?&api_key=DEMO_KEY")
        earth_date = ast.literal_eval( response.content.decode("UTF-8") )['photo_manifest']['max_date']

    urls_by_camera = get_images_by_camera(earth_date) # get urls of all photos taken on earth_date, organized by camera
    log.info("Got urls of all images")
    photos_dict = {}

    if "MAST" in urls_by_camera:
        log.info("MAST is in the urls dictionary")
        photos_dict = get_camera_predictions("MAST", photos_dict, urls_by_camera, model, earth_date) # make predictions on urls from API and add those to photos_dict
        del urls_by_camera["MAST"]

    if "NAVCAM" in urls_by_camera:
        log.info("NAVCAM is in the URLs dictionary")
        photos_dict = get_camera_predictions("NAVCAM", photos_dict, urls_by_camera, model, earth_date) # make predictions on urls from API and add those to photos_dict
        del urls_by_camera["NAVCAM"]

    # take the urls of images taken from all other cameras and add them to photos_dict
    for camera in urls_by_camera:
        photos_dict[camera] = urls_by_camera[camera]
    
    firestore_db.collection("mars_img_url_scores").document(earth_date).set(photos_dict) # add photos_dict to the firestore db
    log.info("Finished making new predictions for date: " + earth_date)
    return ("Success")

# This function checks if any of the images in firestore_obj[camera_name] are in the top 20
# images of the month or all time
def check_top_20(firestore_obj, camera_name, earth_date):
    # Get the top photos of the month and top all time photos
    top_20_month_db = firestore_db.collection("top_20").document(camera_name + "_" + earth_date[:-3]).get()
    top_20_all_time = firestore_db.collection("top_20").document(camera_name + "_all_time").get().to_dict()

    if not top_20_month_db.exists: # if a document doesn't exist with the top photos of the month, we create one
        top_20_month_db = {"images":[{"score":-2}] * 20}
    else: top_20_month_db = top_20_month_db.to_dict()

    # loop through all of the photos for which the model recently made predictions
    for img in firestore_obj[camera_name]:
        # if the image's score is better than the worst photo in the top20 photos of the month or all time, then the worst photos is replaced with this one
        if img["score"] > top_20_all_time["images"][19]["score"]:
            top_20_all_time["images"][19] = {"url":img["url"], "date":earth_date, "score":img["score"]}
            top_20_all_time["images"] = sorted(top_20_all_time["images"], key = lambda x: x["score"], reverse=True)
        if img["score"] > top_20_month_db["images"][19]["score"]:
            top_20_month_db["images"][19] = {"url":img["url"], "date":earth_date, "score":img["score"]}
            top_20_month_db["images"] = sorted(top_20_month_db["images"], key = lambda x: x["score"], reverse=True) 
        else:
            # the imgs in firestore_obj are sorted from best to worst, so if a certain photo isn't as good as the 
            # worst photo in the top20 lists, then non of the consecutive photos will be. So we break the loop
            break 
    
    # updating the firestore dbs
    firestore_db.collection("top_20").document(camera_name + "_" + earth_date[:-3]).set(top_20_month_db)
    firestore_db.collection("top_20").document(camera_name + "_all_time").set(top_20_all_time)
    log.info("Finished check_top_20 for camera: " + camera_name + " for date: " + earth_date)

# This function takes the model, the name of a camera, a firestore object and an object with urls from the API. 
# The function makes predictions on all URLs in api_obj, then adds those predictions to firestore_obj. It returns firestore_obj.
def get_camera_predictions(camera_name, firestore_obj, api_obj, model, earth_date):
    firestore_obj[camera_name] = []

    # loop through all of the urls in api_obj, make predictions on them, then append them to firestore_obj[camera_name]
    for url in api_obj[camera_name]:
        image = Image.open(requests.get(url, stream=True).raw)
        if image.size[0] > 200 and image.size[1] > 200: # we only consider images with a size of more than 200x200, because smaller images look bad
            firestore_obj[camera_name].append( {"url":url, "score":predict_image_score(image, model)} )

    # sort the images in firestore_obj[camera_name] from highest to lowest score
    firestore_obj[camera_name] = sorted(firestore_obj[camera_name], key = lambda x: x["score"], reverse=True)
    log.info("Finished getting predictions on camera: " + camera_name + " for date: " + earth_date)
    check_top_20(firestore_obj, camera_name, earth_date)
    return firestore_obj

# function returns the firestore object with an updated array for the camera_name key
def update_camera_predictions(camera_name, firestore_obj, api_obj, model, earth_date):
    firestore_camera_urls_arr = []
    new_photos = {}
    new_photos[camera_name] = []
    for obj in firestore_obj[camera_name]:
        firestore_camera_urls_arr.append(obj["url"])
    
    for url in api_obj[camera_name]:
        if url not in firestore_camera_urls_arr:
            image = Image.open(requests.get(url, stream=True).raw)
            if image.size[0] > 200 and image.size[1] > 200:
                new_photos[camera_name].append( {"url":url, "score":predict_image_score(image, model)} )
    
    firestore_obj[camera_name] = firestore_obj[camera_name] + new_photos[camera_name]
    firestore_obj[camera_name] = sorted(firestore_obj[camera_name], key = lambda x: x["score"], reverse=True)
    new_photos[camera_name] = sorted(new_photos[camera_name], key = lambda x: x["score"], reverse=True)
    log.info("Finished updating predictions on camera: " + camera_name + " for date: " + earth_date)
    check_top_20(new_photos, camera_name, earth_date) # notice that here, we're only calling the function with the new photos
    return firestore_obj

# this function makes predictions on all photos on the most recent date, then looks at the previous five days and 
# checks if any new photos have been added for them. If they have, then the function updates those firestore documents
def update_firestore_db():
    log.info("update_firestore_db() function called")
    response = requests.get("https://api.nasa.gov/mars-photos/api/v1/manifests/curiosity?&api_key=DEMO_KEY")
    earth_date = ast.literal_eval( response.content.decode("UTF-8") )['photo_manifest']['max_date']
    earth_date_obj = datetime.strptime(earth_date, "%Y-%m-%d")
    log.info("Latest date with images data: " + earth_date)
    model = load_model("model.pth")

    log.info("Making new prediction on date: " + earth_date)
    make_predictions(earth_date, model) # making predictions on the latest date for which photos are available

    # I've noticed that often NASA will only make certain photos available for the most recent date,
    # then later on they'll add more photos for the same date. This function checks if there are any new photos 
    # for the past 5 days, and if so it adds them to the firestore db.
    for i in range(5):
        earth_date_obj = earth_date_obj - timedelta(days=1)
        earth_date = earth_date_obj.strftime("%Y-%m-%d")

        log.info("***Updating predictions for date: " + earth_date)
        api_photos = get_images_by_camera(earth_date)
        firestore_photos = firestore_db.collection("mars_img_url_scores").document(earth_date).get().to_dict()
        if firestore_photos == None:
            make_predictions(earth_date, model)
            log.info("Photos did not exist in the firestore database for date: " + earth_date)
            continue
        log.info("Got API photos and firestore photos")

        for key in api_photos:
            if key not in firestore_photos:
                if key=="MAST" or key=="NAVCAM":
                    firestore_photos = get_camera_predictions(key, firestore_photos, api_photos, model, earth_date)
                else :
                    firestore_photos[key] = api_photos[key]
            else:
                if key=="MAST" or key=="NAVCAM":
                    firestore_photos = update_camera_predictions(key, firestore_photos, api_photos, model, earth_date)
                else:
                    for url in api_photos[key]:
                        if url not in firestore_photos[key]:
                            firestore_photos[key].append(url)
        firestore_db.collection("mars_img_url_scores").document(earth_date).set(firestore_photos)
        log.info("Successfully updated the firestore document for date {}".format(earth_date))

# the flask router to take requests
@app.route("/")
def fetch_handler():
    log.info("Recieved a request")
    if request.args.get("api_key") != nasa_api_key:
        log.info("Invalid api_key")
        return "Invalid api_key!"
    
    earth_date = request.args.get("earth_date")
    if earth_date is not None:
        make_predictions(earth_date)
        return "Got new predictions for date {} and wrote them to the firestore db".format(earth_date) 
    
    update_firestore_db()
    return "Successfully updated the firestore db"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))