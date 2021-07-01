# -*- coding: utf-8 -*-
#run this function from the top level dir, not the Intrinsic-Image-Popularity directory
import argparse
import torch
import torchvision.models
import torchvision.transforms as transforms
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def prepare_image(image):
    if image.mode != 'RGB':
        try:
            image = image.convert("RGB")
        except OSError:
            pass
    Transform = transforms.Compose([
            transforms.Resize([224,224]),      
            transforms.ToTensor(),
            ])
    image = Transform(image)   
    image = image.unsqueeze(0)
    return image.to(device)

def predict(image, model):
    image = prepare_image(image)
    with torch.no_grad():
        preds = model(image)
    return preds.item()

def get_predictions(directory):
    model = torchvision.models.resnet50()
    # model.avgpool = nn.AdaptiveAvgPool2d(1) # for any size of the input
    model.fc = torch.nn.Linear(in_features=2048, out_features=1)
    model.load_state_dict(torch.load('Intrinsic-Image-Popularity/model/model-resnet50.pth', map_location=device)) 
    model.eval().to(device)

    photos = []
    # here we loop through all of the files in the directory, get the model's prediction, then append that to the photos array
    for filename in glob.glob("./{}/*.png".format(directory)):
        image = Image.open(filename)
        prediction = predict(image, model)
        photos.append([filename, prediction])

    photos = sorted(photos, key = lambda x: x[1]) # sorting the photos array by the score

    # here we loop through the photos array and print out the photo name and score
    for photo in photos:
        print ("%s: %.2f" % (photo[0], photo[1]))

get_predictions("MAST")

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