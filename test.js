var fs = require('fs'),
request = require('request');
const fetch = require("isomorphic-fetch")
/*In this function, we want to
- fetch the payload
- fetch the images from the first 20 photos 
- on the images, print the camera full name on the image, and download the images*/

// download function gotten from here: https://stackoverflow.com/questions/12740659/downloading-images-with-node-js
const download = function(uri, filename, callback){
	request.head(uri, function(err, res, body){
		request(uri).pipe(fs.createWriteStream(filename));
  });
};

const url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=2021-6-20&api_key=n8zqHczABgNKMwlvNmFInOXUa3IILc3jvevTYriF"

async function main(){
	let filtered_image_json = {}

	// getting the JSON object with all of the images
	images = await fetch(url).then((res) => res.json())

	// here we loop through all of the image objects and extract the url of the images into a javascript object
	// the javascript object's keys are the camera names and each key stores an array of urls
	for (const image of images.photos){
		let {img_src, camera:{name}} = image // extracting camera name and image url

		if (! (filtered_image_json.hasOwnProperty(name)) ){ // if the camera name doesn't exist in the object
			filtered_image_json[name] = [img_src]
		} else { // if the camera name does exist
			filtered_image_json[name].push(img_src)
		}
	}

	// here we loop through the camera names and the urls, and download all of the images
	for (const camera of Object.keys(filtered_image_json)){
		for (let url_index = 0; url_index < filtered_image_json[camera].length; url_index++){
			download(filtered_image_json[camera][url_index], `${camera}/${url_index}.png`, () => console.log("Done"))
			console.log(`Gotten camera:${camera}, url:${filtered_image_json[camera][url_index]}`)
		}
	}

}

main()