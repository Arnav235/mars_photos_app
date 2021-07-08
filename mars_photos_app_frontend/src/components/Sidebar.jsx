import React from "react";

function Sidebar({ updateCategory, picData }) {
  return (
    <div className="flex flex-col mt-10 text-lg">
      {Object.keys(picData).map((category, index) => (
        <p
          className="mt-10 cursor-pointer"
          onClick={() => updateCategory(category)}
          key={index}
        >
          {category}
        </p>
      ))}
    </div>
  );
}

export default Sidebar;
