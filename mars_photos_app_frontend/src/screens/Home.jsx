import React from "react";

function Home() {
  var today = new Date();
  var day = String(today.getDate()).padStart(2, "0");
  var month = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
  var year = today.getFullYear();

  return (
    <div className="bg-yellow-100 h-screen flex flex-col font-mono">
      <div className="flex flex-col p-10">
        <div className="flex justify-between">
          <h1 className="text-2xl font-bold">Mars Photo App</h1>
          <h1 className="text-2xl font-bold">
            Today's Date: {`${day}/${month}/${year}`}
          </h1>
        </div>
        <div className="flex flex-col mt-10 text-lg">
          <p className="mt-10">Chemistry and Camera Complex</p>
          <p className="mt-10">Front Hazard Avoidance Camera</p>
          <p className="mt-10">Rear Hazard Avoidance Camera</p>
          <p className="mt-10">Mast Camera</p>
          <p className="mt-10">Navigation Camera</p>
        </div>
      </div>
      <div className="flex p-10 justify-between fixed left-0 bottom-0 w-screen">
        <p className="text-xl font-bold">Home</p>
        <p className="text-xl font-bold">Refresh</p>
      </div>
    </div>
  );
}

export default Home;
