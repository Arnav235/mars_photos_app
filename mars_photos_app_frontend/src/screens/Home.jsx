import React from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import Sidebar from "../components/Sidebar";

function Home() {
  return (
    <div className="bg-yellow-100 min-h-screen flex flex-col font-mono">
      <div className="flex flex-col p-10">
        <Navbar />
        <div className="flex">
          <Sidebar />
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
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Home;
