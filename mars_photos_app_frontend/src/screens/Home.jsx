import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Gallery from "../components/Gallery";
import Footer from "../components/Footer";

import axios from "axios";

function Home() {
  const categories = ["FHAZ", "MAST", "NAVCAM", "RHAZ"];
  const [categoryIndex, setCategoryIndex] = useState(0);
  const [picData, setPicData] = useState(null);
  const updateCategory = (updatedIndex) => {
    setCategoryIndex(updatedIndex);
  };

  useEffect(() => {
    const fetchData = async () => {
      const dateData = await axios.get(
        "https://us-central1-mars-photos-318319.cloudfunctions.net/get_mars_photos"
      );

      const pictureData = await axios.post(
        "https://us-central1-mars-photos-318319.cloudfunctions.net/get_mars_photos",
        { earth_date: dateData.data }
      );

      setPicData(pictureData.data);
    };
    fetchData();
  }, []);

  console.log("Hi");

  return (
    <div className="bg-yellow-100 min-h-screen flex flex-col font-mono">
      <div className="flex flex-col p-10">
        <Navbar />
        <div className="flex">
          <Sidebar updateCategory={updateCategory} />
          {picData !== null && (
            <Gallery
              pictureData={picData}
              category={categories[categoryIndex]}
            />
          )}
        </div>
      </div>
      <Footer updateCategory={updateCategory} />
    </div>
  );
}

export default Home;
