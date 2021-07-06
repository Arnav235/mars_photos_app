import React from "react";

function Gallery() {
  return (
    <div className="w-full ml-10 pt-5 flex items-center justify-center flex-wrap">
      {new Array(20).fill(1).map((item, index) => (
        <img
          className="pl-3 pt-3"
          key={index}
          src="https://picsum.photos/200/200"
          alt=""
        />
      ))}
    </div>
  );
}

export default Gallery;
