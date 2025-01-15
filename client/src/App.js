import React, {useEffect, useState} from "react"
import './App.css'
import FilterBlock from "./Components/FilterBlock.jsx"
import SelectedBar from "./Components/SelectedBar.jsx"
const qs = require('qs')


async function requestData(query, setData){
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
  console.log(path)

  const incomingData = await fetch(path, {
    method: "GET"
  })

  const returnedData = await incomingData.json()

  console.log(returnedData)

  setData(returnedData)
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
  const [moviesData, setMoviesData] = useState({})

  const [selected, setSelected] = useState({display:{}, request:{}})
  
  useEffect(()=>{
    requestFilters().then((data)=>{
      setFilters(data)
    })
  }, [])

  useEffect( () =>{
    console.log(moviesData)
    
  }, [moviesData])

  useEffect( () =>{
    console.log(selected.display)
    console.log(selected.request)
    
  }, [selected])

  return(
    <main id="main-content">
      <h1> What are you watching today? </h1>
      {}

      <section>
        <SelectedBar selected={selected} setSelected={setSelected}/> 
        {
        <section>
          {filters.map((fil)=>(
            <FilterBlock filterData={fil} selected={selected} setSelected={setSelected}/>
          ))}
        </section>
        }
        <button onClick = {()=>requestData(selected.request, setMoviesData)} id="search-button">Buscar</button>
      </section>
    </main>
  )
}

export default App