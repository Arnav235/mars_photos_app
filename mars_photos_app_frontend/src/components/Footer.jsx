import React from "react";

function Footer({ updateCategory }) {
  return (
    <div className="flex p-10 justify-between fixed left-0 bottom-0 w-screen h-10">
      <p
        className="text-xl font-bold cursor-pointer"
        onClick={() => updateCategory(0)}
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
