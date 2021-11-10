import React from "react";

// takes a certain category and renders an image given an image link in the array
function Gallery({ pictureData, category }) {
  let pictureLinks = undefined
  if (category in pictureData) {pictureLinks = pictureData[category]}
  else {pictureLinks = pictureData["MAST_top20_overall"]}

  return (
    <div className="w-full ml-10 pt-5 flex items-center justify-center flex-wrap">
      {pictureLinks.map((link, index) => {
        return (
          <div className="flex flex-col imgContainer" key={index}>
            <a href={typeof link === "string" ? link : link.url}>
              <img
                className="pl-3 pt-3"
                src={typeof link === "string" ? link : link.url}
                alt=""
                width="200"
                height="200"
              />
            </a>
            {link.date && (<p>Date: {link.date}</p>)}
            {link.score && (<p>Score: {(JSON.stringify(link.score)).substring(0, 5)}</p>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default Gallery;
