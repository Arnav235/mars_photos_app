import React from "react";

function Navbar() {
  var today = new Date();
  var day = String(today.getDate()).padStart(2, "0");
  var month = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
  var year = today.getFullYear();

  return (
    <div className="flex justify-between">
      <h1 className="text-2xl font-bold">Mars Photo App</h1>
      <h1 className="text-2xl font-bold">
        Today's Date: {`${month}/${day}/${year}`}
      </h1>
    </div>
  );
}

export default Navbar;
