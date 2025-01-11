import React, { useEffect } from "react";

export default function SingleSelectFilter({filterData, selected, setSelected}){

    function selectOption(option){
        if(selected.display?.[filterData.displayText] !== option){
            setSelected((prevState)=>({
                display: {...prevState.display, [filterData.displayText]: option},
                request: {...prevState.request, [filterData.filterId]: filterData.options[option]}
            }))
        }  
    }

    function deselectOption(option){
        if(selected.display?.[filterData.displayText] === option){
            setSelected((prevState)=>{
                const newDisplay = {...prevState.display}
                const newRequest = {...prevState.request}
    
                delete newDisplay[filterData.displayText]
                delete newRequest[filterData.filterId]
    
                return {
                    display: {...newDisplay},
                    request: {...newRequest}
                }
            })
        }  
    }

    return(
        <article>
            {
            <div>
                {filterData.options != null ?(
                    Object.keys(filterData.options).map((o)=>(
                        <div> 
                            <button onClick={()=> selectOption(o)} disabled={selected.display?.[filterData.displayText] === o}>{o}</button>
                            <button onClick={()=> deselectOption(o)}>X</button>
                        </div>
                ))) : null}
            </div>
            }
        </article>
    )
}