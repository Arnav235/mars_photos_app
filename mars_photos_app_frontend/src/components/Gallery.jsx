import React from "react";

// takes a certain category and renders an image given an image link in the array
function Gallery({ pictureData, category }) {
  const pictureLinks = pictureData[category];
  console.log(category);

  return (
    <div className="w-full ml-10 pt-5 flex items-center justify-center flex-wrap">
      {pictureLinks.map((link, index) => {
        return (
          <div className="flex flex-col">
            <img
              className="pl-3 pt-3"
              key={index}
              src={typeof link === "string" ? link : link.url}
              alt=""
              width="200"
              height="200"
            />
            {typeof link === "object" && link.score && (
              <p>Score: {(link.score + "").substring(0, 5)}</p>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default Gallery;
