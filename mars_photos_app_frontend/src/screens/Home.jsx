import React from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Gallery from "../components/Gallery";
import Footer from "../components/Footer";

function Home() {
  return (
    <div className="bg-yellow-100 min-h-screen flex flex-col font-mono">
      <div className="flex flex-col p-10">
        <Navbar />
        <div className="flex">
          <Sidebar />
          <Gallery />
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Home;
