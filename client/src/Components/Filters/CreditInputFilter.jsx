import React, { useRef } from "react";

export default function CreditInputFilter({filterData, selected, setSelected}){

    const inputRef = useRef()

    const filName = filterData.displayText
    const filId = filterData.filterId

    function selectInput(){
        const currentRef = inputRef.current.value
        if((selected.request?.[filId] !== currentRef) && (currentRef !== '')){
            setSelected((prevState)=>({
                display: {...prevState.display, [filName]: currentRef},
                request: {...prevState.request, [filId]: currentRef}
            }))
        }  
    }

    function clearInput(){
        inputRef.current.value = ''
        if(filId in selected.request){
            setSelected((prevState)=>{
                const newState = {...prevState}
    
                delete newState.display[filName]
                delete newState.request[filId]
    
                return newState
            })
        }
    }

    return(
        <article>
            <input ref={inputRef} type="text" maxLength="100" placeholder="Type a name"/>
            <button onClick={()=> clearInput()}> X </button>
            <button onClick={()=> selectInput()} > Add </button>
        </article>
    )
}