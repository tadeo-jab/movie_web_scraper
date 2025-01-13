import React, {useEffect, useState} from "react"
import './App.css'
import FilterBlock from "./Components/FilterBlock.jsx"
import SelectedBar from "./Components/SelectedBar.jsx"
const qs = require('qs')


async function requestData(query, hook){
  let path = "/search"

  const queryParams = query
  const searchParams = qs.stringify(queryParams)
  path += `?${searchParams}`
  console.log(path)

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
  const [filters, setFilters] = useState([])
  const [serverData, setServerData] = useState(null)

  const [selected, setSelected] = useState({display:{}, request:{}})
  
  useEffect(()=>{
    requestFilters().then((data)=>{
      setFilters(data)
    })
  }, [])

  useEffect( () =>{
    console.log(serverData)
    
  }, [serverData])

  useEffect( () =>{
    console.log(selected.display)
    console.log(selected.request)
    
  }, [selected])

  return(
    <main id="main-content">
      <SelectedBar selected={selected} setSelected={setSelected}/> 
      <h1> Encuentra tu película </h1>
      {
      <section>
        {filters.map((fil)=>(
          <FilterBlock filterData={fil} selected={selected} setSelected={setSelected}/>
        ))}
      </section>
}
      <button onClick = {()=>requestData(selected.request, setServerData)} id="search-button">Buscar</button>

    </main>
  )
}

export default App