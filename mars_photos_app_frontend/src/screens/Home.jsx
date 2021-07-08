import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Gallery from "../components/Gallery";
import Footer from "../components/Footer";

import axios from "axios";

//home screen when the user enters
function Home() {
  const [picData, setPicData] = useState(null);
  const [category, setCategory] = useState(null);
  const updateCategory = (updatedCategory) => {
    setCategory(updatedCategory);
  };

  useEffect(() => {
    const fetchData = async () => {
      // gets the date
      const dateData = await axios.get(
        "https://us-central1-mars-photos-318319.cloudfunctions.net/get_mars_photos"
      );

      //uses the date to get picture link data
      const pictureData = await axios.post(
        "https://us-central1-mars-photos-318319.cloudfunctions.net/get_mars_photos",
        { earth_date: dateData.data }
      );

      //sets the picture data and the category of the first key present in the picture data object
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
          {picData !== null && category !== null ? (
            <>
              <Sidebar updateCategory={updateCategory} picData={picData} />
              <Gallery pictureData={picData} category={category} />
              <Footer updateCategory={updateCategory} picData={picData} />
            </>
          ) : (
            <div class="loader-div">
              <div class="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-64 w-64" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Home;
