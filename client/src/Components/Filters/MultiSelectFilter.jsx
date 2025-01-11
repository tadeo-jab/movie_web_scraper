import React, { useState } from "react";

export default function MultiSelectFilter({filterData, selected, setSelected}){


    function selectOption(option){
        if(!(filterData.filterId in selected.request)){
            setSelected((prevState)=>({
                display: {...prevState.display, [filterData.displayText]: [option]},
                request: {...prevState.request, [filterData.filterId]: [filterData.options[option]]}
            }))
        }
        else if((filterData.filterId in selected.request) && !(selected.display?.[filterData.displayText]?.includes(option))){
            setSelected((prevState)=>({
                display: {...prevState.display, [filterData.displayText]: [...prevState.display[filterData.displayText], option]},
                request: {...prevState.request, [filterData.filterId]: [...prevState.request[filterData.filterId], filterData.options[option]]}
            }))
        }  
    }

    function deselectOption(option){
        if(selected.display?.[filterData.displayText]?.length === 1){
            setSelected((prevState)=>{
                const newState = {...prevState}
    
                delete newState.display[filterData.displayText]
                delete newState.request[filterData.filterId]
    
                return newState
            })
        }
        else{
            setSelected((prevState)=>({
                display: {...prevState.display, [filterData.displayText]: prevState.display[filterData.displayText].filter(item => item !== option)},
                request: {...prevState.request, [filterData.filterId]: prevState.request[filterData.filterId].filter(item => item !== filterData.options[option])}
            }))
        }
        
    }

    return(
        <article>
            {
            <div>
                {filterData.options != null ?(
                    Object.keys(filterData.options).map((o)=>(
                        <div> 
                            <button onClick={()=> selectOption(o)} disabled={selected.display?.[filterData.displayText]?.includes(o)}>{o}</button>
                            <button onClick={()=> deselectOption(o)}>X</button>
                        </div>
                ))) : null}
            </div>
            }
        </article>
    )
}