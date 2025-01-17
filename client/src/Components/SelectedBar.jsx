import React from "react";

export default function SelectedBar({filters, selected, setSelected}){

    function clearSelection(fName){
        const fId = filters.find((f)=>f.displayText === fName).filterId
        setSelected((prevState)=>{
            const newState = {...prevState}

            delete newState.display[fName]
            delete newState.request[fId]

            return newState
        })
    }


    return(
        <article>
            {
            <div>
                {selected.display != {} ? (
                    Object.entries(selected.display).map(([filter, option], k)=>(
                    <p key={k} onClick={()=>clearSelection(filter)}>{`${filter}: ${option}`}</p>
                ))) : null}
            </div>
            }
        </article>
    )
}