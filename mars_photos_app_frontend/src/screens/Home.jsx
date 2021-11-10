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
  const [mostRecentDate, setMostRecentDate] = useState(null)
  const [date, setDate] = useState("")
  const updateCategory = (updatedCategory) => {
    setCategory(updatedCategory);
  };
  const updateDate = (newDate) => {
    setDate(newDate);
  };

  useEffect(() => {
    const initial_fetch = async () => {

      // Getting the most recent date for which there is data available
      const defaultDate = await axios.get(
          "https://us-central1-mars-photos-318319.cloudfunctions.net/get_mars_photos"
        );
      // Getting picture data for that date
      const pictureData = await axios.post(
        "https://us-central1-mars-photos-318319.cloudfunctions.net/get_mars_photos",
        { earth_date: defaultDate.data} 
      )
        
      // setting the state variables accordingly
      setPicData(pictureData.data)
      setCategory("MAST_top20_overall")
      setDate(defaultDate.data)
      setMostRecentDate(defaultDate.data)
    }
    initial_fetch()
    }, [])

  // this useEffect is triggered whenever the date variable changes
  useEffect(() => {
    const fetchData = async () => {
    
      // getting picture data
      const pictureData = await axios.post(
        "https://us-central1-mars-photos-318319.cloudfunctions.net/get_mars_photos",
        { earth_date: date} 
      )

      setPicData(pictureData.data)

    };
    fetchData();
  }, [date]);

  return (
    <div className="bg-yellow-100 min-h-screen flex flex-col font-mono">
      <div className="flex flex-col p-10">
        <Navbar updateDate={updateDate} date={date} recentDate={mostRecentDate}/>
        <div className="flex">
          {picData !== null && category !== null ? (
            <>
              <Sidebar updateCategory={updateCategory} picData={picData} chosenCategory={category} />
              <Gallery pictureData={picData} category={category} />
              <Footer updateCategory={updateCategory} picData={picData} />
            </>
          ) : (
            <div className="loader-div">
              <div className="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-64 w-64" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Home;
