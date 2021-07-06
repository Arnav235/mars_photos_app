import React, { useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Gallery from "../components/Gallery";
import Footer from "../components/Footer";
import pictureData from "../datasets/data";

function Home() {
  const categories = ["CHEMCAM", "FHAZ", "MAST", "NAVCAM", "RHAZ"];
  const [categoryIndex, setCategoryIndex] = useState(0);
  const updateCategory = (updatedIndex) => {
    setCategoryIndex(updatedIndex);
  };
  return (
    <div className="bg-yellow-100 min-h-screen flex flex-col font-mono">
      <div className="flex flex-col p-10">
        <Navbar />
        <div className="flex">
          <Sidebar updateCategory={updateCategory} />
          <Gallery
            pictureData={pictureData}
            category={categories[categoryIndex]}
          />
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Home;
