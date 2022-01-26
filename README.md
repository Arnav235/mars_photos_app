# Mars Photos App  
A web app that displays the best photos taken by NASA's Curiosity rover, updated daily, sorted by camera <br>and potential popularity on social media. Check out the website [here](https://arnav235.github.io/mars_photos_app/)!

You can view photos from different days by changing the date in the upper right corner.

## How it works
The app ranks photos using the algorithm outlined in the paper ["Intrinsic Image Popularity Assessment"](https://arxiv.org/abs/1907.01985).<br>
This algorithm scores images based on their potential popularity on social media platforms, based solely <br>on the content of the image (excluding other aspects like upload time and the account which posted <br>the image).  

Every day, an endpoint deployed on Google Cloud Run is called using Google Cloud Scheduler. This endpoint <br>gets the latest photos from the NASA API, scores them using the algorithm, then adds them to the photos <br>Firebase database while also re-ranking the photos.  

The frontend calls an API endpoint deployed on Google Cloud functions, which then fetches the photos from the <br>Firebase DB.  

The frontend is made using React.
