import React, {useEffect, useState} from "react"
import './App.css'
import FilterBlock from "./Components/FilterBlock.jsx"

async function requestData(query, hook){
  let path = "/search"

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

async function requestFilters() {
  const path = "/filters"

  const incomingData = await fetch(path, {
    method: "GET"
  })

  return await incomingData.json()
}

const filterData = {
  filters: {
    years: ["1","2","3"],
    genre: ["a","b","c"],
    type: ["!","?","$"],
  }
}

function App(){
  const yearOptions = ["Cualquiera", "1980", "1990", "2000", "2010", "2020"]
  const genreOptions = ["Cualquiera", "action", "adventure", "animation", "comedy","crime","documentary","drama","family","fantasy","history","horror","music","mystery","romance","science-fiction","thriller","tv-movie","war","western"]

  const [filters, setFilters] = useState({})
  const [serverData, setServerData] = useState({name: null, image: null})

  const [selected, setSelected] = useState({})

  const [year, setYear] = useState(yearOptions[0])
  const [genre, setGenre] = useState(genreOptions[0])
  
  useEffect(()=>{
    setFilters(filterData.filters)

    const defaultOptions = {}
    for (let [fil, val] of Object.entries(filterData.filters)) {
      defaultOptions[fil] = val[0]
    }

    setSelected(defaultOptions)

  }, [])

  useEffect( () =>{
    console.log(serverData)
    
  }, [serverData])

  return(
    <main id="main-content">
      <h1> Encuentra tu película </h1>

      <section>
        {Object.keys(filters).map((fil, k)=>(
          <FilterBlock filter={fil} filterOptions={filters[fil]} selected={selected[fil]} setOptions={setSelected}/>
        ))}
      </section>

      <button onClick = {()=>requestData(selected, setServerData)} id="search-button">Buscar</button>

      <div class="movie-block">
        <img src={serverData.image} ></img>
        <h1>{serverData.name}</h1>
      </div>
    </main>
  )
}

export default App