import React from "react";

//renders a footer which goes back to the first category or reloads the page if needed
function Footer({ updateCategory, picData }) {
  return (
    <div className="flex p-10 justify-between fixed left-0 bottom-0 w-screen h-10">
      <p
        className="text-xl font-bold cursor-pointer"
        onClick={() => updateCategory(Object.keys(picData)[0])}
      >
        Home
      </p>
      <p
        className="text-xl font-bold cursor-pointer"
        onClick={() => window.location.reload()}
      >
        Refresh
      </p>
    </div>
  );
}

export default Footer;
