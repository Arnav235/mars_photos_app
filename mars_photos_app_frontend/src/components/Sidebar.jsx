import React from "react";

//dynamically gets the picture data keys and renders them as sidebar categories
function Sidebar({ updateCategory, picData, chosenCategory}) {

  // Here we re-order the keys of picData so that all of the "Top20" keys are at the end
  let picDataKeys = Object.keys(picData)
  let i = 0
  while (i < Object.keys(picData).length - 4){
    if (picDataKeys[i].includes("_")){
      picDataKeys.push(picDataKeys[i])
      picDataKeys.splice(i, 1)
    } else {i ++}
  }

  return (
    <div className="flex flex-col mt-10 text-lg">
      {picDataKeys.map((category, index) => {
        let sidebar = ""
        if (category === chosenCategory) {sidebar = "sidebar"}
        let display_category = category
        
        // If the category is one of the top20 categories, then we reformat the text so it looks better
        if (category.includes("_")){
          const words = category.split("_")
          for (let i = 0; i < words.length; i++){
            words[i] = words[i][0].toUpperCase() + words[i].substr(1) // capitalize the start of each word
          }
          if (words.includes("Month")){
            words.splice(2, 0, "of the")
          }
          display_category = words.join(" ")
        }

        return (
          <p
            className= {"mt-10 cursor-pointer " + sidebar}
            onClick={() => updateCategory(category)}
            key={index}
          >
            {display_category}
          </p>
        )
      })}
    </div>
  );
}

export default Sidebar;