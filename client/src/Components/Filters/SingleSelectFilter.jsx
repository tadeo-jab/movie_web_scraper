import React from "react";

export default function SingleSelectFilter({filterData, selected, setSelected}){

    const filName = filterData.displayText
    const filId = filterData.filterId
    const filOptions = filterData.options

    function selectOption(option){
        if(selected.display?.[filName] !== option){
            setSelected((prevState)=>({
                display: {...prevState.display, [filName]: option},
                request: {...prevState.request, [filId]: filOptions[option]}
            }))
        }  
    }

    function deselectOption(option){
        if(selected.display?.[filName] === option){
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
            {
            <div>
                {filOptions != null ?(
                    Object.keys(filOptions).map((o)=>(
                        <div> 
                            <button onClick={()=> selectOption(o)} disabled={selected.display?.[filName] === o}>{o}</button>
                            <button onClick={()=> deselectOption(o)}>X</button>
                        </div>
                ))) : null}
            </div>
            }
        </article>
    )
}