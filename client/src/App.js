import React, {useEffect, useState} from "react"
import './App.css'

async function getData(){
  try{
    const incomingData = await fetch("/api",{
      method: "GET"
    })
    return await incomingData.json()
  }catch (err){
    console.log(err)
  }
}

async function requestData(query, hook){
  let path = "/search"
  const filterCheck = Object.values(query).every(value => value === "Cualquiera");

  /*if (!filterCheck) {
    const queryParams = query
    /*Object.keys(queryParams).forEach(key => {
      if (queryParams[key] === "Cualquiera") {
        delete queryParams[key]
      }
    });

    const searchParams = new URLSearchParams(queryParams)
    path += `?${searchParams}`
  }*/

  const queryParams = query
  const searchParams = new URLSearchParams(queryParams)
  path += `?${searchParams}`

  const incomingData = await fetch(path, {
    method: "GET"
  })

  const returnedData = await incomingData.json()

  console.log(returnedData)

  hook(returnedData)
}


window.onclick = function(event) {
  if (!event.target.matches('.filter-btn')) {
    var dropdowns = document.getElementsByClassName("filter-dropdown");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

function App(){
  const yearOptions = ["Cualquiera", "1980", "1990", "2000", "2010", "2020"]
  const genreOptions = ["Cualquiera", "action", "adventure", "animation", "comedy","crime","documentary","drama","family","fantasy","history","horror","music","mystery","romance","science-fiction","thriller","tv-movie","war","western"]

  const [serverData, setServerData] = useState({name: null, image: null})

  const [year, setYear] = useState(yearOptions[0])
  const [genre, setGenre] = useState(genreOptions[0])
  

  useEffect( () =>{
    console.log(serverData)
    
  }, [serverData])

  return(
    <main id="main-content">
      <h1 id="title"> Encuentra tu película </h1>
      <section class="filter-articles">
        <p id="filter-text1"> Año: </p>
        <p id="filter-text2"> Género: </p>
      </section>
      <section class="filter-articles">
        <article id="filter1" class="filter-select">
          <button class="filter-btn" onClick={()=> document.getElementById("dropdown-year").classList.toggle("show")}>{year}</button>
          <div id="dropdown-year" class="filter-dropdown">
            {yearOptions.map((i, j) => (
              <button key={j} onClick={() => setYear(i)}>{i}</button>
            ))}
          </div>
        </article>
        <article id="filter2" class="filter-select">
          <button class="filter-btn" onClick={()=> document.getElementById("dropdown-genre").classList.toggle("show")}>{genre}</button>
          <div id="dropdown-genre" class="filter-dropdown">
            {genreOptions.map((i, j) => (
              <button key={j} onClick={() => setGenre(i)}>{i}</button>
            ))}
          </div>
        </article>
      </section>
      <button onClick = {()=>requestData({year, genre}, setServerData)} id="search-button">Buscar</button>
      <div class="movie-block">
        <img src={serverData.image} ></img>
        <h1>{serverData.name}</h1>
      </div>
    </main>
  )
}

export default App