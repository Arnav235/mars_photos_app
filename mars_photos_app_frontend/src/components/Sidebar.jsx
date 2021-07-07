import React from "react";

function Sidebar({ updateCategory }) {
  return (
    <div className="flex flex-col mt-10 text-lg">
      <p className="mt-10 cursor-pointer" onClick={() => updateCategory(0)}>
        Front Hazard Avoidance Camera
      </p>
      <p className="mt-10 cursor-pointer" onClick={() => updateCategory(1)}>
        Rear Hazard Avoidance Camera
      </p>
      <p className="mt-10 cursor-pointer" onClick={() => updateCategory(2)}>
        Mast Camera
      </p>
      <p className="mt-10 cursor-pointer" onClick={() => updateCategory(3)}>
        Navigation Camera
      </p>
    </div>
  );
}

export default Sidebar;
