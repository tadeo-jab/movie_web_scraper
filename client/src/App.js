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


function App(){
  const [filters, setFilters] = useState({})
  const [serverData, setServerData] = useState({name: null, image: null})

  const [selected, setSelected] = useState({})
  
  useEffect(()=>{
    requestFilters().then((data)=>{
      setFilters(data.filters)

      const defaultOptions = {}
      for (let [fil, val] of Object.entries(data.filters)) {
        defaultOptions[fil] = val[0]
      }
      setSelected(defaultOptions)
    })
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