import React, {useEffect, useState} from "react"
import './App.css'
import FilterBlock from "./Components/FilterBlock.jsx"
import SelectedBar from "./Components/SelectedBar.jsx"
import MovieDisplay from "./Components/MovieDisplay.jsx"
const qs = require('qs')

//qs is used to allow for nested objects in the URL.

async function requestMovies(query, setData){
  let path = "/search"

  const queryParams = query

  const searchParams = qs.stringify(queryParams, {
    encoder: (value) => {
      if (typeof(value) === 'number' || typeof(value) === 'boolean') {
        return String(value); 
      }
      else{
        return value;
      }
    },
  })
  
  path += `?${searchParams}`

  const incomingData = await fetch(path, {
    method: "GET"
  })

  const returnedData = await incomingData.json()

  setData(returnedData)
}

async function requestFilters() {
  const path = "/filters"

  const incomingData = await fetch(path, {
    method: "GET"
  })

  return await incomingData.json()
}

//The idea is for the user to select the filters they want in the movie search.

//When updating the filter selection, it updates two objects:
//The "Display" values, which are seen on the front-end rendering.
//And the "Request" values, which are what the back-end receives through query params.

function App(){
  const [filters, setFilters] = useState([])
  const [moviesData, setMoviesData] = useState(null)

  const [selected, setSelected] = useState({display:{}, request:{}})
  

  //The request for the initial data is only performed at the first render.

  useEffect(()=>{
    requestFilters().then((data)=>{
      setFilters(data)
    })
  }, [])

  //Depending on whether the data has been received from the server, a different view is rendered.
  //Each filter option is rendered dynamically.

  return(
    <main id="main-content">
      <h1> What are you watching today? </h1>
      {moviesData === null ? (
        <section>
          <SelectedBar filters={filters} selected={selected} setSelected={setSelected}/> 
          {
          <section>
            {filters.map((fil)=>(
              <FilterBlock filterData={fil} selected={selected} setSelected={setSelected}/>
            ))}
          </section>
          }
          <button onClick = {()=>requestMovies(selected.request, setMoviesData)} id="search-button">Buscar</button>
        </section>
      ): (
        <MovieDisplay movieList={moviesData.data} setMoviesData={setMoviesData}/>
      )}
    </main>
  )
}

export default App