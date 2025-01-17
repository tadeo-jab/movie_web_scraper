import React from "react";

export default function MultiSelectFilter({filterData, selected, setSelected}){

    const filName = filterData.displayText
    const filId = filterData.filterId
    const filOptions = filterData.options


    function selectOption(option){
        if(!(filId in selected.request)){
            setSelected((prevState)=>({
                display: {...prevState.display, [filName]: [option]},
                request: {...prevState.request, [filId]: [filOptions[option]]}
            }))
        }
        else if((filId in selected.request) && !(selected.display?.[filName]?.includes(option))){
            setSelected((prevState)=>({
                display: {...prevState.display, [filName]: [...prevState.display[filName], option]},
                request: {...prevState.request, [filId]: [...prevState.request[filId], filOptions[option]]}
            }))
        }  
    }

    function deselectOption(option){
        if(selected.display?.[filName]?.length === 1){
            setSelected((prevState)=>{
                const newState = {...prevState}
    
                delete newState.display[filName]
                delete newState.request[filId]
    
                return newState
            })
        }
        else{
            setSelected((prevState)=>({
                display: {...prevState.display, [filName]: prevState.display[filName].filter(item => item !== option)},
                request: {...prevState.request, [filId]: prevState.request[filId].filter(item => item !== filOptions[option])}
            }))
        }
        
    }

    return(
        <article>
            {
            <div>
                {filOptions != null ?(
                    Object.keys(filOptions).map((o)=>(
                        <div> 
                            <button onClick={()=> selectOption(o)} disabled={selected.display?.[filName]?.includes(o)}>{o}</button>
                            <button onClick={()=> deselectOption(o)}>X</button>
                        </div>
                ))) : null}
            </div>
            }
        </article>
    )
}