import React from "react";

// renders a navbar which shows the date and the project name(Rovr)
function Navbar({date, updateDate, mostRecentDate}) {

  // function to handle when the user submits a date
  const handleSubmit = (e) => {
    e.preventDefault()

    // here we split the date string into year, month and date
    let parts = e.target[0].value.match(/(\d+)/g)

    // if the regex obtains more or less than 3 different parts, or any of the parts are 0, then the string
    // is not formatted correctly
    if (parts.length !== 3) {console.log("The inputted date was not formatted correctly"); return} 
    if (parts[0] === 0 || parts[1] === 0 || parts[2] === 0) {console.log("The inputted date was not formatted correctly"); return}

    const dateSubmitObj = new Date(parts[0], parts[1]-1, parts[2])
    const minDate = Date.parse("2021-06-01")
    const maxDate = Date.parse(mostRecentDate)

    if (dateSubmitObj < minDate || dateSubmitObj > maxDate) {
      console.log("The database did not store pictures for that date. The earliest date for which there is data is '2021-06-01', and the latest is " + mostRecentDate)
    } else {
      let year = dateSubmitObj.getFullYear()
      let month = ( "0" + (dateSubmitObj.getMonth() +1).toString() ).slice(-2) // we ensure that the number has 2 digits
      let date = ("0" + dateSubmitObj.getDate().toString()).slice(-2) 
      updateDate(`${year}-${month}-${date}`)
    }
  }

  return (
    <div className="flex justify-between">
      <h1
        className="text-4xl font-bold cursor-pointer"
        onClick={() => window.location.reload()}
      >
        Rovr
      </h1>
        <form action="" className="text-2xl font-bold" onSubmit={handleSubmit}>
          Date: <input type="text" className="font-bold" defaultValue={date}></input>
        </form>
    </div>
  );
}

export default Navbar;
