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
  const [filters, setFilters] = useState([])
  const [serverData, setServerData] = useState(null)

  const [selected, setSelected] = useState([])
  const [response, setResponse] = useState({})
  
  useEffect(()=>{
    requestFilters().then((data)=>{
      setResponse(data)
      setFilters(data)
    })
  }, [])

  useEffect( () =>{
    console.log(serverData)
    console.log(response)
    console.log(filters)
    
  }, [serverData])

  return(
    <main id="main-content">
      <h1> Encuentra tu película </h1>
      {
      <section>
        {filters.map((fil, k)=>(
          <FilterBlock key={k} filterData={fil} setSelected={setSelected}/>
        ))}
      </section>
}
      <button onClick = {()=>requestData(selected, setServerData)} id="search-button">Buscar</button>

    </main>
  )
}

export default App