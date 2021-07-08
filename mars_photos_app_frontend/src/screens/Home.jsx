import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Gallery from "../components/Gallery";
import Footer from "../components/Footer";

import axios from "axios";

function Home() {
  const [picData, setPicData] = useState(null);
  const [category, setCategory] = useState(null);
  const updateCategory = (updatedCategory) => {
    setCategory(updatedCategory);
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
      setCategory(Object.keys(pictureData.data)[0]);
    };
    fetchData();
  }, []);

  console.log("Hi");
  return (
    <div className="bg-yellow-100 min-h-screen flex flex-col font-mono">
      <div className="flex flex-col p-10">
        <Navbar />
        <div className="flex">
          {picData !== null && category !== null && (
            <>
              <Sidebar updateCategory={updateCategory} picData={picData} />
              <Gallery pictureData={picData} category={category} />
            </>
          )}
        </div>
      </div>
      <Footer updateCategory={updateCategory} />
    </div>
  );
}

export default Home;
