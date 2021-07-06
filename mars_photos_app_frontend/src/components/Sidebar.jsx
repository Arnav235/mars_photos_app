import React from "react";

function Sidebar({ updateCategory }) {
  return (
    <div className="flex flex-col mt-10 text-lg">
      <p className="mt-10 cursor-pointer" onClick={() => updateCategory(0)}>
        Chemistry and Camera Complex
      </p>
      <p className="mt-10 cursor-pointer" onClick={() => updateCategory(1)}>
        Front Hazard Avoidance Camera
      </p>
      <p className="mt-10 cursor-pointer" onClick={() => updateCategory(2)}>
        Rear Hazard Avoidance Camera
      </p>
      <p className="mt-10 cursor-pointer" onClick={() => updateCategory(3)}>
        Mast Camera
      </p>
      <p className="mt-10 cursor-pointer" onClick={() => updateCategory(4)}>
        Navigation Camera
      </p>
    </div>
  );
}

export default Sidebar;
